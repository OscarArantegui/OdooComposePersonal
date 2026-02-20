from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Prestamo(models.Model):
    _name = 'biblioteca.prestamo'
    _description = 'Préstamo de un libro'
    _rec_name = 'libro_id' # Para que el título del registro sea el libro

    libro_id = fields.Many2one('biblioteca.libro', string='Libro', required=True)
    nombre_lector = fields.Char(string='Nombre del lector', required=True)
    fecha_prestamo = fields.Date(string='Fecha de préstamo', default=fields.Date.context_today, required=True)
    fecha_devolucion = fields.Date(string='Fecha de devolución')
    
    # Campo calculado
    dias_prestamo = fields.Integer(string='Días de préstamo', compute='_compute_dias_prestamo')
    
    # Estado para el botón de "Marcar como devuelto"
    estado = fields.Selection([
        ('prestado', 'Prestado'),
        ('devuelto', 'Devuelto')
    ], string='Estado', default='prestado')

    @api.depends('fecha_prestamo', 'fecha_devolucion')
    def _compute_dias_prestamo(self):
        for record in self:
            if record.fecha_prestamo and record.fecha_devolucion:
                delta = record.fecha_devolucion - record.fecha_prestamo
                record.dias_prestamo = delta.days
            else:
                record.dias_prestamo = 0

    @api.constrains('fecha_prestamo', 'fecha_devolucion')
    def _check_fechas(self):
        for record in self:
            if record.fecha_devolucion and record.fecha_prestamo > record.fecha_devolucion:
                raise ValidationError("La fecha de devolución no puede ser anterior a la fecha de préstamo.")

    def action_marcar_devuelto(self):
        for record in self:
            record.estado = 'devuelto'
            if not record.fecha_devolucion:
                record.fecha_devolucion = fields.Date.today()