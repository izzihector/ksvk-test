{
    'name': 'Service Management',
    'version': '13.0.1.0.0',
    'description': """
        """,
    'depends': ['sale_management','account','website', 'stock','Nettivene'],
    'data': [
        'wizard/sms.xml',
        'report/service_report.xml',
        'report/service_report_templates.xml',
        'views/service_order_views.xml',
        'views/service_portal_templates.xml',
        'views/assets.xml',
        'views/res_users_views.xml',
        'views/res_partner_views.xml',
        'security/ir.model.access.csv',
        'data/service_data.xml',
        'report/sale_analysis_report.xml',
    ],
    'installable': True,
    'auto_install': False
}
