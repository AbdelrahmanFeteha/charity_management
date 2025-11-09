# models/distribution.py
from odoo import models, fields, api, _

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
                parts.append(f"Req:{rec.request_id.display_name}")   # ← use display_name
            if rec.donation_id:
                parts.append(f"Don:{rec.donation_id.display_name}")  # ← safe too
            if rec.date:
                parts.append(str(rec.date))
            if rec.amount:
                parts.append(f"{rec.amount:.2f}")
            rec.name = " | ".join(parts) if parts else _("Distribution")
