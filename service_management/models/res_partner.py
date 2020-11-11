from odoo import api, fields, models

class ResPartner(models.Model):
    _inherit = 'res.partner'

    boat_make_id = fields.Many2one('boat.make', 'Make')
    boat_model = fields.Char('Model')
    boat_length = fields.Float('Boat Length')
    boat_width = fields.Float('Boat Width')
    year = fields.Char('Year')
    engine_model = fields.Char('Engine Model')
    engine_hours = fields.Integer('Engine Hours')
    engine_mfg_year = fields.Char('Engine Mfg Year')