from odoo import fields,models
class Member(models.Model):
    _name = 'training_members.member'
    _description = 'Training Member'
    card_number = fields.Char('Card')
    partner_id = fields.Many2one("res.partner",delegate=True,ondelete="cascade",required=True)