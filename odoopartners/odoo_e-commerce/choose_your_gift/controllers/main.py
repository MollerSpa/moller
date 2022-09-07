from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo import http
from odoo.http import request


class WebsiteSaleGift(WebsiteSale):

    @http.route(['/shop/cart/update_gift'], type='json', auth="public", methods=['POST'], website=True)
    def cart_update_gift(self, **kw):
        gift_product_ids = kw['product_data']
        if not kw['product_data']:
            return {'warning': 'No hay regalos a validar'}

        product_model = request.env['product.product']
        sale_order_line_model = request.env['sale.order.line']
        origin_product_id = product_model.browse(gift_product_ids[0]['origin_product_id'])
        number_gifts = origin_product_id.number_gifts
        total_gift_qty = sum(list(map(lambda x: x['quantity'], gift_product_ids)))

        if total_gift_qty > number_gifts:
            return {'warning': f'The maximum number of gifts allowed is {number_gifts}'}
        sale_order = request.website.sale_get_order(force_create=True)
        if sale_order.state != 'draft':
            request.session['sale_order_id'] = None
            sale_order = request.website.sale_get_order(force_create=True)

        gift_line_ids = []
        sale_order_line_sudo_env = request.env['sale.order.line'].sudo()
        for gift in gift_product_ids:
            product_id = product_model.sudo().browse(gift['product_id'])
            exist_line_id = None
            if not product_id._is_add_to_cart_allowed():
                values = {
                    'order_id': sale_order.id,
                    'product_uom_qty': 1,
                    'product_uom': product_id.uom_id.id,
                    'product_id': product_id.id,
                }
                exist_line_id = sale_order_line_model.sudo().create(values).id
            line_value = sale_order._cart_update(
                product_id=gift['product_id'],
                line_id=exist_line_id,
                add_qty=0,
                set_qty=gift['quantity'],
                product_custom_attribute_values=[],
                no_variant_attribute_values=[]
            )
            line_id = sale_order_line_sudo_env.browse(line_value['line_id'])
            line_id.is_gift = True
            gift_line_ids.append(line_id.id)
        origin_line_id = sale_order_line_sudo_env.search([('product_id', '=', origin_product_id.id), ('order_id', '=', sale_order.id)], limit=1)
        origin_line_id.gift_line_ids = gift_line_ids

        return request.redirect("/shop/cart")
