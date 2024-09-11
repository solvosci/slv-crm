# © 2024 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3 - See http://www.gnu.org/licenses/lgpl-3.0.html
from odoo import models, fields


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    crm_lead_id = fields.Many2one('crm.lead', string='CRM Lead')
