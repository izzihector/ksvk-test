from odoo import api, fields, models,_
from odoo.exceptions import UserError

class WaterContract(models.Model):
    _name = 'water.contract'
    _description = 'Water Contract'

    name = fields.Char('Name', readonly=1)
    partner_id = fields.Many2one('res.partner','Partner')
    boat = fields.Char(string='Boat')
    price = fields.Float('Price')
    delivery_date = fields.Datetime('Delivery Date')
    comment = fields.Html('Comment')
    street = fields.Char()
    city = fields.Char()
    state_id = fields.Many2one('res.country.state')
    country_id = fields.Many2one('res.country')
    latitude = fields.Float('Latitude')
    longitude = fields.Float('Longitude')
    free_charge = fields.Boolean('Free of Charge')
    state = fields.Selection([('draft','Draft'),('confirmed','Confirmed')],string='State', default='draft')
    invoice_count = fields.Integer('Invoice Count', compute='_compute_invoice_count')
    invoice_id = fields.Many2one('account.move', 'Invoice', copy=False, readonly=True, tracking=True,
                                 domain=[('type', '=', 'out_invoice')])

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'water.contract') or 'New'
        result = super(WaterContract, self).create(vals)
        return result

    @api.onchange('partner_id')
    def onchange_partner(self):
        for rec in self:
            if rec.partner_id.boat_make_id:
                rec.boat = rec.partner_id.boat_make_id.name + " " + rec.partner_id.boat_model
            else:
                rec.boat = ''

    def confirm_contract(self):
        self.write({'state':'confirmed'})

    def _compute_invoice_count(self):
        Invoices = self.env['account.move']
        # can_read = Invoice.check_access_rights('read', raise_exception=False)
        for contract in self:
            contract.invoice_count = Invoices.search_count(
                [('water_contract_id', '=', contract.id)]) or 0

    def action_view_invoices(self):
        self.ensure_one()
        invoices = self.env['account.move'].search([('water_contract_id', '=', self.id)])
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

    def geo_localize(self):
        # We need country names in English below
        for rec in self.with_context(lang='en_US'):
            result = self.env['res.partner']._geo_localize(rec.street,
                                        rec.city,
                                        rec.state_id.name,
                                        rec.country_id.name)

            if result:
                rec.write({
                    'latitude': result[0],
                    'longitude': result[1],
                })
        return True

    def create_invoice(self):
        partner_invoice = self.partner_id
        if not partner_invoice:
            raise UserError(_('You have to select an invoice address in the water contract form.'))
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
            'water_contract_id': [(4,self.id,0)],
            'invoice_line_ids': [],
            # 'prop_id':self.id,
        }
        invoice_line_vals = {}
        # if self.boat_id:
        name = self.boat
        boat = self.env['product.product'].search(
            [('id', '=', self.env.ref('boat_on_water.product_product_water_storage').id)])
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
            'price_unit': self.price,
            'product_id': boat.id,
        }

        balance = -(self.price)
        invoice_line_vals.update({
            'debit': balance > 0.0 and balance or 0.0,
            'credit': balance < 0.0 and -balance or 0.0,
        })
        invoice_vals['invoice_line_ids'].append((0, 0, invoice_line_vals))
        invoice_id = self.env['account.move'].with_context(default_type='out_invoice').create(invoice_vals)

    # def create_service(self):
    #     print("create service order =============== ")
    #     for rec in self:
    #         product_id = self.env['product.product'].create({
    #             'name': rec.boat_make_id.name + ' ' + rec.boat_model,
    #             'boat_make_id':rec.boat_make_id.id,
    #             'boat_model': rec.boat_model,
    #             'engine_model': rec.engine_model,
    #             'engine_mfg_year': rec.engine_mfg_year,
    #             'engine_hours': rec.engine_hours,
    #             'year': rec.year,
    #         })
    #         service_id = self.env['service.order'].create({'partner_id': rec.partner_id.id, 'notes': rec.service})
    #         service_lines = self.env['service.order.line'].create({
    #             'product_id': product_id.id,
    #             'service_id': service_id.id,
    #         })
    #         for line in service_lines:
    #             line.price_unit = line.product_id.list_price
    #             line.name = line.product_id.display_name
    #         # print(service_lines.ids)

