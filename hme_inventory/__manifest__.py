# -*- coding: utf-8 -*-
{
    'name': "HME Inventory",

    'summary': """
       Inventory Customization
        """,

    'description': """
        Crm Customization
    """,

    'author': "Appness",
    'website': "http://www.app-ness.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Custom	',
    'version': '',

    # any module necessary for this one to work correctly
    'depends': ['base','stock','account','contacts','product','hme_purchase'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/stock_picking.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
