from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo import http
from odoo.http import request


class WebsiteSaleGift(WebsiteSale):

    @http.route(['/shop/cart/update_gift'], type='json', auth="public", methods=['POST'], website=True)
    def cart_update_gift(self, **kw):
        gift_product_ids = kw['product_data']
        if not kw['product_data']:
            return {'warning': 'No hay regalos a validar'}

        origin_product_id = request.env['product.product'].browse(gift_product_ids[0]['origin_product_id'])
        number_gifts = origin_product_id.number_gifts
        total_gift_qty = sum(list(map(lambda x: x['quantity'], gift_product_ids)))

        if total_gift_qty > number_gifts:
            return {'warning': f'La cantidad permitida de regalos es {number_gifts}'}

        sale_order = request.website.sale_get_order(force_create=True)
        if sale_order.state != 'draft':
            request.session['sale_order_id'] = None
            sale_order = request.website.sale_get_order(force_create=True)
        gift_line_ids = []
        for gift in gift_product_ids:
            line_value = sale_order._cart_update(
                product_id=gift['product_id'],
                add_qty=0,
                set_qty=gift['quantity'],
                product_custom_attribute_values=[],
                no_variant_attribute_values=[]
            )
            line_id = request.env['sale.order.line'].browse(line_value['line_id'])
            line_id.is_gift = True
            gift_line_ids.append(line_id.id)

        origin_line_id = request.env['sale.order.line'].search([('product_id', '=', origin_product_id.id), ('order_id', '=', sale_order.id)], limit=1)
        origin_line_id.gift_line_ids = gift_line_ids

        return request.redirect("/shop/cart")

