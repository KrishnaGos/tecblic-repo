# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class VenderReport(models.Model):
    _inherit = 'res.partner'


    sales_name = fields.Char(string="Sales Name")