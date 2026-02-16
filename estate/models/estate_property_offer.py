from odoo import api, models,fields
from odoo.exceptions import ValidationError
from odoo.orm.domains import timedelta
from odoo.tools import float_compare

class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offer'

    price = fields.Float()
    status = fields.Selection([
        ('accepted', 'Accepted'),
        ('refused', 'Refused'),
    ], copy=False)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute='_compute_date_deadline', inverse='_inverse_date_deadline')
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    property_type_id = fields.Many2one(related='property_id.property_type_id', store=True)

    _check_price = models.Constraint('CHECK(price > 0)', 'Offer price must be a positive number!')
    _order = "price desc"

    @api.depends('validity')
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = fields.Date.today() + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - fields.Date.today()).days

    @api.constrains('price')
    def _check_offer_price(self):
        for record in self:
            expected_price = record.property_id.expected_price
            if float_compare(record.price, expected_price * 0.9, precision_digits=2) == -1:
                raise ValidationError("The offer price must be at least 90% of the expected price.")
            
    def accept_offer(self):
        for record in self:
            if record.property_id.status in ['sold', 'canceled', 'offer_accepted']:
                raise ValidationError("You cannot accept an offer for a sold or canceled property.")
            record.status = 'accepted'
            record.property_id.status = 'offer_accepted'
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id
        
    def refuse_offer(self):
        for record in self:
            record.status = 'refused'

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            property_id = vals.get("property_id")
            price = vals.get("price")

            # Safety: if missing, let Odoo required fields handle it
            if not property_id or price is None:
                continue

            prop = self.env["estate.property"].browse(property_id)

            best_offer = max(prop.offer_ids.mapped("price") or [0.0])

            # block if new offer is lower than best
            if float_compare(price, best_offer, precision_digits=2) == -1 or float_compare(price, best_offer, precision_digits=2) == 0:
                raise ValidationError("The offer price must be higher than the current best offer.")
            if prop.status == 'new':
                prop.status = 'offer_received'
            return super().create(vals_list)
                
        
        
    

