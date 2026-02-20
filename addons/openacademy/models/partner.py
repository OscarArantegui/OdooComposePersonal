# -*- coding: utf-8 -*-
from odoo import models, fields

class Partner(models.Model):
    _inherit = 'res.partner'

    # Campo booleano para marcar si es instructor
    instructor = fields.Boolean("Instructor", default=False)

    # Relación con las sesiones a las que asiste (inverso de attendee_ids en session)
    session_ids = fields.Many2many('openacademy.session', string="Sesiones como asistente", readonly=True)