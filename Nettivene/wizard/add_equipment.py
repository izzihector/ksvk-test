from odoo import models, fields, api

class AddEquipment(models.TransientModel):
    _name = 'add.equipment.wizard'
    _description = 'Add Equipment Wizard'

    records = fields.Many2many('boat.list',string='Boats')

    def confirm_button(self):
        if self.records:
            for rec in self.records:
                if rec.select:
                    product_id = self.env['product.product'].search([('product_tmpl_id','=',rec.boat_id.id)])
                    self.env['sale.order.line'].create({
                        'product_id':product_id.id,
                        'order_id':self._context['active_id'],

                    })


