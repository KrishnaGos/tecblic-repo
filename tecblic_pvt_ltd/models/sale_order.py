# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class SaleCoupon(models.Model):
    _inherit = 'sale.order'


    sales_name = fields.Char(string="Sales Name")
    coupon_amt = fields.Float(string='Coupon Discount', readonly=True)
    subtotal_amt = fields.Float(string='Subtotal Amount', compute='_compute_coupon_total')

    @api.depends("coupon_amt")
    def _compute_coupon_total(self):
        import json
        for record in self:
            sum = json.loads(record.tax_totals_json).get('amount_total')
            record.subtotal_amt = sum + record.coupon_amt
            print("#################################", record.subtotal_amt)