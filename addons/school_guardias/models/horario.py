from odoo import models, fields, api

class SchoolSchedule(models.Model):
    _name = "school.schedule"
    _description = "Horario Semanal del Profesor"
    _rec_name = "teacher_id"

    teacher_id = fields.Many2one('school.teacher', string='Profesor', required=True, ondelete='cascade')
    period_ids = fields.One2many('school.period', 'schedule_id', string='Periodos')

    _sql_constraints = [
        ('teacher_id_uniq','unique(teacher_id)', 'Este profesor ya tiene un horario asignado.')
    ]

class SchoolPeriod(models.Model):
    _name = "school.period"
    _description = "Franja Horaria"
    _order = "day_select, period_number"

    schedule_id = fields.Many2one('school.schedule', string='Horario', required=True, ondelete='cascade')

    name = fields.Char(string='Periodo', compute='_compute_name', store=True)

    day_select = fields.Selection([
        ('0', 'Lunes'), ('1', 'Martes'), ('2', 'Miércoles'),
        ('3', 'Jueves'), ('4', 'Viernes')
    ], string='Día', required=True)

    period_number = fields.Selection([
        ('1', '1ª Hora'), ('2', '2ª Hora'), ('3', '3ª Hora'),
        ('4', '4ª Hora'), ('5', '5ª Hora'), ('6', '6ª Hora'),
        ('7', '7ª Hora')
    ], string='Hora', required=True)

    is_free = fields.Boolean(string='Hora libre / Guardia', default=False)

    @api.depends('day_select', 'period_number', 'schedule_id.teacher_id')
    def _compute_name(self):
        days = {
            '0': 'Lunes', '1': 'Martes', '2': 'Miércoles',
            '3': 'Jueves', '4': 'Viernes'
        }
        periods = {
            '1': '1ª Hora', '2': '2ª Hora', '3': '3ª Hora',
            '4': '4ª Hora', '5': '5ª Hora', '6': '6ª Hora', '7': '7ª Hora'
        }
        for rec in self:
            if rec.day_select and rec.period_number:
                d = days.get(rec.day_select, '')
                p = periods.get(rec.period_number, '')
                # Obtenemos nombre del profe
                teacher_name = rec.schedule_id.teacher_id.name if rec.schedule_id.teacher_id else "N/A"
                rec.name = f"{teacher_name} -> {d} - {p}"
            else:
                rec.name = "Periodo sin definir"

    _sql_constraints = [
        ('unique_period_per_schedule','unique(schedule_id, day_select, period_number)', 
         'No puedes repetir el mismo dia y hora en el mismo horario.')
    ]