from odoo import models, fields

class ResCompany(models.Model):
    _inherit = 'res.company'

    po_tax_id = fields.Many2one('account.tax',string='Default Tax Setting')
