
import frappe
from frappe import _

from crm.api.doc import get_doctype_fields, get_assigned_users
from crm.fcrm.doctype.crm_form_script.crm_form_script import get_form_script

@frappe.whitelist()
def get_design(name):
  Design = frappe.qb.DocType("Design")

  query = frappe.qb.from_(Design).select("*").where(Design.name == name).limit(1)

  design = query.run(as_dict=True)
  if not len(design):
    frappe.throw(_("Design not found"), frappe.DoesNotExistError)
  design = design.pop()

  design["doctype_fields"], design["all_fields"] = get_doctype_fields("Design", name)
  design["doctype"] = "Design"
  design["_form_script"] = get_form_script('Design')
  design["_assign"] = get_assigned_users("Design", design.name)
  return design