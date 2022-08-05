# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Tecblic Private Limited',
    'version': '1.0',
    'summary': 'office internal machinery',
    'sequence': -100,
    'category': 'Hidden',
    'description': """
    This module contains all the common features of Tecnos Office Management and eCommerce.
    """,
    'depends': ['product', 'base','mail','contacts','board','hr','sale','hr_holidays', 'website_sale', 'purchase'],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'data/department_seq.xml',
        'data/cron_bday.xml',
        'data/email_bday.xml',
        'data/Coupon_master.xml',
        'data/download_xlxs.xml',
        'data/sequences.xml',
        'report/report.xml',
        'report/tecblic_report_template.xml',
        'report/vendor.xml',
        'report/vendor_template.xml',
        'wizard/product_wiz.xml',
        'wizard/sale_coupon.xml',
        'wizard/res_partner.xml',
        'views/customer.xml',
        'views/driver.xml',
        'views/dashboard.xml',
        'views/res_partner.xml',
        'views/Coupon_master_data.xml',
        'views/sale_order.xml',
        'views/setting.xml',
        'views/system_parameter.xml',
        'views/department.xml',

    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}

