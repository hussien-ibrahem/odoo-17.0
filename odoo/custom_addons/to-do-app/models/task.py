from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import timedelta
import logging

_logger = logging.getLogger(__name__)


class Task(models.Model):
    _name = 'task'
    _description = "Task"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    active = fields.Boolean(default=True)

    name = fields.Char()
    description = fields.Text()
    due_date = fields.Date()
    is_late = fields.Boolean()
    estimated_time = fields.Float()
    working_lines_ids = fields.One2many('working.lines', 'task_id')
    total_working_hours = fields.Float(compute='_compute_total_working_hours', store=True)

    employee_id = fields.Many2many('employee' , 'task_ids')
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


    def check_due_date(self):
        task_ids = self.search([])
        for rec in task_ids:
            if rec.due_date and rec.due_date < fields.date.today():
                rec.is_late = True
                rec.activity_schedule(
                    'mail.mail_activity_data_todo',  # نوع الـ activity (تقدر تغييره حسب احتياجك)
                    user_id=self.env.user.id,  # المستخدم المستهدف (ممكن تغير الحقل ده)
                    summary='Task is overdue!',
                    note=f'The task {rec.name} is overdue. Please take action.',
                )
        print(task_ids)
        print("Hello from check_due_date !!!!!!!!!!!")



    def actoin_completed(self):
        for rec in self:
            print("Hello from the \"Closed\" Function!")
            self.status = 'completed'

    @api.depends('working_lines_ids.time')
    def _compute_total_working_hours(self):
        for record in self:
            if record.working_lines_ids:
                total_hours = sum(line.time for line in record.working_lines_ids)
                record.total_working_hours = total_hours


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





class WorkingLines(models.Model):
    _name = 'working.lines'

    description = fields.Text()
    start_date = fields.Datetime(required = 1)
    time = fields.Float()  # Assuming it's in hours
    end_date = fields.Datetime(compute='_compute_end_date', store=True)
    task_id = fields.Many2one('task')

    @api.depends('start_date', 'time')
    def _compute_end_date(self):
        for rec in self:
            if rec.start_date and rec.time:
                rec.end_date = rec.start_date + timedelta(hours=rec.time)
            else:
                rec.end_date = False  # Or keep it empty if values aren't set

    @api.constrains('time')
    def _check_time_within_estimated(self):
        for rec in self:
            task = rec.task_id
            if task:
                total_recorded_hours = sum(line.time for line in task.working_lines_ids)  # حساب الساعات الحالية
                if total_recorded_hours > task.estimated_time:
                    print(f"total_recorded_hours : {total_recorded_hours} \n rec.time : {rec.time} \n task.estimated_time : {task.estimated_time}")
                    raise ValidationError("Total working hours exceed the estimated time for the task!")
