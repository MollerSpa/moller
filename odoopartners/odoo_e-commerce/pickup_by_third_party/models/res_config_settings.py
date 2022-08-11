from odoo import fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    allow_third_party = fields.Boolean(
        string='Allow third party withdrawal',
        config_parameter='pickup_by_third_party.allow_third_party',
        help='Additional fields will be added to indicate who the pick up person is.',
    )