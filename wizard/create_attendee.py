from odoo import api, fields, models

class CreateAttendeeWizard(models.TransientModel):
    _name='academic.create.attendee.wizard'

    session_id = fields.Many2one(
        comodel_name='academic.session',
        string='Session',
    )

    session_ids = fields.Many2many(
        comodel_name='academic.session',
        string="Sessions",
    )

    partner_ids = fields.Many2many(
        comodel_name='res.partner',
        string ='Partner to add to session',
        required=True,
    )

    def action_add_attendee(self):
        self.ensure_one()

        # self.session_id.attendee_ids = [(0,0,{
        #     'partner_id': p.id
        # })for p in self.partner_ids]

        for ses in self.session_ids:
            ses.attendee_ids = [(0,0,{
                'partner_id': p.id
            }) for p in self.partner_ids ]
            
        return{'type':'ir.actions.act_window_close'}