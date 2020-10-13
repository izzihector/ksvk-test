from odoo import api, fields, models


class TradeInProducts(models.Model):
    _name = 'product.tradein'
    _description = 'Product Tradein'

    name = fields.Char('Name')
    year = fields.Char('Year')
    cost = fields.Float('Cost')
    engine_make_id = fields.Many2one('boat.make')
    engine_mfg_year = fields.Integer('Engine Mfg Year')
    engine_hours = fields.Integer('Engine Hours')
    sale_order_id = fields.Many2one('sale.order','Sale Order')
    model = fields.Char('Model', required=1)

class TradeInLines(models.Model):
    _name = 'tradein.lines'
    _description = 'Tradein Lines'

    boat_id = fields.Many2one('product.tradein','Boat')
    product_ref_id = fields.Many2one('product.template')
    cost = fields.Float(related='boat_id.cost',string='Cost')
    sale_order_id = fields.Many2one('sale.order')
    account_move_id = fields.Many2one('account.move')
    sales_price = fields.Float('Sales Price')

    @api.onchange('cost')
    def onchange_cost(self):
        self.boat_id.cost = self.cost

    @api.onchange('boat_id')
    def onchange_boat(self):
        return {'domain': {
            'boat_id': [('sale_order_id','=',False)],
        }}


class MarginLines(models.Model):
    _name = 'margin.lines'
    _description = 'Margin Lines'

    boat_id = fields.Many2one('product.template','Boat')
    standard_price = fields.Float(related='boat_id.standard_price',string='Cost')
    actual_sale_price = fields.Float(related='boat_id.actual_sale_price',string='Sales Price')
    margin = fields.Float(related='boat_id.margin',string='Margin')
    order_id = fields.Many2one('sale.order')
    main_boat_id = fields.Many2one('product.template', 'Boat')
    root = fields.Boolean('Root')
