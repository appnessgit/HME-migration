# -*- coding: utf-8 -*-
{
    'name': "HME Purchase",

    'summary': """
        Purchase Customization
        """,

    'description': """
        Purchase Customization
    """,

    'author': "Appness",
    'website': "http://www.app-ness.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Custom	',
    'version': '14',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account_accountant', 'account', 'contacts', 'product', 'sale_management', 'stock', 'purchase'],

    # always loaded
    'data': [
        'data/terms_of_delivery_data.xml',
        # 'security/groups_hme.xml',
        # 'security/security.xml',
        'data/customer_type_data.xml',
        'views/product.xml',
        'views/res_partner.xml',
        'views/purchase_order.xml',
        'security/security_groups.xml',
        'security/ir.model.access.csv',


    ],

    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
