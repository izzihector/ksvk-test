# -*- encoding: utf-8 -*-

from odoo import api, fields, models, tools, _
from odoo.exceptions import ValidationError, except_orm
import base64  # file encode
from urllib.request import Request, urlopen


class ProductTemplate(models.Model):
    _inherit = "product.template"

    image_url = fields.Char('Image URL')

    @api.model
    def create(self, vals):
        if vals.get('image_url'):
            try:
                image = urlopen(Request(vals.get('image_url'), headers={'User-Agent': 'Mozilla/5.0'})).read()
                vals['image_1920'] = base64.encodestring(image)
            except:
                pass
        return super(ProductTemplate, self).create(vals)

    def write(self, vals):
        if vals.get('image_url'):
            try:
                image = urlopen(Request(vals.get('image_url'), headers={'User-Agent': 'Mozilla/5.0'})).read()
                vals['image_1920'] = base64.encodestring(image)
            except:
                pass
        return super(ProductTemplate, self).write(vals)


class ProductProduct(models.Model):
    _inherit = "product.product"

    image_url = fields.Char('Image URL')

    @api.model
    def create(self, vals):
        if vals.get('image_url'):
            try:
                image = urlopen(Request(vals.get('image_url'), headers={'User-Agent': 'Mozilla/5.0'})).read()
                vals['image_1920'] = base64.encodestring(image)
            except:
                pass
        return super(ProductProduct, self).create(vals)

    def write(self, vals):
        if vals.get('image_url'):
            try:
                image = urlopen(Request(vals.get('image_url'), headers={'User-Agent': 'Mozilla/5.0'})).read()
                vals['image_1920'] = base64.encodestring(image)
            except:
                pass
        return super(ProductProduct, self).write(vals)

