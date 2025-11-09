# -*- coding: utf-8 -*-
from datetime import date
from odoo import api, fields, models, _
from odoo.exceptions import UserError # type: ignore

class CharityCrisis(models.Model):
    _name = "charity.crisis"
    _description = "Humanitarian Crisis (Top Issues)"
    _order = "severity desc, last_update desc, id desc"

    name = fields.Char(required=True, help="Crisis title, e.g., Gaza Humanitarian Emergency")
    country = fields.Char()
    category = fields.Selection([
        ("food", "Food"),
        ("health", "Healthcare"),
        ("shelter", "Shelter"),
        ("education", "Education"),
        ("water", "Water & Sanitation"),
        ("other", "Other"),
    ], default="other")
    severity = fields.Selection([
        ("3", "Critical"),
        ("2", "High"),
        ("1", "Medium"),
    ], default="2", string="Severity")
    last_update = fields.Datetime(string="Last Update")
    summary = fields.Text()
    url = fields.Char(string="Reference Link")
    status = fields.Selection([
        ("active", "Active"),
        ("monitor", "Monitoring"),
        ("resolved", "Resolved"),
    ], default="active")

    project_id = fields.Many2one("charity.project", string="Created Project")
    has_project = fields.Boolean(compute="_compute_has_project")

    @api.depends("project_id")
    def _compute_has_project(self):
        for r in self:
            r.has_project = bool(r.project_id)

    # --- Buttons ---

    def action_create_project(self):
        """Create a charity.project from this crisis (if not already created)."""
        for r in self:
            if r.project_id:
                raise UserError(_("A project already exists for this crisis."))
            proj_vals = {
                "name": r.name,
                "description": (r.summary or "")[:1024],
                "start_date": date.today(),
                "end_date": False,
                # map category if your project model has Selection/Char field 'category'
                "category": r.category if "category" in self.env["charity.project"]._fields else False,
            }
            proj = self.env["charity.project"].create(proj_vals)
            r.project_id = proj.id
        return True

    def action_load_sample_data(self):
        """Seed a few high-signal crises so the UI is useful immediately (no APIs)."""
        samples = [
            {
                "name": "Gaza Humanitarian Emergency",
                "country": "Palestine",
                "category": "food",
                "severity": "3",
                "summary": "Escalating needs in food, medical aid and shelter.",
                "status": "active",
                "url": "https://reliefweb.int/",
            },
            {
                "name": "Sudan Food Insecurity",
                "country": "Sudan",
                "category": "food",
                "severity": "3",
                "summary": "Critical hunger and displacement across multiple states.",
                "status": "active",
                "url": "https://reliefweb.int/",
            },
            {
                "name": "Yemen Health System Strain",
                "country": "Yemen",
                "category": "health",
                "severity": "2",
                "summary": "Outbreak risks and medicine shortages persist.",
                "status": "monitor",
                "url": "https://reliefweb.int/",
            },
        ]
        for s in samples:
            if not self.search([("name", "=", s["name"])]):
                self.create(s)
        return True
