# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import date

from odoo import api, fields, models, _


class ProduceWizard(models.TransientModel):
    _name = "product.wizard"
    _description = "Selected Record Production Line"

    sale_price = fields.Boolean(string="Sale Price  ", active=False)
    cost_price = fields.Boolean(string="Cost Price", active=False)
    percentage = fields.Float(string="Percentage", required=True )

    def _valid_field_parameter(self, field, name):
        return name == 'active' or super()._valid_field_parameter(field, name)

    def update_bulk_prices(self):
        prom = self._context.get('active_ids')
        # print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$", prom) get active id of selected data from form to wizard ....activeid of wizard
        for res in prom:
            mini_rec = self.env['product.template'].browse(res)
            # print("##################################################", mini_rec) active id got from context now it will be browseable id
            total_sale = mini_rec.list_price + (mini_rec.list_price * self.percentage)/100
            total_cost = mini_rec.standard_price + (mini_rec.standard_price * self.percentage)/100
            mini_rec.write({
                'list_price': total_sale if self.sale_price else mini_rec.list_price,
                'standard_price': total_cost if self.cost_price else mini_rec.standard_price,
            })








