from odoo import fields, models, api
from odoo.exceptions import ValidationError


class AssignTasks(models.TransientModel):
    _name = 'assign.tasks'

    task_id = fields.Many2many('task')
    employee_id = fields.Many2many('employee')
    state = fields.Selection([
        ('new', 'New'),
        ('inprogress', 'In Progress'),
    ], default='new')

    # def assign_task(self):
    #     for task in self.task_id:
    #         if task.status != 'new':
    #             raise ValidationError("Please assign Only New Tasks.")
    #
    #         print (self.employee_id.ids)
    #         task.write({'employee_id': [(6, 0, self.employee_id.ids)]})  # Assign new employees
    #         # vals = {'employee_id': [(6, 0, self.employee_id.ids)]}  # Correct syntax
    #         # task.write(vals)
    #     return {'type': 'ir.actions.act_window_close'}

    def assign_task(self):
        for task in self.task_id:
            if task.status != 'new':
                raise ValidationError("Please assign Only New Tasks.")
            current_employee_ids = task.employee_id.ids
            new_employee_ids = self.employee_id.ids
            employees_to_add = set(new_employee_ids) - set(current_employee_ids)
            if employees_to_add:
                task.write({'employee_id': [(4, employee_id, 0) for employee_id in employees_to_add]})
        return {'type': 'ir.actions.act_window_close'}

