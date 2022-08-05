# -*- coding: utf-8 -*-

from odoo import models, fields, _
from odoo.exceptions import ValidationError, UserError


class HrLeave(models.Model):
    _inherit = "hr.leave"

    def action_approve(self):
        print("Approve ==========================")
        # print("self =======================", self.employee_id.address_id.industry_id.full_name)
        # uper call button call, pure odoo mai jo bhi User login hoga vo mai excess kar sakti hu,......,m20 can acess any m20 but only one field in perticular model...,
        # res = super(HrLeave, self).action_approve()
        if self.env.user.name == self.employee_id.parent_id.name:
            if any(holiday.state != 'confirm' for holiday in self):
                raise UserError(_('Time off request must be confirmed ("To Approve") in order to approve it.'))

            current_employee = self.env.user.employee_id
            self.filtered(lambda hol: hol.validation_type == 'both').write(
                {'state': 'validate1', 'first_approver_id': current_employee.id})

            # Post a second message, more verbose than the tracking message
            for holiday in self.filtered(lambda holiday: holiday.employee_id.user_id):
                holiday.message_post(
                    body=_(
                        'Your %(leave_type)s planned on %(date)s has been accepted',
                        leave_type=holiday.holiday_status_id.display_name,
                        date=holiday.date_from
                    ),
                    partner_ids=holiday.employee_id.user_id.partner_id.ids)

            # self.filtered(lambda hol: not hol.validation_type == 'both').action_validate()
            if not self.env.context.get('leave_fast_create'):
                self.activity_update()
            return True
        else:
            raise ValidationError(_('You cannot approve the leave.'))

    def action_validate(self):
        print("Validate =================================")
        res = super(HrLeave, self).action_validate()
        if self.env.user.name == self.employee_id.coach_id.name:
            return res
        else:
            raise ValidationError(_('You cannot Validate the leave.'))