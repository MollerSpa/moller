# -*- coding: utf-8 -*-

import odoo.tests
from odoo import api
from odoo.addons.website_sale_tweaks.controllers.main import WebsiteSaleExtend
from odoo.addons.website_sale.tests.test_sale_process import TestWebsiteSaleCheckoutAddress
from odoo.addons.website.tools import MockRequest


@odoo.tests.tagged('post_install', '-at_install', 'website_sale_address')
class TestWebsiteSaleAddressChange(TestWebsiteSaleCheckoutAddress):

    def setUp(self):
        super(TestWebsiteSaleAddressChange, self).setUp()
        self.WebsiteSaleController = WebsiteSaleExtend()

    def test_10_public_user_without_changing_address_fields(self):
        so = self._create_so(self.website.user_id.partner_id.id)
        env = api.Environment(self.env.cr, self.website.user_id.id, {})
        with MockRequest(env, website=self.website.with_env(env), sale_order_id=so.id):

            billing_address_values = {
                'partner_id': -1,
                'name': 'Billing address',
                'email': 'email@email.email',
                'phone': '0123456789',
                'street': 'ooo',
                'city': 'ABC',
                'state_id': self.env.ref('base.state_au_1').id,
                'country_id': self.env.ref('base.au').id,
                'submitted': 1,
            }

            self.website.write({
                'billing_address_email_required': True,
                'use_billing_address_phone': True,
                'billing_address_phone_required': True,
                'use_billing_address_street': True,
                'billing_address_street_required': True,
                'use_billing_address_street2': True,
                'billing_address_street2_required': False,
                'use_billing_address_city': True,
                'billing_address_city_required': True,
                'use_billing_address_zip': True,
                'billing_address_zip_required': False,
                'use_billing_address_state': True,
                'use_billing_address_country': True,
            })

            self.WebsiteSaleController.address(**billing_address_values)
            new_partner = so.partner_id
            self.assertNotEqual(new_partner, self.website.user_id.partner_id, "Order partner must not be the equal the public user partner.")
            self.assertTrue(new_partner.email, "Order billing email should not be empty.")
            self.assertTrue(new_partner.phone, "Order billing phone should not be empty.")
            self.assertTrue(new_partner.street, "Order billing street should not be empty.")
            self.assertFalse(new_partner.street2, "Order billing street2 can be empty.")
            self.assertTrue(new_partner.city, "Order billing city should not be empty.")
            self.assertFalse(new_partner.zip, "Order billing zip code can be empty.")
            self.assertTrue(new_partner.state_id, "Order billing state should not be empty.")
            self.assertTrue(new_partner.country_id, "Order billing country should not be empty.")

            shipping_address_values = {
                'partner_id': new_partner.id,
                'name': 'Shipping address',
                'email': 'email2@email.email',
                'phone': '111222333',
                'street': 'bbb',
                'city': 'DEF',
                'country_id': self.env.ref('base.ar').id,
                'state_id': self.env.ref('base.state_ar_b').id,
                'zip': '12345',
                'submitted': 1,
            }

            self.website.write({
                'use_shipping_address_phone': True,
                'use_shipping_address_street': True,
                'use_shipping_address_street2': True,
                'use_shipping_address_city': True,
                'use_shipping_address_zip': True,
                'use_shipping_address_state': True,
                'use_shipping_address_country': True,
            })

            self.WebsiteSaleController.address(**shipping_address_values)
            self.assertEqual(new_partner.email, 'email2@email.email', 'Partner uses the same billing and shipping address. So the email should be changed.')
            self.assertEqual(new_partner.city, 'DEF', 'Partner uses the same billing and shipping address. So the city should be changed.')
            self.assertEqual(new_partner.country_id, self.env.ref('base.ar'), 'Partner uses the same billing and shipping address. So the country should be changed.')

            shipping_address_values = {
                'partner_id': -1,
                'name': 'Shipping address',
                'email': 'email3@email.email',
                'phone': '000222999',
                'street': 'fff',
                'city': 'KLM',
                'country_id': self.env.ref('base.ar').id,
                'state_id': self.env.ref('base.state_ar_c').id,
                'zip': '22333',
                'submitted': 1,
            }

            self.WebsiteSaleController.address(**shipping_address_values)
            new_shipping = self._get_last_address(new_partner)
            self.assertNotEqual(new_shipping, new_partner, "Order partner and shipping address must be different.")

    def test_11_public_user_hide_all_address_fields(self):
        so = self._create_so(self.website.user_id.partner_id.id)
        env = api.Environment(self.env.cr, self.website.user_id.id, {})
        with MockRequest(env, website=self.website.with_env(env), sale_order_id=so.id):

            billing_address_values = {
                'partner_id': -1,
                'name': 'Billing address',
                'email': 'email@email.email',
                'country_id': self.env.ref('base.ao').id,
                'submitted': 1,
            }

            self.website.write({
                'billing_address_email_required': False,
                'use_billing_address_phone': False,
                'billing_address_phone_required': False,
                'use_billing_address_street': False,
                'billing_address_street_required': False,
                'use_billing_address_street2': False,
                'billing_address_street2_required': False,
                'use_billing_address_city': False,
                'billing_address_city_required': False,
                'use_billing_address_zip': False,
                'billing_address_zip_required': False,
                'use_billing_address_state': False,
                'billing_address_state_required': False,
                'use_billing_address_country': False,
            })

            address_response = self.WebsiteSaleController.address(**billing_address_values)
            new_partner = so.partner_id
            self.assertNotEqual(new_partner, self.website.user_id.partner_id, "Order partner must not be the equal the public user partner.")
            self.assertTrue(new_partner.email, "Order billing email should not be empty.")
            self.assertFalse(new_partner.phone, "Order billing phone should be empty.")
            self.assertFalse(new_partner.street, "Order billing street should be empty.")
            self.assertFalse(new_partner.street2, "Order billing street2 should be empty.")
            self.assertFalse(new_partner.city, "Order billing city should be empty.")
            self.assertFalse(new_partner.zip, "Order billing zip code should be empty.")
            self.assertFalse(new_partner.state_id, "Order billing state should be empty.")
            self.assertTrue(new_partner.country_id, "Order billing country should not be empty.")

            shipping_address_values = {
                'partner_id': -1,
                'name': 'Shipping address',
                'email': 'email2@email.email',
                'country_id': self.env.ref('base.ao').id,
                'submitted': 1,
            }

            self.website.write({
                'use_shipping_address_phone': False,
                'shipping_address_phone_required': False,
                'use_shipping_address_street': False,
                'shipping_address_street_required': False,
                'use_shipping_address_street2': False,
                'use_shipping_address_city': False,
                'shipping_address_city_required': False,
                'use_shipping_address_zip': False,
                'use_shipping_address_state': False,
                'use_shipping_address_country': False,
            })

            self.WebsiteSaleController.address(**shipping_address_values)
            new_shipping = self._get_last_address(new_partner)
            self.assertNotEqual(new_shipping, new_partner, "Order partner and shipping address must be different.")
            self.assertFalse(new_shipping.phone, "Order shipping phone should be empty.")
            self.assertFalse(new_shipping.street, "Order shipping street should be empty.")
            self.assertFalse(new_shipping.street2, "Order shipping street2 should be empty.")
            self.assertFalse(new_shipping.city, "Order shipping city should be empty.")
            self.assertFalse(new_shipping.zip, "Order shipping zip code should be empty.")
            self.assertFalse(new_shipping.state_id, "Order shipping state should be empty.")
            self.assertTrue(new_shipping.country_id, "Order shipping country should not be empty.")


    def _check_required_address_field(self, field, value, country_type='no_required', mode=None):
        """ This test ensure that after hiding the billing/shipping address fields,
            partner address fields are saved properly.

            mode "new / billing":
                order.partner_id = public_user.partner_id
                kw['partner_id'] = -1
            mode "edit / billing":
                order.partner_id != public_user.partner_id
                kw['partner_id'] > 0 AND kw['partner_id'] = order.partner_id.id
            mode "new / shipping":
                order.partner_id != public_user.partner_id
                kw['partner_id'] = -1
            mode "edit / shipping":
                kw['partner_id'] > 0 AND kw['partner_id'] != order.partner_id.id

            :param country_type: available values ('no_required', 'zip_required', 'state_required', 'zip_state_required')
        """
        so = self._create_so(self.website.user_id.partner_id.id)
        env = api.Environment(self.env.cr, self.website.user_id.id, {})
        with MockRequest(env, website=self.website.with_env(env), sale_order_id=so.id):

            billing_address_values = {
                'partner_id': -1,
                'name': 'Billing address',
                'email': 'email@email.email',
                'submitted': 1,
            }
            shipping_address_values = {
                'partner_id': -1,
                'name': 'Shipping address',
                'email': 'email2@email.email',
                'submitted': 1,
            }
            vals = {}

            if country_type == 'no_required':
                vals = {
                    'country_id': self.env.ref('base.ao').id,
                }
            elif country_type == 'zip_required':
                vals = {
                    'country_id': self.env.ref('base.dk').id,
                    'zip': '001122',
                }
            elif country_type in ['state_required', 'zip_state_required']:
                vals = {
                    'country_id': self.env.ref('base.ca').id,
                    'zip': '001122',
                    'state_id': self.env.ref('base.state_ca_ab').id,
                }
            billing_address_values.update(vals)
            shipping_address_values.update(vals)


            self.website.write({
                'billing_address_phone_required': False,
                'billing_address_street_required': False,
                'billing_address_street2_required': False,
                'billing_address_city_required': False,
                'use_billing_address_%s' % field: True,
                'billing_address_%s_required' % field: True,
            })

            self.WebsiteSaleController.address(**billing_address_values)
            new_partner = so.partner_id
            self.assertEqual(new_partner, self.website.user_id.partner_id, "New partner should not be created as we do not specify the required %s field." % field)

            billing_address_values[field] = value
            self.WebsiteSaleController.address(**billing_address_values)
            new_partner = so.partner_id
            self.assertNotEqual(new_partner, self.website.user_id.partner_id, "New partner should not be created and this order partner must not be the equal the public user partner.")
            self.assertEqual(getattr(new_partner, field), value)

            self.assertEqual(new_partner.email, 'email@email.email')

            billing_address_values = {
                'partner_id': new_partner.id,
                'name': 'Edit Billing address',
                'email': 'new_email@email.email',
                'submitted': 1,
            }
            self.WebsiteSaleController.address(**billing_address_values)



            self.website.write({
                'use_shipping_address_phone': False,
                'shipping_address_phone_required': False,
                'use_shipping_address_street': False,
                'shipping_address_street_required': False,
                'use_shipping_address_street2': False,
                'use_shipping_address_city': False,
                'shipping_address_city_required': False,
                'use_shipping_address_zip': False,
                'use_shipping_address_state': False,
                'use_shipping_address_country': False,
                'use_shipping_address_%s' % field: True,
                'shipping_address_%s_required' % field: True,
            })

            self.WebsiteSaleController.address(**shipping_address_values)
            new_shipping = new_partner if not new_partner.child_ids else self._get_last_address(new_partner)
            self.assertEqual(new_shipping, new_partner, "New shipping should not be created as we do not specify the required %s field." % field)

            shipping_address_values[field] = value
            self.WebsiteSaleController.address(**shipping_address_values)
            new_shipping = self._get_last_address(new_partner)
            self.assertNotEqual(new_shipping, new_partner, "Order partner and shipping address must be different.")

            shipping_address_values.update({
                'partner_id': new_shipping.id,
                'name': 'Edit Shipping address',
                'email': 'new_email2@email.email',
            })

            del shipping_address_values[field]
            self.WebsiteSaleController.address(**shipping_address_values)

            shipping_address_values[field] = value
            self.WebsiteSaleController.address(**shipping_address_values)

    def test_12_public_user_address_phone_field(self):
        self._check_required_address_field('phone', '111222333')
        self._check_required_address_field('phone', '111222333', country_type='zip_required')
        self._check_required_address_field('phone', '111222333', country_type='state_required')

    def test_13_public_user_address_street_field(self):
        self._check_required_address_field('street', 'abcdef')
        self._check_required_address_field('street', 'abcdef', country_type='zip_required')
        self._check_required_address_field('street', 'abcdef', country_type='state_required')

    def test_14_public_user_address_street2_field(self):
        self._check_required_address_field('street2', 'ABC 012')
        self._check_required_address_field('street2', 'ABC 012', country_type='zip_required')
        self._check_required_address_field('street2', 'ABC 012', country_type='state_required')

    def test_15_public_user_address_city_field(self):
        self._check_required_address_field('city', 'Kyiv')
        self._check_required_address_field('city', 'Kyiv', country_type='zip_required')
        self._check_required_address_field('city', 'Kyiv', country_type='state_required')
