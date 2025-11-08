# -*- coding: utf-8 -*-
{
    'name': 'Charity Dashboard',
    'summary': 'Transparent donations, requests, and distributions for CSR/charities',
    'version': '1.0.0',
    'category': 'Productivity',
    'author': 'Hackathon Team',
    'license': 'LGPL-3',
    'website': 'https://example.com',
    'depends': [],                     # Odoo 19 core only
    'data': [
        'security/ir.model.access.csv',
        'views/project_views.xml',
        'views/donor_views.xml',
        'views/donation_views.xml',
        'views/request_views.xml',
        'views/distribution_views.xml',
        'views/menu.xml',
    ],
    'demo': [
        'data/demo_data.xml',
    ],
    'application': True,
    'installable': True,
}
