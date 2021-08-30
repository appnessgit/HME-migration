# -*- coding: utf-8 -*-
{
    'name': "Appness HR: Payslip - Self Service",

    'summary': """Employee payslip self service """,
    'author': "Appness Technology Co.Ltd.",
    'website': "http://www.app-ness.com",
    'category': 'hr',
    'version': '14.0.1',
    'sequence': 24,
    'depends': ['hr_portal', 'hr_payroll'],
    'data': [
        'security/ir.model.access.csv',
        'views/payslip_portal_templates.xml',
    ]
}
