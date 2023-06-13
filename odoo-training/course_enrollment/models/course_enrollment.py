from odoo import fields, models, api

class CourseEnrollment(models.Model):
    _name = 'course.enrollment'
    _description = 'Course Enrollment'
    _inherit = ['mail.thread','mail.activity.mixin']

    name = fields.Char('Title', required=True)
    enroll_date = fields.Date(default=lambda self: fields.Date.today(),tracking=True)
    course_id = fields.Many2one('training_center.course', 'Course',tracking=True)
    member_id = fields.Many2one('training_members.member','Member',tracking=True)
    member_image = fields.Binary(related='member_id.image_1920')
    
    currency_id = fields.Many2one('res.currency')
    price = fields.Monetary('Price', 'currency_id', related='course_id.price')

    discount = fields.Float('Discount', 'currency_id', compute='_compute_discount')
    total_amount = fields.Monetary('Total Amount', 'currency_id', compute='_compute_total_amount')

    state = fields.Selection(
        string="state",
        selection=[('new','New'),('draft','Draft'),('confirmed','Confirmed'),('canceled','Canceled')],
        default='new'
    )

    @api.model_create_multi
    def create(self,vals_list):
        for vals in vals_list:
            vals['name']= self.env['ir.sequence'].next_by_code('enroll.course') or '/'
        return super().create(vals_list)

    #@api.model
    #def create(self,vals_list):
    #    vals_list['name']= self.env['ir.sequence'].next_by_code('course.enrollment') or '/'
    #    return super().create(vals_list)

    
    @api.depends('enroll_date', 'price')
    def _compute_discount(self):
        for enrollment in self:
            if enrollment.enroll_date and enrollment.enroll_date < fields.Date.from_string('2023-06-01'):
                enrollment.discount = enrollment.price * 0.25
            else:
                enrollment.discount = enrollment.price * 0.20

    @api.depends('price', 'discount')
    def _compute_total_amount(self):
        for enrollment in self:
            enrollment.total_amount = enrollment.price - enrollment.discount
            
    def action_do_cancel(self):
        if self.state != "confirmed":
            self.state ="canceled"
        return True
    
    def action_do_confirmed(self):
        return self.write({"state":"confirmed"})
    
    def action_do_draft(self):
        return self.write({"state":"draft"})
