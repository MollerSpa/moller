# -*- coding: utf-8 -*-
# Powered by Kanak Infosystems LLP.
# © 2020 Kanak Infosystems LLP. (<https://www.kanakinfosystems.com>)

import re
from odoo import fields, http, tools, _
from odoo.http import request, route
from odoo.addons.sale.controllers.portal import CustomerPortal


class WebsiteSoludoo(http.Controller):

    @route(["/update/shipping/type"], type="json", auth="public", website=True)
    def update_shipping_type(self, delivery_id=None, store_id=None, **post):
        DeliveryCarrier = request.env['delivery.carrier'].sudo()
        ResPartner = request.env['res.partner'].sudo()
        order_id = request.website.sale_get_order()
        cart_delivery = None
        if order_id and delivery_id and not store_id:
            delivery_id = DeliveryCarrier.browse(delivery_id)
            if not delivery_id.is_pickup:
                order_id.sudo().write({'pickup_store_id': False})
                cart_delivery = request.env['ir.ui.view']._render_template("website_product_store_pickup_knk.cart_delivery_update", {
                        'website_sale_order': order_id,
                        'date': fields.Date.today(),
                    })
        if order_id and store_id:
            store_id = ResPartner.browse(store_id)
            order_id.sudo().write({'pickup_store_id': store_id.id})
            cart_delivery = request.env['ir.ui.view']._render_template("website_product_store_pickup_knk.cart_pickup_address", {
                    'website_sale_order': order_id,
                    'date': fields.Date.today(),
                })
        return {"success": True, 'cart_delivery': cart_delivery}

    @route(["/update/pickup/store"], type="json", auth="public", website=True)
    def update_pickup_store(self, store_id=None, **post):
        ResPartner = request.env['res.partner'].sudo()
        order_id = request.website.sale_get_order()
        pickup_address = None
        if order_id and store_id:
            store_id = ResPartner.browse(store_id)
            order_id.sudo().write({'pickup_store_id': store_id.id})
            pickup_address = request.env['ir.ui.view']._render_template("website_product_store_pickup_knk.cart_pickup_address", {
                    'website_sale_order': order_id,
                    'date': fields.Date.today(),
                })
        return {"success": True, 'pickup_address': pickup_address}