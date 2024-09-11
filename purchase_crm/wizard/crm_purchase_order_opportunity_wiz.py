from odoo import api, fields, models, _
from odoo.exceptions import UserError

class CrmPurchaseOrderOpportunityWiz(models.TransientModel):
    _name = 'crm.purchase.order.opportunity.wiz'
    _description = 'Create new or use existing Vendor on new Purchase Order'
    _inherit = 'crm.partner.binding'

    @api.model
    def default_get(self, fields):
        result = super(CrmPurchaseOrderOpportunityWiz, self).default_get(fields)

        active_model = self._context.get('active_model')
        if active_model != 'crm.lead':
            raise UserError(_('You can only apply this action from a lead.'))

        active_id = self._context.get('active_id')
        if 'lead_id' in fields and active_id:
            result['lead_id'] = active_id
        return result

    action = fields.Selection(
        [('exist', 'Use Existing Vendor'), ('create', 'Create New Vendor'), ('nothing', 'Do not link to a vendor')],
        string='Purchase Order Vendor',
        required=True
    )
    lead_id = fields.Many2one('crm.lead', "Associated Lead", required=True)
    partner_id = fields.Many2one('res.partner', string='Vendor',
        domain="[('supplier_rank', '>', 0)]",
        required=False)

    def action_apply(self):
        """ Apply the chosen action from the wizard: use existing vendor, create a new one, or do nothing. """
        self.ensure_one()
        if self.action == 'exist':
            if not self.partner_id:
                raise UserError(_('Please select a vendor.'))
            self.lead_id.write({
                'partner_id': self.partner_id.id
            })
            self.lead_id._onchange_partner_id()
        elif self.action == 'create':
            new_partner_id = self._create_partner()
            self.lead_id.write({
                'partner_id': new_partner_id
            })
            self.lead_id._onchange_partner_id()

        return self.lead_id.action_new_purchase_order()


        def _create_partner(self):
            self.ensure_one()
            result = self.lead_id.handle_partner_assignation(action='create')
            return result.get(self.lead_id.id)
