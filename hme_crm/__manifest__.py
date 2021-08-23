# -*- coding: utf-8 -*-
{
    'name': "HME Crm",

    'summary': """
       Crm Customization
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
    'depends': ['crm'],

    # always loaded
    'data': [
        # 'security/hme_crmsecurity.xml',
        'security/ir.model.access.csv',
        'views/hme_crm_view.xml',
        # 'security/ir.model.access.csv',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',

    ],
}
