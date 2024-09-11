# © 2024 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3 - See http://www.gnu.org/licenses/lgpl-3.0.html

from odoo import api,fields, models

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    purchase_order_ids = fields.One2many('purchase.order', 'crm_lead_id', string='Purchase Orders')
    purchase_amount_total= fields.Monetary(compute='_compute_purchase_amount_total', string="Sum of Orders", currency_field='company_currency')
    purchase_quotation_count = fields.Integer(compute='_compute_purchase_amount_total', string="Number of Quotations")
    purchase_order_count = fields.Integer(compute='_compute_purchase_amount_total', string="Number of Purchase Order")


    def action_purchase_orders_new(self):
        self.ensure_one()
        
        if not self.partner_id:
            return self.env.ref("purchase_crm.crm_purchase_partner_action").read()[0]
        else:
            return self.action_new_purchase_order()
            
    def action_new_purchase_order(self):
        self.ensure_one()
        
        action = self.env.ref("purchase_crm.purchase_order_action_form").read()[0]
        action['context'] = {
            'default_crm_lead_id': self.id,
            'default_partner_id': self.partner_id.id,
            'default_campaign_id': self.campaign_id.id,
            'default_medium_id': self.medium_id.id,
            'default_origin': self.name,
            'default_source_id': self.source_id.id,
            'default_company_id': self.company_id.id or self.env.company.id,
            'default_tag_ids': self.tag_ids.ids,
        }
        
        if self.team_id:
            action['context']['default_team_id'] = self.team_id.id
        if self.user_id:
            action['context']['default_user_id'] = self.user_id.id
            
        return action


    @api.depends('purchase_order_ids')
    def _compute_purchase_amount_total(self):
        for lead in self:
            total = 0.0
            quotation_cnt = 0
            purchase_order_cnt = 0
            company_currency = lead.company_currency or self.env.user.company_id.currency_id
            for order in lead.purchase_order_ids:
                if order.state in ('draft', 'sent'):
                    quotation_cnt += 1
                if order.state not in ('draft', 'sent', 'cancel'):
                    purchase_order_cnt += 1
                    total += order.currency_id._convert(
                        order.amount_untaxed, company_currency, order.company_id, order.date_order or fields.Date.today())
            lead.purchase_amount_total = total
            lead.purchase_quotation_count = quotation_cnt
            lead.purchase_order_count = purchase_order_cnt

    def action_view_purchase_quotation(self):
        action = self.env.ref('purchase.purchase_form_action').read()[0]
        action['context'] = {
            'search_default_draft': 1,
            'search_default_partner_id': self.partner_id.id,
            'default_partner_id': self.partner_id.id,
            'default_crm_lead_id': self.id
        }
        action['domain'] = [('crm_lead_id', '=', self.id), ('state', 'in', ['draft', 'sent'])]
        quotations = self.purchase_order_ids.filtered(lambda l: l.state in ('draft', 'sent'))
        if len(quotations) == 1:
            action['views'] = [(self.env.ref('purchase.purchase_order_form').id, 'form')]
            action['res_id'] = quotations.id

        return action


    def action_view_purchase_order(self):
        action = self.env.ref('purchase.purchase_form_action').read()[0]
        action['context'] = {
            'search_default_partner_id': self.partner_id.id,
            'default_partner_id': self.partner_id.id,
            'default_crm_lead_id': self.id,
        }
        action['domain'] = [('crm_lead_id', '=', self.id), ('state', 'not in', ('draft', 'sent', 'cancel'))]
        orders = self.purchase_order_ids.filtered(lambda l: l.state not in ('draft', 'sent', 'cancel'))
        if len(orders) == 1:
            action['views'] = [(self.env.ref('purchase.purchase_order_form').id, 'form')]
            action['res_id'] = orders.id

        return action