# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError


class PosOrder(models.Model):
    _inherit = "pos.order"

    transaction_id = fields.Char('Transaction ID')
    refund_transaction_id = fields.Char('Refund Transaction ID')
    aviite = fields.Char('Aviite')
    ala = fields.Char('Ala')
    t_print = fields.Char('T')
    merchant_receipt = fields.Html('Merchant Receipt')
    currency = fields.Char('Currency')
    amount = fields.Char('Amount')
    transaction_data = fields.Text('Transaction Data')
    refund_transaction_data = fields.Text('Refund Data')

    ''' when transaction is successfully then get the data of jS and create
        back-end transaction_data entry. '''
    @api.model
    def _order_fields(self, ui_order):
        rec = super(PosOrder, self)._order_fields(ui_order)
        if 'transaction_data' in ui_order.keys():
            rec['transaction_data'] = ui_order.get('transaction_data')
            rec['ala'] = ui_order.get('ala')
            rec['aviite'] = ui_order.get('aviite')
            rec['t_print'] = ui_order.get('t_print')
        return rec
