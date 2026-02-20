from odoo import models, fields

class SchoolGroup(models.Model):
    _name = 'school.group'
    _description = 'Grupo de alumnos'

    name = fields.Char(string='Nombre del Grupo', required=True)
    student_count = fields.Integer(string= 'Numero de alumnos')