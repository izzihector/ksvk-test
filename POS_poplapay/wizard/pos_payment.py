# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class PosMakePayment(models.TransientModel):
    _inherit = "pos.make.payment"

    ''' refund payment data store the field and base method check called. '''

    # @api.multi
    def get_refund_data(self, data):
        wiz_rec = self.browse(data.get('wiz_id'))
        self.env['pos.order'].browse(data.get('active_id')).write(
            {'refund_transaction_data': data.get('refund_data')})
        return wiz_rec.with_context(active_id=data.get('active_id')).check()

    ''' When client pay for credit card or debit card and product refundeble then
     select credit card and debit card refund time then check_data called and
     payment refund for credit card thou. '''

    # @api.multi
    def check_data(self):
        action = self._context.get('active_id')
        pos_order_ref = self.env['pos.order'].browse(action)
        pos_session_id = pos_order_ref.session_id
        # if pos_order_ref.transaction_data \
        # and pos_order_ref.config_id.poplapay_journal_id == self.journal_id:
        if pos_order_ref.transaction_data:
            api_key = pos_order_ref.config_id.api_key
            transaction_data_dict = pos_order_ref.transaction_data
            data_transaction_id = eval(transaction_data_dict)
            amount = self.amount
            name_customer = pos_order_ref.partner_id.name
            username = pos_order_ref.config_id.username
            password = pos_order_ref.config_id.password
            terminal_id = pos_order_ref.config_id.terminal_id
            url_name = pos_order_ref.config_id.url_name
            transaction_id = data_transaction_id['transaction_id']
            return {
                'type': 'ir.actions.client',
                'tag': 'refund_pop',
                "params": {
                        "api_key": api_key,
                        "cashier_language": "en",
                        "receipt_id": 124,
                        "sequence_id": 235,
                        "amount": abs(amount) * 100,
                        "currency": "EUR",
                        "transaction_id": transaction_id,
                        "preferred_receipt_text_width": 40,
                        "username": username,
                        "password": password,
                        "terminal_id": terminal_id,
                        "url_name": url_name,
                        "active_id": action,
                        "wiz_id": self.id,
                        "external_data": {
                            "name": name_customer,
                            "shift": {
                              "number": 123
                            }
                        }
                    }
                }
        else:
            return self.check()
