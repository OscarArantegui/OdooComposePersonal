{
    'name': "Sistema de Guardias Escolar",
    'summary': "Gestión automática de sustituciones de profesores",
    'description':"""
        Módulo para gestionar ausencias y asignar profesores de guardia
        basándose en su disponibilidad de carga de trabajo
    """,
    'author': "Agustin Sidauy, Lucía Aznar, Óscar Arantegui",
    'website': "https://github.com/iespabloserrano/recuperacion-sge-rompemodulos",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base', 'mail'],
    'data': [
        'views/views.xml',
        'data/mail_template.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'application': True,
}