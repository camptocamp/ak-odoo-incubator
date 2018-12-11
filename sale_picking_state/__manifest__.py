# -*- coding: utf-8 -*-
# Copyright 2018 Akretion (http://www.akretion.com).
# @author Pierrick BRUN <pierrick.brun@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Sale Picking State",
    "summary": "Show the picking state on the sale order",
    "version": "10.0.1.0.0",
    "category": "Product",
    "website": "www.akretion.com",
    "author": " Akretion",
    "license": "AGPL-3",
    "depends": ["sale"],
    "data": [
        "views/sale_order_views.xml",
    ],
    "demo": [
        "demo/sale_demo.xml",
    ],
    "installable": True,
}