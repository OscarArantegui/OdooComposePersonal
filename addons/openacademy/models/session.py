# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Session(models.Model):
    _name = 'openacademy.session'
    _description = "Open Academy Sessions"

    name = fields.Char(required=True)
    start_date = fields.Date(default=fields.Date.today)
    
    # CORRECCIÓN: Usamos Integer para horas enteras
    duration = fields.Integer(string="Duración (Horas)")
    
    seats = fields.Integer(string="Number of seats")
    active = fields.Boolean(default=True)

    # --- RELACIONES ---

    # Cursos: ondelete='cascade': Si borras el curso, se borran las sesiones automáticamente
    course_id = fields.Many2one('openacademy.course', ondelete='cascade', string="Course", required=True)

    # Asistentes: Relación Many2many con Contactos (res.partner)
    attendee_ids = fields.Many2many('res.partner', string="Attendees")

    # Buscamos instructores (instructor=True) O que tengan una categoría que contenga "Teacher"
    instructor_id = fields.Many2one('res.partner', string="Instructor",
        domain=['|', ('instructor', '=', True),
                     ('category_id.name', 'ilike', "Teacher")])

    # CAMPO CALCULADO NUEVO
    taken_seats = fields.Float(string="Taken seats", compute='_taken_seats')

    @api.depends('seats', 'attendee_ids')
    def _taken_seats(self):
        for r in self:
            if not r.seats:
                r.taken_seats = 0.0
            else:
                r.taken_seats = 100.0 * len(r.attendee_ids) / r.seats
    # VALIDACIÓN: El instructor no puede ser asistente
    @api.constrains('instructor_id', 'attendee_ids')
    def _check_instructor_not_in_attendees(self):
        for r in self:
            if r.instructor_id and r.instructor_id in r.attendee_ids:
                raise ValidationError("Un instructor no puede ser asistente de su propia sesión")