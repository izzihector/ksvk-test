{
    'name': 'Boat On Water',
    'version': '13.0.1.0.0',
    'description': """
        """,
    'depends': ['Nettivene','service_management'],
    'data': [
        'views/water_contract_views.xml',
        # 'views/res_config_settings_views.xml',
        'views/res_company_views.xml',
        'security/ir.model.access.csv',
        'data/water_data.xml',
    ],
    'installable': True,
    'auto_install': False

}
