from odoo import api, api, models, fields

class TrainingCourses(models.Model):
    _name = 'training.courses'
    _description = 'Training Courses'

    serial_number = fields.Char(string='Serial Number', required=True)
    name = fields.Char(string='Course Name', required=True)
    description = fields.Text(string='Description')
    teacher_id = fields.Many2one(
    'hr.employee', 
    string='Teacher',
    domain="[('job_id.name', '=', 'Teacher')]"
)
    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')
    number_of_days = fields.Integer(string='Number of Days', compute='_compute_number_of_days')
    time = fields.Float(string='Time (hours)',default=2.0)
    room_id = fields.Many2one('training.rooms', string='Room')
    location_id = fields.Many2one('training.locations', string='Location')
    available_seats = fields.Integer(string='Available Seats', compute='_compute_available_seats')
    total_seats = fields.Integer(string='Total Seats')
    target_gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string='Target Gender')
    deadline = fields.Date(string='Registration Deadline')
    registration_ids = fields.One2many('training.registration', 'course_id', string='Registrations')

    @api.depends("total_seats", "registration_ids")
    def _compute_available_seats(self):
        for course in self:
            taken = len(course.registration_ids)
            course.available_seats = course.total_seats - taken

    @api.depends('start_date', 'end_date')
    def _compute_number_of_days(self):
        for course in self:
            if course.start_date and course.end_date:
                delta = course.end_date - course.start_date
                course.number_of_days = delta.days + 1
            else:
                course.number_of_days = 0

