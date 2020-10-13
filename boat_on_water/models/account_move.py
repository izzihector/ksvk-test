# -*- coding: utf-8 -*-

from odoo import models, fields


class AccountMove(models.Model):
    _inherit = 'account.move'

    water_contract_id = fields.One2many('water.contract', 'invoice_id', readonly=True, copy=False)


