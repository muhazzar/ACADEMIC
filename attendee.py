from odoo import api,fields,models,_

class Attendee(models.Model):
    _name = "academic.attendee"

    name = fields.Char(string="Name")
    session_id = fields.Many2one(comodel_name="academic.session", string="Session")
    partner_id = fields.Many2one(comodel_name="res.partner", string="Partner")

    @api.onchange('partner_id')
    def onchange_partner(self):
        self.name = self.partner_id.id

    
    _sql_constraints = [
        ('partner_session_unik','UNIQUE(session_id,partner_id)','Multiple Attendee Detected')
    ]

    course_id=fields.Many2one(
        comodel_name="academic.course",
        string="Course",
        related="session_id.course_id",
        store=True
    )