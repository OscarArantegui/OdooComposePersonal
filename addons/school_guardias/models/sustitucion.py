from odoo import models, fields, api
from odoo.exceptions import ValidationError

class SchoolSubstitution(models.Model):
    _name = 'school.substitution'
    _description = 'Gestión de Guardias'

    group_id = fields.Many2one('school.group', string='Grupo', required=True)
    classroom_id = fields.Many2one('school.classroom', string='Aula', required=True)

    replaced_teacher_id = fields.Many2one('school.teacher', string='Profesor Sustituido', required=True)
    substitute_teacher_id = fields.Many2one('school.teacher', string='Profesor de Guardia', required=False)

    date = fields.Date(string='Fecha', default=fields.Date.today, required=True)

    period_id = fields.Many2one('school.period', string='Periodo', required=True)

    tasks = fields.Text(string='Tareas')
    state = fields.Selection([('draft', 'Pendiente'),('done','Asignada')], default='draft')

    # Comprobamos que no haya una incidencia para el profesor la misma hora
    @api.constrains('replaced_teacher_id','date','period_id')
    def _check_duplicate(self):
        for rec in self:
            weekday_index = str(rec.date.weekday())
            if rec.period_id.day_select != weekday_index:
                raise ValidationError("La fecha no coincide con el día del periodo seleccionado")
            
            if self.search_count([
                ('replaced_teacher_id', '=', rec.replaced_teacher_id.id),
                ('date', '=', rec.date),
                ('period_id', '=', rec.period_id.id),
                ('id', '!=', rec.id)
            ]) > 0:
                raise ValidationError("Ya existe una incidencia para este profesor para esta hora.")
    
    # Lógica de asignación automática
    def action_assign_substitute(self):
        self.ensure_one()
        weekday_index = str(self.date.weekday())

        if int(weekday_index) > 4:
            raise ValidationError("Es fin de semana")
        
        # Buscamos el periodo libre
        valid_periods = self.env['school.period'].search([
            ('day_select', '=', weekday_index),
            ('period_number', '=', self.period_id.period_number),
            ('is_free', '=', True),
            ('schedule_id.teacher_id','!=', self.replaced_teacher_id.id)
        ])

        if not valid_periods:
            raise ValidationError("No hay profesores disponibles para esta hora")
        
        # Seleccionamos candidato
        candidates = valid_periods.mapped('schedule_id.teacher_id')
        best_candidate = candidates.sorted(key=lambda p: p.substitution_count)[0]

        # 1. Guardamos la asignación
        self.write({
            'substitute_teacher_id': best_candidate.id,
            'state': 'done'
        })

        # 2. Enviamos el correo
        if best_candidate.email:
            template = self.env.ref('school_guardias.email_template_guardia')
            
            # Usamos 'email_values' para inyectar el destinatario directamente
            # ignorando lo que diga (o no diga) la plantilla XML.
            values = {
                'email_to': best_candidate.email
            }
            
            template.send_mail(self.id, force_send=True, email_values=values)
            
            print(f"--- CORREO ENVIADO A {best_candidate.name} ({best_candidate.email}) ---")
        else:
            print("--- EL PROFESOR NO TIENE EMAIL ---")