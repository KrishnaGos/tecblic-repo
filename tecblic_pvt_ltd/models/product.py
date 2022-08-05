# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models, _


class UpdatePricelist(models.Model):
    _inherit = 'product.template'

    mmname = fields.Binary(string="Attach")

    def update_price_product(self):
        purchase_ids = self.ids
        context = {}
        print("*********************************************************************call wizard fucntion")
        wizard_form = self.env.ref('tecblic_pvt_ltd.product_tb_generate_action', False)
        purchase_ids = self.env.context.get('active_ids', [])
        products = self.env['product.template'].browse(purchase_ids)
        context = dict(self._context)
        return {

            'type': 'ir.actions.act_window',

            'view_type': 'form',

            'view_mode': 'form',

            'res_model': 'product.wizard',

            'target': 'new',

            'context': context
        }
