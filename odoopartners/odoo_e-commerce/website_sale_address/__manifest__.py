# -*- coding: utf-8 -*-

# Copyright © 2020 Garazd Creation (<https://garazd.biz>)
# @author: Yurii Razumovskyi (<support@garazd.biz>)
# @author: Iryna Razumovska (<support@garazd.biz>)
# License OPL-1 (https://www.odoo.com/documentation/user/legal/licenses/licenses.html#odoo-apps).

{
    'name': 'eCommerce Address Management',
    'version': '14.0.1.0.0',
    'category': 'eCommerce',
    'author': 'Garazd Creation',
    'website': 'https://garazd.biz/en/blog/ecommerce-2/post/management-of-the-billing-and-shipping-address-fields-in-odoo-ecommerce-49',
    'license': 'OPL-1',
    'summary': 'eCommerce Billing and Shipping Address Fields',
    'images': ['static/description/banner.png'],
    'live_test_url': 'https://apps.garazd.biz/r/Hyw',
    'description': """
eCommerce Billing and Shipping Address Fields
    """,
    'depends': [
        'website_sale',
    ],
    'data': [
        'views/website_views.xml',
        'views/website_sale_templates.xml',
    ],
    'external_dependencies': {
    },
    'price': 39.0,
    'currency': 'EUR',
    'support': 'support@garazd.biz',
    'application': False,
    'installable': True,
    'auto_install': False,
}
