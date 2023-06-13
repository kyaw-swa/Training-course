from odoo import fields, models, api


class Course(models.Model):
    _inherit = 'training_center.course'

    enroll_ids = fields.One2many('course.enrollment', 'course_id')
    price = fields.Monetary('Price')  # Add the price field to the model
    enroll_date = fields.Date(default=lambda self: fields.Date.today(),related='enroll_ids.enroll_date')
    discount = fields.Float(string='Discount', compute='_compute_discount')
    early_bird_discount = fields.Float(string='Early Bird Discount', compute='_compute_early_bird_discount')
    total_amount = fields.Monetary('Total Amount', 'currency_id', related='enroll_ids.total_amount')

    @api.depends('price', 'enroll_date')
    def _compute_discount(self):
        for course in self:
            if course.enroll_date and course.enroll_date > fields.Date.from_string('2023-06-01'):
                course.discount = course.price * 0.2
            else:
                course.discount = 0.0

    @api.depends('price', 'enroll_date')
    def _compute_early_bird_discount(self):
        for course in self:
            if course.enroll_date and course.enroll_date < fields.Date.from_string('2023-06-01'):
                course.early_bird_discount = course.price * 0.25
            else:
                course.early_bird_discount = 0.0
                    



    num_of_students_enrolls = fields.Integer(compute='_compute_num_of_enrollments')

    def _compute_num_of_enrollments(self):
        for course in self:
            course.num_of_students_enrolls = len(course.enroll_ids)

    def name_get(self):
        result = []
        for course in self:
            instructors = course.teacher_ids.mapped('name')
            name = ",".join(instructors)
            result.append((course.id, course.name + f" ({name})"))
        return result

    def action_enrollment(self):
        domain = [('course_id', '=', self.id)]
        action = self.env.ref('course_enrollment.action_training_course_enrollment')
        result = action.read()[0]
        result['domain'] = domain
        return result
