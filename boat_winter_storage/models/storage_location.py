from odoo import models, fields,_

class StorageLocation(models.Model):
    _name = 'storage.location'
    _description = 'Winter Storage Location'

    name = fields.Char('Name')
    street = fields.Char('Street Address')
    city = fields.Char('City')
    state_id = fields.Many2one('res.country.state','State')
    country_id = fields.Many2one('res.country','Country')
    price_meter = fields.Float('Price / m2')
