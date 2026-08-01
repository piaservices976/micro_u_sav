"""
micro_u_sav.install
--------------------
Hook after_install : recree de maniere idempotente le DocType enfant
"SAV Piece Utilisee", les champs personnalises sur Issue, et le Client Script
du bouton "Facturer les pieces utilisees" - au cas ou cette app serait
installee sur un site vierge (reconstruction/disaster recovery). Sur le site
de production actuel, ces objets existent deja en base (ils ont ete crees
lors de la mise en place initiale du module SAV) : ce hook ne fait alors rien
d'utile mais reste sans danger (verifications d'existence partout).
"""

import re

import frappe

CLIENT_SCRIPT_NAME = "SAV Filtre Site de Dépôt"

BUTTON_SCRIPT = """
    refresh: function(frm) {
        frm.set_query('custom_site_depot', function() {
            return {
                filters: {
                    name: ['in', ['MICRO-U COMBANI - MU', 'MICRO-U MAMOUDZOU - MU', 'MICRO-U TSINGONI - MU']]
                }
            };
        });
        if (!frm.is_new() && frm.doc.custom_pieces_utilisees && frm.doc.custom_pieces_utilisees.length && !frm.doc.custom_facture_pieces) {
            frm.add_custom_button('Facturer les pièces utilisées', function() {
                frappe.call({
                    method: 'micro_u_sav.api.facturer_pieces_sav',
                    args: { ticket_name: frm.doc.name },
                    freeze: true,
                    freeze_message: 'Création de la facture...',
                    callback: function(r) {
                        if (r.message) {
                            frappe.set_route('Form', 'Sales Invoice', r.message);
                        }
                    }
                });
            }).addClass('btn-primary');
        }
        if (frm.doc.custom_facture_pieces) {
            frm.add_custom_button('Voir la facture pièces', function() {
                frappe.set_route('Form', 'Sales Invoice', frm.doc.custom_facture_pieces);
            });
        }
    },
"""


def create_piece_doctype():
    if frappe.db.exists("DocType", "SAV Piece Utilisee"):
        return

    doc = frappe.get_doc({
        "doctype": "DocType",
        "name": "SAV Piece Utilisee",
        "module": "Custom",
        "custom": 1,
        "istable": 1,
        "editable_grid": 1,
        "fields": [
            {
                "fieldname": "item_code",
                "fieldtype": "Link",
                "options": "Item",
                "label": "Article",
                "reqd": 1,
                "in_list_view": 1,
            },
            {
                "fieldname": "item_name",
                "fieldtype": "Data",
                "label": "Désignation",
                "fetch_from": "item_code.item_name",
                "read_only": 1,
                "in_list_view": 1,
            },
            {
                "fieldname": "qty",
                "fieldtype": "Float",
                "label": "Quantité",
                "default": "1",
                "reqd": 1,
                "in_list_view": 1,
            },
            {
                "fieldname": "rate",
                "fieldtype": "Currency",
                "label": "Prix unitaire",
                "fetch_from": "item_code.standard_rate",
                "in_list_view": 1,
            },
        ],
        "permissions": [
            {"role": "System Manager", "read": 1, "write": 1, "create": 1, "delete": 1}
        ],
    })
    doc.insert(ignore_permissions=True)


def add_pieces_fields():
    from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

    fields = {
        "Issue": [
            {
                "fieldname": "sav_pieces_section",
                "fieldtype": "Section Break",
                "label": "Pièces détachées utilisées",
                "insert_after": "custom_email_deposant",
            },
            {
                "fieldname": "custom_pieces_utilisees",
                "fieldtype": "Table",
                "options": "SAV Piece Utilisee",
                "label": "Pièces utilisées",
                "insert_after": "sav_pieces_section",
            },
            {
                "fieldname": "custom_facture_pieces",
                "fieldtype": "Link",
                "options": "Sales Invoice",
                "label": "Facture pièces",
                "read_only": 1,
                "insert_after": "custom_pieces_utilisees",
            },
        ]
    }
    create_custom_fields(fields, update=True)


def setup_client_script():
    if not frappe.db.exists("Client Script", CLIENT_SCRIPT_NAME):
        frappe.get_doc({
            "doctype": "Client Script",
            "name": CLIENT_SCRIPT_NAME,
            "dt": "Issue",
            "view": "Form",
            "enabled": 1,
            "script": "frappe.ui.form.on('Issue', {\n" + BUTTON_SCRIPT.strip("\n") + "\n});\n",
        }).insert(ignore_permissions=True)
        return

    cs = frappe.get_doc("Client Script", CLIENT_SCRIPT_NAME)
    if "micro_u_sav.api.facturer_pieces_sav" in (cs.script or ""):
        return

    new_script = re.sub(
        r"refresh:\s*function\(frm\)\s*\{.*?\n\s*\},\n",
        BUTTON_SCRIPT.strip("\n") + "\n",
        cs.script,
        flags=re.DOTALL,
        count=1,
    )
    if new_script != cs.script:
        cs.script = new_script
        cs.save(ignore_permissions=True)


def after_install():
    create_piece_doctype()
    add_pieces_fields()
    setup_client_script()
    frappe.db.commit()
    print("micro_u_sav : installation/verification terminee.")
