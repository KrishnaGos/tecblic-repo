# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'POS Total: items-qty',
    'version': '1.0',
    'summary': 'module internal machinery',
    'sequence': -100,
    'category': 'Productivity',
    'description': """
    This module contains all the common features of Office Management and eCommerce.
    """,
    'depends': ['base', 'sale', 'point_of_sale', 'product'],
    'data': [
         'views/pos_order.xml',
         'views/assets.xml',
         'views/sales.xml',


    ],
    'demo': [],
    'installable': True,
    'application': False,
    'qweb': [
            'static/src/xml/product_total.xml',
            'static/src/xml/pos_receipt.xml',
    ],
    'auto_install': False,
    'application': True,
    'license': 'LGPL-3',

}
