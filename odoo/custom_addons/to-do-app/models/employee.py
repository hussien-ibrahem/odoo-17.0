from odoo import models,fields,api


class Employee(models.Model):
    _name = 'employee'
    name = fields.Char(required = 1)
    address = fields.Char()
    phone = fields.Char()
    task_ids = fields.One2many('task', 'employee_id')

