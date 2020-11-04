from odoo import api, fields, models, _
from odoo.exceptions import UserError
from datetime import datetime
from datetime import timedelta

class ServiceOrder(models.Model):
    _name = 'service.order'
    _description = 'Service Order'
    _inherit = ['portal.mixin','mail.thread']
    _rec_name = 'partner_id'

    def _default_currency_id(self):
        return self.env.user.company_id.currency_id.id


    partner_id = fields.Many2one('res.partner','Customer',required=1)
    name = fields.Char('Service Reference', readonly=True, default='New')
    state = fields.Selection([('quotation','Quotation'),('wait','Waiting for Repair'),('ongoing','Ongoing'),('done','Done'),('cancel','Cancel')],
                             string='State', default='quotation')
    currency_id = fields.Many2one('res.currency',default=_default_currency_id)
    responsible = fields.Many2one('res.users', 'Responsible')
    warranty = fields.Date('Warranty Expiration')
    estimated_hours = fields.Float('Estimated Hours')
    completion_date = fields.Datetime('Completion Date',compute='compute_completion_date')
    planned_date = fields.Datetime('Planned Date')
    serviceman = fields.Many2one('res.users','Serviceman')
    address_id = fields.Char('Delivery Address',states={'confirmed': [('readonly', True)]})
    service_lines = fields.One2many('service.order.line','service_id',string='Service Order Lines')
    service_operations = fields.One2many('service.operations', 'service_id', string='Service Operations')
    amount_untaxed = fields.Float('Untaxed Amount', compute='_amount_untaxed', store=True)
    amount_tax = fields.Float('Taxes', compute='_amount_tax', store=True)
    amount_total = fields.Float('Total', compute='_amount_total', store=True)
    notes = fields.Html('Notes')
    serviced = fields.Boolean('Serviced')
    invoiced = fields.Boolean('Invoiced')
    date_start = fields.Date('Started On')
    date_stop = fields.Date('Completed On')
    invoice_id = fields.Many2one('account.move', 'Invoice',copy=False, readonly=True, tracking=True,domain=[('type', '=', 'out_invoice')])
    contract_id = fields.Many2one('storage.contract')
    order_id = fields.Many2one('sale.order')
    picking_id = fields.Many2one('stock.picking','Picking')
    fiscal_position_id = fields.Many2one('account.fiscal.position', string='Fiscal Position', compute='compute_fiscal_position')

    def _compute_access_url(self):
        super(ServiceOrder, self)._compute_access_url()
        for order in self:
            order.access_url = '/my/service_orders/%s' % (order.id)

    def _get_report_base_filename(self):
        self.ensure_one()
        return '%s' % (self.name)

    def compute_completion_date(self):
        for rec in self:
            if rec.planned_date and rec.estimated_hours:
                rec.completion_date = rec.planned_date + timedelta(hours=rec.estimated_hours)
            else:
                rec.completion_date = rec.planned_date

    def compute_fiscal_position(self):
        for rec in self:
            if rec.serviceman and rec.serviceman.default_service_fiscal_position_id:
                rec.fiscal_position_id = rec.serviceman.default_service_fiscal_position_id.id
            else:
                rec.fiscal_position_id = False


    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'service.order') or 'New'
        result = super(ServiceOrder, self).create(vals)
        return result

    @api.depends('service_lines.price_subtotal', 'service_operations.price_subtotal')
    def _amount_untaxed(self):
        for order in self:
            total = sum(line.price_subtotal for line in order.service_lines)
            total += sum(line.price_subtotal for line in order.service_operations)
            order.amount_untaxed = total

    @api.depends('service_lines.price_unit', 'service_lines.product_uom_qty', 'service_lines.product_id',
                 'service_operations.price_unit', 'service_operations.product_uom_qty', 'service_operations.product_id','partner_id')
    def _amount_tax(self):
        for order in self:
            val = 0.0
            for line in order.service_lines:
                if line.tax_id:
                    tax_calculate = line.tax_id.compute_all(line.price_unit, currency=None, quantity=line.product_uom_qty, product=line.product_id, partner=order.partner_id)
                    for c in tax_calculate['taxes']:
                        val += c['amount']
            for line in order.service_operations:
                if line.tax_id:
                    tax_calculate = line.tax_id.compute_all(line.price_unit, currency=None, quantity=line.product_uom_qty, product=line.product_id, partner=order.partner_id)
                    for c in tax_calculate['taxes']:
                        val += c['amount']
            order.amount_tax = val

    @api.depends('amount_tax', 'amount_untaxed')
    def _amount_total(self):
        for order in self:
            order.amount_total = order.amount_untaxed + order.amount_tax

    @api.onchange('completion_date')
    def estimate_hours(self):
        for rec in self:
            if rec.completion_date:
                rec.estimated_hours = (rec.completion_date - rec.planned_date) / timedelta(hours=1)

    def confirm_service(self):
        """ Repair order state is set to 'To be invoiced' when invoice method
        is 'Before repair' else state becomes 'Confirmed'.
        @param *arg: Arguments
        @return: True
        """
        if self.filtered(lambda service: service.state != 'quotation'):
            raise UserError(_("Only services in quotation state can be confirmed."))
        # before_repair = self.filtered(lambda repair: repair.invoice_method == 'b4repair')
        # before_repair.write({'state': '2binvoiced'})
        # to_confirm = self - before_repair
        # to_confirm_operations = to_confirm.mapped('operations')
        # to_confirm_operations.write({'state': 'confirmed'})
        vals = {'state': 'wait'}
        if not self.responsible:
            vals.update({'responsible': self.env.uid})
        self.write(vals)
        return True

    def cancel_service(self):
        if self.filtered(lambda service: service.state == 'done'):
            raise UserError(_("Cannot cancel completed services."))
        if any(service.invoiced for service in self):
            raise UserError(_('The service order is already invoiced.'))
        # self.mapped('operations').write({'state': 'cancel'})
        return self.write({'state': 'cancel'})

    def start_service(self):
        if self.filtered(lambda service: service.state not in ['wait']):
            raise UserError(_("Service must be confirmed before starting."))
        # self.mapped('operations').write({'state': 'confirmed'})
        if not self.planned_date:
            self.write({'planned_date': datetime.now()})
        return self.write({'state': 'ongoing','serviceman':self.env.uid,'date_start':datetime.today()})

    def end_service(self):
        if self.filtered(lambda service: service.state not in ['ongoing']):
            raise UserError(_("Service has not been started yet."))
        # self.mapped('operations').write({'state': 'confirmed'})
        return self.write({'state': 'done','serviced':True, 'date_stop':datetime.today()})

    def set_quotation_service(self):
        if self.filtered(lambda service: service.state != 'cancel'):
            raise UserError(_("Service must be canceled in order to reset it to quotation state."))
        # self.mapped('operations').write({'state': 'draft'})
        return self.write({'state': 'quotation', 'serviceman':False, 'estimated_hours':False})

    def action_send_mail(self):
        self.ensure_one()
        template_id = self.env.ref('service_management.mail_template_service_quotation').id
        ctx = {
            'default_model': 'service.order',
            'default_res_id': self.id,
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
            'custom_layout': 'mail.mail_notification_light',
        }
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'target': 'new',
            'context': ctx,
        }

    def print_service_order(self):
        return self.env.ref('service_management.action_report_service_order').report_action(self)

    def confirm_parts(self):
        customerloc, supplierloc = \
            self.env['stock.warehouse']._get_partner_locations()
        existing_id = self.env['stock.picking'].search([('origin','=',self.name)])
        if existing_id:
            raise UserError('A transfer already exists for this service order.')
        picking_vals = {
            'origin': self.name,
            'name': self.name,
            'partner_id': self.partner_id.id or False,
            'picking_type_id': self.env.ref('stock.picking_type_out').id,
            'user_id':self.responsible.id,
            'location_id': customerloc.id,
            'location_dest_id': supplierloc.id,
            'service_id':self.id,
        }
        picking_id = self.env['stock.picking'].create(picking_vals)
        self.write({'picking_id':picking_id.id})
        for line in self.service_lines:
            move_vals = {
                'origin': self.name,
                'name': self.name,
                'partner_id': self.partner_id.id or False,
                'location_id': customerloc.id,
                'location_dest_id': supplierloc.id,
                'product_id':line.product_id.id,
                'product_uom':line.product_id.uom_id.id,
                'product_uom_qty':line.product_uom_qty,
                'picking_id':picking_id.id,
            }
            self.env['stock.move'].create(move_vals)

    def create_invoice(self):
        for service in self:
            partner_invoice = service.partner_id
            if not partner_invoice:
                raise UserError(_('You have to select an invoice address in the service form.'))

            narration = service.notes
            currency = service.currency_id

            company = self.env.user.company_id

            journal = self.env['account.move'].with_context(force_company=company.id,
                                                            type='out_invoice')._get_default_journal()
            if not journal:
                raise UserError(_('Please define an accounting sales journal for the company %s (%s).') % (
                self.company_id.name, self.company_id.id))

            invoice_vals = {
                'type': 'out_invoice',
                'partner_id': partner_invoice.id,
                'currency_id': currency.id,
                'narration': narration,
                'line_ids': [],
                'invoice_origin': service.name,
                'service_ids': [(4, service.id)],
                'invoice_line_ids': [],
                'fiscal_position_id':self.fiscal_position_id.id,
            }

            # Create invoice lines from operations.
            for line in service.service_lines:

                name = line.name

                account = line.product_id.product_tmpl_id._get_product_accounts()['income']
                if not account:
                    raise UserError(_('No account defined for product "%s".') % line.product_id.name)

                invoice_line_vals = {
                    'name': name,
                    'account_id': account.id,
                    'quantity': line.product_uom_qty,
                    'tax_ids': [(6, 0, line.tax_id.ids)],
                    # 'product_uom_id': line.product_uom.id,
                    'price_unit': line.price_unit,
                    'product_id': line.product_id.id,
                    'service_line_ids': [(4, line.id)],
                }

                balance = -(line.product_uom_qty * line.price_unit)
                invoice_line_vals.update({
                    'debit': balance > 0.0 and balance or 0.0,
                    'credit': balance < 0.0 and -balance or 0.0,
                })
                invoice_vals['invoice_line_ids'].append((0, 0, invoice_line_vals))

            # Create invoice lines from fees.
            for operation in service.service_operations:

                name = operation.name

                if not operation.product_id:
                    raise UserError(_('No product defined on operations.'))

                account = operation.product_id.product_tmpl_id._get_product_accounts()['income']
                if not account:
                    raise UserError(_('No account defined for product "%s".') % operation.product_id.name)

                invoice_line_vals = {
                    'name': name,
                    'account_id': account.id,
                    'quantity': operation.product_uom_qty,
                    'tax_ids': [(6, 0, operation.tax_id.ids)],
                    # 'product_uom_id': fee.product_uom.id,
                    'price_unit': operation.price_unit,
                    'product_id': operation.product_id.id,
                    'service_operation_ids': [(4, operation.id)],
                }

                balance = -(operation.product_uom_qty * operation.price_unit)
                invoice_line_vals.update({
                    'debit': balance > 0.0 and balance or 0.0,
                    'credit': balance < 0.0 and -balance or 0.0,
                })
                invoice_vals['invoice_line_ids'].append((0, 0, invoice_line_vals))
            self.env['account.move'].with_context(default_type='out_invoice').create(invoice_vals)

            service.write({'invoiced': True})

    def action_created_invoice(self):
        self.ensure_one()
        return {
            'name': _('Invoice created'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'account.move',
            'view_id': self.env.ref('account.view_move_form').id,
            'target': 'current',
            'res_id': self.invoice_id.id,
            }

    def show_picking(self):
        self.ensure_one()
        return {
            'name': _('Picking'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'stock.picking',
            'view_id': self.env.ref('stock.view_picking_form').id,
            'target': 'current',
            'res_id': self.picking_id.id,
            }


class ServiceOrderLines(models.Model):
    _name = 'service.order.line'
    _description = 'Service Order Line'

    product_id = fields.Many2one('product.product','Product')
    name = fields.Text(string='Description')
    product_uom_qty = fields.Float(string='Quantity', digits='Product Unit of Measure', required=True, default=1.0)
    price_unit = fields.Float('Unit Price', required=True, digits='Product Price', default=0.0)
    tax_id = fields.Many2many('account.tax', string='Taxes',domain=['|', ('active', '=', False), ('active', '=', True)])
    price_subtotal = fields.Float(compute='_compute_amount', string='Subtotal', readonly=True, store=True)
    service_id = fields.Many2one('service.order')
    invoice_line_id = fields.Many2one('account.move.line', 'Invoice Line',copy=False, readonly=True)

    @api.depends('product_uom_qty', 'price_unit', 'tax_id')
    def _compute_amount(self):
        """
        Compute the amounts of the SO line.
        """
        for line in self:
            price = line.price_unit
            taxes = line.tax_id.compute_all(price,currency=None, quantity=line.product_uom_qty,
                                            product=line.product_id, partner=line.service_id.partner_id)
            line.update({
                'price_subtotal': taxes['total_excluded'],
            })


    @api.onchange('service_id', 'product_id', 'product_uom_qty')
    def onchange_product_id(self):
        if not self.product_id or not self.product_uom_qty:
            return
        self.price_unit = self.product_id.list_price
        self.name = self.product_id.display_name

class ServiceOperations(models.Model):
    _name = 'service.operations'
    _description = 'Service Operations'

    name = fields.Text('Description', index=True, required=True)
    product_id = fields.Many2one('product.product', 'Product', domain=[('type','=','service')])
    product_uom_qty = fields.Float('Quantity', digits='Product Unit of Measure', required=True, default=1.0)
    price_unit = fields.Float('Unit Price', required=True)
    price_subtotal = fields.Float('Subtotal', compute='_compute_price_subtotal', store=True, digits=0)
    tax_id = fields.Many2many('account.tax', 'service_op_line_tax', 'service_op_line_id', 'tax_id', 'Taxes')
    service_id = fields.Many2one('service.order', 'Service Order')
    invoice_line_id = fields.Many2one('account.move.line', 'Invoice Line', copy=False, readonly=True)

    @api.depends('price_unit', 'service_id', 'product_uom_qty', 'product_id')
    def _compute_price_subtotal(self):
        for op in self:
            taxes = op.tax_id.compute_all(op.price_unit, currency=None, quantity=op.product_uom_qty,
                                           product=op.product_id, partner=op.service_id.partner_id)
            op.price_subtotal = taxes['total_excluded']

    @api.onchange('service_id', 'product_id', 'product_uom_qty')
    def onchange_product_id(self):
        if not self.product_id or not self.product_uom_qty:
            return
        self.price_unit = self.product_id.list_price
        self.name = self.product_id.display_name