from odoo import api, fields, models


class PaymentAcquirer(models.Model):
    _inherit = 'payment.acquirer'

    ecommerce_currency_sequence_ids = fields.Many2many(
        comodel_name='ecommerce.currency.sequence',
        string='Cambiar tipo de moneda',
        help='''
    Si se añade Monedas en este campo, cuando se escoge este método de pago en el comercio electrónico, Odoo modificará en automático, 
    la moneda del carrito de compra, por la primera moneda de esta lista, también se mostrará una Lista desplegable, donde el comprador, 
    podrá escoger entre cualquiera de las monedas de esta lista. 
        '''
    )


class EcommerceCurrencySequence(models.Model):
    _name = 'ecommerce.currency.sequence'
    _description = 'Ecommerce currency sequence'

    sequence = fields.Integer(string='Elige tu regalo')
    price_list_id = fields.Many2one(
        comodel_name='product.pricelist',
        string='Tarifa',
        required=True,
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]"
    )
    company_id = fields.Many2one('res.company', 'Company', required=True, index=True, default=lambda self: self.env.company)

    def name_get(self):
        return [(obj.id, f'{obj.price_list_id and obj.price_list_id.name or ""}') for obj in self]
