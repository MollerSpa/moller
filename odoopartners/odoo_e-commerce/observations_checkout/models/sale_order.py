from odoo import fields, models

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    checkout_observations = fields.Text(
        string='Customer Observations'
    )