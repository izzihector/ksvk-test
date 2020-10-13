from odoo import api, fields, models,_
from odoo.exceptions import UserError
import requests
import json

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    nettix_location_id = fields.Many2one('nettix.location',string="Nettix Location")
    access_token = fields.Text()

    def get_access_token(self):
        if self.env['res.config.settings'].search([]):
            settings = self.search([])[-1]
            # Generate access token
            credentials = {
                "grant_type": "client_credentials",
                "client_id": settings.nettix_location_id.client_id,
                "client_secret": settings.nettix_location_id.client_secret
            }
            response = requests.post("https://auth-test.nettix.fi/oauth2/token", data=credentials)
            settings.write({'access_token': json.loads(response.text)["access_token"]})
        # else:
        #     raise UserError(_('Please save client id and client secret information in general settings'))

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        res.update(
            nettix_location_id=int(self.env['ir.config_parameter'].sudo().get_param(
                'Nettivene.nettix_location_id')),
            access_token=self.env['ir.config_parameter'].sudo().get_param(
                'Nettivene.access_token'),
        )
        return res

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        param = self.env['ir.config_parameter'].sudo()

        access_token = self.access_token or False
        nettix_location_id = self.nettix_location_id.id or False

        param.set_param('Nettivene.access_token', access_token)
        param.set_param('Nettivene.nettix_location_id', nettix_location_id)