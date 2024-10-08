from odoo import models, fields, api
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class Property(models.Model):
    _name = 'property'

    name = fields.Char(required=1)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date()
    expected_price = fields.Float()
    selling_price = fields.Float()
    bedrooms = fields.Integer()
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    owner_id = fields.Many2one('owner')
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West'),
    ])

    state = fields.Selection([
        ('draft', 'Draft'),
        ('pending', 'Pending'),
        ('sold', 'Sold'),
    ], default='draft')

    _sql_constraints = [
        ('unique_name', 'unique(name)', 'This name is exist!!')
    ]

    @api.constrains('bedrooms')
    def _check_bedrooms_greater_zero(self):
        for rec in self:
            if rec.bedrooms < 0:
                _logger.info("This is search method")
                raise ValidationError("Please Enter Num of bedrooms")

    def actoin_draft(self):
        for rec in self:
            print("Hello from the \"Draft\" Function!")
            self.state = 'draft'

    def actoin_pending(self):
        for rec in self:
            print("Hello from the \"Pending\" Function!")
            self.state = 'pending'

    def actoin_sold(self):
        for rec in self:
            print("Hello from the \"Sold\" Function!")
            self.state = 'sold'

    @api._model_create_multi
    def create(self, vals_list):
        res = super(Property, self).create(vals_list)
        print("-----This is create method-----")
        return res

    @api.model
    def _search(self, domain, offset=0, limit=None, order=None, access_rights_uid=None):
        res = super(Property, self)._search(domain, offset=0, limit=None, order=None, access_rights_uid=None)
        print("This is search method")
        return res

    def write(self, vals):
        res = super(Property, self).write(vals)
        print("This is Update method")
        return res

    def unlink(self):
        res = super(Property, self).unlink()
        print("-----This is unlink method-----")
        return res
