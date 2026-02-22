from odoo.tests.common import TransactionCase

class TestHospitalAppointment(TransactionCase):

    def setUp(self):
        # super() inicializa el entorno de pruebas de Odoo
        super(TestHospitalAppointment, self).setUp()
        
        # 1. PREPARACIÓN DE DATOS (Se ejecuta antes de cada test)
        # self.env nos permite acceder a la base de datos simulada
        self.doctor_test = self.env['hospital.doctor'].create({
            'name': 'Dr. Gregory House',
            'specialty': 'Diagnóstico Médico',
            'dni': '12345678A'
        })
        
        self.patient_test = self.env['hospital.patient'].create({
            'name': 'John Doe',
            'blood_type': 'O-',
            'dni': '87654321B'
        })

    def test_appointment_confirmation(self):
        # Todo método que empiece por la palabra "test_" será ejecutado por Odoo.
        
        # 2. CREAMOS LA CITA
        appointment = self.env['hospital.appointment'].create({
            'patient_id': self.patient_test.id,
            'doctor_id': self.doctor_test.id,
            'date': '2026-10-15 10:00:00'
        })

        # 3. PRIMERA COMPROBACIÓN (Opcional pero da puntos)
        # Comprobamos que al nacer, la cita está en borrador ('draft')
        self.assertEqual(
            appointment.state, 
            'draft', 
            "La cita debería crearse en estado 'Borrador' (draft)."
        )

        # 4. EJECUTAMOS LA LÓGICA DE NEGOCIO (Llamamos al botón)
        appointment.action_confirm()

        # 5. COMPROBACIÓN FINAL (El Assert principal del examen)
        self.assertEqual(
            appointment.state, 
            'confirmed', 
            "El estado de la cita no cambió a 'Confirmada' tras llamar a action_confirm()."
        )