
# models/distribution.py
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError # type: ignore

class CharityDistribution(models.Model):
    _name = "charity.distribution"
    _description = "Distribution (Outgoing to Requests)"
    _order = "date desc, id desc"

    name = fields.Char(compute="_compute_name", store=True)
    project_id = fields.Many2one("charity.project", string="Project / Campaign")
    request_id = fields.Many2one("charity.request", string="Request", required=True)
    donation_id = fields.Many2one("charity.donation", string="Source Donation")
    amount = fields.Float(string="Amount", required=True)
    date = fields.Date(string="Distribution Date", default=fields.Date.context_today)

    @api.depends('request_id', 'donation_id', 'date', 'amount')
    def _compute_name(self):
        for rec in self:
            parts = []
            if rec.request_id:
                parts.append(f"Req:{rec.request_id.display_name}")
            if rec.donation_id:
                parts.append(f"Don:{rec.donation_id.display_name}")
            if rec.date:
                parts.append(str(rec.date))
            if rec.amount:
                parts.append(f"{rec.amount:.2f}")
            rec.name = " | ".join(parts) if parts else _("Distribution")

    # --- SANITY CHECKS BELOW ---
    @api.constrains('amount')
    def _check_positive_amount(self):
        for rec in self:
            if rec.amount <= 0:
                raise ValidationError(_("Distribution amount must be positive."))

    @api.constrains('donation_id', 'amount')
    def _check_donation_balance(self):
        for rec in self:
            if rec.donation_id:
                total_distributed = sum(d.amount for d in rec.donation_id.distribution_ids if d.id != rec.id)
                available = rec.donation_id.amount - total_distributed
                if rec.amount > available:
                    raise ValidationError(_(
                        "Distribution amount (%.2f) exceeds available funds from this donation (%.2f)."
                    ) % (rec.amount, available))

    @api.constrains('project_id', 'donation_id', 'request_id')
    def _check_project_consistency(self):
        for rec in self:
            proj = rec.project_id
            if rec.donation_id and rec.donation_id.project_id and rec.donation_id.project_id != proj:
                raise ValidationError(_("Donation project mismatch with selected project."))
            if rec.request_id and rec.request_id.project_id and rec.request_id.project_id != proj:
                raise ValidationError(_("Request project mismatch with selected project."))