# -*- coding: utf-8 -*-

from odoo import models, fields

class ResUsers(models.Model):
    _inherit = 'res.users'

    default_water_fiscal_position_id = fields.Many2one('account.fiscal.position','Fiscal Position for Water Contract')
