from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo import http
from odoo.http import request


class WebsiteSaleGift(WebsiteSale):

    @http.route(['/shop/cart/update_currency_checkout'], type='json', auth="public", methods=['POST'], website=True)
    def cart_update_currency_checkout(self, **kw):
        order_id = kw['order_id']
        price_list_id = kw['price_list_id']

        sale_order_id = request.env['sale.order'].browse(order_id)
        if sale_order_id.pricelist_id and sale_order_id.pricelist_id.id == price_list_id:
            return {'equal': True}
        sale_order_id.pricelist_id = price_list_id
        sale_order_id._onchange_pricelist_id()

        return request.redirect("/shop/payment")

