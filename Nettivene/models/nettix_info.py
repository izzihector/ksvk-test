from odoo import api, fields, models, _
import requests
import json

class NettixOptions(models.Model):
    _name = 'nettix.options'
    _description = 'Nettix Options'

    def sync_data(self):
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
            # Boat Type
            response = requests.get("https://api-test.nettix.fi/rest/boat/options/boatType", headers=headers)
            response = json.loads(response.text)
            for rec in response:
                existing_boat_type = self.env['boat.type'].search([('nettix_id', '=', rec['id'])])
                if not existing_boat_type:
                    self.env['boat.type'].create({
                        'fi': rec['fi'],
                        'nettix_id': rec['id'],
                        'en': rec['en'],
                    })
                else:
                    existing_boat_type.write({
                        'fi': rec['fi'],
                        'nettix_id': rec['id'],
                        'en': rec['en'],
                    })

            # Body Material
            response = requests.get("https://api-test.nettix.fi/rest/boat/options/bodyMaterial", headers=headers)
            response = json.loads(response.text)
            for rec in response:
                existing_body_material = self.env['body.material'].search([('nettix_id', '=', rec['id'])])
                if not existing_body_material:
                    self.env['body.material'].create({
                        'fi': rec['fi'],
                        'nettix_id': rec['id'],
                        'en': rec['en'],
                    })
                else:
                    existing_body_material.write({
                        'fi': rec['fi'],
                        'nettix_id': rec['id'],
                        'en': rec['en'],
                    })

            # Country
            response = requests.get("https://api-test.nettix.fi/rest/boat/options/country", headers=headers)
            response = json.loads(response.text)
            for rec in response:
                existing_country = self.env['country.option'].search([('nettix_id', '=', rec['id'])])
                if not existing_country:
                    self.env['country.option'].create({
                        'fi': rec['fi'],
                        'nettix_id': rec['id'],
                        'en': rec['en'],
                        'iso_code':rec['isoCode']
                    })
                else:
                    existing_country.write({
                        'fi': rec['fi'],
                        'nettix_id': rec['id'],
                        'en': rec['en'],
                        'iso_code': rec['isoCode']
                    })

            # Sail Type
            response = requests.get("https://api-test.nettix.fi/rest/boat/options/sailType", headers=headers)
            response = json.loads(response.text)
            for rec in response:
                existing_sail_type = self.env['sail.type'].search([('nettix_id', '=', rec['id'])])
                if not existing_sail_type:
                    self.env['sail.type'].create({
                        'fi': rec['fi'],
                        'nettix_id': rec['id'],
                        'en': rec['en'],
                    })
                else:
                    existing_sail_type.write({
                        'fi': rec['fi'],
                        'nettix_id': rec['id'],
                        'en': rec['en'],
                    })

            # Sail Make
            response = requests.get("https://api-test.nettix.fi/rest/boat/options/sailMake", headers=headers)
            response = json.loads(response.text)
            for rec in response:
                existing_sail_make = self.env['sail.make'].search([('nettix_id', '=', rec['id'])])
                if not existing_sail_make:
                    self.env['sail.make'].create({
                        'name': rec['name'],
                        'nettix_id': rec['id'],
                    })
                else:
                    existing_sail_make.write({
                        'name': rec['name'],
                        'nettix_id': rec['id'],
                    })

            # Sail Material
            response = requests.get("https://api-test.nettix.fi/rest/boat/options/sailMaterial", headers=headers)
            response = json.loads(response.text)
            for rec in response:
                existing_sail_material = self.env['sail.material'].search([('nettix_id', '=', rec['id'])])
                if not existing_sail_material:
                    self.env['sail.material'].create({
                        'name': rec['name'],
                        'nettix_id': rec['id'],
                    })
                else:
                    existing_sail_material.write({
                        'name': rec['name'],
                        'nettix_id': rec['id'],
                    })

            # Engine Type
            response = requests.get("https://api-test.nettix.fi/rest/boat/options/engineType", headers=headers)
            response = json.loads(response.text)
            for rec in response:
                existing_engine_type = self.env['engine.type'].search([('nettix_id', '=', rec['id'])])
                if not existing_engine_type:
                    self.env['engine.type'].create({
                        'fi': rec['fi'],
                        'en': rec['en'],
                        'nettix_id': rec['id'],
                    })
                else:
                    existing_engine_type.write({
                        'fi': rec['fi'],
                        'en': rec['en'],
                        'nettix_id': rec['id'],
                    })

            # Engine Stroke
            response = requests.get("https://api-test.nettix.fi/rest/boat/options/engineStroke", headers=headers)
            response = json.loads(response.text)
            for rec in response:
                existing_engine_stroke = self.env['engine.stroke'].search([('nettix_id', '=', rec['id'])])
                if not existing_engine_stroke:
                    self.env['engine.stroke'].create({
                        'fi': rec['fi'],
                        'en': rec['en'],
                        'nettix_id': rec['id'],
                    })
                else:
                    existing_engine_stroke.write({
                        'fi': rec['fi'],
                        'en': rec['en'],
                        'nettix_id': rec['id'],
                    })

            # Engine Rig
            response = requests.get("https://api-test.nettix.fi/rest/boat/options/engineRig", headers=headers)
            response = json.loads(response.text)
            for rec in response:
                existing_engine_rig = self.env['engine.rig'].search([('nettix_id', '=', rec['id'])])
                if not existing_engine_rig:
                    self.env['engine.rig'].create({
                        'fi': rec['fi'],
                        'en': rec['en'],
                        'nettix_id': rec['id'],
                    })
                else:
                    existing_engine_rig.write({
                        'fi': rec['fi'],
                        'en': rec['en'],
                        'nettix_id': rec['id'],
                    })

            # Engine Fuel Type
            response = requests.get("https://api-test.nettix.fi/rest/boat/options/engineFuelType", headers=headers)
            response = json.loads(response.text)
            for rec in response:
                existing_engine_fuel_type = self.env['engine.fuel.type'].search([('nettix_id', '=', rec['id'])])
                if not existing_engine_fuel_type:
                    self.env['engine.fuel.type'].create({
                        'fi': rec['fi'],
                        'en': rec['en'],
                        'nettix_id': rec['id'],
                    })
                else:
                    existing_engine_fuel_type.write({
                        'fi': rec['fi'],
                        'en': rec['en'],
                        'nettix_id': rec['id'],
                    })

            # Engine Power
            response = requests.get("https://api-test.nettix.fi/rest/boat/options/enginePower", headers=headers)
            response = json.loads(response.text)
            for rec in response:
                existing_engine_power = self.env['engine.power'].search([('nettix_id', '=', rec['id'])])
                if not existing_engine_power:
                    self.env['engine.power'].create({
                        'name': rec['name'],
                        'nettix_id': rec['id'],
                    })
                else:
                    existing_engine_power.write({
                        'name': rec['name'],
                        'nettix_id': rec['id'],
                    })

            # Cooling Type
            response = requests.get("https://api-test.nettix.fi/rest/boat/options/coolingType", headers=headers)
            response = json.loads(response.text)
            for rec in response:
                existing_cooling_type = self.env['cooling.type'].search([('nettix_id', '=', rec['id'])])
                if not existing_cooling_type:
                    self.env['cooling.type'].create({
                        'fi': rec['fi'],
                        'en': rec['en'],
                        'nettix_id': rec['id'],
                    })
                else:
                    existing_cooling_type.write({
                        'fi': rec['fi'],
                        'en': rec['en'],
                        'nettix_id': rec['id'],
                    })

            # Heating Make
            response = requests.get("https://api-test.nettix.fi/rest/boat/options/heatingMake", headers=headers)
            response = json.loads(response.text)
            for rec in response:
                existing_heating_make = self.env['heating.make'].search([('nettix_id', '=', rec['id'])])
                if not existing_heating_make:
                    self.env['heating.make'].create({
                        'name': rec['name'],
                        'nettix_id': rec['id'],
                    })
                else:
                    existing_heating_make.write({
                        'name': rec['name'],
                        'nettix_id': rec['id'],
                    })

            # Heating Fuel Type
            response = requests.get("https://api-test.nettix.fi/rest/boat/options/heatingFuelType", headers=headers)
            response = json.loads(response.text)
            for rec in response:
                existing_heating_fuel_type = self.env['heating.fuel.type'].search([('nettix_id', '=', rec['id'])])
                if not existing_heating_fuel_type:
                    self.env['heating.fuel.type'].create({
                        'fi': rec['fi'],
                        'en': rec['en'],
                        'nettix_id': rec['id'],
                    })
                else:
                    existing_heating_fuel_type.write({
                        'fi': rec['fi'],
                        'en': rec['en'],
                        'nettix_id': rec['id'],
                    })

            # Availability
            response = requests.get("https://api-test.nettix.fi/rest/boat/options/availability", headers=headers)
            response = json.loads(response.text)
            for rec in response:
                existing_availability = self.env['availability.option'].search([('code', '=', rec['code'])])
                if not existing_availability:
                    self.env['availability.option'].create({
                        'fi': rec['fi'],
                        'en': rec['en'],
                        'code': rec['code'],
                    })
                else:
                    existing_availability.write({
                        'fi': rec['fi'],
                        'en': rec['en'],
                        'code': rec['code'],
                    })

            # Sail Steering
            response = requests.get("https://api-test.nettix.fi/rest/boat/options/sailSteering", headers=headers)
            response = json.loads(response.text)
            for rec in response:
                existing_sail_steering = self.env['sail.steering'].search([('nettix_id', '=', rec['id'])])
                if not existing_sail_steering:
                    self.env['sail.steering'].create({
                        'fi': rec['fi'],
                        'en': rec['en'],
                        'nettix_id': rec['id'],
                    })
                else:
                    existing_sail_steering.write({
                        'fi': rec['fi'],
                        'en': rec['en'],
                        'nettix_id': rec['id'],
                    })

            # Sub Type
            boat_type_ids = self.env['boat.type'].search([])
            for bt in boat_type_ids:
                response = requests.get("https://api-test.nettix.fi/rest/boat/options/subType",params={'boatTypeId':bt.nettix_id}, headers=headers)
                response = json.loads(response.text)
                for rec in response:
                    existing_sub_type = self.env['sub.type'].search([('fi', '=', rec['fi'])])
                    if not existing_sub_type:
                        self.env['sub.type'].create({
                            'fi': rec['fi'],
                            'en': rec['en'],
                            'nettix_id': rec['id'],
                            'boat_type_id': [(4,bt.id)]
                        })
                    else:
                        existing_sub_type.write({
                            'fi': rec['fi'],
                            'en': rec['en'],
                            'nettix_id': rec['id'],
                            'boat_type_id': [(4,bt.id)]
                        })
                # Boat Make
                response = requests.get("https://api-test.nettix.fi/rest/boat/options/make",params={'boatTypeId':bt.nettix_id}, headers=headers)
                response = json.loads(response.text)
                for rec in response:
                    existing_boat_make = self.env['boat.make'].search([('name', '=', rec['name'])])
                    if not existing_boat_make:
                        self.env['boat.make'].create({
                            'name': rec['name'],
                            'mostPopular': rec['mostPopular'],
                            'nettix_id': rec['id'],
                            'boat_type_id': [(4,bt.id)]
                        })
                    else:
                        existing_boat_make.write({
                            'name': rec['name'],
                            'mostPopular': rec['mostPopular'],
                            'nettix_id': rec['id'],
                            'boat_type_id': [(4,bt.id)]
                        })

                # Accessories
                response = requests.get("https://api-test.nettix.fi/rest/boat/options/accessories",
                                        params={'boatTypeId': bt.nettix_id}, headers=headers)
                response = json.loads(response.text)
                for rec in response:
                    existing_accessory = self.env['accessory.option'].search([('fi', '=', rec['fi'])])
                    if not existing_accessory:
                        self.env['accessory.option'].create({
                            'fi': rec['fi'],
                            'en': rec['en'],
                            'nettix_id': rec['id'],
                            'boat_type_id': [(4, bt.id)],
                            'info':rec['info'],
                        })
                    else:
                        existing_accessory.write({
                            'fi': rec['fi'],
                            'en': rec['en'],
                            'nettix_id': rec['id'],
                            'boat_type_id': [(4, bt.id)],
                            'info': rec['info'],
                        })

            # Region
            country_ids = self.env['country.option'].search([])
            for ct in country_ids:
                response = requests.get("https://api-test.nettix.fi/rest/boat/options/region",
                                        params={'countryId': ct.nettix_id}, headers=headers)
                response = json.loads(response.text)
                for rec in response:
                    existing_region = self.env['region.option'].search([('fi', '=', rec['fi'])])
                    if not existing_region:
                        self.env['region.option'].create({
                            'fi': rec['fi'],
                            'en': rec['en'],
                            'nettix_id': rec['id'],
                            'country_id': [(4,ct.id)]
                        })
                    else:
                        existing_region.write({
                            'fi': rec['fi'],
                            'en': rec['en'],
                            'nettix_id': rec['id'],
                            'country_id': [(4,ct.id)]
                        })

            # Town
            region_ids = self.env['region.option'].search([])
            for rt in region_ids:
                response = requests.get("https://api-test.nettix.fi/rest/boat/options/town",
                                        params={'regionId': rt.nettix_id}, headers=headers)
                response = json.loads(response.text)
                for rec in response:
                    existing_town = self.env['town.option'].search([('fi', '=', rec['fi'])])
                    if not existing_town:
                        self.env['town.option'].create({
                            'fi': rec['fi'],
                            'en': rec['en'],
                            'nettix_id': rec['id'],
                            'region_id': [(4, rt.id)]
                        })
                    else:
                        existing_town.write({
                            'fi': rec['fi'],
                            'en': rec['en'],
                            'nettix_id': rec['id'],
                            'region_id': [(4, rt.id)]
                        })
        # else:
        #     self.env['res.config.settings'].get_access_token()

class BoatType(models.Model):
    _name = 'boat.type'
    _rec_name= 'fi'
    _description= 'Boat Type Model'

    nettix_id = fields.Integer(string="Id of the option")
    fi = fields.Char(string="Finnish Name")
    en = fields.Char(string="English Name")
    aliases = fields.Char(string="Alias Name")

class SubType(models.Model):
    _name = 'sub.type'
    _rec_name= 'fi'
    _description = 'Sub Type'

    boat_type_id = fields.Many2many('boat.type',string="Boat Type Nettix ID")
    nettix_id = fields.Integer(string="Id of the option")
    fi = fields.Char(string="Finnish Name")
    en = fields.Char(string="English Name")
    aliases = fields.Char(string="Alias Name")

class BoatMake(models.Model):
    _name = 'boat.make'
    _rec_name= 'name'
    _description = 'Boat Make'

    boat_type_id = fields.Many2many('boat.type','boat_type_make_rel','boat_type_id','make_id',string="Boat Type Nettix ID")
    nettix_id = fields.Integer(string="Id of the option")
    name = fields.Char(string="Name for option value")
    mostPopular = fields.Boolean(string="Most Popular")

class BodyMaterial(models.Model):
    _name = 'body.material'
    _rec_name= 'fi'
    _description = 'Body Material'

    nettix_id = fields.Integer(string="Id of the option")
    fi = fields.Char(string="Finnish Name")
    en = fields.Char(string="English Name")
    aliases = fields.Char(string="Alias Name")

class CountryOption(models.Model):
    _name = 'country.option'
    _rec_name= 'fi'
    _description = 'Country Option'

    nettix_id = fields.Integer(string="Id of the option")
    fi = fields.Char(string="Finnish Name")
    en = fields.Char(string="English Name")
    aliases = fields.Char(string="Alias Name")
    iso_code = fields.Char(string="Country ISO code")
    country_id =fields.Many2one('res.country')

class RegionOption(models.Model):
    _name = 'region.option'
    _rec_name= 'fi'
    _description = 'Region Option'

    nettix_id = fields.Integer(string="Id of the option")
    fi = fields.Char(string="Finnish Name")
    en = fields.Char(string="English Name")
    aliases = fields.Char(string="Alias Name")
    country_id =fields.Many2many('country.option','country_region_rel','country_id','region_id')


class TownOption(models.Model):
    _name = 'town.option'
    _rec_name= 'fi'
    _description = 'Town Option'

    nettix_id = fields.Integer(string="Id of the option")
    fi = fields.Char(string="Finnish Name")
    en = fields.Char(string="English Name")
    aliases = fields.Char(string="Alias Name")
    region_id = fields.Many2many('region.option', 'region_town_rel', 'region_id', 'town_id')

class SailType(models.Model):
    _name = 'sail.type'
    _rec_name= 'fi'
    _description = 'Sail Type'

    nettix_id = fields.Integer(string="Id of the option")
    fi = fields.Char(string="Finnish Name")
    en = fields.Char(string="English Name")
    aliases = fields.Char(string="Alias Name")

class SailMake(models.Model):
    _name = 'sail.make'
    _rec_name= 'name'
    _description = 'Sail Make'

    nettix_id = fields.Integer(string="Id of the option")
    name = fields.Char(string="Name for option value")

class SailMaterial(models.Model):
    _name = 'sail.material'
    _rec_name= 'name'
    _description = 'Sail Material'

    nettix_id = fields.Integer(string="Id of the option")
    name = fields.Char(string="Name for option value")

class EngineType(models.Model):
    _name = 'engine.type'
    _rec_name= 'fi'
    _description = 'Engine Type Model'

    nettix_id = fields.Integer(string="Id of the option")
    fi = fields.Char(string="Finnish Name")
    en = fields.Char(string="English Name")
    aliases = fields.Char(string="Alias Name")

class EngineStroke(models.Model):
    _name = 'engine.stroke'
    _rec_name= 'fi'
    _description = 'Engine Stroke Model'

    nettix_id = fields.Integer(string="Id of the option")
    fi = fields.Char(string="Finnish Name")
    en = fields.Char(string="English Name")
    aliases = fields.Char(string="Alias Name")

class EngineRig(models.Model):
    _name = 'engine.rig'
    _rec_name= 'fi'
    _description = 'Engine Rig Model'

    nettix_id = fields.Integer(string="Id of the option")
    fi = fields.Char(string="Finnish Name")
    en = fields.Char(string="English Name")
    aliases = fields.Char(string="Alias Name")

class EngineFuelType(models.Model):
    _name = 'engine.fuel.type'
    _rec_name= 'fi'
    _description = 'Engine Fuel Type Model'

    nettix_id = fields.Integer(string="Id of the option")
    fi = fields.Char(string="Finnish Name")
    en = fields.Char(string="English Name")
    aliases = fields.Char(string="Alias Name")

class EnginePower(models.Model):
    _name = 'engine.power'
    _rec_name= 'name'
    _description = 'Engine Power'

    nettix_id = fields.Integer(string="Id of the option")
    name = fields.Char(string="Name for option value")

class CoolingType(models.Model):
    _name = 'cooling.type'
    _rec_name= 'fi'
    _description = 'Cooling Type'

    nettix_id = fields.Integer(string="Id of the option")
    fi = fields.Char(string="Finnish Name")
    en = fields.Char(string="English Name")
    aliases = fields.Char(string="Alias Name")

class HeatingMake(models.Model):
    _name = 'heating.make'
    _rec_name= 'name'
    _description = 'Heating Make'

    nettix_id = fields.Integer(string="Id of the option")
    name = fields.Char(string="Name for option value")

class HeatingFuelType(models.Model):
    _name = 'heating.fuel.type'
    _rec_name= 'fi'
    _description = 'Heating Fuel Type'

    nettix_id = fields.Integer(string="Id of the option")
    fi = fields.Char(string="Finnish Name")
    en = fields.Char(string="English Name")
    aliases = fields.Char(string="Alias Name")

class AccessoryOption(models.Model):
    _name = 'accessory.option'
    _rec_name= 'fi'
    _description = 'Accessory Option'

    nettix_id = fields.Integer(string="Id of the option")
    fi = fields.Char(string="Finnish Name")
    en = fields.Char(string="English Name")
    aliases = fields.Char(string="Alias Name")
    info = fields.Char(string="Accessory info")
    boat_type_id = fields.Many2many('boat.type', 'boat_type_accessory_rel',string="Boat Type Nettix ID")

class Availability(models.Model):
    _name = 'availability.option'
    _rec_name= 'code'
    _description = 'Availability Option'

    code = fields.Char(string="code value of the option")
    fi = fields.Char(string="Finnish Name")
    en = fields.Char(string="English Name")

class CategoryOption(models.Model):
    _name = 'category.option'
    _rec_name= 'fi'
    _description = 'Category Option'

    nettix_id = fields.Integer(string="Id of the option")
    fi = fields.Char(string="Finnish Name") 
    en = fields.Char(string="English Name")
    aliases = fields.Char(string="Alias Name")

class SailSteering(models.Model):
    _name = 'sail.steering'
    _rec_name= 'fi'
    _description = 'Sail Steering'

    nettix_id = fields.Integer(string="Id of the option")
    fi = fields.Char(string="Finnish Name")
    en = fields.Char(string="English Name")
    aliases = fields.Char(string="Alias Name")

class TagOptions(models.Model):
    _name = 'tag.option'
    _rec_name= 'fi'
    _description = 'Tag Option'

    nettix_id = fields.Integer(string="Id of the option")
    fi = fields.Char(string="Finnish Name")
    en = fields.Char(string="English Name")
    descriptionFi = fields.Char(string="Finnish description of the option")
    descriptionEn = fields.Char(string="English description of the option")

class BoatImage(models.Model):
    _name = 'boat.image'
    _description = 'Boat Image'

    binary_value = fields.Char('Binary')
    product_id = fields.Integer('Product ID')
    image_id = fields.Integer('Image Number')
    nettix_id = fields.Integer('Nettix ID')

class BoatLabels(models.Model):
    _name = 'boat.label'
    _description = 'Boat Label'

    name = fields.Char('Name')

class BoatSails(models.Model):
    _name = 'boat.sail'
    _description = 'Boat Sail'

    sail_type_id = fields.Many2one('sail.type')
    sail_make_id = fields.Many2one('sail.make')
    sail_material_id = fields.Many2one('sail.material')
    sail_mfg_year = fields.Integer('Sail Mfg Year')
    product_tmpl_id = fields.Many2one('product.template')

class NettixLocation(models.Model):
    _name = 'nettix.location'
    _description = 'Nettix Location'

    name = fields.Char('Name')
    client_id = fields.Char('Client ID')
    client_secret = fields.Char('Client Secret')

