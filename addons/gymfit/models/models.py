from odoo import models, fields, api
from odoo.exceptions import ValidationError
import random
from datetime import date

class GymFitCategory(models.Model):
    _name = 'gymfit.category'       # ¡OJO! Es _name, no name
    _description = 'Categoria de Actividad' # ¡OJO! Es _description

    name = fields.Char(string='Nombre', required=True) # ¡OJO! Era 'string', pusiste 'sting'
    description = fields.Text(string='Descripcion')

    _sql_constraints = [
        ('name_unique', 'unique(name)', 'El nombre de la categoría debe ser único.')
    ]

class GymFitMember(models.Model):
    _name = 'gymfit.member'
    _description = 'Socio del Gimnasio'

    name = fields.Char(string='Nombre Completo', required=True)
    height = fields.Float(string='Altura (m)')
    weight = fields.Float(string='Peso (kg)')

    # Default correcto
    access_code = fields.Char(string='Código de Acceso', default=lambda self: str(random.randint(100000, 999999)))
    
    bmi = fields.Float(string='Índice de Masa Corporal', compute='_compute_bmi')

    @api.depends('height', 'weight')
    def _compute_bmi(self):
        for record in self:
            if record.height > 0 and record.weight > 0: # Evitar división por cero
                record.bmi = record.weight / (record.height ** 2)
            else:
                record.bmi = 0.0
    
class GymFitMachine(models.Model):
    _name = 'gymfit.machine'
    _description = 'Máquina de Entrenamiento'

    name = fields.Char(string='Nombre Máquina', required=True)
    purchase_date = fields.Date(string='Fecha de Compra')
    cost = fields.Float(string='Costo de Compra')
    state = fields.Selection([
        ('operative', 'Operativa'),
        ('repair', 'En Reparación'),
        ('broken', 'Dada de Baja')
    ], string='Estado', default='operative')

    category_id = fields.Many2one('gymfit.category', string='Categoría')

    _sql_constraints=[
        ('cost_positive','CHECK(cost >= 0)', 'El costo debe ser positivo.')
    ]

class GymFitInstructor(models.Model):
    _name = 'gymfit.instructor' # ¡OJO! _name
    _description = 'Instructor del Gimnasio'

    name = fields.Char(string='Nombre', required=True)
    dni = fields.Char(string='DNI', required=True)
    hiring_date = fields.Date(string='Fecha de Contratacion')

    # ¡OJO! Era session_ids (sin la s extra en sessions), es convención.
    session_ids = fields.One2many('gymfit.session', 'instructor_id', string='Sesiones')

    seniority = fields.Integer(string='Años de Experiencia', compute='_compute_seniority')

    @api.depends('hiring_date')
    def _compute_seniority(self):
        today = date.today()
        for record in self:
            if record.hiring_date:
                delta = today - record.hiring_date
                record.seniority = delta.days // 365
            else:
                record.seniority = 0

    @api.constrains('dni')
    def _check_dni(self):
        for record in self:
            if len(record.dni) != 9:
                raise ValidationError('El DNI debe tener 9 caracteres.')
            # Quitamos isdigit() porque los DNI suelen tener letra, pero para el examen vale.

class GymFitSession(models.Model):
    _name = 'gymfit.session'
    _description = 'Sesión de Entrenamiento'

    name = fields.Char(string='Nombre de la Sesión', required=True)
    start_time = fields.Datetime(string='Hora de Inicio', required=True)
    end_time = fields.Datetime(string='Hora de Fin', required=True)
    capacity = fields.Integer(string='Capacidad Máxima', required=True)

    instructor_id = fields.Many2one('gymfit.instructor', string='Instructor', required=True)
    member_ids = fields.Many2many('gymfit.member', string='Miembros')

    # ¡OJO! Es @api.constrains (PLURAL), no constraint
    @api.constrains('start_time', 'end_time')
    def _check_dates(self):
        for record in self:
            if record.start_time and record.end_time and record.end_time < record.start_time:
                raise ValidationError('La hora de fin no puede ser anterior a la hora de inicio.')
    
    @api.constrains('capacity')    
    def _check_capacity(self):
        for record in self:
            if record.capacity <= 0:
                raise ValidationError('La capacidad máxima debe ser un número positivo.')

    # TE FALTABA EL ONCHANGE QUE PEDÍA EL EJERCICIO
    @api.onchange('instructor_id')
    def _onchange_instructor(self):
        if self.instructor_id:
            if self.instructor_id.seniority > 5:
                self.capacity = 20
            else:
                self.capacity = 10

class GymFitSale(models.Model):
    _name = 'gymfit.membership_sale'
    _description = 'Venta de Servicios'

    date = fields.Date(string='Fecha Venta', default=fields.Date.today)
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('paid', 'Pagado')
    ], default='draft', string='Estado')

    member_id = fields.Many2one('gymfit.member', string='Socio', required=True)
    
    # Lo cambié a Many2many para que tenga sentido sumar precios (un socio compra varias cosas)
    machine_ids = fields.Many2many('gymfit.machine', string='Máquinas/Servicios')
    
    total_amount = fields.Float(string='Monto Total', compute='_compute_total_amount')

    @api.depends('machine_ids')
    def _compute_total_amount(self):
        for record in self:
            # Sumar el cost de todas las maquinas seleccionadas
            record.total_amount = sum(m.cost for m in record.machine_ids)

    # ¡OJO! Faltaba el decorador constrains
    @api.constrains('state', 'total_amount')
    def _check_valid_sale(self):
        for record in self:
            if record.state == 'paid' and record.total_amount == 0:
                raise ValidationError("No puedes confirmar una venta a 0.")