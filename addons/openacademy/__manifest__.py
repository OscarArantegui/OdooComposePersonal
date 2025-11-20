{
    'name': "Open Academy",
    'version': '1.0',
    'depends': ['base'],
    'author': "Tu Nombre",
    'category': 'Test',
    'description': """
    Módulo de prueba para el tutorial de Open Academy.
    """,
    # Añadimos nuestro archivo de vistas
    'data': [
        'views/openacademy.xml',
    ],
    # Añadimos nuestro archivo de demo
    'demo': [
        'demo/demo.xml',
    ],
    'application': True,
    'installable': True,
}
