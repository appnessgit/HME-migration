# -*- coding: utf-8 -*-
{
    'name': "Appness HR: Self Service",
    'summary': """Employee self service""",
    'author': "Appness Technology Co.Ltd.",
    'website': "http://app-ness.com",
    'category': 'hr',
    'version': '14.0.1',
    'sequence': 1,
    'depends': ['calendar', 'portal', 'hr_contract'],
    'price': 120,
    'currency': 'EUR',
    'data': [
        'security/ir.model.access.csv',
        'templates/website_assets.xml',
        'views/dashboard_portal_template.xml',
        'views/res_config_views.xml',
    ],
    'images': [
        'static/description/ss_sc_00.png',
    ]
}
