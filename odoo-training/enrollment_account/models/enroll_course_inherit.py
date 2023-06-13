from odoo import fields,models,api

class EnrollCourseInherit(models.Model):
    _inherit = "course.enrollment"

    def action_do_confirmed(self):
        res = super().action_do_confirmed()
        journal = self.env['account.journal'].search([("type","=","sale")],limit=1)
        for prop in self:
            self.env["account.move"].create(
                {
                    "partner_id": prop.member_id.partner_id.id,
                    "currency_id": prop.currency_id.id,
                    "invoice_date": prop.enroll_date,
                    "enroll_ref": prop.name,
                    "move_type": "out_invoice",
                    "journal_id": journal.id,
                    "invoice_line_ids": [
                        (0, 0, {
                                "name": prop.name,
                                "quantity": 1.0,
                                "price_unit": prop.total_amount,
                        }, ), (0,0,
                            {
                                "name": "Administrative fees",
                                "quantity": 1.0,
                                "price_unit": 100.0
                            

                        })
                    ]
                }
            )