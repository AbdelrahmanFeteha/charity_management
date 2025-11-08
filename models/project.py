# -*- coding: utf-8 -*-
from odoo import models, fields, api

class CharityProject(models.Model):
    _name = "charity.project"
    _description = "Project / Campaign"
    _order = "create_date desc"

    name = fields.Char(required=True)
    category = fields.Char()
    description = fields.Text()
    start_date = fields.Date()
    end_date = fields.Date()

    # Relations
    request_ids = fields.One2many("charity.request", "project_id", string="Requests")
    donation_ids = fields.One2many("charity.donation", "project_id", string="Donations")
    distribution_ids = fields.One2many("charity.distribution", "project_id", string="Distributions")

    # Aggregates
    total_requested = fields.Float(compute="_compute_totals", store=True)
    total_donations = fields.Float(compute="_compute_totals", store=True)
    total_distributed = fields.Float(compute="_compute_totals", store=True)
    funding_progress = fields.Float(string="Funding Progress (%)", compute="_compute_totals", store=True)

    @api.depends(
        "request_ids.amount_requested",
        "donation_ids.amount", "donation_ids.status",
        "distribution_ids.amount"
    )
    def _compute_totals(self):
        for proj in self:
            req = sum(r.amount_requested for r in proj.request_ids)
            don = sum(d.amount for d in proj.donation_ids if d.status == "completed")
            dist = sum(x.amount for x in proj.distribution_ids)
            proj.total_requested = req
            proj.total_donations = don
            proj.total_distributed = dist
            proj.funding_progress = (dist / req * 100.0) if req else 0.0
