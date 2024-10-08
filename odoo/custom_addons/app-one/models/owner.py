from odoo import models,fields,api


class Owner(models.Model):
    _name = 'owner'
    name = fields.Char(required = 1)
    address = fields.Char()
    phone = fields.Char()
    property_ids = fields.One2many('property' , 'owner_id')


