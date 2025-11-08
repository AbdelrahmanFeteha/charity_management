# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError # type: ignore

class CharityDistribution(models.Model):
    _name = "charity.distribution"
    _description = "Distribution (Outgoing to Requests)"
    _order = "date desc, id desc"

    project_id = fields.Many2one("charity.project", string="Project / Campaign")
    request_id = fields.Many2one("charity.request", string="Request", required=True)
    donation_id = fields.Many2one("charity.donation", string="Source Donation")
    amount = fields.Float(string="Amount", required=True)
    date = fields.Date(string="Distribution Date", default=fields.Date.context_today)

    @api.constrains("amount")
    def _check_amount_positive(self):
        for rec in self:
            if rec.amount <= 0:
                raise ValidationError(_("Distribution amount must be positive."))

    @api.onchange("request_id")
    def _onchange_request_id(self):
        if self.request_id and not self.project_id:
            self.project_id = self.request_id.project_id
