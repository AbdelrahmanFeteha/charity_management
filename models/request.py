# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError # type: ignore

class CharityRequest(models.Model):
    _name = "charity.request"
    _description = "Help Request"
    _order = "create_date desc"

    # Requester info
    requester_name = fields.Char(string="Requester Name", required=True)
    location = fields.Char(string="Location")
    category = fields.Selection([
        ("food", "Food"),
        ("shelter", "Shelter"),
        ("education", "Education"),
        ("medical", "Medical"),
        ("other", "Other"),
    ], string="Category", required=True)
    description = fields.Text(string="Description")

    # Amounts
    amount_requested = fields.Float(string="Amount Requested", required=True)
    amount_funded = fields.Float(string="Amount Funded", compute="_compute_funded", store=True)
    funding_progress = fields.Float(string="Funding Progress (%)", compute="_compute_funded", store=True)

    # Status + Tracking
    status = fields.Selection([
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("funded", "Funded"),
        ("rejected", "Rejected"),
    ], default="pending", string="Status", required=True)
    date_requested = fields.Date(default=fields.Date.context_today, string="Requested On")
    approved_at = fields.Datetime(string="Approved At")
    funded_at = fields.Datetime(string="Funded At")

    # Relations
    project_id = fields.Many2one("charity.project", string="Project / Campaign")
    distribution_ids = fields.One2many("charity.distribution", "request_id", string="Distributions")

    @api.constrains("amount_requested")
    def _check_amount_positive(self):
        for rec in self:
            if rec.amount_requested <= 0:
                raise ValidationError(_("Requested amount must be positive."))

    @api.depends("distribution_ids.amount", "amount_requested")
    def _compute_funded(self):
        for rec in self:
            total = sum(d.amount for d in rec.distribution_ids)
            rec.amount_funded = total
            rec.funding_progress = (total / rec.amount_requested * 100.0) if rec.amount_requested else 0.0
