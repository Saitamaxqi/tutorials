from odoo import api, models, fields
from odoo.exceptions import ValidationError
from datetime import timedelta


class estateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property Model"
    
    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False,default=lambda self: fields.Date.today() + timedelta(days=90))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True,default=0.00,copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West'),
    ])
    active = fields.Boolean(default=True)
    status = fields.Selection(
        [
        ('new', 'New'),
        ('offer_received', 'Offer Received'),
        ('offer_accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('canceled', 'Canceled'),
    ],
    default='new',required=True
    )
    total_area = fields.Float(compute='_compute_total_area')
    best_offer = fields.Float(compute='_compute_best_offer')
    property_type_id = fields.Many2one('estate.property.type', string='Property Type')
    buyer_id = fields.Many2one('res.partner', string='Buyer', copy=False)
    salesperson_id = fields.Many2one('res.users', string='Salesperson', default=lambda self: self.env.user.id)
    tags_ids = fields.Many2many('estate.property.tags', string='Tags')
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offers')
    
    _check_expected_price = models.Constraint(
        'CHECK(expected_price >= 0)',
        'Expected price must be a positive number!'
    )
    _check_selling_price = models.Constraint(
        'CHECK(selling_price >= 0)',
        'Selling price must be a positive number!'
    )
    _order = "id desc"

    def unlink(self):
        self.ondelete()
    def ondelete(self):
        for record in self:
            if record.status not in ['new', 'canceled']:
                raise ValidationError("You cannot delete a property that is not new or canceled.")
            record.delete_offer()
        return super().unlink()
    def delete_offer(self):
        for record in self:
            if record.offer_ids:
                record.offer_ids.unlink()
    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_offer(self):
        for record in self:
            if record.offer_ids:
                record.best_offer = max(record.offer_ids.mapped('price'))
            else:
                record.best_offer = 0.00

    @api.onchange('garden')
    def _onchange_garden(self):
            if not self.garden:
                self.garden_area = 0
                self.garden_orientation = False
            else:
                self.garden_area = 10
                self.garden_orientation = 'north'

    def set_sold(self):
        for record in self:
            if record.status == 'offer_accepted':
                record.status = 'sold'
            else:
                raise ValidationError("Only properties with an accepted offer can be marked as sold.")
            
    def set_canceled(self):
        for record in self:
            if record.status not in ['sold', 'canceled']:
                record.status = 'canceled'
            else:
                raise ValidationError("Sold or already canceled properties cannot be canceled.")
            
    