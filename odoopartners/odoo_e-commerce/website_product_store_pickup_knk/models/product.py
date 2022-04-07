# -*- coding: utf-8 -*-
# Powered by Kanak Infosystems LLP.
# © 2020 Kanak Infosystems LLP. (<https://www.kanakinfosystems.com>)

from odoo import fields, models


class DeliveryCarrier(models.Model):
    _inherit = "delivery.carrier"

    is_pickup = fields.Boolean('Is Pickup')
    available_pickup_ids = fields.Many2many('res.partner', string='Available Stores')


class SaleOrder(models.Model):
    _inherit = "sale.order"

    pickup_store_id = fields.Many2one('res.partner', string='Pickup Store')


class ResPartner(models.Model):
    _inherit = "res.partner"

    is_pickup = fields.Boolean('Is Pickup')
    opening_closing_hours = fields.Html(string='Opening Closing Hours')
