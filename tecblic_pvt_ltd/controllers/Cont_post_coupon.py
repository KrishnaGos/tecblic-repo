# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http
from odoo.http import request
import json


class CouponMasterApi(http.Controller):

    @http.route('/api/create_coupon_master', type='json', auth='public', website=True, methods=['POST'])
    def get_coupon_details(self, **kwargs):
        lst_coupons = []
        existing_couponse = []
        response = {}
        for rec in kwargs.get("coupon_data"):
            coupon_sudo = request.env['coupon.master'].sudo().search([('coupon_code', '=', rec.get('coupon_code'))])
            if coupon_sudo:
                existing_couponse.append(coupon_sudo.id)
            else:
                coupon = request.env['coupon.master'].sudo().create({
                    "coupon_code": rec.get("coupon_code"),
                    "typee": rec.get("typee"),
                    "usage_limit": rec.get("usage_limit"),
                    "status": rec.get("status"),
                    "expirty": rec.get("expirty"),
                    "usage": rec.get("usage"),
                    "discount": rec.get("discount"),
                    "validity": rec.get("validity"),
                    "delivery": rec.get("delivery"),
                    "activation": rec.get("activation"),
                    "click": rec.get("click")
                })
                lst_coupons.append(coupon.id)
        response["Status"] = 200
        response['Existing coupons'] = existing_couponse
        response["list of coupons created"] = lst_coupons
        cop = json.dumps(response)
        return cop
