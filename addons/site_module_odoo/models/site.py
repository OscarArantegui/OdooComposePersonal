from odoo import fields, models


class Site(models.Model):
    _name = 'site.management.site'
    _description = 'Site'
    _order = 'name'

    name = fields.Char(string='Name', required=True)
    code = fields.Char(string='Code', size=10)
    address = fields.Text(string='Address')
    city = fields.Char(string='City')
    country_id = fields.Many2one('res.country', string='Country')
    active = fields.Boolean(string='Active', default=True)
    person_ids = fields.One2many(
        'site.management.person', 'site_id', string='Persons'
    )
    person_count = fields.Integer(
        string='Person Count', compute='_compute_person_count'
    )

    def _compute_person_count(self):
        for site in self:
            site.person_count = len(site.person_ids)
