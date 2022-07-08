{
    'name': 'Modify currency in odoo e-commerce checkout',
    'version': '14.0.2.0.1',
    'author': 'Ganemo',
    'website': 'https://www.ganemo.co/demo',
    'summary': 'Modify the currency when choosing the payment method in odoo e-commerce',
    'category': 'Sales',
    'depends': ['website_sale'],
    'data': [
        'static/src/xml/assets.xml',
        'security/ir.model.access.csv',
        'views/payment.xml',
        'views/web_templates.xml'
    ],
    'installable': True,
    'auto_install': False,
    'license': 'Other proprietary',
    'currency': 'USD',
    'price': 199.0
}
