{
    'name': 'Boat On Water',
    'version': '13.0.1.0.0',
    'description': """
        """,
    'depends': ['Nettivene','service_management','boat_winter_storage'],
    'data': [
        'views/water_contract_views.xml',
        'views/res_users_views.xml',
        'views/res_company_views.xml',
        'security/ir.model.access.csv',
        'data/water_data.xml',
    ],
    'installable': True,
    'auto_install': False

}
