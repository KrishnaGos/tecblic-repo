# -*- coding: utf-8 -*-

from datetime import date, timedelta
from odoo import models, fields


class BdayReminder(models.Model):
    _inherit = 'hr.employee'

    student_name = fields.Char(string='Name of the student', required=False)

    def cron_bday_method(self, cr=None):
        template = self.env.ref('tecblic_pvt_ltd.bday_email_template')
        result = self.env['hr.employee'].search([('birthday', '=', date.today() + timedelta(days=-1))])
        for rec in result:
            if rec and template:
                template.send_mail(rec.id, force_send=True)



