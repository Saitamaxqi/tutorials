from odoo import models, fields

class EstateProperty(models.Model):
    _inherit = "estate.property"
    def set_sold(self):
        invoice_vals = {
            'move_type': 'out_invoice',
            'partner_id': self.buyer_id.id,
            'invoice_line_ids': [
                fields.Command.create({
                    "name": 'Selling Price Commisson',
                    "quantity": 1,
                    "price_unit": self.selling_price * 0.06,
                }),
                fields.Command.create({
                    "name": 'Administrative fees',
                    "quantity": 1,
                    "price_unit": 100.00,
                }),
            ],
        }
        self.env['account.move'].create(invoice_vals)
        return super(EstateProperty, self).set_sold()