from odoo import fields, models


class Person(models.Model):
    _name = 'site.management.person'
    _description = 'Person'
    _order = 'name'

    name = fields.Char(string='Name', required=True)
    height = fields.Float(string='Height (cm)')
    weight = fields.Float(string='Weight (kg)')
    phone = fields.Char(string='Phone')
    birth_date = fields.Date(string='Birth Date')
    active = fields.Boolean(string='Active', default=True)
    site_id = fields.Many2one(
        'site.management.site', string='Site', ondelete='restrict'
    )
    notes = fields.Text(string='Notes')
