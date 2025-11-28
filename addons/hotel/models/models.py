from odoo import models, fields, api
from odoo.exceptions import ValidationError
import random
from datetime import date, timedelta

# ---------------------------------------------------------
# 1. TIPO DE HABITACIÓN
# ---------------------------------------------------------
class HotelRoomType(models.Model):
    _name = 'hotel.room_type'
    _description = 'Tipo de Habitación'

    name = fields.Char(string='Tipo', required=True)
    daily_price = fields.Float(string='Precio por Noche')

    # TODO: SQL Constraint (Precio > 0)
    _sql_constraints = [
        ('daily_price_positive', 'CHECK(daily_price > 0)', 'El precio por noche debe ser positivo.')
    ]



# ---------------------------------------------------------
# 2. HABITACIÓN
# ---------------------------------------------------------
class HotelRoom(models.Model):
    _name = 'hotel.room'
    _description = 'Habitación'

    number = fields.Char(string='Número Habitación', required=True)
    floor = fields.Integer(string='Planta')
    is_clean = fields.Boolean(string='Está Limpia', default=True)

    # TODO: Relación Many2one con 'hotel.room_type'
    type_id = fields.Many2one('hotel.room_type', string='Tipo de Habitación', required=True)

    # TODO: SQL Constraint (Número único)
    _sql_constraints =[
        ('number_unique', 'unique(number)', 'El número de habitación debe ser único.')
    ]

# ---------------------------------------------------------
# 3. HUÉSPED
# ---------------------------------------------------------
class HotelGuest(models.Model):
    _name = 'hotel.guest'
    _description = 'Huésped'

    name = fields.Char(string='Nombre Completo', required=True)
    passport_id = fields.Char(string='Pasaporte/DNI')
    country = fields.Char(string='País Origen')

    # TODO: Python Constrains (Pasaporte >= 8 caracteres)
    @api.constrains('passport_id')
    def _check_passport(self):
        for record in self:
            if record.passport_id and len(record.passport_id) < 8:
                raise ValidationError("El número de pasaporte/DNI debe tener al menos 8 caracteres.")


# ---------------------------------------------------------
# 4. SERVICIO EXTRA
# ---------------------------------------------------------
class HotelService(models.Model):
    _name = 'hotel.service'
    _description = 'Servicio Extra'

    name = fields.Char(string='Servicio', required=True)
    cost = fields.Float(string='Coste')
    is_available = fields.Boolean(string='Disponible', default=True)


# ---------------------------------------------------------
# 5. RESERVA (BOOKING)
# ---------------------------------------------------------
class HotelBooking(models.Model):
    _name = 'hotel.booking'
    _description = 'Reserva de Hotel'

    # TODO: Default con Lambda para generar código (Ej. "RES-" + random)
    booking_code = fields.Char(string='Ref. Reserva', readonly=True)
    
    check_in = fields.Date(string='Fecha Entrada', required=True, default=fields.Date.today)
    check_out = fields.Date(string='Fecha Salida', required=True)
    
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('confirm', 'Confirmada'),
        ('cancel', 'Cancelada')
    ], string='Estado', default='draft')

    # TODO: Relación Many2one con Guest
    guest_id = fields.Many2one('hotel.guest', string='Huésped', required=True)

    # TODO: Relación Many2one con Room
    room_id = fields.Many2one('hotel.room',string='Habitación', required=True)

    # TODO: Relación Many2many con Service
    service_ids = fields.Many2many('hotel.service', string='Servicios', required=True)

    # TODO: Campo calculado total_price
    total_price = fields.Float(string='Precio Total', compute='_compute_total_price', store=True)


    # TODO: Función Compute para calcular precio (Días * PrecioHabitación + Servicios)
    @api.depends('check_in','check_out', 'room_id', 'service_ids')
    def _compute_total_price(self):
        for record in self:
            days = (record.check_out - record.check_in).days
            record.total_price = days * record.room_id.type_id.daily_price + sum(service.cost for service in record.service_ids)

    # TODO: Python Constrains (Check out > Check in)
    # def _check_dates(self): ...
    @api.constrains('check_in', 'check_out')
    def _check_dates(self):
        for record in self:
            if record.check_out < record.check_in:
                raise ValidationError("La fecha de salida no puede ser anterior a la fecha de entrada.")


# ---------------------------------------------------------
# 6. MANTENIMIENTO
# ---------------------------------------------------------
class HotelMaintenance(models.Model):
    _name = 'hotel.maintenance'
    _description = 'Mantenimiento'

    date = fields.Date(string='Fecha', default=fields.Date.today)
    description = fields.Text(string='Descripción Avería')
    cost = fields.Float(string='Coste Reparación')

    # TODO: Relación Many2one con Room
    room_id = fields.Many2one('hotel.room',string='Habitación', required=True)

    # TODO: Onchange. Si room_id cambia y is_clean es False -> Warning
    @api.onchange('room_id')
    def _onchange_room_warning(self):
        for record in self:
            if record.room_id and not record.room_id.is_clean:
                return {
                    'warning': {
                        'title': "Habitación Sucia",
                        'message': "La habitación seleccionada no está limpia. ¿Desea continuar?"
                    }
                }