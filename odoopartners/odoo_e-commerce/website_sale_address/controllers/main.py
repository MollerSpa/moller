# -*- coding: utf-8 -*-

import logging

from odoo import api
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale

_logger = logging.getLogger(__name__)


class WebsiteSaleExtend(WebsiteSale):

    def _get_country_related_render_values(self, kw, render_values):
        result = super(WebsiteSaleExtend, self)._get_country_related_render_values(kw=kw, render_values=render_values)
        mode = render_values['mode']
        order = render_values['website_sale_order']
        default_billing_country = request.website.default_billing_country_id
        default_shipping_country = request.website.default_shipping_country_id

        if default_billing_country and (\
            mode == ('new', 'billing') and order.partner_id.id == request.website.user_id.sudo().partner_id.id or \
            mode == ('edit', 'billing') and not result['country']):

            result.update({
                'country': default_billing_country,
                'country_states': default_billing_country.get_website_sale_states(mode=mode[1]),
                'countries': default_billing_country.get_website_sale_countries(mode=mode[1]),
            })

            if mode == ('edit', 'billing'):
                order.partner_id.country_id = default_billing_country.id

        if default_shipping_country and mode[1] == 'shipping':
            result.update({
                'country': default_shipping_country,
                'country_states': default_shipping_country.get_website_sale_states(mode=mode[1]),
                'countries': default_shipping_country.get_website_sale_countries(mode=mode[1]),
            })
            if order.partner_id != order.partner_shipping_id:
                order.partner_shipping_id.country_id = default_shipping_country.id

        return result

    @api.model
    def _remove_field(self, field_list, field):
        res = field_list
        if field in field_list:
            res.remove(field)
        return res

    def _get_mandatory_fields_billing(self, country_id=False):
        """ Change original field list:
            ["name", "email", "street", "city", "country_id"] """
        req = super(WebsiteSaleExtend, self)._get_mandatory_fields_billing(country_id=country_id)
        website = request.website.sudo()
        _logger.debug("   --IN--  _get_mandatory_fields_billing: req={}".format(req))

        if not website.use_billing_address_street or website.use_billing_address_street and not website.billing_address_street_required:
            self._remove_field(req, 'street')
        if not website.use_billing_address_city or website.use_billing_address_city and not website.billing_address_city_required:
            self._remove_field(req, 'city')


        if website.billing_address_zip_required:
            req += ['zip']
        else:
            self._remove_field(req, 'zip')
        if website.billing_address_state_required:
            req += ['state_id']
        else:
            self._remove_field(req, 'state_id')

        if website.use_billing_address_phone and website.billing_address_phone_required:
            req += ['phone']
        if website.use_billing_address_street2 and website.billing_address_street2_required:
            req += ['street2']

        _logger.debug("   --OUT--  _get_mandatory_fields_billing: req={}".format(req))
        return req

    def _get_mandatory_fields_shipping(self, country_id=False):
        """ Change original field list:
            ["name", "street", "city", "country_id"] """
        req = super(WebsiteSaleExtend, self)._get_mandatory_fields_shipping(country_id=country_id)
        website = request.website
        _logger.debug("   --IN--  _get_mandatory_fields_shipping: req={}".format(req))

        if not website.use_shipping_address_street or website.use_shipping_address_street and not website.shipping_address_street_required:
            self._remove_field(req, 'street')
        if not website.use_shipping_address_city or website.use_shipping_address_city and not website.shipping_address_city_required:
            self._remove_field(req, 'city')


        if website.shipping_address_zip_required:
            req += ['zip']
        else:
            self._remove_field(req, 'zip')
        if website.shipping_address_state_required:
            req += ['state_id']
        else:
            self._remove_field(req, 'state_id')

        if website.use_shipping_address_phone and website.shipping_address_phone_required:
            req += ['phone']
        if website.use_shipping_address_street2 and website.shipping_address_street2_required:
            req += ['street2']

        _logger.debug("   --OUT--  _get_mandatory_fields_shipping: req={}".format(req))
        return req

    def checkout_form_validate(self, mode, all_form_values, data):
        result = super(WebsiteSaleExtend, self).checkout_form_validate(mode=mode, all_form_values=all_form_values, data=data)
        _logger.debug("   ---   checkout_form_validate: mode={}, error={}, error_message={}, website={}".format(mode, result[0], result[1], request.website))
        return result

    def checkout_values(self, **kw):
        result = super(WebsiteSaleExtend, self).checkout_values(**kw)
        _logger.debug("   ---   checkout_values: result={}, kw={}".format(result, kw))
        return result
