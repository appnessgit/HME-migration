# -*- coding: utf-8 -*-
{
    'name': "Appness HR: Salary Advance - Self Service",
    'summary': """Employee Salart Advance self service """,
    'author': "Appness Technology",
    'website': "http://www.app-ness.com",
    'category': 'hr',
    'version': '14.1.0',
    'sequence': 14,
    'depends': ['hr_portal', 'hr_salary_advance'],
    'data': [
        'security/ir.model.access.csv',
        'views/salary_advance_portal_templates.xml',
    ]
}
