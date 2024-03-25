# -*- coding: utf-8 -*-
################################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2023-TODAY Cybrosys Technologies(<https://www.cybrosys.com>).
#    Author: Ammu Raj (odoo@cybrosys.com)
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
from odoo import fields, models


class ApplyDiscounts(models.Model):
    """This class is used to define the discounts in percentage according the
    points acquired"""
    _name = 'apply.discounts'
    _description = 'Apply discounts according to the points'

    starting_points = fields.Integer(string='Starting point',
                                     help='Starting point for getting the'
                                          'discount')
    end_points = fields.Integer(string='Ending points',
                                help='The ending point of discount')
    discount = fields.Float(string='Discount in %',
                            help='The percentage discount that can give between'
                                 'these point')