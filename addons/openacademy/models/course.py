# -*- coding: utf-8 -*-
from odoo import models, fields

class Course(models.Model):
    _name = 'openacademy.course'
    _description = "Cursos de Open Academy"

    name = fields.Char(string="Título", required=True)
    description = fields.Text(string="Descripción")
    
