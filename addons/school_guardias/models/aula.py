
from odoo import models, fields

class SchoolClassroom(models.Model):
    _name = 'school.classroom'
    _description = 'Aula física'

    name = fields.Char(string='Nombre/numero')
    location = fields.Char(string='Edificio/Localizacion')