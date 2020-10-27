from odoo import models, fields

class ResCompany(models.Model):
    _inherit = 'res.company'

    water_contract_sms = fields.Text('Default Water Contract SMS Text',translate=True)
