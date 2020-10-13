from odoo import models, fields, api

class Confirmation(models.TransientModel):
    _name = 'confirmation.message'
    _description = 'Confirmation Message'

    def confirm_button(self):
        return True