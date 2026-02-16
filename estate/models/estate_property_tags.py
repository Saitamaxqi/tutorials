from odoo import fields, models

class EstatePropertyTags(models.Model):
    _name = 'estate.property.tags'
    _description = 'Estate Property Tags'

    name = fields.Char(required=True)
    color = fields.Integer(string='Color Index')
    _unique_tag = models.Constraint(
        'unique(name)', 'This tag already exists!'
    )
    _order = "name"