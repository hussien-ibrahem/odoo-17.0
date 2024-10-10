from odoo import models, fields, api
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class Task(models.Model):
    _name = 'task'
    _description = "Task"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char()
    description = fields.Text()
    due_date = fields.Date()
    employee_id = fields.Many2many('employee')
    employee_address = fields.Char(related='employee_id.address')
    employee_phone = fields.Char(related='employee_id.phone')

    status = fields.Selection([
        ('new', 'New'),
        ('inprogress', 'In Progress'),
        ('completed', 'Completed'),
    ], default='new')

    _sql_constraints = [
        ('unique_name', 'unique(name)', 'This name is exist!!')
    ]

    @api.constrains('employee_id')
    def _check_assigned(self):
        for rec in self:
            if not rec.employee_id:
                raise ValidationError("Please assign the task to an employee.")

    @api.constrains('name')
    def _check_name(self):
        for rec in self:
            if not rec.name:
                raise ValidationError("Please Enter Valid Name")

    def actoin_new(self):
        for rec in self:
            print("Hello from the \"New\" Function!")
            self.status = 'new'

    def actoin_inprogress(self):
        for rec in self:
            print("Hello from the \"In Progress\" Function!")
            self.status = 'inprogress'

    def actoin_completed(self):
        for rec in self:
            print("Hello from the \"Completed\" Function!")
            self.status = 'completed'

    @api._model_create_multi
    def create(self, vals_list):
        res = super(Task, self).create(vals_list)
        print("-----This is create method Task-----")
        return res

    @api.model
    def _search(self, domain, offset=0, limit=None, order=None, access_rights_uid=None):
        res = super(Task, self)._search(domain, offset=0, limit=None, order=None, access_rights_uid=None)
        print("This is search method Task")
        return res

    def write(self, vals):
        res = super(Task, self).write(vals)
        print("This is Update method Task")
        return res

    def unlink(self):
        res = super(Task, self).unlink()
        print("-----This is unlink method Task-----")
        return res
