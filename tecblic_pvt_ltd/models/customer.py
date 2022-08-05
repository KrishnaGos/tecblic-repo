# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import datetime, date
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError
import base64


class CustomerInfo(models.Model):
    _name = "customer.info.details"
    _description = "Customer Information"

    name = fields.Char(string="Name")
    surname = fields.Char(string="Surname")
    age = fields.Integer(string="Age")
    scheduled_date = fields.Date(string="Scheduled Date")
    appointment_date = fields.Date(string="Appointment Date Started")
    appointment_end_date = fields.Date(string="Appointment End Date")
    amount = fields.Float(string="Total Amount", )
    customer_email = fields.Char(string="Email")
    customer_address = fields.Char(string="Address")
    customer_zip = fields.Char(string="Zip")
    customer_city = fields.Char(string="City")
    customer_state_id = fields.Many2one(string="State", comodel_name='res.country.state')
    customer_country_id = fields.Many2one(string="Country", comodel_name='res.country')
    customer_phone = fields.Char(string="Phone")
    salesperson_id = fields.Many2one('res.users', string="Salesperson")
    image = fields.Binary(string="Image")
    customer_id = fields.Many2one('res.partner', string="Customer")
    customer_sales_id = fields.Many2one('sale.order', string="Customer Sales")
    appointment_count = fields.Integer(string="Appointment Count", compute='_compute_appointment_count')

    status = fields.Selection([('active', 'Active'), ('resigned', 'Resigned')], string="Status", readonly=True)
    coupon_Details = fields.Many2one('coupon.master', string="Coupon Details")

    seq_name = fields.Char(string="Sequence", readonly=True, required=True, copy=False, index=True,
                           default=lambda self: _('New'))

    def _valid_field_parameter(self, field, name):
        # allow tracking on abstract models; see also 'mail.thread'
        return (
                name == 'tracking' and self._abstract
                or super()._valid_field_parameter(field, name)
        )

    def _compute_appointment_count(self):
        for rec in self:
            appointment_count = self.env['customer.info.details'].search_count([('name', '=', rec.id)])
            rec.appointment_count = appointment_count

    def action_appointment_count(self):
        print("\n\n\n\n\n\n\n\function")
    # @api.model
    # def _name_search(self, name='', args=None, operator='ilike', limit=100, name_get_uid=None):
    #     iteams = self.env['crm.team'].search([('name', '=', 'Tecblic')])
    #     if self.user_has_groups('tecblic_pvt_ltd.group_tecblic_pvt_administrator'):
    #         args += [('salesperson_id', '!=', self.env.user.id)]
    #         print("DOmain ============================search readf", args)
    #     return super(CustomerInfo, self)._name_search(name, args, operator=operator, limit=limit,
    #                                                   name_get_uid=name_get_uid)

    @api.model
    def search_read(self, domain, fields=False, offset=0, limit=False, order=None):
        teams = self.env['crm.team'].search([('name', '=', 'Tecblic')])
        if self.user_has_groups('tecblic_pvt_ltd.group_tecblic_pvt_administrator'):
            domain += domain
        if self.user_has_groups('tecblic_pvt_ltd.group_tecblic_Officer'):
            domain += ['|', ('salesperson_id', '=', self.env.user.id),
                       ('salesperson_id', 'in', teams.mapped('member_ids').ids)]
        if self.user_has_groups('tecblic_pvt_ltd.group_tecblic_employees'):
            domain += [('salesperson_id', 'in', teams.mapped('member_ids').ids)]
        return super(CustomerInfo, self).search_read(domain, fields, offset, limit, order)

    def download_xlxs(self):
        orderlist = [str(order.id) for order in self]
        orderlist = (',').join(orderlist)
        print("Type of order list ==========================", type(orderlist))
        # orderlist = []
        # for order in self:
        #     orderlist.append(str(order.id))
        print("##################################", "/excel/download/print_xlxs_report/%s" % (orderlist))
        return {
            'type': 'ir.actions.act_url',
            'url': '/excel/download/print_xlxs_report/%s' % (orderlist),
            # 'url': 'https://mail.google.com',
            'target': 'new',
        }

    # def action_email_leads(self):
    #     print("HHHHHHHHHHHHHHHHHHHHHHHHHHHH")
    #     vals = {
    #         'customer_email': self.customer_email,
    #         'name': self.name,
    #         'age': self.age,
    #     }
    #     # print("##########################################################")
    #     template_id = self.env.ref("tecblic_pvt_ltd.email_template").id
    #     # print("#################################################", template_id)
    #     template = self.env['mail.template'].browse(template_id)
    #     template.with_context(vals).send_mail(self.id, force_send=True)
    #     # print("#################################################", template)
    #     template.send_mail(self.id, force_send=True)

    def action_email_leads(self):
        print("******************************")
        with open("/home/tecblic/Downloads/INV_2022_00005.pdf", "rb") as pdf:
            # print("pdf ==============================", pdf)
            str = base64.b64encode(pdf.read())
            print(str)
        attachment = self.env['ir.attachment'].create({
            'type': 'binary',
            'name': "Invoice",
            'datas': str
        })
        mail_values = {
            'auto_delete': True,
            # 'author_id': self.env.user.partner_id.id,
            'email_from':
                'mailto:mittalnayar.tecblic@gmail.com',
            'email_to': self.customer_email,
            'body_html': ('<p> Dear </p>', self.name),
            'state': 'outgoing',
            'subject': 'MAIL TEMPLATE',
            'attachment_ids': [(4, a.id) for a in attachment],
        }
        mail = self.env['mail.mail'].sudo().create(mail_values)
        mail.send()

    def do_resigned(self):
        for rec in self:
            rec.status = 'resigned'

    @api.constrains('age')
    def val_age(self):
        for rec in self:
            if rec.age <= 18:
                raise ValidationError(_('The age must be above than 18.'))

    @api.model
    def default_get(self, fields):
        res = super(CustomerInfo, self).default_get(fields)
        res['name'] = 'New'
        res['age'] = 19
        res['customer_email'] = 'xyz@gmail.com'
        res['appointment_date'] = date.today()
        res['coupon_Details'] = 29
        return res

    @api.model
    def create(self, vals):

        if vals.get('seq_name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'customer.info.details') or _('New')

        result = super(CustomerInfo, self).create(vals)
        return result


    # @api.model
    # def haho(self, fields):
    #     pass
    # purchase_ids = self.env.context.get('active_ids', [])
    # active_ids = self.env.context.get('active_id')
    # sale_oder_id = self.env['sale.order'].browse(active_ids)
        # res = self._context([])
        # res = self.env._context([])
        # res = self.env.context[customer.info.details]
        # print("#######################################################################", res)
