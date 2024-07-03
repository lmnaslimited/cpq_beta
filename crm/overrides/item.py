# import frappe
from frappe import _
from erpnext.stock.doctype.item.item import Item


class CustomItem(Item):
	@staticmethod
	def default_list_data():
		columns = [
            {
                'label': 'Name',
                'type': 'Data',
                'key': 'item_name',
                'width': '16rem',
            },
            {
                'label': 'Item Code',
                'type': 'Data',
                'key': 'item_code',
                'width': '16rem',
            },
			{
                'label': 'Status',
                'type': 'Data',
                'key': 'status',
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
                'width': '20rem',
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