from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale


class websiteSaleOrder(WebsiteSale):

    @http.route(['/shop/payment/allow_third_party'], type='json', auth="public", methods=['POST'], website=True)
    def order_allow_third_party(self, **post):
        if post.get('allow_third_party') == 'another':
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
                    'third_party_name': third_party_name.strip(),
                    'third_party_lastname': third_party_lastname.strip(),
                    'third_party_lastname2': third_party_lastname2.strip(),
                    'third_party_name_vat': third_party_name_vat.strip()
                }
                order.sudo().write(vals)
            return True

    @http.route(['/shop/payment/delivery_carrier_selection'], type='json', auth="public", methods=['POST'],
                website=True)
    def delivery_carrier_selection(self, **kw):
        delivery_ids = request.env['delivery.carrier'].sudo().search(
            [('allow_third_party', '=', True), ('is_published', '=', True)])
        delivery_carrier_id = int(kw.get('delivery_type_id'))
        allow_third_party = any(delivery_ids.filtered(lambda delivery: delivery.id == delivery_carrier_id))
        return {'allow_third_party': allow_third_party}
