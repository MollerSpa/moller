{
    'name': 'Who picks up',
    'version': '14.0.0.0.0',
    'author': 'Ganemo',
    'website': 'https://www.ganemo.co',
    'description': """Add information of the person who picks up or receives the package""",
    'summary': 'Add information of the person who picks up the package',
    'category': 'eCommerce',
    'depends': ['website_sale', 'website_sale_delivery'],
    'data': [
        'templates/assets.xml',
        'templates/template.xml',
        'views/res_config_settings.xml',
        'views/sale_order_views.xml',
    ],
    'installable': True,
    'auto_install': False,
    'license': 'Other proprietary',
    'currency': 'USD',
    'price': 40.0
}