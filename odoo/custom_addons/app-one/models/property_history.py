from odoo import models, fields
from odoo.exceptions import ValidationError
import logging



class PropertyHistory(models.Model):
    _name = 'property.history'
    _description = "Property History Record"

    user_id = fields.Many2one('res.users')
    property_id = fields.Many2one('property')
    old_state = fields.Char()
    new_state = fields.Char()
    reason = fields.Char()
