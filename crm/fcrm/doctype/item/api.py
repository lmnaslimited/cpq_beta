
# import frappe
# from frappe import _

# from crm.api.doc import get_doctype_fields, get_assigned_users
# from crm.fcrm.doctype.crm_form_script.crm_form_script import get_form_script

# @frappe.whitelist()
# def get_item(name):
#   Item = frappe.qb.DocType("Item")

#   query = frappe.qb.from_(Item).select("*").where(Item.name == name).limit(1)

#   item = query.run(as_dict=True)
#   if not len(item):
#     frappe.throw(_("Item not found"), frappe.DoesNotExistError)
#   item = item.pop()

#   item["doctype_fields"], item["all_fields"] = get_doctype_fields("item", name)
#   item["doctype"] = "Item"
#   item["_form_script"] = get_form_script('Item')
#   item["_assign"] = get_assigned_users("Item", item.name)
#   return item

import frappe
from frappe import _

from crm.api.doc import get_doctype_fields, get_assigned_users
from crm.fcrm.doctype.crm_form_script.crm_form_script import get_form_script

@frappe.whitelist()
def get_item(name):
    Item = frappe.qb.DocType("Item")
    ItemPrice = frappe.qb.DocType("Item Price")

    # Fetch the item details
    query = frappe.qb.from_(Item).select("*").where(Item.name == name).limit(1)
    item = query.run(as_dict=True)
    if not len(item):
        frappe.throw(_("Item not found"), frappe.DoesNotExistError)
    item = item.pop()

    # Fetch the item price list details
    price_query = (
        frappe.qb.from_(ItemPrice)
        .select(ItemPrice.price_list, ItemPrice.price_list_rate, ItemPrice.currency)
        .where(ItemPrice.item_code == item["item_code"])
    )
    prices = price_query.run(as_dict=True)

    # Fetch the item variant attributes
    variant_attributes = frappe.get_all(
        'Item Variant Attribute',
        filters={'parent': item['name']},
        fields=['*']
    )

    # Fetch variants if the item is a template
    variants = []
    if item.get('has_variants') and not item.get('variant_of'):
        variants_query = frappe.qb.from_(Item).select("*").where(Item.variant_of == name)
        variants = variants_query.run(as_dict=True)

    # Add additional details to the item
    item["doctype_fields"], item["all_fields"] = get_doctype_fields("Item", name)
    item["doctype"] = "Item"
    item["_form_script"] = get_form_script('Item')
    item["_assign"] = get_assigned_users("Item", item["name"])
    item["prices"] = prices
    item["variant_attributes"] = variant_attributes
    item["variants"] = variants

    # Log the response for debugging
    frappe.logger().info(f"get_item response: {item}")

    return item
