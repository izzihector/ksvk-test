# -*- coding: utf-8 -*-

from odoo import models, fields


class AccountMove(models.Model):
    _inherit = 'account.move'

    contract_id = fields.One2many('storage.contract', 'invoice_id', readonly=True, copy=False)


