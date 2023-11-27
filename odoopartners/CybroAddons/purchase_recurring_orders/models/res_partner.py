# -*- coding: utf-8 -*-
################################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2023-TODAY Cybrosys Technologies(<https://www.cybrosys.com>).
#    Author: Ruksana P (odoo@cybrosys.com)
#
#    You can modify it under the terms of the GNU AFFERO
#    GENERAL PUBLIC LICENSE (AGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU AFFERO GENERAL PUBLIC LICENSE (AGPL v3) for more details.
#
#    You should have received a copy of the GNU AFFERO GENERAL PUBLIC LICENSE
#    (AGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
################################################################################
from odoo import models


class ResPartner(models.Model):
    """ Inherited for adding new smart button purchase agreement"""
    _inherit = 'res.partner'

    def action_purchase_agreement(self):
        """Method of agreement smart button """
        return {
            'name': 'agreements',
            'type': 'ir.actions.act_window',
            'res_model': 'purchase.recurring.agreement',
            'view_mode': 'tree,form',
            'view_id': False,
            'domain': [('partner_id', '=', self.id)]
        }