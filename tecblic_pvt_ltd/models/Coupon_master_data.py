# -*- coding: utf-8 -*-

from datetime import date, timedelta
from odoo import models, fields, _


class CouponMaster(models.Model):
    _name = "coupon.master"
    _description = "Coupon Apply"
    _rec_name = 'coupon_code'

    coupon_code = fields.Char(string='Coupon Code')
    discount = fields.Float(string='Discount')
    typee = fields.Char(string='Type(%/E)')
    validity = fields.Selection(selection=[('per', 'Permanent'), ('tem', 'Temporary')])
    usage_limit = fields.Integer(string='Usage Limit')
    delivery = fields.Selection(string='Free two man Delivery', selection=[('yes', 'Yes'), ('no', 'No')])
    status = fields.Selection(selection=[('active', 'Active'), ('inactive', 'Inactive')])
    activation = fields.Date(string="Activiation Data")
    expirty = fields.Date(string="Expiry Data")
    click = fields.Integer(string='Clicked')
    usage = fields.Integer(string='Usage')

    def name_get(self):
        result = []
        for rec in self:
            name = str(rec.coupon_code) + '-' + str(rec.discount)
            # result.append((rec.id, '%s - %s' % (rec.name)))
            result.append((rec.id, name))
        return result

