# © 2024 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3 - See http://www.gnu.org/licenses/lgpl-3.0.html
{
    "name": "Purchase Order Opportunity",
    "summary": """
        This module adds a shortcut on one or several purchase order opportunity cases in the CRM.
    """,
    "author": "Solvos",
    "license": "LGPL-3",
    "version": "13.0.1.0.0",
    'category': "CRM",
    "website": "https://github.com/solvosci/slv-crm",
    "depends": ['purchase', 'crm'],
    "data": [
        "views/crm_lead_views.xml",
        "views/purchase_order_views.xml",
        "wizard/crm_purchase_order_opportunity_wiz.xml",
    ],
    'installable': True,
}
