"""
micro_u_sav.api
----------------
Fonction whitelisted appelee par le bouton "Facturer les pieces utilisees"
sur le Ticket (Issue). Remplace l'ancien frappe.micro_u_pieces_sav.facturer_pieces_sav
qui vivait directement dans apps/frappe/frappe/ (non persiste, perdu a chaque
recreation du conteneur backend). Ici, le code fait partie d'une vraie app
Frappe installee, donc il est baked dans l'image Docker personnalisee et ne
peut plus disparaitre.
"""

import frappe


@frappe.whitelist()
def facturer_pieces_sav(ticket_name):
    ticket = frappe.get_doc("Issue", ticket_name)

    if not ticket.get("custom_pieces_utilisees"):
        frappe.throw("Aucune pièce à facturer sur ce ticket.")

    warehouse = ticket.custom_site_depot
    if not warehouse:
        frappe.throw("Site de dépôt manquant sur le ticket.")

    if ticket.get("custom_facture_pieces"):
        frappe.throw("Ce ticket a déjà une facture de pièces liée.")

    company = "MICRO-U"

    # 1) Stock Entry (Material Receipt) : fait entrer temporairement la quantite utilisee dans ERPNext
    se = frappe.get_doc({
        "doctype": "Stock Entry",
        "stock_entry_type": "Material Receipt",
        "company": company,
        "items": [
            {
                "item_code": row.item_code,
                "qty": row.qty,
                "t_warehouse": warehouse,
                "basic_rate": row.rate or 0,
            }
            for row in ticket.custom_pieces_utilisees
        ],
    })
    se.insert(ignore_permissions=True)
    se.submit()

    # 2) Sales Invoice avec sortie de stock : ramene le stock a 0 et facture le client
    si = frappe.get_doc({
        "doctype": "Sales Invoice",
        "customer": ticket.customer,
        "company": company,
        "update_stock": 1,
        "set_warehouse": warehouse,
        "items": [
            {
                "item_code": row.item_code,
                "qty": row.qty,
                "rate": row.rate or 0,
                "warehouse": warehouse,
            }
            for row in ticket.custom_pieces_utilisees
        ],
    })
    si.insert(ignore_permissions=True)

    ticket.db_set("custom_facture_pieces", si.name)
    frappe.db.commit()

    return si.name
