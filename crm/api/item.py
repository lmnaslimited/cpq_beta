import frappe
from frappe import _

@frappe.whitelist()
def get_item(name):
    try:
        # Fetch item details from the database
        item = frappe.get_doc("Item", name)
        # Customize the response data as needed
        item_data = {
            "name": item.name,
            "item_group": item.item_group,
            # Add more fields as needed
        }
        return item_data
    except Exception as e:
        frappe.log_error(_("Error fetching item data: {0}").format(e))
        frappe.throw(_("Error fetching item data"))
