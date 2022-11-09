# -*- coding: utf-8 -*-
# Powered by Kanak Infosystems LLP.
# © 2020 Kanak Infosystems LLP. (<https://www.kanakinfosystems.com>)

{
    'name': 'Website Product Store Pickup',
    'version': '14.0.1.0.1',
    'author': 'Kanak Infosystems LLP.',
    'license': 'OPL-1',
    'summary': 'This module is used to setup multiple pickup stores and allows the customer to select the pickup store based on their convenience. pickup product | store pickup | shop pickup | product pickup | pick product from shop | pick product from store | wharehouse pickup | pickup from shop',
    'description': """This module is used to setup multiple pickup stores and allows the customer to select the pickup store based on their convenience.""",
    'website': 'http://www.kanakinfosystems.com',
    'category': 'Website',
    'depends': ['sale', 'website_sale_delivery'],
    'data': [
        'views/assets.xml',
        'data/data.xml',
        'views/product_views.xml',
        'views/partner_views.xml',
        'views/templates.xml',
    ],
    'qweb': [
        'static/src/xml/widget.xml',
    ],
    'images': ['static/description/banner.jpg'],
    'installable': True,
    'application': True,
    'price': 150,
    'currency': 'EUR',
    'live_test_url': 'https://www.youtube.com/watch?v=X354p3GFCTQ',
}
