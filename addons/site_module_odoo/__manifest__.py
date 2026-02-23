{
    'name': 'Site Management',
    'version': '19.0.1.0.0',
    'summary': 'Manage sites and their associated persons',
    'category': 'General',
    'author': 'Custom',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/person_views.xml',
        'views/site_views.xml',
        'views/menu.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
