from odoo import models, fields, api , _
from odoo.exceptions import ValidationError


class KodeBlacklistRevisionRequest(models.Model):
    _name = 'kode.blacklist.revision.request'
    _description = 'Blacklist Revision Request'
    _order = 'request_date desc'

# =========================
# Fields
# =========================

    name = fields.Char(
        string="Request Code",
        required=True,
        copy=False,
        readonly=True,
        default=lambda self: self.env['ir.sequence'].next_by_code('kode.blacklist.revision.request'))

    blacklist_id = fields.Many2one('kode.blacklist.history', string="Blacklist Record", required=True, ondelete="cascade")

    member_id = fields.Many2one(
        related='blacklist_id.member_id',
        string="Member",
        store=True
    )

    request_date = fields.Datetime(
        string="Request Date",
        default=fields.Datetime.now
    )

    requested_by = fields.Many2one(
        'res.users',
        string="Requested By",
        default=lambda self: self.env.user
    )

    revision_reason = fields.Text(string="Revision Reason", required=True)

    revision_status = fields.Selection(
        [
            ('pending', 'Pending'),
            ('accepted', 'Accepted'),
            ('denied', 'Denied')
        ],
        default='pending',
        string="Status",
        tracking=True
    )
    # active = fields.Boolean(default=True)



# ====================
# Constraints And Overrides
# ====================
    def _check_manager_permission(self, vals):
        if 'revision_status' in vals:
            if not self.env.user.has_group('kode_membership.group_membership_manager'):
                raise ValidationError(_('Only managers can change the revision status.'))

    @api.model
    def create(self, vals):
        self._check_manager_permission(vals)
        return super().create(vals)

    def write(self, vals):
        self._check_manager_permission(vals)
        res = super().write(vals)
        for rec in self:
            if vals.get('revision_status') == 'accepted' and rec.member_id:
                rec.member_id.status = 'draft'
                # rec.active = False
        return res



# # ====================
# # Computed Fields
# # ====================
#     @api.onchange("revision_status")
#     def _handle_status_change(self):
#         for rec in self:
#             if not self.env.user.has_group('kode_membership.group_membership_manager'):
#                 raise ValidationError(_('Only managers can Edit this Field'))
#             if rec.revision_status == 'accepted' and rec.member_id:
#                 rec.member_id.status = 'draft'