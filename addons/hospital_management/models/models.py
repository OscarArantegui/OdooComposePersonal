from odoo import models, fields, api

# Modelo Abstracto: No crea tabla en la Base de Datos, sirve para ser heredado.
class HospitalPerson(models.AbstractModel):
    _name = 'hospital.person'
    _description = 'Campos comunes para personas'

    name = fields.Char(string="Nombre Completo", required=True)
    dni = fields.Char(string="DNI / Pasaporte")
    phone = fields.Char(string="Teléfono")

# AQUÍ DEBERÁS CREAR LOS MODELOS hospital.patient Y hospital.doctor
# QUE HEREDEN DE hospital.person
class HospitalPatient(models.Model):
    _name='hospital.patient'
    _description='Paciente'
    _inherit='hospital.person'

    apointment_ids = fields.One2many('hospital.appointment', 'patient_id', string="Citas médicas")
    blood_type = fields.Char(string="Grupo sanguíneo")

class HospitalDoctor(models.Model):
    _name='hospital.doctor'
    _description='Doctor'
    _inherit='hospital.person'

    apointment_ids = fields.One2many('hospital.appointment', 'doctor_id', string="Citas médicas")
    specialty = fields.Char(string="Especialidad")


# Modelo Transaccional
class HospitalAppointment(models.Model):
    _name = 'hospital.appointment'
    _description = 'Cita Médica'

    name = fields.Char(string="Referencia", default="Nueva Cita", readonly=True)
    
    # Estos campos darán error hasta que no crees los modelos arriba
    patient_id = fields.Many2one('hospital.patient', string="Paciente", required=True)
    doctor_id = fields.Many2one('hospital.doctor', string="Médico", required=True)
    
    date = fields.Datetime(string="Fecha y Hora de la Cita", required=True)
    observations = fields.Text(string="Observaciones")
    
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('confirmed', 'Confirmada'),
        ('done', 'Realizada'),
        ('cancelled', 'Cancelada')
    ], string="Estado", default='draft')

    def action_confirm(self):
        for record in self:
            record.state = 'confirmed'