# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import tools
from odoo import api, fields, models


class SaleReport(models.Model):
    _name = "service.report"
    _description = "Sales Analysis Report"
    _auto = False
    _rec_name = 'date'
    _order = 'date desc'

    @api.model
    def _get_done_states(self):
        return ['sale', 'done', 'paid']

    name = fields.Char('Order Reference', readonly=True)
    date = fields.Datetime('Order Date', readonly=True)
    product_id = fields.Many2one('product.product', 'Product Variant', readonly=True)
    partner_id = fields.Many2one('res.partner', 'Customer', readonly=True)
    price_subtotal = fields.Float('Untaxed Total', readonly=True)
    amount_total = fields.Float('Total', compute='_amount_total', store=True)
    product_tmpl_id = fields.Many2one('product.template', 'Product', readonly=True)
    categ_id = fields.Many2one('product.category', 'Product Category', readonly=True)
    nbr = fields.Integer('# of Lines', readonly=True)
    country_id = fields.Many2one('res.country', 'Customer Country', readonly=True)
    industry_id = fields.Many2one('res.partner.industry', 'Customer Industry', readonly=True)
    commercial_partner_id = fields.Many2one('res.partner', 'Customer Entity', readonly=True)
    state = fields.Selection([
        ('draft', 'Draft Quotation'),
        ('sent', 'Quotation Sent'),
        ('sale', 'Sales Order'),
        ('done', 'Sales Done'),
        ('cancel', 'Cancelled'),
    ], string='Status', readonly=True)
    service_id = fields.Many2one('service.order', 'Order #', readonly=True)
    serviceman = fields.Many2one('res.users','Serviceman', readonly=1)



    def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
        with_ = ("WITH %s" % with_clause) if with_clause else ""

        select_ = """
            min(l.id) as id,
            l.product_id as product_id,
            count(*) as nbr,
            s.name as name,
            s.planned_date as date,
            sum(l.price_subtotal / 1)as price_subtotal,
            s.state as state,
            s.partner_id as partner_id,
            s.serviceman as serviceman,
            s.amount_total as amount_total,
            t.categ_id as categ_id,
            p.product_tmpl_id,
            partner.country_id as country_id,
            partner.industry_id as industry_id,
            partner.commercial_partner_id as commercial_partner_id,
            s.id as service_id
        """

        for field in fields.values():
            select_ += field

        from_ = """
                service_order_line l
                      join service_order s on (l.service_id=s.id)
                      join res_partner partner on s.partner_id = partner.id
                        left join product_product p on (l.product_id=p.id)
                            left join product_template t on (p.product_tmpl_id=t.id)
                %s
        """ % from_clause

        groupby_ = """
            l.product_id,
            l.service_id,
            t.categ_id,
            s.name,
            l.price_subtotal,
            s.partner_id,
            s.state,
            p.product_tmpl_id,
            partner.country_id,
            partner.industry_id,
            partner.commercial_partner_id,
            s.id %s
        """ % (groupby)

        return '%s (SELECT %s FROM %s WHERE l.product_id IS NOT NULL GROUP BY %s)' % (with_, select_, from_, groupby_)

    def init(self):
        # self._table = sale_report
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""CREATE or REPLACE VIEW %s as (%s)""" % (self._table, self._query()))


class SaleOrderReportProforma(models.AbstractModel):
    _name = 'report.service.report_saleproforma'
    _description = 'Proforma Report'

    def _get_report_values(self, docids, data=None):
        docs = self.env['service.order'].browse(docids)
        return {
            'doc_ids': docs.ids,
            'doc_model': 'service.order',
            'docs': docs,
            'proforma': True
        }
