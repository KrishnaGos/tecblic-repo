from odoo import http
from odoo.http import request
from odoo.tools.misc import xlwt
import xlrd
import io
import xlsxwriter
from odoo.tools import pycompat
import requests
from odoo.http import content_disposition

class DownloadXLXS(http.Controller):

    @http.route('/excel/download/print_xlxs_report/<string:ids>', type='http', auth='public', csrf=False)
    def xlxs_report_details(self, ids, **kwargs):
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
        print("\n\n\n==========================================", kwargs)
        workbook = xlsxwriter.Workbook('Example25.xlsx')
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!", workbook)
        worksheet = workbook.add_worksheet("krishu xlxs sheet")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!", worksheet)
        columns = ['Sr.No.', 'name', 'age', 'customer_phone', 'customer_email']
        sr_no = 1
        rows = []
        # order_ids = sorted([int(id)for id in ids.split(',')])
        # 2,3,7,5
        order_ids = sorted([int(id) for id in ids.split(',')])
        print("order_ids =======================", order_ids)
        for order_id in order_ids:
            row = []
            order = request.env['customer.info.details'].browse([order_id]).sudo()
            # # sr_no = 1
            # rows = []
            # row = []
            # order = request.env['customer.info.details'].browse([id]).sudo()
            row.append(sr_no)
            row.append(order.name)
            row.append(order.age)
            row.append(order.customer_phone)
            row.append(order.customer_email)
            rows.append(row)
            sr_no += 1
        fp = io.BytesIO()
        writer = pycompat.csv_writer(fp, quoting=0)
        writer.writerow(columns)
        for row in rows:
            writer.writerow(row)
        max_pro_csv = fp.getvalue()
        workbook.close()
        fp.seek(0)
        response.stream.write(fp.read())
        fp.close()
        return response




