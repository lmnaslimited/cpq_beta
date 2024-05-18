
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

@frappe.whitelist()
def get_item_variant():
  item_variant = frappe.get_list("Item", filters={"has_variants": 1})
  item_names = [item['name'] for item in item_variant]
  return item_names

@frappe.whitelist(allow_guest=True)
def save_design(data):
    try:
        data = frappe.parse_json(data)
        
        # Define the doctype where the dynamic fields will be added
        doctype = "Design"  # Replace with your actual DocType

        # Check for each field in data if it exists in the doctype
        meta = frappe.get_meta(doctype)
        for fieldname, value in data.items():
            if not meta.has_field(fieldname):
                # Add the field to the doctype
                frappe.get_doc({
                    "doctype": "Custom Field",
                    "dt": doctype,
                    "fieldname": fieldname,
                    "label": fieldname.replace("_", " ").title(),
                    "fieldtype": "Data",  # You can customize the fieldtype based on your needs
                }).insert(ignore_permissions=True)
                frappe.clear_cache(doctype=doctype)  # Clear cache to reflect new fields

        # Create a new document for your target DocType
        doc = frappe.get_doc({
            "doctype": doctype,
            **data  # Spread the dynamic fields into the new document
        })

        # Save the document to the database
        doc.insert()
        frappe.db.commit()

        return {
            "status": "success",
            "message": _("Document saved successfully"),
            "docname": doc.name
        }
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), _("Failed to save design"))
        return {
            "status": "error",
            "message": str(e)
        }
