from odoo import models, fields

class ResCompany(models.Model):
    _inherit = 'res.company'

    service_sms = fields.Text('Default Service SMS Text',translate=True)
