# -*- coding: utf-8 -*-

from odoo import models, fields

class PosOrderinInherit(models.Model):
    _inherit = 'pos.order'

    pro_total = fields.Integer(string="Total Items")
    pro_qty = fields.Integer(string="Total Qty", compute='_compute_product_total' )


    def _compute_product_total(self):
        self.pro_qty = 0
        self.pro_total = 0
        for record in self:
            if record.lines:
                total_qty = 0
                count = 0
                for rec in record.lines:
                    count += 1
                    print("\n\n\n ", count)
                    total_qty += rec.qty
                record.pro_qty = total_qty
                print("\n\n\n pro_total", count)
                record.pro_total = count
                print("\n\n\npro_qty===", record.pro_qty)









