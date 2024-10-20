from odoo import models

class AccountMove(models.Model):
    _inherit = 'account.move'

    def action_do_something(self):
        print("insideeee")


