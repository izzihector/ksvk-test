from odoo import api, fields, models, _

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    trade_in_lines = fields.One2many('tradein.lines','sale_order_id',string='Trade-In Lines')
    chain_lines = fields.One2many('margin.lines','order_id',string='Chain Lines')
    trade_in_amount = fields.Float('Trade-In Amount', compute='compute_tradein_amount')
    margin_amount = fields.Float('Margin',compute='compute_margin', default=0)
    margin_percentage = fields.Float('Margin Percentage', default=0)
    default_margin_percentage = fields.Float('Margin Percentage', compute='compute_def_percent', default=0)
    model_id = fields.Many2one('boat.model')
    chain_lines_length = fields.Integer(compute='compute_chain_lines_length')
    purchase_order_id = fields.Many2one('purchase.order')
    service_count = fields.Integer('Service Count', compute='_compute_service_count')
    winter_storage_count = fields.Integer('Winter Storage Count', compute='_compute_winter_storage_count')
    water_contract_count = fields.Integer('Water Contract Count', compute='_compute_water_contract_count')

    def create_winter_storage(self):
        for rec in self:
            storage_id = self.env['storage.contract'].create({
                'order_id': rec.id,
                'partner_id': rec.partner_id.id,
                'boat': rec.order_line[0].product_id.name,
                'boat_length': rec.order_line[0].product_id.boat_length,
                'boat_width': rec.order_line[0].product_id.boat_width,
            })

    def create_water_contract(self):
        for rec in self:
            contract_id = self.env['water.contract'].create({
                'order_id': rec.id,
                'partner_id': rec.partner_id.id,
                'boat': rec.order_line[0].product_id.name,
            })

    def create_service(self):
        for rec in self:
            # product_id = self.env['product.product'].search([('product_tmpl_id', '=', rec.boat_id.id)])
            service_id = self.env['service.order'].create({'order_id':rec.id,'partner_id': rec.partner_id.id})

    def _compute_service_count(self):
        ServiceOrder = self.env['service.order']
        for order in self:
            order.service_count = ServiceOrder.search_count(
                [('order_id', '=', order.id)]) or 0

    def _compute_winter_storage_count(self):
        WinterStorage = self.env['storage.contract']
        for order in self:
            order.winter_storage_count = WinterStorage.search_count(
                [('order_id', '=', order.id)]) or 0

    def _compute_water_contract_count(self):
        WaterContract = self.env['water.contract']
        for order in self:
            order.water_contract_count = WaterContract.search_count(
                [('order_id', '=', order.id)]) or 0

    def action_view_services(self):
        self.ensure_one()
        services = self.env['service.order'].search([('order_id', '=', self.id)])
        action = self.env.ref('service_management.service_order_action').read()[0]
        action["context"] = {"create": False}
        if len(services) > 1:
            action['domain'] = [('id', 'in', services.ids)]
        elif len(services) == 1:
            action['views'] = [(self.env.ref('service_management.service_order_form_view').id, 'form')]
            action['res_id'] = services.ids[0]
        else:
            action = {'type': 'ir.actions.act_window_close'}
        return action

    def action_view_winter_storage(self):
        self.ensure_one()
        winter_storages = self.env['storage.contract'].search([('order_id', '=', self.id)])
        action = self.env.ref('boat_winter_storage.storage_contract_action').read()[0]
        action["context"] = {"create": False}
        if len(winter_storages) > 1:
            action['domain'] = [('id', 'in', winter_storages.ids)]
        elif len(winter_storages) == 1:
            action['views'] = [(self.env.ref('boat_winter_storage.storage_contract_form_view').id, 'form')]
            action['res_id'] = winter_storages.ids[0]
        else:
            action = {'type': 'ir.actions.act_window_close'}
        return action

    def action_view_water_contract(self):
        self.ensure_one()
        contracts = self.env['water.contract'].search([('order_id', '=', self.id)])
        action = self.env.ref('boat_on_water.water_contract_action').read()[0]
        action["context"] = {"create": False}
        if len(contracts) > 1:
            action['domain'] = [('id', 'in', contracts.ids)]
        elif len(contracts) == 1:
            action['views'] = [(self.env.ref('boat_on_water.water_contract_form_view').id, 'form')]
            action['res_id'] = contracts.ids[0]
        else:
            action = {'type': 'ir.actions.act_window_close'}
        return action

    def compute_chain_lines_length(self):
        for rec in self:
            rec.chain_lines_length = 0
            if rec.chain_lines:
                rec.chain_lines_length = len(rec.chain_lines.ids)


    @api.onchange('margin')
    def compute_def_percent(self):
        for rec in self:
            total_cost = 0
            if rec.margin and rec.amount_untaxed > 0:
                rec.default_margin_percentage = (rec.margin / rec.amount_untaxed) * 100
            else:
                rec.default_margin_percentage = 0

    def _find_mail_template(self, force_confirmation_template=False):
        template_id = False
        # partner_id = self.env['res.partner'].search([('use')])
        # user_id = self.env['res.users'].search([('partner_id', '=', self.partner_id.id)])
        # if user_id.id and user_id.template_id:
        #     template_id = user_id.template_id.id
        partner_id = self.env['res.users'].search([('id','=',self.env.uid)]).partner_id
        if partner_id.template_id:
            template_id = partner_id.template_id.id
        else:
            if force_confirmation_template or (self.state == 'sale' and not self.env.context.get('proforma', False)):
                template_id = int(self.env['ir.config_parameter'].sudo().get_param('sale.default_confirmation_template'))
                template_id = self.env['mail.template'].search([('id', '=', template_id)]).id
                if not template_id:
                    template_id = self.env['ir.model.data'].xmlid_to_res_id('sale.mail_template_sale_confirmation', raise_if_not_found=False)
            if not template_id:
                template_id = self.env['ir.model.data'].xmlid_to_res_id('sale.email_template_edi_sale', raise_if_not_found=False)

        return template_id


    @api.model
    def create(self,vals):
        result = super(SaleOrder, self).create(vals)
        equipment_total = 0
        for lines in result.order_line:
            if lines.product_id.is_equipment:
                equipment_total += lines.price_unit
        for lines in result.order_line:
            if lines.product_id.is_boat:
                # Add trade in lines to boat chain tab
                lines.product_id.product_tmpl_id.actual_sale_price = self.amount_untaxed - equipment_total
                trade_in_amount = 0
                if result.trade_in_lines:
                    for line in result.trade_in_lines:
                        trade_in_amount += line.cost
                        line.boat_id.write({"sale_order_id": self.id})
                        parent_ids = [lines.product_id.product_tmpl_id.id]
                        self._cr.execute("""select parent_id from boat_chain_parent_rel where boat_id = %s""" % (
                            lines.product_id.product_tmpl_id.id))
                        boat_recs = self._cr.fetchall()

                        for boat in boat_recs:
                            parent_ids.append(boat)
                        if not line.product_ref_id:
                            tradein_product_id = self.env['product.product'].create({
                                'is_boat': True,
                                'name': line.boat_id.name,
                                'standard_price': line.cost,
                                'engine_mfg_year': line.boat_id.engine_mfg_year,
                                'year': line.boat_id.year,
                                'engine_make_id': line.boat_id.engine_make_id.id,
                                'engine_hours': line.boat_id.engine_hours,
                                'parent_ids': [(6, 0, parent_ids)],
                                'type': 'product',
                                'boat_model': line.boat_id.model,
                                'register_number':line.boat_id.register_number,
                            })
                            line.write({"product_ref_id": tradein_product_id.product_tmpl_id.id})

                        # for id in parent_ids:
                        #     existing_lines = self.env['margin.lines'].search(
                        #         [('boat_id', '=', id), ('order_id', '=', self.id)])
                        #     if not existing_lines:
                        #         self.env['margin.lines'].create({
                        #             'boat_id': id,
                        #             'order_id': result.id,
                        #             'main_boat_id': lines.product_id.product_tmpl_id.id,
                        #         })

                # else:
                parent_ids = [lines.product_id.product_tmpl_id.id]
                self._cr.execute("""select parent_id from boat_chain_parent_rel where boat_id = %s""" % (
                    lines.product_id.product_tmpl_id.id))
                boat_recs = self._cr.fetchall()



                for boat in boat_recs:
                    parent_ids.append(boat)
                for id in parent_ids:
                    existing_lines = self.env['margin.lines'].search(
                        [('boat_id', '=', id)])
                    if not existing_lines:
                        chain_id = self.env['margin.lines'].create({
                            'boat_id': id,
                            'order_id': result.id,
                            'main_boat_id': lines.product_id.product_tmpl_id.id,
                        })
                        if not boat_recs:
                            chain_id.write({'root':True})


        # if "order_line" in vals:
        #     for line in vals["order_line"]:
        #         line = line[2]
        #         boat = line["product_template_id"]
        #         boat = self.env['product.template'].browse([boat])
                # if boat.is_boat:
                #     boat.write({
                #         'order_id':result.id,
                #     })
        return result

    def write(self,vals):
        if "trade_in_lines" in vals:
            for row in vals["trade_in_lines"]:
                if row[0] == 2:
                    boat_id = self.env['tradein.lines'].browse(row[1]).product_ref_id
                    if not boat_id.reference_model:
                        boat_id.active = False
                    # boat_id.product_tmpl_id.active = False
                    self._cr.execute("""delete from boat_chain_parent_rel where boat_id = %s or parent_id = %s""" % (boat_id.id, boat_id.id))
        result = super(SaleOrder, self).write(vals)
        equipment_total = 0
        for lines in self.order_line:
            if lines.product_id.is_equipment:
                equipment_total += lines.price_unit
        for lines in self.order_line:
            lines.product_id.product_tmpl_id.actual_sale_price = self.amount_untaxed - equipment_total
            if lines.product_id.is_boat:
                # Add trade in lines to boat chain tab
                trade_in_amount = 0
                if self.trade_in_lines:
                    for line in self.trade_in_lines:
                        trade_in_amount += line.cost
                        line.boat_id.write({"sale_order_id": self.id})
                        parent_ids = [lines.product_id.product_tmpl_id.id]
                        self._cr.execute("""select parent_id from boat_chain_parent_rel where boat_id = %s""" % (
                            lines.product_id.product_tmpl_id.id))
                        boat_recs = self._cr.fetchall()

                        for boat in boat_recs:
                            parent_ids.append(boat)
                        if not line.product_ref_id:
                            tradein_product_id = self.env['product.product'].create({
                                'is_boat': True,
                                'name': line.boat_id.name,
                                'standard_price': line.cost,
                                'engine_mfg_year': line.boat_id.engine_mfg_year,
                                'year': line.boat_id.year,
                                'engine_make_id': line.boat_id.engine_make_id.id,
                                'engine_hours': line.boat_id.engine_hours,
                                'parent_ids': [(6, 0, parent_ids)],
                                'type': 'product',
                                'boat_model': line.boat_id.model,
                                'register_number': line.boat_id.register_number,
                            })
                            line.write({"product_ref_id":tradein_product_id.product_tmpl_id.id})

                        # for id in parent_ids:
                        #     existing_lines = self.env['margin.lines'].search([('boat_id','=',id),('order_id','=',self.id)])
                        #     if not existing_lines:
                        #         self.env['margin.lines'].create({
                        #             'boat_id': id,
                        #             'order_id': self.id,
                        #             'main_boat_id': lines.product_id.product_tmpl_id.id,
                        #         })

                # else:
                parent_ids = [lines.product_id.product_tmpl_id.id]
                self._cr.execute("""select parent_id from boat_chain_parent_rel where boat_id = %s""" % (
                    lines.product_id.product_tmpl_id.id))
                boat_recs = self._cr.fetchall()
                for boat in boat_recs:
                    parent_ids.append(boat)
                for id in parent_ids:
                    existing_lines = self.env['margin.lines'].search(
                        [('boat_id', '=', id), ('order_id', '=', self.id)])
                    if not existing_lines:
                        chain_id = self.env['margin.lines'].create({
                            'boat_id': id,
                            'order_id': self.id,
                            'main_boat_id': lines.product_id.product_tmpl_id.id,
                        })
                        if not boat_recs:
                            chain_id.write({'root':True})
        # if "order_line" in vals:
        #     for line in vals["order_line"]:
        #         line = line[2]
        #         boat = line["product_template_id"]
        #         boat = self.env['product.template'].browse([boat])
        #         if boat.is_boat:
        #             boat.write({
        #                 'order_id':self.id,
        #             })
        return result

    def open_equipment_wizard(self):
        if self.model_id:
            model_id = self.model_id
            equipments = model_id.equipment_ids
            recs = []
            for equip in equipments:
                list_id = self.env['boat.list'].create({
                    'boat_id':equip.equip_id.id,
                })
                recs.append(list_id.id)
            return {
                'name': _("Add Equipments"),
                'view_mode': 'form',
                'view_type': 'form',
                'view_id': False,
                'res_model': 'add.equipment.wizard',
                'type': 'ir.actions.act_window',
                'nodestroy': True,
                'target': 'new',
                'domain': '[]',
                'context':{'default_records':[(6,0,recs)]},
            }
        else:
            equipments = self.env['product.template'].search([('is_equipment','=',True)])
            recs = []
            for equip in equipments:
                list_id = self.env['boat.list'].create({
                    'boat_id': equip.id,
                })
                recs.append(list_id.id)
            return {
                'name': _("Add Equipments"),
                'view_mode': 'form',
                'view_type': 'form',
                'view_id': False,
                'res_model': 'add.equipment.wizard',
                'type': 'ir.actions.act_window',
                'nodestroy': True,
                'target': 'new',
                'domain': '[]',
                'context': {'default_records': [(6, 0, recs)]},
            }

    @api.depends('chain_lines')
    def compute_margin(self):
        for rec in self:
            rec.margin_amount = 0
            rec.margin_percentage = 0
            total_price = 0
            for line in self.chain_lines:
                if line.actual_sale_price >= 1:
                    total_price += line.actual_sale_price
                    rec.margin_amount += line.margin
                if total_price > 0:
                    rec.margin_percentage = (rec.margin_amount/total_price) * 100

    @api.depends('trade_in_lines')
    def compute_tradein_amount(self):
        self.trade_in_amount = 0
        if self.trade_in_lines:
            for line in self.trade_in_lines:
                self.trade_in_amount += line.cost


    @api.depends('order_line.price_total','trade_in_lines')
    def _amount_all(self):
        """
                Compute the total amounts of the SO.
                """
        for order in self:
            amount_untaxed = amount_tax = 0.0
            for line in order.order_line:
                amount_untaxed += line.price_subtotal
                amount_tax += line.price_tax
            order.update({
                'amount_untaxed': amount_untaxed,
                'amount_tax': amount_tax,
                'amount_total': amount_untaxed + amount_tax - order.trade_in_amount,
            })

    def action_confirm(self):
        result = super(SaleOrder, self).action_confirm()
        equipment_total = 0
        for lines in self.order_line:
            if lines.product_id.is_equipment:
                equipment_total += lines.price_unit
        for lines in self.order_line:
            if lines.product_id.is_boat:
                if not lines.product_id.reference_model:
                    lines.product_id.active = False
                    lines.product_id.product_tmpl_id.active = False
                    lines.product_id.boat_status = 'sold'
                    lines.product_id.sold_info = True
                    lines.product_id.sold_date = self.date_order
                    lines.product_id.sold_price = self.amount_untaxed - equipment_total
                lines.product_id.actual_sale_price = self.amount_untaxed - equipment_total

                #Add trade in lines to boat chain tab
                trade_in_amount = 0
                if self.trade_in_lines:
                    warehouse_id = self.warehouse_id
                    purchase_order_id = self.env['purchase.order'].create({
                        "company_id": self.env.user.company_id.id,
                        "currency_id": self.env.user.company_id.currency_id.id,
                        "date_order": self.date_order,
                        "name": self.env['ir.sequence'].next_by_code('purchase.order') or '/',
                        "partner_id": self.partner_id.id,
                        "picking_type_id": warehouse_id.in_type_id.id,
                    })
                    self.purchase_order_id = purchase_order_id.id

                    for line in self.trade_in_lines:
                        trade_in_amount += line.cost
                        line.boat_id.write({"sale_order_id":self.id})
                        parent_ids = [lines.product_id.product_tmpl_id.id]
                        self._cr.execute("""select parent_id from boat_chain_parent_rel where boat_id = %s""" % (lines.product_id.product_tmpl_id.id))
                        boat_recs = self._cr.fetchall()

                        for boat in boat_recs:
                            parent_ids.append(boat)

                        if not line.product_ref_id:
                            tradein_product_vals = {
                                'is_boat':True,
                                'name':line.boat_id.name,
                                'standard_price':line.cost,
                                'engine_mfg_year': line.boat_id.engine_mfg_year,
                                'year': line.boat_id.year,
                                'engine_make_id': line.boat_id.engine_make_id.id,
                                'engine_hours': line.boat_id.engine_hours,
                                'parent_ids':[(6,0,parent_ids)],
                                'type':'product',
                                'boat_model':line.boat_id.model,
                                'register_number': line.boat_id.register_number,
                            }
                            if self.env.company.po_tax_id:
                                tradein_product_vals.update({'supplier_taxes_id':[(4,self.env.company.po_tax_id.id,0)]})
                            tradein_product_id = self.env['product.product'].create(tradein_product_vals)
                            line.write({"product_ref_id": tradein_product_id.product_tmpl_id.id})
                        else:
                            tradein_product_id = self.env['product.product'].search([('product_tmpl_id','=',line.product_ref_id.id)])
                            if self.env.company.po_tax_id:
                                tradein_product_id.write({'supplier_taxes_id':[(4,self.env.company.po_tax_id.id,0)]})
                        lines.product_id.tradein_boats = [
                            (0, 0, {"boat_id": tradein_product_id.product_tmpl_id.id, "cost": line.cost, })]

                        # for id in parent_ids:
                        #     existing_lines = self.env['margin.lines'].search(
                        #         [('boat_id', '=', id), ('order_id', '=', self.id)])
                        #     if not existing_lines:
                        #         self.env['margin.lines'].create({
                        #             'boat_id': id,
                        #             'order_id': self.id,
                        #             'main_boat_id': lines.product_id.product_tmpl_id.id,
                        #         })

                        purchase_vals = {
                            "name": line.boat_id.name,
                            "order_id": purchase_order_id.id,
                            "price_unit":line.cost,
                            "product_qty":1,
                            "product_id":tradein_product_id.id,
                            "display_type": False,
                            "product_uom": 1,
                            "date_planned": self.date_order,
                        }
                        if self.env.company.po_tax_id:
                            purchase_vals.update({"taxes_id": [(4, self.env.company.po_tax_id.id, 0)]})
                        print(purchase_vals,"kkjkkj")
                        self.env['purchase.order.line'].create(purchase_vals)
                        print("%%%%%%%%%%%")
                # else:
                parent_ids = [lines.product_id.product_tmpl_id.id]
                self._cr.execute("""select parent_id from boat_chain_parent_rel where boat_id = %s""" % (
                    lines.product_id.product_tmpl_id.id))
                boat_recs = self._cr.fetchall()

                for boat in boat_recs:
                    parent_ids.append(boat)
                for id in parent_ids:
                    existing_lines = self.env['margin.lines'].search(
                        [('boat_id', '=', id), ('order_id', '=', self.id)])
                    if not existing_lines:
                        chain_id = self.env['margin.lines'].create({
                            'boat_id': id,
                            'order_id': self.id,
                            'main_boat_id': lines.product_id.product_tmpl_id.id,
                        })
                        if not boat_recs:
                            chain_id.write({'root': True})




                lines.product_id.product_tmpl_id.actual_sale_price = self.amount_untaxed - equipment_total
                lines.product_id.exchange_trade = True

                # Check if exchange product
                tradein_id = self.env['boat.chain'].search([('boat_id', '=', lines.product_id.product_tmpl_id.id)])
                if tradein_id:
                        tradein_id.sales_price = self.amount_untaxed - equipment_total
                if lines.product_id.product_tmpl_id.nettix_id:
                    lines.product_id.product_tmpl_id.post_nettivene()
        
        return result

    def action_cancel(self):
        result = super(SaleOrder, self).action_cancel()
        self.purchase_order_id.button_cancel()
        for lines in self.order_line:
            if lines.product_id.is_boat:
                lines.product_id.active = True
                lines.product_id.product_tmpl_id.active = True
                lines.product_id.boat_status = 'forsale'
                lines.product_id.sold_info = False
                lines.product_id.sold_date = ''
                lines.product_id.sold_price = ''
                lines.product_id.actual_sale_price = ''
                # lines.product_id.product_tmpl_id.order_id = False
        for lines in self.chain_lines:
            lines.order_id = False
        for lines in self.trade_in_lines:
            product_id = lines.product_ref_id
            if not product_id.reference_model:
                product_id.active = False
        return result

    def action_draft(self):
        result = super(SaleOrder, self).action_draft()
        for lines in self.order_line:
            if lines.product_id.is_boat:
                lines.product_id.active = True
                lines.product_id.product_tmpl_id.active = True
                lines.product_id.boat_status = 'forsale'
                lines.product_id.sold_info = False
                lines.product_id.sold_date = ''
                lines.product_id.sold_price = ''
                lines.product_id.actual_sale_price = ''
                # lines.product_id.product_tmpl_id.order_id = False
        for lines in self.chain_lines:
            lines.order_id = self.id
        for lines in self.trade_in_lines:
            product_id = lines.product_ref_id
            product_id.active = True
        return result


    def _create_invoices(self, grouped=False, final=False):
        moves = super(SaleOrder, self)._create_invoices()
        for move in moves:
            tradein_ids = []
            tradein_vals = {}
            for tl in self.trade_in_lines:
                tl_product_id = self.env['product.product'].search([('product_tmpl_id','=',tl.product_ref_id.id)])
                move.write({
                    'invoice_line_ids':[(0,0,{
                        'name': tl.boat_id.name,
                        'price_unit': -tl.cost,
                        'quantity': 1.0,
                        'product_id': tl_product_id.id,
                    })]
                })
                tradein_ids.append(self.env['tradein.lines'].create({
                    'boat_id': tl.boat_id.id,
                    'cost': tl.cost,
                    'sales_price': tl.sales_price,
                    'account_move_id': move.id,
                    'sale_order_id': '',
                }).id)

            move.write({
                'trade_in_lines': [(6, 0, tradein_ids)],
            })
        return moves


# class SaleOrderLine(models.Model):
#     _inherit = 'sale.order.line'
#
#     @api.onchange('product_id')
#     def onchange_product(self):
#         return {'domain': {
#             'product_id': [('order_id','=',False)],
#         }
#     }

