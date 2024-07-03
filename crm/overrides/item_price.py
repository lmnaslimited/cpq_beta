# import frappe
from frappe import _
from erpnext.stock.doctype.item_price.item_price import ItemPrice


class CustomItemPrice(ItemPrice):
	@staticmethod
	def default_list_data():
		columns = [
            {
                'label': 'Item Code',
                'type': 'Data',
                'key': 'item_code',
                'width': '16rem',
            },
            {
                'label': 'Price List',
                'type': 'Link',
                'key': 'price_list',
                'width': '16rem',
            },
			{
                'label': 'Currency',
                'type': 'Link',
                'key': 'currency',
                'width': '12rem',
            },
            {
                'label': 'Rate',
                'type': 'Currency',
                'key': 'price_list_rate',
                'width': '8rem',
            },
            
        ]
		rows = [
            "item_code",
            "price_list",
            "currency",
            "price_list_rate",
        ]
		return {'columns': columns, 'rows': rows}