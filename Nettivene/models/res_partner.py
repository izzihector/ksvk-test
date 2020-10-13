from odoo import api, fields, models
import requests
import json

class ResPartner(models.Model):
    _inherit = 'res.partner'

    nettix_id = fields.Char('Nettix ID')
    username = fields.Char('Username')
    ads_url = fields.Char('Ads Url')
    on_hold_ads_url = fields.Char('On Hold Ads Url')
    template_id = fields.Many2one('mail.template', 'SO mail template')
    boat_make_id = fields.Many2one('boat.make', 'Make')
    boat_model = fields.Char('Model')
    boat_length = fields.Float('Boat Length')
    boat_width = fields.Float('Boat Width')
    year = fields.Char('Year')
    engine_model = fields.Char('Engine Model')
    engine_hours = fields.Integer('Engine Hours')
    engine_mfg_year = fields.Char('Engine Mfg Year')
    comment = fields.Html('Comment')

    def sync_dealers(self):
        if self.env['res.config.settings'].search([]):
            access_token = self.env['res.config.settings'].search([])[-1].access_token
            if not access_token:
                self.env['res.config.settings'].get_access_token()
                access_token = self.env['res.config.settings'].search([])[-1].access_token
            headers = {
                'accept': 'application/json',
                'X-Access-Token': access_token,
                'Content-Type': 'multipart/form-data',
                'Accept-Language': 'en',
            }
            response = requests.get("https://api-test.nettix.fi/rest/boat/my-dealers",headers=headers)
            response = json.loads(response.text)
            for rec in response:
                existing_partner_id = self.env['res.partner'].search([('nettix_id','=',rec['userId'])])
                if not existing_partner_id:
                    self.env['res.partner'].create({
                        'name':rec['name'],
                        'nettix_id':rec['userId'],
                        'username':rec['username'],
                        'ads_url':rec['adsUrl'],
                        'on_hold_ads_url':rec['onHoldAdsUrl'],
                    })
                else:
                    existing_partner_id.write({
                        'name': rec['name'],
                        'nettix_id': rec['userId'],
                        'username': rec['username'],
                        'ads_url': rec['adsUrl'],
                        'on_hold_ads_url': rec['onHoldAdsUrl'],
                    })
        else:
            self.env['res.config.settings'].get_access_token()