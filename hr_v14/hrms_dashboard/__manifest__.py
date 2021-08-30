# -*- coding: utf-8 -*-
{
    'name': "Appness HR: HR Dashboard",
    'summary': """Appness HR: HR Dashboard""",
    'description': """Appness HR: HR Dashboard""",
    'version': '13.0.1.0.0',
    'category': 'HR',
    'version': '13.0.1.0.0',
    'author': 'Appness Technology',
    'website': "https://www.appness.net",
    'depends': ['hr', 'hr_holidays', 'hr_payroll', 'hr_recruitment', 'hr_resignation','hr_appraisal','hr_loan_base','hr_overtime'],
    'external_dependencies': {'python': ['pandas'],},
    'data': [
        'security/ir.model.access.csv',
        'report/broadfactor.xml',
        'views/dashboard_views.xml',
    ],
    'qweb': ["static/src/xml/hrms_dashboard.xml"],
    'images': ["static/description/banner.gif"],
    'license': "AGPL-3",
    'installable': True,
    'application': True,
}
