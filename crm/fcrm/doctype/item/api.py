
import frappe
from frappe import _

from crm.api.doc import get_doctype_fields, get_assigned_users
from crm.fcrm.doctype.crm_form_script.crm_form_script import get_form_script

@frappe.whitelist()
def get_item(name):
  Item = frappe.qb.DocType("Item")

  query = frappe.qb.from_(Item).select("*").where(Item.name == name).limit(1)

  item = query.run(as_dict=True)
  if not len(item):
    frappe.throw(_("Item not found"), frappe.DoesNotExistError)
  item = item.pop()

  item["doctype_fields"], item["all_fields"] = get_doctype_fields("item", name)
  item["doctype"] = "Item"
  item["_form_script"] = get_form_script('Item')
  item["_assign"] = get_assigned_users("Item", item.name)
  return item