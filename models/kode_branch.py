from odoo import models, fields ,api
from odoo.modules.module import get_module_resource
import base64
from odoo.exceptions import ValidationError

class KodeBranch(models.Model):
    _name = 'kode.branch'
    _description = 'KODE Sports Club Branch'
    _inherit = ['mail.thread', 'mail.activity.mixin']

# =========================================
# Fields
# =========================================
    code = fields.Char(string="Branch Code", readonly=True, copy=False, default='New')
    active = fields.Boolean(default=True)


    name = fields.Char(string='Branch Name', required=True)
    location = fields.Char(string='Location')

    member_ids = fields.Many2many(
        'kode.member',
        'kode_branch_member_rel',
        'branch_id',
        'member_id',
        string='Members'
    )

    count_of_members = fields.Integer(
        compute='_compute_count_of_members',
        string="Count Of Members",
        readonly=True,
        store=True
    )

# =========================================
# Constraints
# =========================================
    _sql_constraints = [
        ('unique_name', 'UNIQUE(name)', 'This branch name already exists.'),
    ]

    @api.constrains('name')
    def _check_name_not_empty_or_numeric(self):
        for rec in self:
            if not rec.name.strip():
                raise ValidationError("Branch name cannot be empty or just spaces.")
            if rec.name.isdigit():
                raise ValidationError("Branch name cannot be numbers.")

# =========================================
# Compute Methods
# =========================================
    # def _compute_member_ids(self):
    #     for branch in self:
    #         related_members = self.env['kode.member'].search(
    #             [('branch_ids','in',branch.id)]
    #             )
    #         print('=' * 50)
    #         print(related_members)
    #         print('=' * 50)
    #         branch.member_ids = related_members

    @api.depends('member_ids')
    def _compute_count_of_members(self):
        for branch in self:
            branch.count_of_members = len(branch.member_ids)



# =========================================
# Sequance
# =========================================
# create
    @api.model
    def create(self, vals):
        if vals.get('code', 'New') == 'New':
            vals['code'] = self.env['ir.sequence'].next_by_code('kode.branch') or 'New'
        return super(KodeBranch, self).create(vals)

