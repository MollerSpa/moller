{
    'name': 'Shipping label printing',
    'version': '14.0.0.2.1',
    'author': 'Ganemo',
    'website': 'https://www.ganemo.co',
    'description': """From sales orders, print shipping label""",
    'summary': 'From sales orders, print shipping label',
    'category': 'eCommerce',
    'depends': ['pickup_by_third_party', 'website_product_store_pickup_knk'],
    'data': [
        'reports/report.xml',
        'reports/template.xml'
    ],
    'installable': True,
    'auto_install': False,
    'license': 'Other proprietary',
    'currency': 'USD',
    'price': 40.0
}