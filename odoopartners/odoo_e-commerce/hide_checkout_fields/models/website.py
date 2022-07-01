from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = 'website'

    use_billing_delivery_address = fields.Boolean(
        string='Delivery address',
        default=True,
        help='Si Activas este campo, Odoo ocultará el campo “Enviar a la misma dirección” en la página de checkout'
    )
    use_billing_company = fields.Boolean(
        string='Company',
        default=True,
    )
    billing_company_required = fields.Boolean(
        string='Company required',
        default=False,
    )
    use_billing_vat = fields.Boolean(
        string='VAT',
        default=True,
    )
    billing_vat_required = fields.Boolean(
        string='VAT required',
        default=False,
    )
