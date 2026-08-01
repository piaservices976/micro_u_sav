# micro_u_sav

App Frappe dédiée au module SAV de MICRO-U sur ERPNext.

Contient le code Python nécessaire au bouton "Facturer les pièces utilisées"
du Ticket (Issue) : `micro_u_sav.api.facturer_pieces_sav`.

Cette app existe pour que ce code survive à toute recréation des conteneurs
Docker (backend/frontend) — avant sa création, ce code vivait uniquement
copié à la main dans `apps/frappe/frappe/`, non persisté, et disparaissait
à chaque recréation de conteneur (voir incident du 31/07/2026).

## Installation

```bash
bench get-app micro_u_sav <url-du-repo-git>
bench --site app.piaservices.fr install-app micro_u_sav
```

Ou, de façon durable, en l'intégrant à l'image Docker personnalisée via
`apps.json` (voir `PLAN_PERSISTANCE_HRMS_ERPNEXT_FRANCE.md`).

## Licence

MIT
