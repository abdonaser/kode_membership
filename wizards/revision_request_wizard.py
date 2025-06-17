from odoo import models, fields, api
from odoo.exceptions import UserError

class KodeRevisionRequestWizard(models.TransientModel):
    _name = 'kode.revision.request.wizard'
    _description = 'Request Revision Wizard'

    member_id = fields.Many2one('kode.member', string="Member", required=True)
    revision_reason = fields.Text(string="Reason for Revision", required=True)

    def confirm_revision_request(self):
        self.ensure_one()

        blacklist = self.env['kode.blacklist.history'].search([
            ('member_id', '=', self.member_id.id)
        ], order="blacklist_date desc", limit=1)

        if not blacklist:
            raise UserError("No blacklist history found for this member.")

        if blacklist.revision_request_ids:
            for request in blacklist.revision_request_ids:
                if request.revision_status == "pending":
                    raise UserError("There is arequest in pending.")

        self.env['kode.blacklist.revision.request'].create({
            'blacklist_id': blacklist.id,
            'revision_reason': self.revision_reason,
        })

        return {'type': 'ir.actions.act_window_close'}
