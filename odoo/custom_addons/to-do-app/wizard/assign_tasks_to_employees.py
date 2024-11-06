from odoo import fields, models
from odoo.exceptions import ValidationError


class AssignTasks(models.TransientModel):
    _name = 'assign.tasks'

    task_id = fields.Many2many('task')
    employee_id = fields.Many2many('employee')
    # state = fields.Selection([
    #     ('new', 'New'),
    #     ('inprogress', 'In Progress'),
    # ], default='new')

    def assign_task(self):
        for task in self.task_id:
            if task.status != 'new':
                raise ValidationError("Please assign Only New Tasks.")

        for task in self.task_id:
            # employee.write({'task_ids': [(4 , task.id) for task in self.task_id]}
            task.write({'employee_id': [(4, [employee.id]) for employee in self.employee_id ]})
            # employee.write({'task_ids': [(4, task.id) for task in self.task_id]})
            # employee.write({'task_ids': [(6, 0, self.task_id.ids)]})


