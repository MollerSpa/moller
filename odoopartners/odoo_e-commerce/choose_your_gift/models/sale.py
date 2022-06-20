from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    is_gift = fields.Boolean(string='Es un regalo?')


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    is_gift = fields.Boolean(string='Es un regalo?')
    gift_line_ids = fields.Many2many(
        comodel_name='sale.order.line',
        relation='gift_line_ids_sale_order_line_rel',
        string='Gift lines',
        column1='order_id',
        column2='id'
    )

    def unlink(self):
        lines_ids = self
        for line in lines_ids:
            if line.gift_line_ids:
                self = self + line.gift_line_ids
        return super(SaleOrderLine, self).unlink()
