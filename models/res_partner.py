from odoo import api, fields, models
from odoo.exceptions import ValidationError

class ResPartner(models.Model):
    _inherit = "res.partner"

    arabic_name = fields.Char(
        string='Arabic Full Name',
        required=True,
    )

    _sql_constraints = [
        ('unique_arabic_name', 'unique(arabic_name)', 'Arabic Name must be unique.'),
    ]

    @api.constrains('arabic_name')
    def _check_arabic_name(self):
        for rec in self:
            if not rec.arabic_name or not rec.arabic_name.strip():
                raise ValidationError("Arabic Name cannot be empty.")

            if rec.arabic_name.isdigit():
                raise ValidationError("Arabic Name cannot contain only digits.")
