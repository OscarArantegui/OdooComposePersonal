# -*- coding: utf-8 -*-
from odoo import models, fields

class Course(models.Model):
    _name = 'openacademy.course'
    _description = "Cursos de Open Academy"

    name = fields.Char(string="Título", required=True)
    description = fields.Text(string="Descripción")
    duration = fields.Integer(string="Duration (hours)")
    active = fields.Boolean(string="Active", default=True)

    # --- RELACIONES---
    # 1. Responsable: Un usuario del sistema (res.users)
    responsible_id = fields.Many2one('res.users', ondelete='set null', string="Responsible", index=True)


    # 2. Sesiones: Relación inversa (One2many) hacia el modelo Session
    session_ids = fields.One2many('openacademy.session', 'course_id', string="Sessions")
