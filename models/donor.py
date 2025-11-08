# -*- coding: utf-8 -*-
from odoo import models, fields, api

class CharityDonor(models.Model):
    _name = "charity.donor"
    _description = "Donor (Individual or Company)"
    _rec_name = "display_name"
    _order = "create_date desc"

    # Basic Info
    name = fields.Char(required=True, string="Donor Name")
    is_company = fields.Boolean(string="Is a Company?")
    organization = fields.Char(string="Organization")
    hide_name = fields.Boolean(string="Show as Anonymous")

    # Relations
    donation_ids = fields.One2many("charity.donation", "donor_id", string="Donations")

    # Computed
    total_donated = fields.Float(string="Total Donated", compute="_compute_total_donated", store=True)
    display_name = fields.Char(string="Display Name", compute="_compute_display_name", store=True)

    @api.depends("donation_ids.amount", "donation_ids.status")
    def _compute_total_donated(self):
        for donor in self:
            donor.total_donated = sum(d.amount for d in donor.donation_ids if d.status == "completed")

    @api.depends("name", "hide_name")
    def _compute_display_name(self):
        for donor in self:
            donor.display_name = "Anonymous" if donor.hide_name else (donor.name or "Unknown")
