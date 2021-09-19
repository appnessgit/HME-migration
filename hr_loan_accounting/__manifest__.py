
{
    'name': 'Appness HR: Loan Accounting',
    'summary': 'Appness HR: Loan Accounting',
    'description': """Create accounting entries for loan requests.""",
    'version': '14.0.1',
    'sequence': 10,
    'category': 'HR',
    'author': 'Appness Technology',
    'website': "https://www.appness.net",
    'depends': [
        'base','hr', 'account', 'hr_loan_base',
    ],
    'data': [
        # 'views/hr_loan_config.xml',
        'views/hr_loan_acc.xml',
    ],
    'demo': [],
    'images': [],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
