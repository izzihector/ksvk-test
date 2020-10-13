# -*- coding: utf-8 -*-
{
    'name': "Poplapay Payment POS",

    'summary': """
        This module worked payment intigration of Poplapay this module used to creadit card and debit card of Poplapay payment.
        """,

    'description': """
        Poplapay payment  method getways
    """,

    'author': 'TechUltra Solutions',
    'category': 'Sales',
    'website': "www.techultrasolutions.com",
    'version': '13.0.1.0.0',

    # any module necessary for this one to work correctly
    'depends': ['point_of_sale'],

    # always loaded
    'data': [
        'views/assets.xml',
        'views/templates.xml',
        'wizard/pos_payment_view.xml',
        'views/pos_order_view.xml',
        'views/templates.xml',
        'views/pos_poplapay_view.xml',
    ],
    'qweb': [
        'static/src/xml/custome_button.xml',
    ],
}
