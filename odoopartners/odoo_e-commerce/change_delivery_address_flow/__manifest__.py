{
    'name': 'Modify shipping address selection flow in Odoo',
    'version': '14.0.1.0.0',
    'author': 'Ganemo',
    'website': 'https://www.ganemo.co/demo',
    'summary': 'Modify the Select delivery address flow so that it is chosen after choosing the shipping method',
    'category': 'eCommerce',
    'depends': ['website_sale_delivery'],
    'data': [
        'views/delivery_views.xml',
        'views/web_templates.xml'
    ],
    'installable': True,
    'auto_install': False,
    'license': 'Other proprietary',
    'currency': 'USD',
    'price': 180.0
}
