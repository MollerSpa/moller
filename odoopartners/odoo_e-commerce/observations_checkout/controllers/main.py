from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale

class websiteSaleOrder(WebsiteSale):

    @http.route(['/checkout_observations'], type='json', auth="public", methods=['POST'], website=True)
    def order_checkout_observations(self, **post):
        checkout_observations = post.get('checkout_observations')
        if checkout_observations:
            order = request.website.sale_get_order()
            redirection = self.checkout_redirection(order)
            if redirection:
                return redirection
            if order and order.id:
                order.sudo().write({'checkout_observations': checkout_observations})
        return True