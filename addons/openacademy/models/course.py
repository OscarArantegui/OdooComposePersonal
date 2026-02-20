# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

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

    # VALIDACIÓN 1: Comprobar que Nombre y Descripción son diferentes
    @api.constrains('name', 'description')
    def _check_description(self):
        for r in self:
            if r.name == r.description:
                raise ValidationError("El título del curso no puede ser igual a la descripción")

    # VALIDACIÓN 2: Nombre único
    @api.constrains('name')
    def _check_name_unique(self):
        for r in self:
            # Buscamos en la BD si existe otro registro con el mismo nombre y diferente ID
            domain = [('name', '=', r.name), ('id', '!=', r.id)]
            if self.search(domain):
                raise ValidationError("El título del curso debe ser único.")
    
    def copy(self, default=None):
        default = dict(default or {})

        # Buscamos si ya existen copias con este nombre
        copied_count = self.search_count(
            [('name', '=like', _("Copy of {}%").format(self.name))])
        
        if not copied_count:
            new_name = _("Copy of {}").format(self.name)
        else:
            new_name = _("Copy of {} ({})").format(self.name, copied_count)

        default['name'] = new_name
        return super(Course, self).copy(default)