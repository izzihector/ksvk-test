from odoo import models, fields

class ResCompany(models.Model):
    _inherit = 'res.company'

    winter_storage_sms = fields.Text('Default Winter Storage SMS Text',translate=True)
