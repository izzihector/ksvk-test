# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class PosConfig(models.Model):
    _inherit = 'pos.config'

    def _default_config(self):
        active_id = self.env.context.get('active_id')
        if active_id:
            return self.env['pos.order'].browse(active_id).session_id.config_id
        return False

    url_name = fields.Char('URL')
    api_key = fields.Char('API Key')
    username = fields.Char('Username')
    password = fields.Char('password')
    terminal_id = fields.Char('Terminal ID')
    hardware_id = fields.Char('Hardware ID')
    poplapay_journal_id = fields.Many2one('pos.payment.method', string='Payment Methods')

    @api.onchange('poplapay_journal_id')
    def add_poplaypay_journals(self):
        domain = []
        list3 = self.payment_method_ids.ids
        data = {'payment_method_ids': domain}
        if self.poplapay_journal_id:
            list3.append(self.poplapay_journal_id.id)
        journal_browse_ids = self.env['pos.payment.method'].browse(list3)
        self.payment_method_ids = journal_browse_ids
