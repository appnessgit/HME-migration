# -*- coding: utf-8 -*-
{
    'name': "Appness HR :Employee Rotation",
    'summary': """Employee Rotation """,
    'description': """Employee Rotation""",
    'author': "Appness Technology",
    'website': "http://www.app-ness.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'HR',
    'version': '14.0.1',
    'sequence': 5,

    # any module necessary for this one to work correctly
    'depends': ['base','hr','hr_contract'],

    # always loaded
    'data': [
      'security/ir.model.access.csv',
      'views/employee_rotation.xml',
      'data/mail_data.xml',
    #    'security/record_rule.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
   #     'demo.xml',
    ],
}