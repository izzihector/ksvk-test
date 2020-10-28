from odoo import api, fields, models, _
from odoo.exceptions import UserError

class StorageContract(models.Model):
    _name = 'storage.contract'
    _description = 'Winter Contract'
    _inherit = 'mail.thread'

    def _default_fiscal_position(self):
        return self.env.user.default_storage_fiscal_position_id.id or ''

    name = fields.Char('Name', readonly=1)
    partner_id = fields.Many2one('res.partner','Partner')
    boat = fields.Char(string='Boat')
    boat_registry = fields.Char('Boat Registry')
    boat_length = fields.Float('Boat Length')
    boat_width = fields.Float('Boat Width')
    in_storage = fields.Boolean('In Storage')
    storage_cost = fields.Float('Storage Cost per Year')
    notes = fields.Html('Notes')
    service = fields.Html('Service')
    location_id = fields.Many2one('storage.location','Location')
    latitude = fields.Float('Latitude')
    longitude = fields.Float('Longitude')
    service_count = fields.Integer('Service Count', compute='_compute_service_count')
    invoice_count = fields.Integer('Invoice Count', compute='_compute_invoice_count')
    water_contract_count = fields.Integer('Water Contract Count', compute='_compute_water_contract_count')
    invoice_id = fields.Many2one('account.move', 'Invoice', copy=False, readonly=True, tracking=True,
                                 domain=[('type', '=', 'out_invoice')])
    fiscal_position_id = fields.Many2one('account.fiscal.position',string='Fiscal Position', default=_default_fiscal_position)
    delivery_address = fields.Text('Delivery Address')
    delivered = fields.Boolean('Delivered')
    order_id = fields.Many2one('sale.order')

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'storage.contract') or 'New'
        result = super(StorageContract, self).create(vals)
        return result

    @api.onchange('partner_id')
    def onchange_partner(self):
        for rec in self:
            # print(rec.partner_id.boat_make_id.name, rec.partner_id.boat_model)
            if rec.partner_id.boat_make_id:
                rec.boat = rec.partner_id.boat_make_id.name +" "+ rec.partner_id.boat_model
            else:
                rec.boat = ''
            if rec.partner_id.boat_length:
                rec.boat_length = rec.partner_id.boat_length + 1
            if rec.partner_id.boat_width:
                rec.boat_width = rec.partner_id.boat_width


    @api.onchange('location_id')
    def onchange_location(self):
        for rec in self:
            if rec.location_id.price_meter and rec.boat_length and rec.boat_width:
                rec.storage_cost = rec.boat_width * rec.boat_length * rec.location_id.price_meter

    def geo_localize(self):
        # We need country names in English below
        for rec in self.with_context(lang='en_US'):
            result = self.env['res.partner']._geo_localize(rec.location_id.street,
                                        rec.location_id.city,
                                        rec.location_id.state_id.name,
                                        rec.location_id.country_id.name)

            if result:
                rec.write({
                    'latitude': result[0],
                    'longitude': result[1],
                })
        return True

    def create_water_contract(self):
        for rec in self:
            contract_id = self.env['water.contract'].create({
                'winter_contract_id':rec.id,
                'partner_id': rec.partner_id.id,
                'boat': rec.boat,
            })

    def create_service(self):
        for rec in self:
            # product_id = self.env['product.product'].search([('product_tmpl_id', '=', rec.boat_id.id)])
            service_id = self.env['service.order'].create({'notes':rec.service, 'contract_id':rec.id,'partner_id': rec.partner_id.id})
            # service_lines = self.env['service.order.line'].create({
            #     'product_id': product_id.id,
            #     'service_id': service_id.id,
            # })
            # for line in service_lines:
            #     line.price_unit = self.storage_cost
            #     line.name = line.product_id.display_name

    def _compute_service_count(self):
        ServiceOrder = self.env['service.order']
        # can_read = Invoice.check_access_rights('read', raise_exception=False)
        for contract in self:
            contract.service_count = ServiceOrder.search_count(
                [('contract_id', '=', contract.id)]) or 0

    def _compute_water_contract_count(self):
        WaterContract = self.env['water.contract']
        # can_read = Invoice.check_access_rights('read', raise_exception=False)
        for contract in self:
            contract.water_contract_count = WaterContract.search_count(
                [('winter_contract_id', '=', contract.id)]) or 0


    def _compute_invoice_count(self):
        Invoices = self.env['account.move']
        # can_read = Invoice.check_access_rights('read', raise_exception=False)
        for contract in self:
            contract.invoice_count = Invoices.search_count(
                [('contract_id', '=', contract.id)]) or 0

    def create_invoice(self):
        partner_invoice = self.partner_id
        if not partner_invoice:
            raise UserError(_('You have to select an invoice address in the storage contract form.'))
        company = self.env.user.company_id

        journal = self.env['account.move'].with_context(force_company=company.id,
                                                        type='out_invoice')._get_default_journal()
        if not journal:
            raise UserError(_('Please define an accounting sales journal for the company %s (%s).') % (
                self.company_id.name, self.company_id.id))


        invoice_vals = {
            'type': 'out_invoice',
            'partner_id': partner_invoice.id,
            # 'currency_id': currency.id,
            # 'narration': narration,
            'line_ids': [],
            'invoice_origin': self.name,
            'contract_id': [(4,self.id,0)],
            'invoice_line_ids': [],
            # 'prop_id':self.id,
            'fiscal_position_id':self.fiscal_position_id.id,
        }
        invoice_line_vals = {}
        # if self.boat_id:
        name = self.boat
        boat = self.env['product.product'].search(
            [('id', '=', self.env.ref('boat_winter_storage.product_product_winter_storage').id)])
        boat_id = boat.product_tmpl_id
        print(boat,"PPP")
        account = boat_id._get_product_accounts()['income']
        if not account:
            raise UserError(_('No account defined for product "%s".') % boat.name)
        invoice_line_vals = {
            'name': name,
            'account_id': account.id,
            'quantity': 1,
            # 'tax_ids': [(6, 0, line.tax_id.ids)],
            # 'product_uom_id': line.product_uom.id,
            'price_unit': self.storage_cost,
            'product_id': boat.id,
        }

        balance = -(self.storage_cost)
        invoice_line_vals.update({
            'debit': balance > 0.0 and balance or 0.0,
            'credit': balance < 0.0 and -balance or 0.0,
        })
        invoice_vals['invoice_line_ids'].append((0, 0, invoice_line_vals))
        invoice_id = self.env['account.move'].with_context(default_type='out_invoice').create(invoice_vals)

    def action_view_services(self):
        self.ensure_one()
        services = self.env['service.order'].search([('contract_id', '=', self.id)])
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

    def action_view_water_contract(self):
        self.ensure_one()
        water_contracts = self.env['water.contract'].search([('winter_contract_id', '=', self.id)])
        action = self.env.ref('boat_on_water.water_contract_action').read()[0]
        action["context"] = {"create": False}
        if len(water_contracts) > 1:
            action['domain'] = [('id', 'in', water_contracts.ids)]
        elif len(water_contracts) == 1:
            action['views'] = [(self.env.ref('boat_on_water.water_contract_form_view').id, 'form')]
            action['res_id'] = water_contracts.ids[0]
        else:
            action = {'type': 'ir.actions.act_window_close'}
        return action


    def action_view_invoices(self):
        self.ensure_one()
        invoices = self.env['account.move'].search([('contract_id', '=', self.id)])
        action = self.env.ref('account.action_move_out_invoice_type').read()[0]
        action["context"] = {"create": False}
        if len(invoices) > 1:
            action['domain'] = [('id', 'in', invoices.ids)]
        elif len(invoices) == 1:
            action['views'] = [(self.env.ref('account.view_move_form').id, 'form')]
            action['res_id'] = invoices.ids[0]
        else:
            action = {'type': 'ir.actions.act_window_close'}
        return action

