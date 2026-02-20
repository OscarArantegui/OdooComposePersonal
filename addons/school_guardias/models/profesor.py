from odoo import models, fields, api
from datetime import date

class SchoolTeacher(models.Model):
    _name = 'school.teacher'
    _description = 'Profesor'

    name = fields.Char(string='Nombre Completo', required=True)
    dni = fields.Char(string='DNI', required=True)
    email = fields.Char(string='Email')
    phone = fields.Char(string='Teléfono')
    birth_date = fields.Date(string='Fecha de Nacimiento')
    active = fields.Boolean(default=True)
    #Campo computado Edad
    age = fields.Integer(string='Edad', compute='_compute_age')


    schedule_id = fields.Many2one('school.schedule', compute='_compute_schedule_id', string='Ver Horario')

    substitution_ids = fields.One2many('school.substitution', 'substitute_teacher_id', string='Guardias')
    #Contador de carga de trabajo
    substitution_count = fields.Integer(string='Contador de guardias', 
                                        compute='_compute_substitution_count', 
                                        store=True)
    @api.depends('birth_date')
    def _compute_age(self):
        today = date.today()
        for rec in self:
            if rec.birth_date:
                rec.age = today.year - rec.birth_date.year - ((today.month, today.day) < (rec.birth_date.month, rec.birth_date.day))
            else:
                rec.age = 0


    #Mostrar el horario del profesor correspondiente
    def _compute_schedule_id(self):
        for rec in self:
            rec.schedule_id = self.env['school.schedule'].search([('teacher_id', '=', rec.id)], limit=1)

    #Realizar el conteo de las sustituciones hechas por el profesor    
    @api.depends('substitution_ids')
    def _compute_substitution_count(self):
        for rec in self:
            rec.substitution_count = len(rec.substitution_ids)