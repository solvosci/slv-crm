# © 2023 Solvos Consultoría Informática (<http://www.solvos.es>)
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, fields


class Lead(models.Model):
    _inherit = "crm.lead"

    event_date = fields.Datetime()
    duration = fields.Float()
