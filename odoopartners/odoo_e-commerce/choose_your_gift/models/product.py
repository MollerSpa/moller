from odoo import api, fields, models


class ProductPublicCategory(models.Model):
    _inherit = 'product.public.category'

    choose_your_gift = fields.Boolean(string='Elige tu regalo')
    number_gifts = fields.Integer(string='N° de Regalos permitidos')
    gifts_ids = fields.Many2many(
        comodel_name='product.product',
        string='Opciones de Regalo',
    )


class ProductProduct(models.Model):
    _inherit = "product.product"

    def filter_gifts(self, warehouse_id):
        data = []
        for gift_id in self.gifts_ids:
            gift_sudo = gift_id.sudo()
            virtual_available = gift_sudo.with_context(warehouse=warehouse_id).virtual_available
            available_threshold = gift_sudo.product_tmpl_id.available_threshold
            data.append({
                'gift_id': gift_sudo,
                'gift_image': gift_sudo.image_128,
                'error': False if virtual_available > available_threshold else True
            })
        return data


class ProductTemplate(models.Model):
    _inherit = "product.template"

    website_gift_active = fields.Boolean(
        string='Regalos activos?',
        compute='compute_website_gift_active',
        store=True
    )
    gifts_ids = fields.Many2many(
        comodel_name='product.product',
        string='Opciones de Regalo',
        compute='compute_website_gift_active',
        store=True
    )
    number_gifts = fields.Integer(
        string='N° de Regalos permitidos',
        compute='compute_website_gift_active',
        store=True
    )

    @api.depends('public_categ_ids', 'public_categ_ids.choose_your_gift', 'public_categ_ids.gifts_ids')
    def compute_website_gift_active(self):
        for rec in self:
            website_gift_active = False
            gifts_ids = False
            number_gifts = 0
            if rec.public_categ_ids:
                public_categ_ids = rec.public_categ_ids.filtered(lambda x: x.choose_your_gift)
                if public_categ_ids:
                    lower_categ_id = self.env['product.public.category'].search([('id', 'in', public_categ_ids.ids)], limit=1, order='sequence')
                    website_gift_active = True
                    gifts_ids = lower_categ_id.gifts_ids
                    number_gifts = lower_categ_id.number_gifts
            rec.website_gift_active = website_gift_active
            rec.gifts_ids = gifts_ids
            rec.number_gifts = number_gifts
