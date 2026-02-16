from odoo import models, fields, api

class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate Property Type'
    name = fields.Char(string='Property Type', required=True)
    property_ids = fields.One2many('estate.property', 'property_type_id', string='Properties')
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id', string='Offers')
    offer_count = fields.Integer(string='Offer Count', compute='_compute_offer_count')
    _unique_type = models.Constraint(
        'unique(name)', 'This property type already exists!'
    )
    sequence = fields.Integer(string='Sequence', default=1, help='Used to order property types in the UI')
    _order = "sequence, name"
    
    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)

    def action_view_offers(self):
        self.ensure_one()
        return {
            'name': 'Offers',
            'type': 'ir.actions.act_window',
            'res_model': 'estate.property.offer',
            'view_mode': 'list,form',
            'domain': [('property_type_id', '=', self.id)],
        }   
