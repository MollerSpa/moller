from odoo import api, fields, models


class DeliveryCarrier(models.Model):
    _inherit = 'delivery.carrier'

    send_other_address = fields.Boolean(string='Enviar a Otra dirección')


class ResPartner(models.Model):
    _inherit = 'res.partner'

    def get_shipping_address_count(self):
        partner = self.with_context(show_address=1).sudo()
        shipping_count = partner.search_count([
            ("id", "child_of", self.commercial_partner_id.ids),
            '|', ("type", "in", ["delivery", "other"]), ("id", "=", self.commercial_partner_id.id)
        ])
        shipping_href = '/shop/checkout'
        if shipping_count == 1:
            shipping_href = '/shop/address'
        return shipping_href
