from odoo import api, fields, models,_

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    service_sms = fields.Text('Default SMS Text')

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        res.update(
            service_sms=self.env['ir.config_parameter'].sudo().get_param(
                'service_management.service_sms'),
        )
        return res

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        param = self.env['ir.config_parameter'].sudo()

        service_sms = self.service_sms or False

        param.set_param('service_management.service_sms', service_sms)