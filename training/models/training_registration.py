from odoo import api, models, fields
from odoo.exceptions import ValidationError

class TrainingRegistration(models.Model):
    _name = 'training.registration'
    _description = 'Training Registration'

    serial_number = fields.Char(string='Trainee Serial Number', required=True)
    trainee_name = fields.Char(string='Trainee Name', required=True)
    course_id = fields.Many2one('training.courses', string='Course', required=True)
    course_name = fields.Char(string='Course Name', related='course_id.name',readonly=True)
    course_desc = fields.Text(string='Course Description', related='course_id.description',readonly=True)
    teacher_name = fields.Char(string='Teacher Name', related='course_id.teacher_id.name',readonly=True)
    start_date = fields.Date(string='Start Date', related='course_id.start_date',readonly=True)
    end_date = fields.Date(string='End Date', related='course_id.end_date',readonly=True)
    number_of_days = fields.Integer(string='Number of Days', related='course_id.number_of_days',readonly=True)
    time = fields.Float(string='Time (hours)', related='course_id.time',readonly=True)
    room_name = fields.Char(string='Room Name', related='course_id.room_id.name',readonly=True)
    location_name = fields.Char(string='Location Name', related='course_id.location_id.name',readonly=True)

    @api.model_create_multi
    def create(self, vals):
        for val in vals:
            course = self.env['training.courses'].browse(val['course_id'])
            if course.available_seats <= 0:
                raise ValidationError("No available seats for this course.")
            if course.deadline and fields.Date.today() > course.deadline:
                raise ValidationError("Registration deadline has passed.")
        return super(TrainingRegistration, self).create(vals)