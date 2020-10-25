from odoo import api, fields, models,_

class WinterResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    winter_storage_sms = fields.Text('Default SMS Text')

    @api.model
    def get_values(self):
        res = super(WinterResConfigSettings, self).get_values()
        res.update(
            winter_storage_sms=self.env['ir.config_parameter'].sudo().get_param(
                'boat_winter_storage.winter_storage_sms'),
        )
        return res

    def set_values(self):
        super(WinterResConfigSettings, self).set_values()
        param = self.env['ir.config_parameter'].sudo()

        winter_storage_sms = self.winter_storage_sms or False

        param.set_param('boat_winter_storage.winter_storage_sms', winter_storage_sms)