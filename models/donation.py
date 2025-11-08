# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError # type: ignore

class CharityDonation(models.Model):
    _name = "charity.donation"
    _description = "Donation (Incoming)"
    _order = "create_date desc"

    donor_id = fields.Many2one("charity.donor", string="Donor", required=True)
    amount = fields.Float(string="Donation Amount", required=True)
    currency = fields.Char(string="Currency", default="AED")
    date = fields.Date(string="Donation Date", default=fields.Date.context_today)
    status = fields.Selection([
        ("pending", "Pending"),
        ("completed", "Completed"),
        ("failed", "Failed"),
    ], default="pending", required=True, string="Status")

    organization = fields.Char(string="Organization")
    is_anonymous = fields.Boolean(string="Hide Donor Name")
    note = fields.Text(string="Note")

    project_id = fields.Many2one("charity.project", string="Project / Campaign")
    distribution_ids = fields.One2many("charity.distribution", "donation_id", string="Distributions")

    @api.constrains("amount")
    def _check_amount_positive(self):
        for rec in self:
            if rec.amount <= 0:
                raise ValidationError(_("Donation amount must be positive."))
