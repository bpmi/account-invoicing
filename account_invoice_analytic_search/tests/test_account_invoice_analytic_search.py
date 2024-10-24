# Copyright 2023 ForgeFlow S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase


class TestAccountMove(TransactionCase):
    def setUp(self):
        super(TestAccountMove, self).setUp()
        self.account_invoice = self.env["account.move"]
        self.account_model = self.env["account.account"]
        self.account_invoice_line = self.env["account.move.line"]
        self.analytic_account = self.env["account.analytic.account"]
        self.partner_2 = self.env.ref("base.res_partner_2").id
        self.product_4 = self.env.ref("product.product_product_4").id
        self.type_receivable = self.env.ref("account.data_account_type_receivable")
        self.type_expenses = self.env.ref("account.data_account_type_expenses")
        self.invoice_line_account = self.account_model.search(
            [("user_type_id", "=", self.type_expenses.id)], limit=1
        ).id
        self.analytic_account = self.analytic_account.create(
            {"name": "Test Account", "code": "TA"}
        )
        self.invoice = self.account_invoice.create(
            {
                "partner_id": self.partner_2,
                "move_type": "in_invoice",
            }
        )
        self.account_invoice_line.create(
            {
                "product_id": self.product_4,
                "quantity": 1.0,
                "debit": 0.0,
                "credit": 0.0,
                "move_id": self.invoice.id,
                "name": "product that cost 100",
                "account_id": self.invoice_line_account,
                "analytic_account_id": self.analytic_account.id,
            }
        )
        self.account_invoice_line.create(
            {
                "product_id": self.product_4,
                "quantity": 1.0,
                "debit": 0.0,
                "credit": 0.0,
                "move_id": self.invoice.id,
                "name": "product that cost 10",
                "account_id": self.invoice_line_account,
                "analytic_account_id": self.analytic_account.id,
            }
        )

    def test_search_analytic_accounts(self):
        self.invoice_search = self.account_invoice._search_analytic_accounts(
            "ilike", "Test Account"
        )
        invoice_id = self.account_invoice.search(self.invoice_search)
        self.assertEqual(invoice_id.invoice_line_ids, self.invoice.invoice_line_ids)
