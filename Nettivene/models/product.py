from odoo.exceptions import ValidationError, UserError
from odoo import api, fields, models, _
from datetime import datetime
import requests
import json

class ProductTemplate(models.Model):
    _inherit = "product.template"

    is_boat = fields.Boolean('Is a Boat?',default=False)

# NETTIX INFO FIELDS
    boat_status = fields.Selection([
        ('sketch','Sketch'),
        ('forsale','For Sale'),
        ('onhold','On Hold'),
        ('disabled','Disabled'),
        ('expired','Expired'),
        ('sold','Sold'),
        ('idle','Idle')
    ], copy=False)
    ad_type = fields.Selection([
        ('forsale','For Sale'),
        ('purchase','Purchase'),
        ('forrent','For Rent')
    ])
    user_id = fields.Many2one('res.partner', string='User ID')
    nettix_id = fields.Char('Nettix ID', readonly=1, copy=0)
    boat_type_id = fields.Many2one('boat.type')
    sub_type_id = fields.Many2one('sub.type')
    boat_make_id = fields.Many2one('boat.make')
    body_material_id = fields.Many2one('body.material')
    sail_steering_id = fields.Many2one('sail.steering')
    country_option_id = fields.Many2one('country.option')
    region_option_id = fields.Many2one('region.option')
    town_option_id = fields.Many2one('town.option')
    accessory_option_id = fields.Many2many('accessory.option')
    availability_id = fields.Many2one('availability.option')
    sail_description = fields.Char('Sail Description')
    boat_sails = fields.One2many('boat.sail','product_tmpl_id',string='Sails')
    has_engine = fields.Boolean('Has Engine')
    two_engine = fields.Boolean('Two Engine')
    engine_make_id = fields.Many2one('boat.make')
    engine_power = fields.Integer('Engine Power')
    engine_type_id = fields.Many2one('engine.type')
    engine_stroke_id = fields.Many2one('engine.stroke')
    engine_rig_id = fields.Many2one('engine.rig')
    engine_fuel_type_id = fields.Many2one('engine.fuel.type')
    cooling_type_id = fields.Many2one('cooling.type')
    engine_model = fields.Char('Engine Model')
    engine_model_specification = fields.Char('Engine Model Specification')
    engine_mfg_year = fields.Integer('Engine Mfg Year')
    engine_hours = fields.Integer('Engine Hours')
    engine_description = fields.Char('Engine Description')
    heat_make_id = fields.Many2one('heating.make')
    heat_fuel_type_id = fields.Many2one('heating.fuel.type')
    heat_model = fields.Char('Heating Model')
    heat_model_specification = fields.Char('Heating Model Specification')
    heat_mfg_year = fields.Integer('Heating Mfg Year')
    heat_description = fields.Char('Heating Description')
    boat_model = fields.Char('Model')
    boat_length = fields.Float('Boat Length')
    boat_height = fields.Float('Boat Height')
    boat_width = fields.Float('Boat Width')
    boat_weight = fields.Float('Boat Weight')
    boat_draft = fields.Float('Boat Draft')
    no_of_beds = fields.Integer('No. of Beds')
    year = fields.Integer('Year')
    year_model_from = fields.Integer('Year Model From')
    year_model_to = fields.Integer('Year Model To')
    unused = fields.Boolean('Unused')
    price = fields.Integer('Price')
    price_per_day = fields.Integer('Price Per Day')
    is_priced = fields.Boolean('Is Priced')
    register_number = fields.Char('Register Number')
    color = fields.Char('Color')
    storage_equip = fields.Char('Storage Equipment')
    total_owners = fields.Integer('Total Owners')
    description = fields.Char('Description')
    show_posting_date = fields.Boolean('Show Posting Date')
    show_exact_location = fields.Boolean('Show Exact Location')
    street_address = fields.Char('Street Address')
    show_price_history = fields.Boolean('Show Price History')
    nett_price = fields.Float('Nett Price')
    nett_price_note = fields.Char('Nett Price Note')
    delivery_cost = fields.Float('Delivery Cost')
    warranty_month = fields.Integer('Warranty Month')
    warranty_km = fields.Float('Warranty Km')
    warranty_date = fields.Date('Warranty Date')
    video = fields.Char('Video URL')
    sold_info = fields.Boolean('Add Sold Info', copy=False)
    sold_date = fields.Date('Sold Date', copy=False)
    sold_price = fields.Float('Sold Price', copy=False)
    sold_through_nettivene = fields.Boolean('Sold Through Nettivene',default=True, copy=False)
    sold_comment = fields.Char('Sold Comment', copy=False)
    exchange_trade = fields.Boolean('Exchange Trade',default=False, copy=False)
    labels = fields.Many2many('boat.label',string='Labels')
    is_show_calendar = fields.Boolean('Is Show Calendar')
    has_active_bos = fields.Boolean('Has Active BoS')
    show_bos_status = fields.Boolean('Show BoS Status')
    people_id = fields.Many2many('res.partner', string='People')
    boat_image_ids = fields.One2many('product.image', 'product_tmpl_id', string="Boat Images")
    # nettix_location_id = fields.Many2one(string='Location')
    tradein_boats = fields.One2many('boat.chain','product_id', string='Boat Chain', copy=0)
    margin = fields.Float('Margin', compute='compute_margin', copy=False)
    actual_sale_price = fields.Float('Actual Sale Price', default=1, copy=False)
    # actual_cost = fields.Float('Actual Cost')
    ad_url = fields.Char('Ad URL', readonly=1, copy=0)
    is_equipment = fields.Boolean('Is an Equipment?')
    parent_ids = fields.Many2many('product.template','boat_chain_parent_rel','boat_id','parent_id',string='Chain Parent', copy=0)
    model_id = fields.Many2one('boat.model','Boat Model')
    reference_model = fields.Boolean('Reference Model')
    # order_id = fields.Many2one('sale.order','Quotation')

    @api.depends('product_variant_ids', 'product_variant_ids.standard_price')
    def _compute_standard_price(self):
        for tmpl in self:
            if tmpl.active == False:
                variants = self.env['product.product'].search([('product_tmpl_id','=',tmpl.id),('active','=',False)])
                if len(variants) > 0:
                    tmpl.standard_price = variants[0].standard_price
                else:
                    tmpl.standard_price = 0
            else:
                unique_variants = self.filtered(lambda template: len(template.product_variant_ids) == 1)
                for template in unique_variants:
                    template.standard_price = template.product_variant_ids.standard_price
                for template in (self - unique_variants):
                    variants = self.env['product.product'].search(
                        [('product_tmpl_id', '=', tmpl.id), ('active', '=', False)])
                    if len(variants) > 0:
                        template.standard_price = variants[0].standard_price
                    else:
                        template.standard_price = 0

    def copy(self, default=None):
        pr_id = super(ProductTemplate, self).copy(default)
        pr_id.list_price = 0
        pr_id.active = True
        return pr_id


    @api.depends('actual_sale_price','list_price','standard_price')
    def compute_margin(self):
        for rec in self:
            if rec.actual_sale_price > 1:
                rec.margin = rec.actual_sale_price - rec.standard_price
            elif rec.list_price > 0 and rec.actual_sale_price == 1:
                rec.margin = rec.list_price - rec.standard_price
            else:
                rec.margin = 0


    def create_product_vals(self,function):
        if function == 'create':
            product_vals = {
                "status": self.boat_status,
                "adType": self.ad_type,
                "userId": int(self.user_id.nettix_id),
                "boatType": str(self.boat_type_id.nettix_id),
                "make": str(self.boat_make_id.nettix_id),
                "country": str(self.country_option_id.nettix_id),
                "region": str(self.region_option_id.nettix_id),
                "town": str(self.town_option_id.nettix_id),
                "engineMake": self.engine_make_id.nettix_id,
                "engineType": str(self.engine_type_id.nettix_id),
                "engineStroke": str(self.engine_stroke_id.nettix_id),
                "engineFuelType": str(self.engine_fuel_type_id.nettix_id),
                "yearModelFrom": self.year_model_from,
                "yearModelTo": self.year_model_to,
                "price": self.price,
                "deliveryCost": self.delivery_cost,
                "hasEngine": self.has_engine,
                "twoEngine": self.two_engine,
            }

        if self.boat_sails:
            sail_list = []
            for sails in self.boat_sails:
                sail_dict = {
                    'sailMaterial': sails.sail_material_id.nettix_id,
                    'sailType': sails.sail_type_id.nettix_id,
                    'sailMake': sails.sail_make_id.nettix_id,
                    'sailMfgYear': sails.sail_mfg_year,
                }
                sail_list.append(sail_dict)
            product_vals.update({"sails":sail_list})

        if self.accessory_option_id:
            accessories = []
            for acc in self.accessory_option_id:
                accessories.append({'id': acc.nettix_id, 'info': acc.info})
            if accessories:
                product_vals.update({'accessories': accessories})
        if self.sub_type_id:
            product_vals.update({'subType': int(self.sub_type_id.nettix_id)})
        if self.body_material_id:
            product_vals.update({'bodyMaterial': int(self.body_material_id.nettix_id)})
        if self.sail_steering_id:
            product_vals.update({'sailSteering': int(self.sail_steering_id.nettix_id)})
        if self.availability_id:
            product_vals.update({'availability': str(self.availability_id.code)})
        if self.sail_description:
            product_vals.update({'sailDescription': self.sail_description})
        # if 'has_engine' in vals:
        #     product_vals.update({'hasEngine': vals["has_engine"]})
        if self.engine_rig_id:
            product_vals.update({'engineRig': self.engine_rig_id.nettix_id})
        if self.engine_power:
            product_vals.update({'engPower': self.engine_power})
        if self.engine_model:
            product_vals.update({'engineModel': self.engine_model})
        if self.engine_model_specification:
            product_vals.update({'engineModelSpecification': self.engine_model_specification})
        if self.engine_mfg_year:
            product_vals.update({'engineMfgYear': self.engine_mfg_year})
        if self.engine_hours:
            product_vals.update({'engineHours': self.engine_hours})
        if self.engine_description:
            product_vals.update({'engineDescription': self.engine_description})
        if self.cooling_type_id:
            product_vals.update({'coolingType': str(self.cooling_type_id.nettix_id)})
        if self.heat_fuel_type_id:
            product_vals.update({'heatingFuelType': str(self.heat_fuel_type_id.nettix_id)})
        if self.heat_model_specification:
            product_vals.update({'heatingModelSpecification': self.heat_model_specification})
        if self.heat_make_id:
            product_vals.update({'heatingMake': str(self.heat_make_id.nettix_id)})
        if self.heat_description:
            product_vals.update({'heatingDescription': self.heat_description})
        if self.heat_model:
            product_vals.update({'heatingModel': self.heat_model})
        if self.heat_mfg_year:
            product_vals.update({'heatingMfgYear': self.heat_mfg_year})
        if self.boat_model:
            product_vals.update({'model': self.boat_model})
        if self.boat_length:
            product_vals.update({'boatLength': self.boat_length})
        if self.boat_height:
            product_vals.update({'boatHeight': self.boat_height})
        if self.boat_width:
            product_vals.update({'boatWidth': self.boat_width})
        if self.boat_draft:
            product_vals.update({'boatDraft': self.boat_draft})
        if self.boat_weight:
            product_vals.update({'boatWeight': self.boat_weight})
        if self.year:
            product_vals.update({'year': self.year})
        if self.no_of_beds:
            product_vals.update({'noOfBeds': self.no_of_beds})
        if self.unused:
            product_vals.update({'unused': self.unused})
        if self.price_per_day:
            product_vals.update({'pricePerDay': self.price_per_day})
        if self.is_priced:
            product_vals.update({'isPriced': self.is_priced})
        if self.color:
            product_vals.update({'color': self.color})
        if self.register_number:
            product_vals.update({'registerNumber': self.register_number})
        if self.total_owners:
            product_vals.update({'totalOwners': self.total_owners})
        if self.show_posting_date:
            product_vals.update({'showPostingDate': self.show_posting_date})
        if self.storage_equip:
            product_vals.update({'storageEquipment': self.storage_equip})
        if self.description:
            product_vals.update({'description': self.description})
        if self.show_exact_location:
            product_vals.update({'showExactLocation': self.show_exact_location})
        if self.street_address:
            product_vals.update({'streetAddress': self.street_address})
        if self.show_price_history:
            product_vals.update({'showPriceHistory': self.show_price_history})
        if self.nett_price:
            product_vals.update({'nettPrice': self.nett_price})
        if self.nett_price_note:
            product_vals.update({'nettPriceNote': self.nett_price_note})
        if self.warranty_month:
            product_vals.update({'warrantyMonth': self.warranty_month})
        if self.warranty_date:
            product_vals.update(
                {'warrantyDate': self.warranty_date.strftime("%d.%m.%Y")})
        if self.warranty_km:
            product_vals.update({'warrantyKm':self.warranty_km})
        if self.video:
            product_vals.update({'video':self.video})
        if self.sold_info:
            product_vals.update({
                'soldInfo':{
                    'soldDate': self.sold_date.strftime("%Y-%m-%d"),
                    'soldPrice':int(self.sold_price),
                    'soldThroughNettivene':self.sold_through_nettivene,
                    'soldComment':self.sold_comment,
                    'exchangeTrade':self.exchange_trade,
                }
            })
        if self.people_id:
            people_list = []
            for people in self.people_id:
                people_list.append(people.nettix_id)
            product_vals.update({"people":people_list})

        return product_vals


    def post_nettivene(self):
        idset = []
        if self.env.context.get('active_ids'):
            idset = self.env.context.get('active_ids')
        else:
            idset.append(self.id)
        for rec in idset:
            rec = self.browse([rec])

            if rec.is_boat:
                # Generate access token
                credentials = {
                  "grant_type": "client_credentials",
                  "client_id": self.env.user.nettix_location_id.client_id,
                  "client_secret": self.env.user.nettix_location_id.client_secret
                }
                response = requests.post("https://auth-test.nettix.fi/oauth2/token",data = credentials)
                response = json.loads(response.text)
                if "error" in response:
                    raise UserError(_(response["error_description"]))
                access_token = response["access_token"]
                # Post new product API
                product_vals = rec.create_product_vals('create')
                # Post Image API
                count = 0
                headers = {
                    'X-Access-Token': access_token,
                    'Accept-Language': 'en',
                }
                images = []
                for image in rec.boat_image_ids:
                    if image.nettix_id:
                        images.append(image.nettix_id)
                        continue
                    count = count + 1
                    base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
                    image_url = base_url + "/url/image/" + str(image.boat_image_id)
                    files = []
                    payload = {'imageUrl': image_url, }
                    response = requests.post("https://api-test.nettix.fi/rest/boat/ad/image", data=payload, files=files,
                                             headers=headers)
                    response = json.loads(response.text)
                    images.append({"id": response["id"]})
                    self.env.cr.execute("""update boat_image set binary_value = '', nettix_id = %s where id=%s""" % (response["id"],image.boat_image_id))
                    self.env.cr.execute("""update product_image set nettix_id = %s where id=%s""" % (response["id"], image.id))
                    self.env.cr.commit()
                    if "status" in response and response["status"] != '200':
                        raise ValidationError(response["error"])
                product_vals.update({"images": images})

                headers.update({'Content-Type':'application/json'})
                payload = json.dumps(product_vals)
                if self.nettix_id:
                    response = requests.put("https://api-test.nettix.fi/rest/boat/ad/%s" % (self.nettix_id) , data=payload, headers=headers)
                else:
                    response = requests.post("https://api-test.nettix.fi/rest/boat/ad",data=payload,headers=headers)
                resp = json.loads(response.text)
                message = ''

                if "id" not in resp:
                    for key in resp:
                        message += key + ": " + str(resp[key]) + "\n"
                    raise ValidationError(message)

                else:
                    rec.write({"nettix_id": resp["id"], "ad_url": resp["adUrl"]})
                    view_id = self.env.ref('Nettivene.confirmation_wizard').id
                    # new = view_id.create(params[0])
                    return {
                        'type': 'ir.actions.act_window',
                        'res_model': 'confirmation.message',
                        'view_type': 'form',
                        'view_mode': 'form',
                        # 'res_id': new.id,
                        'view_id': view_id,
                        'target': 'new',
                    }





    @api.model
    def create(self, vals):
        result = super(ProductTemplate, self).create(vals)
        count = 0
        if "boat_image_ids" in vals:
            for image in vals["boat_image_ids"]:
                boat_image = image[2]
                self.env.cr.execute("INSERT INTO boat_image ( binary_value, product_id, image_id )"
                                    "VALUES ('%s', %s, %s)" % (boat_image["image_1920"], result.id, count))
                self.env.cr.commit()
                self.env.cr.execute("""select max(id) from boat_image""")
                res = self._cr.fetchall()
                self.env.cr.execute("""update product_image set boat_image_id = %s where id=%s""" % (res[0][0], result.boat_image_ids[count - 1].id))
                self.env.cr.commit()
                count = count + 1
        return result

    def write(self, vals):
        result = super(ProductTemplate, self).write(vals)
        count = 0
        if "boat_image_ids" in vals:
            for image in vals["boat_image_ids"]:
                boat_image = image[2]
                if boat_image:
                    self.env.cr.execute("INSERT INTO boat_image ( binary_value, product_id, image_id )"
                                        "VALUES ('%s', %s, %s)" % (boat_image["image_1920"], self.id, count))
                    self.env.cr.commit()
                    self.env.cr.execute("""select max(id) from boat_image""")
                    res = self._cr.fetchall()
                    self.env.cr.execute("""update product_image set boat_image_id = %s where id=%s""" % (
                    res[0][0], self.boat_image_ids[count - 1].id))
                    self.env.cr.commit()
                    count = count + 1
        return result

    @api.onchange('boat_type_id')
    def _onchange_boat_type(self):
        return {'domain': {
            'sub_type_id': [('boat_type_id', '=', self.boat_type_id.id)],
            'boat_make_id': [('boat_type_id', '=', self.boat_type_id.id)],
            'accessory_option_id': [('boat_type_id', '=', self.boat_type_id.id)],
        }}

    @api.onchange('country_option_id')
    def _onchange_country(self):
        return {'domain': {
            'region_option_id': [('country_id', '=', self.country_option_id.id)],
        }}

    @api.onchange('region_option_id')
    def _onchange_region(self):
        return {'domain': {
            'town_option_id': [('region_id', '=', self.region_option_id.id)],
        }}

    @api.onchange('price')
    def _onchange_price(self):
        self.list_price = self.price

    @api.onchange('list_price')
    def _onchange_list_price(self):
        self.price = self.list_price

    @api.onchange('model_id')
    def _onchange_model(self):
        if self.model_id:
            self.boat_model = self.model_id.model


class ProductImage(models.Model):
    _inherit = 'product.image'

    nettix_id = fields.Char('Nettix ID')
    boat_image_id = fields.Char('Boat Image ID')


class BoatChain(models.Model):
    _name = 'boat.chain'
    _description = 'Boat Chain'

    boat_id = fields.Many2one('product.template','Boat')
    cost = fields.Float('Cost')
    product_id = fields.Many2one('product.template')
    sales_price=fields.Float('Sales Price')
