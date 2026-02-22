{
    'name': 'Gestión de Hospital',
    'version': '1.0',
    'summary': 'Módulo para gestionar personal de hospital',
    'description': 'Un módulo de ejercicio para gestionar una hospital básico.',
    'author': 'Oscar Arantegui',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/views.xml',
        'reports/appointments_report.xml'
    ],
    'installable': True,
    'application': True,
}