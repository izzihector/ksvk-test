# import logging
from odoo import http,_
from odoo.http import request, route
import base64
import io
import imghdr

# _logger = logging.getLogger(__name__)


class UrlBinary(http.Controller):

    @http.route([
        '/url/image/<id>',
    ], type='http', auth="none", website=False, multilang=False)
    def content_image(self, id=None, **kw):
        model = request.env['boat.image'].sudo().search_read([('id','=',int(id))],['binary_value'])
        if model[0].get('binary_value'):
            image_base64 = base64.b64decode(model[0].get('binary_value'))
            image_data = io.BytesIO(image_base64)
            imgext = '.' + (imghdr.what(None, h=image_base64) or 'png')
            response = http.send_file(image_data, filename= 'url' + imgext, mtime=False)
            return response