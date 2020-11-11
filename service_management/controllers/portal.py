from odoo import fields, http, _
from odoo.http import request
from odoo.exceptions import AccessError, MissingError
from odoo.addons.portal.controllers.mail import _message_post_helper
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager, get_records_pager


class CustomerPortal(CustomerPortal):

    def _prepare_portal_layout_values(self):
        values = super(CustomerPortal, self)._prepare_portal_layout_values()
        partner = request.env.user.partner_id

        ServiceOrder = request.env['service.order']
        service_count = ServiceOrder.search_count([
            ('partner_id', '=', request.env.user.partner_id.id),

        ])
        values.update({
            'service_count': service_count,
        })
        return values

    @http.route(['/ask_quotation'], type='http', auth="public", website=True)
    def portal_ask_quotation(self, **kw):
        values = {
            'products': request.env['product.product'].search([])
        }
        return request.render('service_management.request_quotation', values)

    @http.route(['/submit_quotation'], type='http', auth="public", website=True)
    def portal_submit_quotation(self, **kw):
        print(kw,"######")
        partner = request.env.user.partner_id
        lines = request.env['service.order.line'].create({
            'product_id': int(kw.get('product')),
        })
        order_id = request.env['service.order'].create({
            'partner_id': partner.id,
            'address_id': kw.get('location'),
            'notes': kw.get('notes'),
            'service_lines': [(6, 0, [lines.id])]
        })
        line_id = request.env['service.order.line'].search([('id', '=', lines.id)])
        line_id.price_unit = line_id.product_id.list_price
        line_id.name = line_id.product_id.display_name
        template_obj = request.env['mail.mail']
        print(request.env.company,"LLLLL")
        receiver_email = request.env.company.service_email
        template_data = {
            'subject': 'Administrator Service Orders (Ref %s)' % (order_id.name),
            'body': """
                <p>Hello %s,<p>
                Here is your service order <b>%s</b> (with reference: %s ) amounting in <b>%s €</b>.
                You can reply to this email if you have any questions. <br/><br/>

                Thank you,
                <br/>
                -- 
                Administrator""" % (partner.name, order_id.name, order_id.name, order_id.amount_total),
            'email_from': 'admin@example.com',
            'email_to': receiver_email or '',
            'record_name': order_id.name,
        }
        template_id = template_obj.create(template_data)
        template_obj.send(template_id)

    @http.route(['/my/service_orders', '/my/service_orders/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_service_orders(self, page=1, date_begin=None, date_end=None, sortby=None, **kw):
        values = self._prepare_portal_layout_values()
        partner = request.env.user.partner_id
        ServiceOrder = request.env['service.order']

        domain = [
            ('partner_id', '=', request.env.user.partner_id.id),
        ]

        searchbar_sortings = {
            'date': {'label': _('Planned Date'), 'order': 'planned_date desc'},
            'name': {'label': _('Reference'), 'order': 'name'},
            'stage': {'label': _('State'), 'order': 'state'},
        }

        # default sortby order
        if not sortby:
            sortby = 'date'
        sort_order = searchbar_sortings[sortby]['order']

        archive_groups = self._get_archive_groups('service.order', domain)
        if date_begin and date_end:
            domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]

        # count for pager
        service_count = ServiceOrder.search_count(domain)
        # make pager
        pager = portal_pager(
            url="/my/service_order",
            # url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby},
            total=service_count,
            page=page,
            step=self._items_per_page
        )
        # search the count to display, according to the pager data
        services = ServiceOrder.search(domain, order=sort_order, limit=self._items_per_page, offset=pager['offset'])
        request.session['service_history'] = services.ids[:100]

        values.update({
            'date': date_begin,
            'services': services.sudo(),
            'page_name': 'service',
            'pager': pager,
            'archive_groups': archive_groups,
            'default_url': '/my/service_order',
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby,
        })
        return request.render("service_management.portal_my_services", values)

    @http.route(['/my/service_orders/<int:order_id>'], type='http', auth="public", website=True)
    def portal_service_order_page(self, order_id, report_type=None, access_token=None, message=False, download=False,
                                  **kw):
        try:
            order_sudo = self._document_check_access('service.order', order_id, access_token=access_token)
        except (AccessError, MissingError):
            return request.redirect('/my')

        if report_type in ('html', 'pdf', 'text'):
            return self._show_report(model=order_sudo, report_type=report_type,
                                     report_ref='service_management.action_report_service_order', download=download)

        # use sudo to allow accessing/viewing orders for public user
        # only if he knows the private token
        now = fields.Date.today()

        # Log only once a day
        if order_sudo and request.session.get(
                'view_quote_%s' % order_sudo.id) != now and request.env.user.share and access_token:
            request.session['view_quote_%s' % order_sudo.id] = now
            body = _('Quotation viewed by customer %s') % order_sudo.partner_id.name
            _message_post_helper('service.order', order_sudo.id, body, token=order_sudo.access_token,
                                 message_type='notification', subtype="mail.mt_note")

        values = {
            'service_order': order_sudo,
            'message': message,
            'token': access_token,
            # 'return_url': '/shop/payment/validate',
            'bootstrap_formatting': True,
            'partner_id': order_sudo.partner_id.id,
            'report_type': 'html',
            'action': request.env.ref('service_management.service_order_action'),
        }

        return request.render('service_management.service_order_portal_template', values)