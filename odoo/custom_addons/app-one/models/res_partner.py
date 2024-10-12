from odoo import models,fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    price = fields.Float(related='property_id.selling_price')
    property_id = fields.Many2one('property')


