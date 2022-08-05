# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import json
from datetime import date
import datetime

from odoo import api, fields, models, _


class VendorsPartner(models.TransientModel):
    _name = "res.partner.wizard"
    _description = "Generate The Vendors Report"

    vendors_date = fields.Date(string="Date From")
    deliver_date = fields.Date(string="Date To")
    rating = fields.Selection([('qty', 'Quantity'), ('dure', 'Duration')], string="Vendors Rating")
    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id')
    vendors_id = fields.Many2one('res.partner', string="vendors id")

    def get_report_values_with_account_move(self):
        data = []
        months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
                  "November", "December"]
        vendor_details = self.env['account.move'].search([('invoice_date', '>=', self.vendors_date),
                                                          ('invoice_date', '<=', self.deliver_date)])
        startmonth = months[self.vendors_date.month - 1]
        endmonth = months[self.deliver_date.month - 1]
        total_months = months[self.vendors_date.month - 1: self.deliver_date.month]
        vals = {
            'records': vendor_details,
            'startmonth': startmonth,
            'endmonth': endmonth,
            'total_months': total_months,
        }
        data.append(vals)
        print("\n\n\n\n\ndata ------------------", data)
        return data

    def confirm(self):
        return self.env.ref('tecblic_pvt_ltd.applicant_report_vendor').report_action(self)


