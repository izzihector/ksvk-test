{
    'name': 'Nettivene',
    'version': '13.0.1.0.0',
    'description': """
        """,
    'depends': ['product','sale','stock','website_sale','purchase','account','sale_margin'],
    'data': [
        'wizard/confirmation.xml',
        'wizard/add_boat_view.xml',
        'wizard/add_equipment_view.xml',
        'security/ir.model.access.csv',
        'views/product_view.xml',
        'views/nettix_info_view.xml',
        'views/res_config_settings_view.xml',
        'views/res_partner_view.xml',
        'views/sale_order_view.xml',
        'views/schedulers.xml',
        'views/trade_in_views.xml',
        'views/boat_model_views.xml',
        'views/res_users_view.xml',
        'views/account_invoice_views.xml',
        'views/templates.xml',
        'views/res_company_views.xml',
    ],
    'installable': True,
    'auto_install': False

}
