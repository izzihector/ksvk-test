from odoo import models, fields, api, _
from odoo.exceptions import UserError

class AddBoat(models.TransientModel):
    _name = 'add.boat.wizard'
    _description = 'Add Boat Wizard'

    make = fields.Many2one('boat.make', string='Make')
    year = fields.Char('Year')
    model = fields.Char('Model')
    boat_model_id = fields.Many2one('boat.model','Boat Model')
    records = fields.Many2many('boat.list',string='Boats')
    show_boats = fields.Boolean('Show Boats Without Boat Model')

    def search_recs(self):
        return {
            "type": "ir.actions.do_nothing",
        }

    @api.onchange('make','year','model','boat_model_id')
    def _onchange_model(self):
        if self.model and self.make and self.year:
            self.show_boats = False
            model_id = self.env['boat.model'].search(
                [('make', '=', self.make.id), ('year', '=', self.year), ('model', '=', self.model)])
            boats = []
            if model_id.boat_ids:
                for boat in model_id.boat_ids:
                    list_id = self.env['boat.list'].search([('boat_id','=',boat.id)])
                    if not list_id:
                        list_id = self.env['boat.list'].create({'boat_id':boat.id})
                    boats.append(list_id.id)
                self.records = [(6, 0, boats)]
            else:
                raise UserError(_("This model does not have any boats"))
        if self.boat_model_id:
            self.show_boats = False
            boats = []
            if self.boat_model_id.boat_ids:
                for boat in self.boat_model_id.boat_ids:
                    list_id = self.env['boat.list'].search([('boat_id', '=', boat.id)])
                    if not list_id:
                        list_id = self.env['boat.list'].create({'boat_id': boat.id})
                    boats.append(list_id.id)
                self.records = [(6, 0, boats)]
            else:
                raise UserError(_("This model does not have any boats"))

    @api.onchange('show_boats')
    def onchange_boats(self):
        boats = []
        if self.show_boats:
            self.boat_model_id = False
            self.model = ''
            self.year = ''
            self.make = ''
            boat_ids = self.env['product.template'].search([('is_boat', '=', True), ('active', '=', True),('model_id','=',False)])
            for boat in boat_ids:
                list_id = self.env['boat.list'].search([('boat_id', '=', boat.id)])
                if not list_id:
                    list_id = self.env['boat.list'].create({'boat_id': boat.id})
                boats.append(list_id.id)
            self.records = [(6, 0, boats)]
        if not self.show_boats:
            self.records = [(5,0,0)]


    def confirm_button(self):
        model_id = ''
        if self.records:
            if self.model and self.make and self.year:
                model_id = self.env['boat.model'].search(
                    [('make', '=', self.make.id), ('year', '=', self.year), ('model', '=', self.model)])
            if self.boat_model_id:
                model_id = self.boat_model_id
            for rec in self.records:
                if rec.select:
                    product_id = self.env['product.product'].search([('product_tmpl_id','=',rec.boat_id.id)])
                    self.env['sale.order.line'].create({
                        'product_id':product_id.id,
                        'order_id':self._context['active_id'],

                    })
                    # rec.boat_id.write({
                    #     'order_id':self._context['active_id'],
                    # })
                    if model_id:
                        self.env['sale.order'].browse([self._context["active_id"]]).write({'model_id':model_id.id})


