{
    'name': 'Gestión de Biblioteca',
    'version': '1.0',
    'summary': 'Módulo para gestionar libros, autores y préstamos',
    'description': 'Un módulo de ejercicio para gestionar una biblioteca básica.',
    'author': 'Tu Nombre',
    'depends': ['base'],
    'data': [
        'views/autor_views.xml',
        'views/libro_views.xml',
        'views/prestamo_views.xml',
        'views/menu.xml',
    ],
    'installable': True,
    'application': True,
}