# -*- coding: utf-8 -*-

from odoo import fields, osv, models, api


class ResCompany(models.Model):
    _inherit = "res.company"

    def _get_mercadopago_cl_account(self, ids, name, arg, context=None):
        Acquirer = self.env['payment.acquirer']
        company_id = company = self.env.user.company_id
        mercadopago_ids = Acquirer.search( [
            ('website_published', '=', True),
            ('name', 'ilike', 'mercadopago_cl'),
            ('company_id', '=', company_id),
        ], limit=1, context=context)
        if mercadopago_ids:
            MP = Acquirer.browse( mercadopago_ids[0], context=context)
            return dict.fromkeys(ids, MP.mercadopago_email_account)
        return dict.fromkeys(ids, False)

    def _set_mercadopago_cl_account(self, id, name, value, arg, context=None):
        Acquirer = self.env['payment.acquirer']
        company_id = company = self.env.user.company_id
        mercadopago_account = self.browse( id, context=context).mercadopago_account
        mercadopago_ids = Acquirer.search( [
            ('website_published', '=', True),
            ('mercadopago_email_account', '=', mercadopago_account),
            ('company_id', '=', company_id),
        ], context=context)
        if mercadopago_ids:
            Acquirer.write(mercadopago_ids, {'mercadopago_email_account': value}, context=context)
        return True

    mercadopago_cl_account = fields.Char( compute=_get_mercadopago_cl_account,
            fnct_inv=_set_mercadopago_cl_account,
            nodrop=True,
            string='MercadoPago Account Chile',
            help="MercadoPago Chile username (usually email) for receiving online payments."
        )
