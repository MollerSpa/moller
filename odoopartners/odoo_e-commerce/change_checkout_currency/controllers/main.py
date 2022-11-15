from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo import http
from odoo.http import request


class WebsiteSaleGift(WebsiteSale):

    @http.route(['/shop/cart/update_currency_checkout'], type='json', auth="public", methods=['POST'], website=True)
    def cart_update_currency_checkout(self, **kw):
        order_id = kw['order_id']
        price_list_id = kw['price_list_id']
        sale_order_id = request.env['sale.order'].sudo().browse(order_id)
        if sale_order_id.pricelist_id and sale_order_id.pricelist_id.id == price_list_id or not price_list_id:
            return {'equal': True}
        # Validation for enterprise shipping types
        if sale_order_id.carrier_id.delivery_type in ['fedex']:
            return {'equal': True}
        sale_order_id.pricelist_id = price_list_id
        for line in sale_order_id.order_line:
            line.product_id_change()
        sale_order_id._onchange_pricelist_id()

        # This is to run minor update as /shop/update_carrier controller
        data = {'carrier_id': sale_order_id.carrier_id.id}
        return self._update_website_sale_delivery_return(sale_order_id, **data)
