from odoo import models, fields

class Autor(models.Model):
    _name = 'biblioteca.autor'
    _description = 'Autor de libros'

    name = fields.Char(string='Nombre', required=True)
    nacionalidad = fields.Char(string='Nacionalidad')
    fecha_nacimiento = fields.Date(string='Fecha de nacimiento')
    
    # Relación inversa para ver los libros desde el autor
    libro_ids = fields.One2many('biblioteca.libro', 'autor_id', string='Libros')