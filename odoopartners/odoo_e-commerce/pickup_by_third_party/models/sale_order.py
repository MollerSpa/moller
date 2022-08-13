from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    third_party_name = fields.Char(
        string='Name',
    )
    third_party_lastname = fields.Char(
        string='Last name',
    )
    third_party_lastname2 = fields.Char(
        string='Mother last name',
    )
    third_party_name_vat = fields.Char(
        string='N° de RUT',
    )
