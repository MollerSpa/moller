{
    'name': 'Choose your gift in e-commerce',
    'version': '14.0.1.1.3',
    'author': 'Ganemo',
    'website': 'https://www.ganemo.co/demo',
    'summary': 'Allows the customer to choose their gift according to the product they buy',
    'category': 'Sales',
    'depends': ['website_sale_stock'],
    'data': [
        'security/ir.model.access.csv',
        'static/src/xml/assets.xml',
        'views/product.xml',
        'views/sale.xml',
        'views/web_templates.xml',
    ],
    'installable': True,
    'auto_install': False,
    'license': 'Other proprietary',
    'currency': 'USD',
    'price': 120.0
}
