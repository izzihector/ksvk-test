from odoo import api, fields, models, _
from odoo.exceptions import UserError

class AccountInvoice(models.Model):
    _inherit = 'account.move'

    trade_in_lines = fields.One2many('tradein.lines', 'account_move_id', string='Trade-In Lines')
    trade_in_amount = fields.Float('Trade-In Amount', compute='compute_tradein_amount')

    @api.depends('trade_in_lines')
    def compute_tradein_amount(self):
        self.trade_in_amount = 0
        if self.trade_in_lines:
            for line in self.trade_in_lines:
                self.trade_in_amount += line.cost

    def action_post(self):
        res = super(AccountInvoice, self).action_post()
        self.amount_total = self.amount_total - self.trade_in_amount
        self.amount_residual = self.amount_residual - self.trade_in_amount
        return res

    def button_draft(self):
        res = super(AccountInvoice, self).button_draftd()
        self.amount_total = self.amount_total - self.trade_in_amount
        self.amount_residual = self.amount_residual - self.trade_in_amount
        return res



class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = "sale.advance.payment.inv"

    def _create_invoice(self, order, so_line, amount):
        if (self.advance_payment_method == 'percentage' and self.amount <= 0.00) or (self.advance_payment_method == 'fixed' and self.fixed_amount <= 0.00):
            raise UserError(_('The value of the down payment amount must be positive.'))
        if self.advance_payment_method == 'percentage':
            amount = order.amount_untaxed * self.amount / 100
            name = _("Down payment of %s%%") % (self.amount,)
        else:
            amount = self.fixed_amount
            name = _('Down Payment')

        invoice_vals = {
            'type': 'out_invoice',
            'invoice_origin': order.name,
            'invoice_user_id': order.user_id.id,
            'narration': order.note,
            'partner_id': order.partner_invoice_id.id,
            'fiscal_position_id': order.fiscal_position_id.id or order.partner_id.property_account_position_id.id,
            'partner_shipping_id': order.partner_shipping_id.id,
            'currency_id': order.pricelist_id.currency_id.id,
            'invoice_payment_ref': order.client_order_ref,
            'invoice_payment_term_id': order.payment_term_id.id,
            'team_id': order.team_id.id,
            'campaign_id': order.campaign_id.id,
            'medium_id': order.medium_id.id,
            'source_id': order.source_id.id,
            'invoice_line_ids': [(0, 0, {
                'name': name,
                'price_unit': amount,
                'quantity': 1.0,
                'product_id': self.product_id.id,
                'sale_line_ids': [(6, 0, [so_line.id])],
                'analytic_tag_ids': [(6, 0, so_line.analytic_tag_ids.ids)],
                'analytic_account_id': order.analytic_account_id.id or False,
            })],
            # 'trade_in_lines': [(6, 0, tradein_ids)],
        }
        if order.fiscal_position_id:
            invoice_vals['fiscal_position_id'] = order.fiscal_position_id.id
        invoice = self.env['account.move'].create(invoice_vals)
        tradein_ids = []
        tradein_vals = {}
        for tl in order.trade_in_lines:
            tradein_ids.append(self.env['tradein.lines'].create({
                'boat_id': tl.boat_id.id,
                'cost': tl.cost,
                'sales_price': tl.sales_price,
                'account_move_id': invoice.id,
                'sale_order_id':'',
            }).id)

        invoice.write({
            'trade_in_lines': [(6, 0, tradein_ids)],
        })
        invoice.write({
            'amount_total': invoice.amount_total - invoice.trade_in_amount,
        })
        invoice.message_post_with_view('mail.message_origin_link',
                    values={'self': invoice, 'origin': order},
                    subtype_id=self.env.ref('mail.mt_note').id)
        return invoice

