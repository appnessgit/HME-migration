# -*- coding: utf-8 -*-
{
    'name': "Appness HR: Expenses - Self Service",
    'summary': """
         Employee expenses self service """,
    'author': "Appness Technology",
    'website': "http://www.app-ness.com",
    'category': 'hr',
    'version': '14.0.1',
    'sequence': 23,
    'depends': ['hr_portal', 'hr_expense'],
    'data': [
        'security/ir.model.access.csv',
        'views/expense_portal_templates.xml',
    ]
}
