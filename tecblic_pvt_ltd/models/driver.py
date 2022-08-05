# -*- coding: utf-8 -*-

from datetime import date, timedelta
from odoo import api, fields, models, _


class DriverLogin(models.Model):
    _name = "diver.login"
    _description = "Driver Login Device"
    _order = "check_in desc"
    _rec_name = 'driver_id'

    driver_id = fields.Many2one('res.users', string="Driver", index=True)
    check_in = fields.Datetime(string="Check In", default=fields.Datetime.now, required=True)
    check_out = fields.Datetime(string="Check Out")
    work_hours = fields.Float(string="Work Hours", compute='_compute_work_hours', store=True, readonly=True)

    @api.depends('check_in', 'check_out')
    def _compute_work_hours(self):
        for drive in self:
            if drive.check_out and drive.check_in:
                print("#############")
                delta = drive.check_out - drive.check_in
                drive.work_hours = delta.total_seconds() / 3600.0
            else:
                drive.work_hours = False

    def get_first_check_in_time(self):
        pass
        # res = super(DriverLogin, self).get_first_check_in_time()
        # 5/0
        # return res

        # print("#################################", res)
        # for emp in self:
        #     attn_ids = self.env['diver.login'].search([('driver_id', '=', emp.id)])
        #     first_sign_in = []
        #     last_sign_out = []
        #     f_sign_in = 0
        #     l_sugn_in = 0
        #     if attn_ids:
        #         for a in attn_ids:
        #             if a.check_in not in first_sign_in:
        #                 first_sign_in.append(a.check_in)
        #             if a.check_out not in last_sign_out:
        #                 last_sign_out.append(a.check_out)
        #             f_sign_in = min(first_sign_in)
        #             l_sugn_in = max(last_sign_out)
        #             retun
        #     else:
        #         emp.first_sign_in = False
        # return res


    def drive_download_xlxs(self):
        drivelist = [str(order.id) for order in self]
        drivelist = (',').join(drivelist)
        print("Type of order list ==========================", type(drivelist))
        # print("##################################", "/excel/download/print_drive_xlxs_report/%s" % (drivelist))
        return {
            'type': 'ir.actions.act_url',
            'url': '/excel/download/print_drive_xlxs_report/%s' % (drivelist),
            'target': 'new',
        }



