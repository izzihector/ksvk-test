from odoo import models, fields


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    service_id = fields.Many2one('service.order', readonly=True, copy=False)

