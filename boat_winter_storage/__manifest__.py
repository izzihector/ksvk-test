{
    'name': 'Boat Winter Storage',
    'version': '13.0.1.0.0',
    'description': """
        """,
    'depends': ['Nettivene','service_management','web_widget_google_maps'],
    'data': [
        'views/storage_contract_views.xml',
        'views/location_views.xml',
        'views/res_users_views.xml',
        'security/ir.model.access.csv',
        'data/storage_data.xml',
    ],
    'installable': True,
    'auto_install': False

}
