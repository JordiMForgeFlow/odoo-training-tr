
from odoo import models, fields, api, exceptions


class Course(models.Model):
    _name = 'openacademy.course'
    _description = 'OpenAcademy Courses'

    name = fields.Char(string="Title", required=True)
    description = fields.Text()
    responsible_id = fields.Many2one("res.users", ondelete='set null', string="Responsible", index=True)
    session_ids = fields.One2many("openacademy.session", "course_id", string="Sessions")

    _sql_constraints = [
        ('name_description_check',
         'CHECK(name != description)',
         "The title of the course should not be the description"),

        ('name_unique',
         'UNIQUE(name)',
         "The course title must be unique")
    ]


class Session(models.Model):
    _name = 'openacademy.session'
    _description = 'OpenAcademy Sessions'

    name = fields.Char(string="Session name", required=True)
    instructor_id = fields.Many2one("res.partner", string="Instructor", domain=[('instructor', '=', True)])
    course_id = fields.Many2one("openacademy.course", ondelete='cascade', string="Course", required=True)
    start_date = fields.Date(default=fields.Date.today)
    duration = fields.Float(digits=(6, 2), help="Duration in days")
    active = fields.Boolean(default=True)
    seats = fields.Integer(string="Number of seats")
    taken_seats = fields.Float(string="Taken seats", compute='_taken_seats')
    attendee_ids = fields.Many2many("res.partner", string="Attendees")

    @api.depends('seats', 'attendee_ids')
    def _taken_seats(self):
        for r in self:
            if not r.seats:
                r.taken_seats = 0.0
            else:
                r.taken_seats = 100.0 * len(r.attendee_ids) / r.seats

    @api.onchange('seats', 'attendee_ids')
    def _verify_valid_seats(self):
        if self.seats < 0:
            return {
                'warning': {
                    'title': "Incorrect seats value",
                    'message': "Value of number of seats may not be negative",
                },
            }
        if self.seats < len(self.attendee_ids):
            return {
                'warning': {
                    'title': "Too many attendees",
                    'message': "Increase seats or remove excess attendees",
                },
            }

    @api.constrains(attendee_ids)
    def _check_instructor_not_in_attendees(self):
        for r in self:
            if r.instructor_id and r.instructor_id in r.attendee_ids:
                raise exceptions.ValidationError("A session's instructor can't be an attendee")
