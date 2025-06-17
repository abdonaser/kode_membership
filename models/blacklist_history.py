from odoo import models, fields, api
from odoo.exceptions import ValidationError

class KodeBlacklistHistory(models.Model):
    _name = 'kode.blacklist.history'
    _description = 'Blacklist History'
    _order = 'blacklist_date desc'

# =========================
# Fields
# =========================

    name = fields.Char(
        string="Blacklist Code",
        required=True,
        copy=False,
        readonly=True,
        default=lambda self: self.env['ir.sequence'].next_by_code('kode.blacklist.history'))

    member_id = fields.Many2one('kode.member', string="Member", required=True)

    blacklist_date = fields.Datetime(string="Blacklist Date", default=fields.Datetime.now, readonly=True)

    blocked_by = fields.Many2one('res.users', string="Blocked By", default=lambda self: self.env.user, readonly=True)

    blacklist_reason = fields.Text(string="Blacklist Reason", required=True)

    revision_request_ids = fields.One2many(
        'kode.blacklist.revision.request',
         'blacklist_id',
         string="Revision Requests"
     )
    blacklist_status =fields.Selection(
        [
            ('pending', 'Pending'),
            ('solved', 'Solved'),
            ('denied', 'Denied')
        ],
        default='pending',
        string="Status",
        tracking=True,
        compute='_compute_blacklist_status',
        store=True
    )

# ====================
# Computed Fields
# ====================
    @api.depends('revision_request_ids.revision_status', 'revision_request_ids.request_date')
    def _compute_blacklist_status(self):
        for rec in self:
            # Sort the revision requests by request_date descending to get the latest one
            latest_request = rec.revision_request_ids.sorted(key=lambda r: r.request_date, reverse=True)[:1]
            # print('='*50)
            # print(latest_request)
            # print('='*50)
            if latest_request:
                latest_status = latest_request.revision_status
                if latest_status == 'accepted':
                    rec.blacklist_status = 'solved'
                elif latest_status == 'denied':
                    rec.blacklist_status = 'denied'
                else:
                    rec.blacklist_status = 'pending'
            else:
                rec.blacklist_status = 'pending'