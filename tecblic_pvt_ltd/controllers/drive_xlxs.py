from odoo import http
from odoo.http import request
from odoo.tools.misc import xlwt
import xlrd
import io
import xlsxwriter
from odoo.tools import pycompat
import requests
from odoo.http import content_disposition
from datetime import date, datetime
from odoo.exceptions import ValidationError, UserError
from odoo import api, fields, models, _


# from pytz import timezone, UTC


class DownloadXLXSDriver(http.Controller):

    @http.route('/excel/download/print_drive_xlxs_report/<string:ids>', type='http', auth='public', csrf=False)
    def xlxs_drive_report_details(self, ids, **kwargs):
        response = request.make_response(
            None,
            headers=[
                ('Content-Type', 'application/vnd.ms-excel'),
                ('content-disposition', content_disposition('emps' + '.xlsx'))
            ]
        )

        def make_multipart(
                self, content_disposition=None, content_type=None, content_location=None
        ):
            self.headers["Content-Disposition"] = content_disposition or u"form-data"
            ...

        output = io.BytesIO()
        workbook = xlsxwriter.Workbook('Example25.xlsx')
        worksheet = workbook.add_worksheet("krishu xlxs sheet")
        columns = ['Sr.No.', 'driver_id', 'First Check In', 'Last Check Out', 'work_hours']
        sr_no = 1
        rows = []
        order_ids = sorted([int(id) for id in ids.split(',')])
        driver_id = request.env['diver.login'].browse(order_ids).mapped('driver_id')
        # print("\n\n\n====driver_id===", driver_id)name 2 hai

        for driver in driver_id:
            driver_login_ids = request.env['diver.login'].search([('driver_id', '=', driver.id)])
            # print("\n\n\n\====driver_login_ids===", driver_login_ids) same name ?

            if driver_login_ids:
                check_in_datetimes = request.env['diver.login'].browse(driver_login_ids.ids).mapped('check_in')
                # [datetime.datetime(20...19, 1, 15), datetime.datetime(20...19, 0, 25)]    0.....1
                chek_in_strings = [d.strftime('%m-%d-%Y') for d in check_in_datetimes]
                # ['07-05-2022', '07-05-2022']   0 ...1
                chek_in_dates = list(set(chek_in_strings))  # set dublication remove ....set convert to list
                print("\n\n\n===chek_in_dates===", chek_in_dates)  # ['07-05-2022']

                for date in chek_in_dates:
                    d_date = datetime.strptime(date, "%m-%d-%Y").date()
                    records = driver_login_ids.filtered(
                        lambda
                            l: l.check_in.date() == d_date)  # driver_login_ids:-diver.login(11, 12)  d_date:-datetime.date(2022, 7, 5)
                    print("\n\n\n==records===", records)  # diver.login(11, 12)
                    #         check_out_datetimes = request.env['diver.login'].browse(driver_login_ids).mapped('check_out')
                    #         check_out_strings = [d.strftime('%m-%d-%Y') for d in check_out_datetimes]
                    #         last_sign_out = list(set(check_out_strings))
                    first_sign_in = []
                    last_sign_out = []
                    work_hrs = []
                    f_sign_in = 0
                    l_sign_out = 0
                    for a in records:
                        if a.check_in not in first_sign_in:  # a.check_in:-datetime.datetime(2022, 7, 5, 19, 1, 15)  first_sign_in:-[]
                            first_sign_in.append(
                                a.check_in)  # first_sign_in:-[datetime.datetime(20...19, 1, 15)   a.check_in:-datetime.datetime(2022, 7, 5, 19, 0, 25)
                        if a.check_out not in last_sign_out:  # a.check_out:-datetime.datetime(2022, 7, 6, 5, 1, 15)  last_sign_out:-[]
                            last_sign_out.append(
                                a.check_out)  # last_sign_out:-[datetime.datetime(20... 5, 1, 15), datetime.datetime(20... 5, 2, 25)]
                            work_hrs.append(
                                a.work_hours)  # work_hrs:-[10.0, 10.033333333333333]   a.work_hours:-10.033333333333333
                        if first_sign_in == last_sign_out:
                            raise ValidationError(_('The same date is not allowed'))
                    f_sign_in = min(first_sign_in)
                    # f_sign_in
                    # datetime.datetime(2022, 7, 5, 19, 0, 25)
                    # first_sign_in
                    # [datetime.datetime(20...19, 1, 15), datetime.datetime(20...19, 0, 25)]
                    # min(first_sign_in)
                    # datetime.datetime(2022, 7, 5, 19, 0, 25)
                    l_sign_out = max(last_sign_out)
                    # l_sign_out
                    # datetime.datetime(2022, 7, 6, 5, 2, 25)
                    # last_sign_out
                    # [datetime.datetime(20... 5, 1, 15), datetime.datetime(20...
                    # 5, 2, 25)]
                    # max(last_sign_out)
                    # datetime.datetime(2022, 7, 6, 5, 2, 25)

                    row = []
                    row.append(sr_no)
                    row.append(driver.name)
                    row.append(f_sign_in)
                    row.append(l_sign_out)
                    row.append(sum(work_hrs))
                    rows.append(row)
                    sr_no += 1
                    print("\n\n\n===sr_no===", sr_no)
        if rows:
            fp = io.BytesIO()
            writer = pycompat.csv_writer(fp, quoting=0)
            writer.writerow(columns)
            for row in rows:
                # row
                # [2, 'Marc Demo', datetime.datetime(20...19, 6, 58), datetime.datetime(20...
                # 5, 6, 58), 10.0, 3, 'Marc Demo', datetime.datetime(20..
                # .19, 6, 58), 10.0]
                # rows
                # [[1, 'Joel Willis', datetime.datetime(20...19, 0, 25), datetime.datetime(20...
                # 5, 2, 25), 20.03333333333333], [2, 'Marc Demo', datetime.datetime(20...19, 6, 58), datetime.datetime(
                #     20...
                # 5, 6, 58), 10.0, 3, 'Marc Demo', datetime.datetime(20..
                # .19, 6, 58), 10.0]]
                writer.writerow(row)
            max_pro_csv = fp.getvalue()  # max_pro_csv b'Sr.No.,driver_id,First Check In,Last Check Out,work_hours\r\n1,Joel Willis,2022-07-05 19:00:25,2022-07-06 05:02:25,20.03333333333333\r\n2,Marc Demo,2022-07-06 19:06:58,2022-07-07 05:06:58,10.0\r\n'
            workbook.close()
            fp.seek(0)
            response.stream.write(fp.read())
            fp.close()
            return response

    @api.constrains('check_in','check_out')
    def val_date(self):
        for date in self:
            if date.check_in == date.check_out:
                raise ValidationError(_('The same date is not allowed'))
