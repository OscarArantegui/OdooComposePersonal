{
    'name': "Open Academy",
    'version': '1.0',
    'depends': ['base', 'board'],
    'author': "Tu Nombre",
    'category': 'Test',
    'description': """
    Módulo de prueba para el tutorial de Open Academy.
    """,
    # Añadimos nuestro archivo de vistas
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/openacademy.xml',
        'views/session_board.xml',
        'reports.xml',
    ],
    # Añadimos nuestro archivo de demo
    'demo': [
        'demo/demo.xml',
    ],
    'application': True,
    'installable': True,
}
