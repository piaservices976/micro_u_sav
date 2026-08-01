app_name = "micro_u_sav"
app_title = "Micro U Sav"
app_publisher = "PIA Services"
app_description = "Fonctions SAV MICRO-U (facturation des pieces detachees) pour ERPNext."
app_email = "contact@piaservices.fr"
app_license = "mit"

required_apps = ["frappe", "erpnext"]

# Pas de nouveaux DocTypes ni de pages : cette app existe uniquement pour heberger
# de maniere durable le code Python deja utilise en production (facturer_pieces_sav),
# afin qu'il survive a toute recreation du conteneur backend/frontend.

after_install = "micro_u_sav.install.after_install"
web_include_js = "/assets/micro_u_sav/js/login_banner.js?v=3"
