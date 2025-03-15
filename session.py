from odoo import api,fields,models,_
from odoo.exceptions import ValidationError
import time


class session(models.Model):
    _name = "academic.session"

    name = fields.Char(string="Name", required=True)

    course_id = fields.Many2one(comodel_name="academic.course",
                                string="Course", required=True)
    
    instructor_id = fields.Many2one(comodel_name="res.partner",
                                    string="Instructor", required=True)
    
    start_date = fields.Date(string="Start Date",default=lambda self: time.strftime("%Y-%m-%d"))
    duration = fields.Integer(string="Duration")
    seats = fields.Integer(string="Seats")
    active = fields.Boolean(string="Active", default=True)

    attendee_ids = fields.One2many(
        comodel_name="academic.attendee",
        inverse_name="session_id",
        string="Attendees",
    )

    taken_seats = fields.Float(string="Taken Seats",
                               compute="_calc_taken_seats")
    
    image_small = fields.Binary("Image Small")


    state = fields.Selection(string="State",
                             selection=[('draft','Draft'),('open',"Open"),('done','Done')],
                             default='draft',
                             required=True,
                             readonly=True
                             )


    def action_open(self):
        self.state='open'

    def action_done(self):
        self.state='done'

    def action_draft(self):
        self.state='draft'

    def _calc_taken_seats(self):
        for rec in self:
            if rec.seats > 0:
                rec.taken_seats = 100.0 * len(rec.attendee_ids) / rec.seats
            else:
                rec.taken_seats = 0.0


    @api.onchange('seats','attendee_ids')
    def onchange_seats(self):
        for rec in self:
            if rec.seats > 0:
                rec.taken_seats = 100.0 * len(rec.attendee_ids) / rec.seats
            else:
                rec.taken_seats = 0.0


    @api.constrains('instructor_id','attendee_ids')
    def _cek_instructor(self):
        for session in self:
            partner_ids = [ att.partner_id.id for att in session.attendee_ids ]

            if session.instructor_id.id in partner_ids:
                raise ValidationError("instructor tidak boleh menjadi peserta")


    def copy (self,default=None):
        self.ensure_one
        d = dict(default or {},
                 name = f"copy of {self.name}"
                 )
        return super(session,self).copy(default=d)