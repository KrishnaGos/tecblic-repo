# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import date

from odoo import api, fields, models, _


class SaleCoupon(models.TransientModel):
    _name = "sale.coupon"
    _description = "Apply the coupon get discount"


    coupon_id = fields.Many2one(string="Coupon", comodel_name='coupon.master')



    def apply(self):
        active_ids =self.env.context.get('active_id')
        print("#################################active_ids$$$$$$$$$$$$$$$$$$$$$self.env.context", active_ids, self.env.context)
        sale_oder_id = self.env['sale.order'].browse(active_ids)
        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$browse(active_ids)", sale_oder_id)
        import json
        for rec in sale_oder_id:
            # total = rec.tax_totals_json
            total = json.loads(rec.tax_totals_json).get('amount_total')
            print("@@@@@@@@@@@@@@@total fields", total)
            sum = (total * self.coupon_id.discount)/100
            # print("1!!!!!!!!!!", sum)
            rec.update({
                'coupon_amt': sum
            })

