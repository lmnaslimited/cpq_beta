# import frappe
from frappe import _
from erpnext.selling.doctype.quotation.quotation import Quotation


class CustomQuotation(Quotation):
	@staticmethod
	def default_list_data():
		columns = [
			{
				'label': 'Name',
				'type': 'Data',
				'key': 'name',
				'width': '17rem',
			},
			{
				'label': 'Grand Total',
				'type': 'Data',
				'key': 'grand_total',
				'width': '12rem',
			},
			{
				'label': 'Customer Name',
				'type': 'data',
				'key': 'customer_name',
				'width': '12rem',
			},
			{
				'label': 'Status',
				'type': 'Data',
				'key': 'status',
				'width': '12rem',
			},
			{
				'label': 'Person Responsible',
				'type': 'Link',
				'key': 'custom_person_responsible',
				'width': '12rem',
			},
			{
				'label': 'Project Name',
				'type': 'Data',
				'key': 'custom_project_name',
				'width': '12rem',
			},
		]
		rows = [
			"name",
			"grand_total",
			"customer_name",
			"status",
			"custom_person_responsible",
			"custom_project_name",
		]
		return {'columns': columns, 'rows': rows}
