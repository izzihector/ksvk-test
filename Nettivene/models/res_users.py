from odoo import api, fields, models

class ResUsers(models.Model):
    _inherit = 'res.users'

    nettix_location_id = fields.Many2one('nettix.location', string='Location')