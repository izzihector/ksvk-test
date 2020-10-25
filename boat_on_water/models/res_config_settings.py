from odoo import api, fields, models,_

class WaterResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    water_contract_sms = fields.Text('Default SMS Text')

    @api.model
    def get_values(self):
        res = super(WaterResConfigSettings, self).get_values()
        res.update(
            water_contract_sms=self.env['ir.config_parameter'].sudo().get_param(
                'boat_on_water.water_contract_sms'),
        )
        return res

    def set_values(self):
        super(WaterResConfigSettings, self).set_values()
        param = self.env['ir.config_parameter'].sudo()

        water_contract_sms = self.water_contract_sms or False

        param.set_param('boat_on_water.water_contract_sms', water_contract_sms)