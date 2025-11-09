# -*- coding: utf-8 -*-
from odoo import models, fields, api

class CharityDonor(models.Model):
    _name = "charity.donor"
    _description = "Donor (Individual or Company)"
    _rec_name = "public_name"
    _order = "create_date desc"

    # Enable Archive instead of delete
    active = fields.Boolean(default=True)

    # Basic Info
    name = fields.Char(required=True, string="Donor Name")
    is_company = fields.Boolean(string="Is a Company?")
    organization = fields.Char(string="Organization")
    hide_name = fields.Boolean(string="Show as Anonymous")

    # Relations (ondelete is controlled by the Many2one on charity.donation.donor_id)
    donation_ids = fields.One2many(
        "charity.donation",
        "donor_id",
        string="Donations",
    )

    # Computed
    total_donated = fields.Float(
        string="Total Donated",
        compute="_compute_total_donated",
        store=True,
    )
    public_name = fields.Char(
        string="Public Name",
        compute="_compute_public_name",
        store=True,
    )

    @api.depends("donation_ids.amount", "donation_ids.status")
    def _compute_total_donated(self):
        for donor in self:
            donor.total_donated = sum(
                d.amount for d in donor.donation_ids if d.status == "completed"
            )

    @api.depends("name", "hide_name")
    def _compute_public_name(self):
        for donor in self:
            donor.public_name = "Anonymous" if donor.hide_name else (donor.name or "Unknown")
