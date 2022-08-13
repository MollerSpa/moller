from odoo import fields, models


class DeliveryCarrier(models.Model):
    _inherit = 'delivery.carrier'

    allow_third_party = fields.Boolean(
        string='Allow third party withdrawal'
    )
