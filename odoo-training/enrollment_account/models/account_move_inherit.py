from odoo import models, fields

class AccountMove(models.Model):
    _inherit = 'account.move'

    enroll_ref = fields.Char("Enroll Reference")
