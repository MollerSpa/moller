from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale

class websiteSaleOrder(WebsiteSale):

    @http.route(['/shop/payment/allow_third_party'], type='json', auth="public", methods=['POST'], website=True)
    def order_allow_third_party(self, **post):
        order = request.website.sale_get_order()
        redirection = self.checkout_redirection(order)
        if redirection:
            return redirection
        if order and order.id:
            third_party_name = post.get('third_party_name')
            third_party_lastname = post.get('third_party_lastname')
            third_party_lastname2 = post.get('third_party_lastname2')
            third_party_name_vat = post.get('third_party_name_vat')
            vals = {
                'allow_third_party': True,
                'third_party_name': third_party_name.strip(),
                'third_party_lastname': third_party_lastname.strip(),
                'third_party_lastname2': third_party_lastname2.strip(),
                'third_party_name_vat': third_party_name_vat.strip()
            }
            order.sudo().write(vals)
        return True
        
    def _get_shop_payment_values(self, order, **kwargs):
        res = super(websiteSaleOrder, self)._get_shop_payment_values(order, **kwargs)
        allow_third_party = request.env['ir.config_parameter'].sudo().get_param(
            'pickup_by_third_party.allow_third_party')
        res['allow_third_party'] = allow_third_party
        return res