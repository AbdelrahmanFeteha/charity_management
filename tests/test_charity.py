# -*- coding: utf-8 -*-
from odoo.tests import TransactionCase, tagged

@tagged('post_install', '-at_install')
class TestCharityBasics(TransactionCase):

    def setUp(self):
        super().setUp()
        self.Project = self.env['charity.project']
        self.Request = self.env['charity.request']
        self.Donor = self.env['charity.donor']
        self.Donation = self.env['charity.donation']
        self.Distribution = self.env['charity.distribution']

    def test_funding_flow(self):
        proj = self.Project.create({'name': 'Test Campaign'})
        req = self.Request.create({
            'requester_name': 'Tester',
            'category': 'food',
            'amount_requested': 100.0,
            'status': 'approved',
            'project_id': proj.id,
        })
        donor = self.Donor.create({'name': 'Alice'})
        don = self.Donation.create({
            'donor_id': donor.id,
            'amount': 120.0,
            'status': 'completed',
            'project_id': proj.id,
        })
        self.Distribution.create({
            'project_id': proj.id,
            'request_id': req.id,
            'donation_id': don.id,
            'amount': 60.0,
        })

        req.invalidate_recordset()   # refresh computed
        proj.invalidate_recordset()

        self.assertEqual(req.amount_funded, 60.0)
        self.assertEqual(round(req.funding_progress, 2), 60.00)
        self.assertEqual(round(proj.total_distributed, 2), 60.00)
        self.assertEqual(round(proj.total_donations, 2), 120.00)
        self.assertEqual(round(proj.funding_progress, 2), 0.00 if proj.total_requested == 0 else round(60.0 / req.amount_requested * 100.0, 2))
