# © 2023 Solvos Consultoría Informática (<http://www.solvos.es>)
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import models


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    def action_new_quotation(self):
        action = super(CrmLead, self).action_new_quotation()
        if self.event_date:
            action["context"]["default_commitment_date"] = self.event_date
        return action
