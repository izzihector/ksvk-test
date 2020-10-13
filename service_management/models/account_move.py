# -*- coding: utf-8 -*-

from odoo import models, fields


class AccountMove(models.Model):
    _inherit = 'account.move'

    service_ids = fields.One2many('service.order', 'invoice_id', readonly=True, copy=False)


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    service_line_ids = fields.One2many('service.order.line', 'invoice_line_id', readonly=True, copy=False)
    service_operation_ids = fields.One2many('service.operations', 'invoice_line_id', readonly=True, copy=False)
