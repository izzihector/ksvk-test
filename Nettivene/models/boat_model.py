from odoo import api, fields, models, _

class BoatModel(models.Model):
    _name = 'boat.model'
    _description = 'Boat Model'

    name = fields.Char('Name', compute='_compute_name')
    make = fields.Many2one('boat.make',string='Make', required=1)
    year = fields.Char('Year', required=1)
    model = fields.Char('Model', required=1)
    boat_ids = fields.One2many('product.template','model_id','Boats')
    equipment_ids = fields.One2many('equipment.lines','model_id','Equipments')

    @api.depends('make','model','year')
    def _compute_name(self):
        for rec in self:
            if rec.make and rec.model and rec.year:
                rec.name = rec.make.name + " " + rec.model + " " + rec.year
            else:
                rec.name = ""


class ModelEquipmentLines(models.Model):
    _name = 'equipment.lines'
    _description = 'Equipment Lines'

    equip_id = fields.Many2one('product.template','Equipment',domain=[('is_equipment','=',True)])
    model_id = fields.Many2one('boat.model')
    default_code = fields.Char(related = 'equip_id.default_code')

class BoatList(models.Model):
    _name = 'boat.list'
    _description = 'Boat List'

    boat_id = fields.Many2one('product.template','Boat')
    standard_price = fields.Float(related='boat_id.standard_price')
    list_price = fields.Float(related='boat_id.list_price')
    select = fields.Boolean(string='')
