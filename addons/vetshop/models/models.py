
from odoo import models, fields, api
from odoo.exceptions import ValidationError
import random
from datetime import date

# ---------------------------------------------------------
# ENTIDAD 1: SPECIES
# ---------------------------------------------------------
class VetShopSpecies(models.Model):
    _name = 'vetshop.species'
    _description = 'Especie Animal'

    name = fields.Char(string='Nombre Especie', required=True)
    description = fields.Text(string='Descripción')

    # TODO: Escribe aquí la Restricción SQL para que el nombre sea único (_sql_constraints)
    _sql_constraints = [
        ('name_unique', 'unique(name)', 'El nombre de la especie debe ser único.')
    ]

# ---------------------------------------------------------
# ENTIDAD 2: OWNER (Dueño)
# ---------------------------------------------------------
class VetShopOwner(models.Model):
    _name = 'vetshop.owner'
    _description = 'Dueño de Mascota'

    name = fields.Char(string='Nombre', required=True)
    phone = fields.Char(string='Teléfono')
    signup_date = fields.Date(string='Fecha Registro', default=fields.Date.today)
    vip_member = fields.Boolean(string='Miembro VIP')
    
    # TODO: Define la relación One2many con 'vetshop.pet'
    pet_ids = fields.One2many('vetshop.pet', 'owner_id', string='Mascotas')

    # TODO: Escribe la Restricción Python (@api.constrains) para validar que el teléfono tenga 9 dígitos
    @api.constrains('phone')
    def _check_phone(self): 
        for record in self:
            if record.phone and len(record.phone) != 9:
                raise ValidationError('El teléfono debe tener 9 dígitos.')

# ---------------------------------------------------------
# ENTIDAD 3: PRODUCT
# ---------------------------------------------------------
class VetShopProduct(models.Model):
    _name = 'vetshop.product'
    _description = 'Producto Veterinario'

    name = fields.Char(string='Producto', required=True)
    price = fields.Float(string='Precio')
    category = fields.Selection([
        ('toy', 'Juguete'),
        ('food', 'Comida'),
        ('med', 'Medicina')
    ], string='Categoría')
    stock = fields.Integer(string='Stock')

    # TODO: Escribe las Restricciones SQL (_sql_constraints):
    # 1. Stock positivo
    # 2. Precio mayor que 0
    _sql_constraints = [
        ('stock_positive', 'CHECK(stock >= 0)', 'El stock debe ser un número positivo.'),
        ('price_positive', 'CHECK(price > 0)', 'El precio debe ser mayor que 0.')
    ]

# ---------------------------------------------------------
# ENTIDAD 4: PET (Mascota)
# ---------------------------------------------------------
class VetShopPet(models.Model):
    _name = 'vetshop.pet'
    _description = 'Mascota'

    name = fields.Char(string='Nombre', required=True)
    birth_date = fields.Date(string='Fecha Nacimiento')
    weight = fields.Float(string='Peso (kg)')
    
    # TODO: Modifica este campo para añadir un default que genere un número aleatorio
    chip_code = fields.Char(string='Código Chip',default=lambda self: str(random.randint(100000, 999999))) 

    # TODO: Define la relación Many2one con 'vetshop.owner'
    owner_id = fields.Many2one('vetshop.owner', string='Dueño')

    # TODO: Define la relación Many2one con 'vetshop.species'
    species_id = fields.Many2one('vetshop.species', string='Especie')

    # TODO: Define el campo calculado 'age' (Integer)
    age = fields.Integer(string='Edad (años)', compute='_compute_age')

    # TODO: Escribe la función para calcular la edad (@api.depends)
    @api.depends('birth_date')
    def _compute_age(self): 
        for record in self:
            if record.birth_date:
                today = date.today()
                record.age = today.year - record.birth_date.year - ((today.month, today.day) < (record.birth_date.month, record.birth_date.day))
            else:
                record.age = 0


# ---------------------------------------------------------
# ENTIDAD 5: SALE ORDER (Venta/Compra)
# ---------------------------------------------------------
class VetShopSaleOrder(models.Model):
    _name = 'vetshop.sale_order'
    _description = 'Orden de Venta'

    date = fields.Date(string='Fecha', required=True, default=fields.Date.today)
    code = fields.Char(string='Código Referencia', readonly=True, default='NUEVO')
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('confirmed', 'Confirmado')
    ], default='draft', string='Estado')

    # TODO: Define la relación Many2one con 'vetshop.pet'
    pet_id = fields.Many2one('vetshop.pet', string='Mascota')

    # TODO: Define la relación Many2many con 'vetshop.product'
    product_ids = fields.Many2many('vetshop.product', string='Productos')

    # TODO: Define el campo calculado 'total_price' (Float)
    total_price =  fields.Float(string='Precio Total', compute='_compute_total_price')

    # TODO: Escribe la función para sumar los precios de los productos (@api.depends)
    @api.depends('product_ids')
    def _compute_total_price(self): 
        for record in self:
            total = sum(product.price for product in record.product_ids)
            record.total_price = total

    # TODO: Escribe la Restricción Python (@api.constrains) para impedir confirmar si el total es 0
    @api.constrains('state')
    def _check_valid_sale(self): 
        for record in self:
            if record.state == 'confirmed' and record.total_price == 0:
                raise ValidationError('No se puede confirmar una venta con precio total 0.')


# ---------------------------------------------------------
# ENTIDAD 6: APPOINTMENT (Cita)
# ---------------------------------------------------------
class VetShopAppointment(models.Model):
    _name = 'vetshop.appointment'
    _description = 'Cita Médica'

    date_start = fields.Datetime(string='Inicio Cita', required=True)
    date_end = fields.Datetime(string='Fin Cita', required=True)
    doctor_note = fields.Text(string='Notas del Doctor')
    urgency_level = fields.Selection([
        ('low', 'Baja'),
        ('medium', 'Media'),
        ('high', 'Alta')
    ], string='Urgencia')

    # TODO: Define la relación Many2one con 'vetshop.pet'
    pet_id = fields.Many2one('vetshop.pet', string='Mascota')

    # TODO: Escribe la Restricción Python (@api.constrains) para validar que date_end > date_start
    @api.constrains('date_start', 'date_end')
    def _check_dates(self): 
        for record in self:
            if record.date_end <= record.date_start:
                raise ValidationError('La fecha de fin debe ser posterior a la fecha de inicio.')