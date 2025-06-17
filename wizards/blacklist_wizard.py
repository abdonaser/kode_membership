from odoo import models, fields, api
from odoo.exceptions import UserError

class KodeBlacklistWizard(models.TransientModel):
    _name = 'kode.blacklist.wizard'
    _description = 'Blacklist Member Wizard'

    member_id = fields.Many2one('kode.member', string="Member", required=True)

    blacklist_reason = fields.Text(string="Reason for Blacklist", required=True)


    def confirm_blacklist(self):
        self.ensure_one()
        if self.member_id.status == 'black_list':
            raise UserError("Member is already blacklisted.")

        blacklist_record = self.env['kode.blacklist.history'].create({
            'member_id': self.member_id.id,
            'blacklist_reason': self.blacklist_reason,
        })
        # Change the membership status
        self.member_id.write({
            'status': 'black_list',
        })
        return {'type': 'ir.actions.act_window_close'}