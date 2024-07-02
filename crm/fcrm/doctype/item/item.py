# Copyright (c) 2024, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document

class Item(Document):
    @staticmethod
    def default_list_data():
        columns = [
            {
                'label': 'Name',
                'type': 'Data',
                'key': 'item_name',
                'width': '12rem',
            },
            {
                'label': 'Item Code',
                'type': 'Data',
                'key': 'item_code',
                'width': '12rem',
            },
            {
                'label': 'Variant Of',
                'type': 'Link',
                'key': 'variant_of',
                'options': 'Item',
                'width': '8rem',
            },
            {
                'label': 'Item Group',
                'type': 'Link',
                'key': 'item_group',
                'options': 'Item Group',
                'width': '12rem',
            },
            {
                'label': 'Last Modified',
                'type': 'Datetime',
                'key': 'modified',
                'width': '8rem',
            },
        ]
        rows = [
            "name",
            "item_name",
            "item_code",
            "variant_of",
            "item_group",
            "modified",
        ]
        return {'columns': columns, 'rows': rows}