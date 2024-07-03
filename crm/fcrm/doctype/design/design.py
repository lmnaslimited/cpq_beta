# Copyright (c) 2024, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import json
import frappe
from frappe import _
from frappe.model.document import Document

class Design(Document):
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
                'label': 'Status',
                'type': 'Data',
                'key': 'status',
                'width': '12rem',
            },
            {
                'label': 'Last Modified',
                'type': 'Datetime',
                'key': 'modified',
                'width': '8rem',
            }
        ]
		rows = [
            "name",
			"status",
            "modified"
        ]
		return {'columns': columns, 'rows': rows}