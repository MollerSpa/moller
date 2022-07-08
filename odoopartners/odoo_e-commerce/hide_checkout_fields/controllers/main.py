from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSaleExtend(WebsiteSale):

    def _get_mandatory_fields_billing(self, country_id=False):
        req = super(WebsiteSaleExtend, self)._get_mandatory_fields_billing(country_id=country_id)
        website = request.website
        self.update_mandatory_data_billing(website, req)
        return req

    def update_mandatory_data_billing(self, website, mandatory_fields):
        if not website.use_billing_company or website.use_billing_company and not website.billing_company_required:
            self._remove_field(mandatory_fields, 'company_name')
        else:
            if 'company_name' not in mandatory_fields:
                mandatory_fields += ['company_name']

        if not website.use_billing_vat or website.use_billing_vat and not website.billing_vat_required:
            self._remove_field(mandatory_fields, 'vat')
        else:
            if 'vat' not in mandatory_fields:
                mandatory_fields += ['vat']
