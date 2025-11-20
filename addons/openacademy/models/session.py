# -*- coding: utf-8 -*-
from odoo import models, fields, api

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
    # 1. Instructor: Relación con Contactos (res.partner)
    instructor_id = fields.Many2one('res.partner', string="Instructor")

    # 2. Curso:
    # ondelete='cascade': Si borras el curso, se borran las sesiones automáticamente
    course_id = fields.Many2one('openacademy.course', ondelete='cascade', string="Course", required=True)

    # 3. Asistentes: Relación Many2many con Contactos (res.partner)
    attendee_ids = fields.Many2many('res.partner', string="Attendees")