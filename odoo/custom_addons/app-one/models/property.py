from odoo import models, fields, api
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class Property(models.Model):
    _name = 'property'
    _description = "Property"
    _inherit = ['mail.thread' , 'mail.activity.mixin']

    active = fields.Boolean()

    name = fields.Char(required=1)
    ref = fields.Char(default='New', readonly=1)
    description = fields.Text(tracking=1)
    postcode = fields.Char(tracking=1)
    date_availability = fields.Date()

    expected_selling_date = fields.Date()
    is_late = fields.Boolean()

    expected_price = fields.Float()
    selling_price = fields.Float()
    diff = fields.Float(compute='_compute_diff')

    bedrooms = fields.Integer()
    line_ids = fields.One2many('property.line', 'property_id')

    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    owner_id = fields.Many2one('owner')
    owner_address = fields.Char(related='owner_id.address')
    owner_phone = fields.Char(related='owner_id.phone')
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
        ('closed', 'Closed'),
    ], default='draft')

    _sql_constraints = [
        ('unique_name', 'unique(name)', 'This name is exist!!')
    ]


    # @api.one
    # def open_owner_record(self):
    #     # owner_id = self.owner_id.id
    #     # action = self.env['ir.actions.actions']._for_xml_id('app-one.owner_action')
    #     # action['context'] = {'default_owner_id': owner_id}
    #     # return action
    #     print("hello")

    def create_history_property_record(self , old_state , new_state , reason):
        for rec in self:
            rec.env['property.history'].create({
                'user_id' : rec.env.uid,
                'property_id' : rec.id,
                'old_state' : old_state,
                'new_state' : new_state,
                'reason' : reason or "",
            })

    def check_expected_selling_date(self):
        property_ids = self.search([])
        for rec in property_ids:
            if rec.expected_selling_date and rec.expected_selling_date < fields.date.today():
                rec.is_late = True
        print(property_ids)
        print("Hello from check_expected_selling_date !!!!!!!!!!!")

    @api.constrains('bedrooms')
    def _check_bedrooms_greater_zero(self):
        for rec in self:
            if rec.bedrooms < 0:
                _logger.info("This is search method")
                raise ValidationError("Please Enter Num of bedrooms")

    @api.depends('expected_price', 'selling_price')
    def _compute_diff(self):
        for rec in self:
            self.diff = self.expected_price - self.selling_price

    @api.onchange('expected_price')
    def onchange_expected_price_diff(self):
        for rec in self:
            print("Hello from Onchange Function")
            if (rec.expected_price < rec.selling_price):
                return {
                    'warning': {
                        'title': 'warning',
                        'message': 'negative message',
                        'type': 'notification'
                    }
                }


    def actoin_draft(self):
        for rec in self:
            rec.create_history_property_record(rec.state , 'draft', "")
            print("Hello from the \"Draft\" Function!")
            self.state = 'draft'

    def actoin_pending(self):
        for rec in self:
            rec.create_history_property_record(rec.state , 'pending' , "")
            print("Hello from the \"Pending\" Function!")
            self.state = 'pending'

    def actoin_sold(self):
        for rec in self:
            rec.create_history_property_record(rec.state , 'sold', "")
            print("Hello from the \"Sold\" Function!")
            self.state = 'sold'

    def actoin_closed(self):
        for rec in self:
            rec.create_history_property_record(rec.state , 'closed', "")
            print("Hello from the \"Closed\" Function!")
            self.state = 'closed'

    def actoin_open_closed_wizard(self):
        action = self.env['ir.actions.actions']._for_xml_id('app-one.property_change_state_action')
        action['context'] = {'default_property_id': self.id}
        return action

    @api._model_create_multi
    def create(self, vals_list):
        res = super(Property, self).create(vals_list)
        if res.ref == 'New':
            res.ref = self.env['ir.sequence'].next_by_code('property_seq')
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




class PropertyLine(models.Model):
    _name = 'property.line'

    property_id = fields.Many2one('property')
    area = fields.Float()
    description = fields.Char()