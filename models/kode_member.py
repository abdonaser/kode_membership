from odoo import models, fields, api
from odoo.exceptions import UserError
from odoo.modules.module import get_module_resource
import base64
from odoo.exceptions import UserError, ValidationError


class KodeMember(models.Model):
    _name = 'kode.member'
    _description = 'KODE Sports Club Member'
    _inherit = ['mail.thread', 'mail.activity.mixin']

# =========================================
# Fields
# =========================================
    code = fields.Char(string="Member Code", readonly=True, copy=False, default='New')


    # branch_ids = fields.Many2many('kode.branch', string='Branches')
    branch_ids = fields.Many2many(
        'kode.branch',
        'kode_branch_member_rel',
        'member_id',
        'branch_id',
        string='Branches'
    )
    partner_id = fields.Many2one('res.partner', string="English Full Name", required=True)

    # english_name = fields.Char(string='English Full Name', required=True)
    name = fields.Char(compute="_compute_name", store=True)
    arabic_name = fields.Char(string='Arabic Full Name' , related="partner_id.arabic_name")
    first_name = fields.Char(string='First Name', compute="_compute_name_parts", store=True)
    last_name = fields.Char(string='Last Name', compute="_compute_name_parts", store=True)

    status = fields.Selection([
             ('draft', 'Draft'),
             ('approved', 'Approved'),
             ('black_list', 'Black List'),
         ], string='Status', default='draft', required=True)

    last_renewal_order_id = fields.Many2one(
    'sale.order',
        string='Last Renewal Order',
        compute="_compute_last_renewal_info",
        store=True,
    )

    last_renewal_date = fields.Datetime(
             string='Last Renewal Date',
             compute="_compute_last_renewal_info",
             store=True,
    )

    currency_id = fields.Many2one(
        'res.currency',
        string="Currency",
        required=False,
        default=lambda self: self.env.company.currency_id
    )

    total_last_renewal_data = fields.Monetary(
        string='Total Last Renewal Order',
        currency_field='currency_id',
        compute="_compute_last_renewal_info",
        store=True,
        readonly=True
        )

    image_1920 = fields.Image(
      compute='_compute_partner_image',
       readonly=True,
       string="Member Image"
   )
    active = fields.Boolean(default=True)

    current_blacklist_id = fields.Many2one(
        'kode.blacklist.history',
        compute="_compute_current_blacklist",
        store=True
    )

    latest_revision_status = fields.Selection(
        selection=[
            ('pending', 'Pending'),
            ('accepted', 'Accepted'),
            ('denied', 'Denied')
        ],
        compute="_compute_latest_revision_status",
        store=True,
        string="Latest Revision Status"
    )

# =========================================
# Constraints
# =========================================
    _sql_constraints = [
        ('unique_partner_id', 'unique(partner_id)', 'This Member Already Exist.')
    ]

    @api.constrains('partner_id')
    def _check_partner_validity(self):
        for rec in self:
            if not rec.partner_id:
                raise ValidationError("Member name must be set.")


# =========================================
# Compute Methods
# =========================================
    @api.depends('partner_id')
    def _compute_name(self):
        for rec in self:
            rec.name = rec.partner_id.name or 'Unnamed Member'

    @api.depends('partner_id.name')
    def _compute_name_parts(self):
        for member in self:
            full_name = member.partner_id.name or ''
            name_parts = full_name.strip().split(" ", 1)
            member.first_name = name_parts[0]
            member.last_name = name_parts[1] if len(name_parts) > 1 else ''



    def _update_renewal_info(self):
        template = self.env['sale.order.template'].search([('name', '=', 'Renewal')], limit=1)
        for member in self:
            order = self.env['sale.order'].search([
                ('partner_id', '=', member.partner_id.id),
                ('sale_order_template_id', '=', template.id),
                ],order="date_order desc", limit=1)

            if order:
                member.last_renewal_date = order.date_order if order else False
                if order.tax_totals and isinstance(order.tax_totals, dict):
                    member.total_last_renewal_data = float(order.tax_totals.get('amount_total', 0.0))
                else:
                    member.total_last_renewal_data = order.amount_total or 0.0
            else:
                member.total_last_renewal_data = 0.0


    def read(self, fields=None, load='_classic_read'):

        self._update_renewal_info()
        return super().read(fields=fields, load=load)


    @api.depends('partner_id' ,'last_renewal_order_id.amount_total')
    def _compute_last_renewal_info(self):
        template = self.env['sale.order.template'].search([('name', '=', 'Renewal')], limit=1)
        for member in self:
            if member.partner_id:
                order = self.env['sale.order'].search([
                    ('partner_id', '=', member.partner_id.id),
                    ('sale_order_template_id', '=', template.id),
                    ],order="date_order desc", limit=1)
                member.last_renewal_order_id = order
                member.last_renewal_date = order.date_order if order else False
                member.total_last_renewal_data = float(order.tax_totals['amount_total']) if order else 0.0

            else:
                member.last_renewal_date = False

    def _get_default_image(self, image_name):
        try:
            image_path = get_module_resource(
            'kode_membership', 'static/img', image_name)
            with open(image_path, 'rb') as f:
                return base64.b64encode(f.read())
        except FileNotFoundError:
            return False

    @api.depends('partner_id')
    def _compute_partner_image(self):
        for member in self:
            if member.partner_id and member.partner_id.image_1920:
                 member.image_1920 = member.partner_id.image_1920
            else:
                image_name = "default_image.png"
                member.image_1920 = self._get_default_image(image_name)


# =========================================
# Status
# =========================================
    def set_to_draft(self):
        for rec in self:
            rec.status = 'draft'

    def set_to_approved(self):
        for rec in self:
            rec.status = 'approved'

# revision_request_ids -> revision_status
    @api.depends('status')
    def _compute_current_blacklist(self):
        for rec in self:
            if rec.status == 'black_list':
                related_blacklist_id = self.env['kode.blacklist.history'].search([
                    ('member_id', '=', rec.id)
                ], order='blacklist_date desc', limit=1)
                rec.current_blacklist_id = related_blacklist_id
            else:
                rec.current_blacklist_id = False


    @api.depends('current_blacklist_id.revision_request_ids')
    def _compute_latest_revision_status(self):
        for rec in self:
            requests = rec.current_blacklist_id.revision_request_ids
            latest_request = requests.sorted(key=lambda r: r.request_date, reverse=True)[:1]
            rec.latest_revision_status = latest_request.revision_status if requests else False

    def action_open_blacklist_wizard(self):
        self.ensure_one()
        for rec in self:
            if rec.status == 'black_list':
                raise UserError("This membersip ALlready in the blackList.")
        return {
            'type': 'ir.actions.act_window',
            'name': 'Blacklist Member',
            'res_model': 'kode.blacklist.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_member_id': self.id,
            }
        }

    def action_open_revision_request_wizard(self):
        self.ensure_one()
        for rec in self:
            if rec.status != 'black_list':
                raise UserError("This membersip not in the blackList.")

            if rec.current_blacklist_id:
                for request in rec.current_blacklist_id.revision_request_ids:
                    if request.revision_status == "pending":
                        raise UserError("There is arequest in pending.")
        return {
            'type': 'ir.actions.act_window',
            'name': 'Request Revision',
            'res_model': 'kode.revision.request.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_blacklist_id': self.current_blacklist_id.id,
                'default_member_id': self.id,
            }
        }




# =========================================
# Actions
# =========================================
    def open_invoice(self):
        self.ensure_one()
        order = self.env['sale.order'].search([
        ('partner_id', '=', self.partner_id.id),
        ('sale_order_template_id.name', '=', 'Renewal'),
         ], order="date_order desc", limit=1)

        if not order:
            raise UserError("No renewal sale order found for this member.")

        action = self.env.ref('sale.action_orders').read()[0]

        view_id = self.env.ref('sale.view_order_form').id
        action['res_id'] = order.id
        action['views'] = [(view_id, 'form')]
        return action

# =========================================
# Sequance
# =========================================
    # create
    @api.model
    def create(self, vals):
        if vals.get('code', 'New') == 'New':
            vals['code'] = self.env['ir.sequence'].next_by_code('kode.member') or 'New'
        return super(KodeMember, self).create(vals)


# =========================================
# Generate Excel Reports
# =========================================
    def member_xlsx_report(self):
        print("member_xlsx_report")
        ids = self.env.context.get("active_ids")
        return {
            'type': 'ir.actions.act_url',
            'url': f'/member/excel/report/{ids}',
            'target': 'new',
        }