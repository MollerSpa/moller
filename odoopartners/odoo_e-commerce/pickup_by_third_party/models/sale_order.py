from odoo import fields, models

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    third_party_name = fields.Char(
        string='Name',
        readonly=True
    )
    third_party_lastname = fields.Char(
        string='Last name',
        readonly=True
    )
    third_party_lastname2 = fields.Char(
        string='Mother last name',
        readonly=True
    )
    third_party_name_vat = fields.Char(
        string='N° de RUT',
        readonly=True
    )
    allow_third_party = fields.Boolean(
        string='Allow third party withdrawal',
        readonly=True
    )