# -*- coding: utf-8 -*-
# © 2018 Pierrick Brun @ Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from datetime import datetime

from odoo.tests.common import TransactionCase


class Tests(TransactionCase):
    def setUp(self):
        super(Tests, self).setUp()
        self.wizard_obj = self.env["wizard.update.invoice.supplierinfo"]
        self.supplierinfo_obj = self.env["product.supplierinfo"]
        self.invoice_model = self.env["account.invoice"]
        journal_model = self.env["account.journal"]
        self.journal = journal_model.search([("type", "=", "sale")], limit=1)
        self.product1 = self.env.ref("product.product_product_4b")
        self.product2 = self.env.ref("product.product_delivery_01")
        self.prod_account = self.env.ref("account.demo_coffee_machine_account")
        unit = self.env.ref("product.product_uom_unit")

        self.invoice = self.invoice_model.create(
            {
                "journal_id": self.journal.id,
                "partner_id": self.env.ref("base.res_partner_12").id,
                "account_id": self.env["account.account"]
                .search([("user_type_id.type", "=", "payable")], limit=1)
                .id,
                "date_invoice": "%s-01-01" % datetime.now().year,
                "invoice_line_ids": [
                    (
                        0,
                        0,
                        {
                            "product_id": self.product1.id,
                            "name": "iPad Retina Display",
                            "quantity": 10.0,
                            "price_unit": 400.0,
                            "uom_id": unit.id,
                            "account_id": self.prod_account.id,
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "name": "line without product",
                            "quantity": 1.0,
                            "price_unit": 35.0,
                            "uom_id": unit.id,
                            "account_id": self.prod_account.id,
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "product_id": self.product2.id,
                            "name": "product supplier info" " to update",
                            "quantity": 1.0,
                            "price_unit": 10.0,
                            "uom_id": unit.id,
                            "account_id": self.prod_account.id,
                        },
                    ),
                ],
            }
        )

    def test_update_standard_price_on_product_product(self):
        vals_wizard = self.invoice.check_supplierinfo().get("context", {})

        line_ids = vals_wizard.get("default_line_ids", {})
        invoice_id = vals_wizard.get("default_invoice_id", {})

        self.assertEquals(len(line_ids), 2)
        self.assertEquals(line_ids[0][2]["current_price"], False)
        self.assertEquals(line_ids[0][2]["new_price"], 400.0)

        # Create and launch update process
        wizard = self.wizard_obj.create(
            {"line_ids": line_ids, "invoice_id": invoice_id}
        )
        self.assertEquals(wizard.line_ids[1].new_price, 10.0)
        wizard.update_supplierinfo()

        self.assertEquals(self.product1.standard_price, 400.0)
        self.assertEquals(self.product2.standard_price, 10.0)
