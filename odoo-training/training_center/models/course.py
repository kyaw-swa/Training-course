from odoo import fields,models,api
from odoo.exceptions import UserError
from datetime import timedelta
class Course(models.Model):
    _name = 'training_center.course'
    _description = 'Training Center Course'
    name = fields.Char('Course Title', required=True)
    descr = fields.Html('Description')
    course_level = fields.Selection([
        ("basic","Basic"),
        ("intermediate","Intermediate"),
        ("advanced","Advanced"),
    ],"Course Level")
    
    remarks = fields.Text('Manager Remarks')
    remarks2 = fields.Text('Supervisor Remarks')
    
    # Boolean
    active = fields.Boolean('Active',default=True)
    # Date Time Field
    start_date = fields.Date(default=lambda self: fields.Date.today())
    #Relational Fields
    company_id = fields.Many2one("res.partner",string="Company")
    teacher_ids = fields.Many2many("res.partner",string="Teacher")
    course_items_ids = fields.One2many('training_center.course.line.item','course_id',string='Course Contents')
    country_id = fields.Many2one("res.country",string='Country',related='company_id.country_id')
    # Image
    cover_image = fields.Binary("Course Cover")
    
    # price helper
    #res.*, ir.*
    currency_id = fields.Many2one("res.currency",groups='training_center.course_group_manager')
    price = fields.Monetary("Price","currency_id" ,groups='training_center.course_group_manager')
    
    # Compute Field
    num_of_contents = fields.Integer(compute='_compute_num_of_contents')
    
    # Reserved Field
    state = fields.Selection(
        string="state",
        selection=[('new','New'),('completed','Completed'),('progress','In progress'),('canceled','Canceled')],
        default='new'
    )
    
    total_duration = fields.Integer(string='Total Duration',compute='_compute_total_duration')
    
    deadline_date = fields.Date(string='Deadline Date',compute='_compute_deadline_date')
    
    @api.depends('course_items_ids.duration')
    def _compute_total_duration(self):
        for record in self:
            record.total_duration = sum(record.course_items_ids.mapped('duration'))
            
    @api.depends('start_date','total_duration')
    def _compute_deadline_date(self):
        for record in self:
            duration_in_days = record.total_duration * 7 #Assuming duration is given
            record.deadline_date = record.start_date + timedelta (days=duration_in_days)
            
    @api.depends('course_items_ids')
    def _compute_num_of_contents(self):
        for course in self:
            course.num_of_contents = len(course.course_items_ids)
            
    @api.model
    def create(self,values):
        if not self.user_has_groups('training_center.course_group_manager'):
            if values.get('remarks'):
                raise UserError("You are not allowed to create manager's remarks")
            if values.get('remarks2'):
                raise UserError("You are not allowed to create supervisor's remarks")
                                 
        return super(Course,self).create(values)
    
    def write(self,values):
        if not self.user_has_groups('training_center.course_group_manager'):
            if values.get('remarks'):
                raise UserError("You are not allowed to write manager's remarks")
            if values.get('remarks2'):
                raise UserError("You are not allowed to write supervisor's remarks")                      
        return super(Course,self).write(values)
    
    def action_do_cancel(self):
        if self.state != "completed":
            self.state ="canceled"
        return True
    
    def action_do_complete(self):
        return self.write({"state":"completed"})
    
    def action_do_progress(self):
        return self.write({"state":"progress"})
   