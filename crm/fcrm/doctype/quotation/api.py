import frappe
from frappe import _

from crm.api.doc import get_doctype_fields, get_assigned_users
from crm.fcrm.doctype.crm_form_script.crm_form_script import get_form_script

# @frappe.whitelist()
# def get_quotation(name):
#   Quotation = frappe.qb.DocType("Quotation")

#   query = frappe.qb.from_(Quotation).select("*").where(Quotation.name == name).limit(1)

#   quotation = query.run(as_dict=True)
#   if not len(quotation):
#     frappe.throw(_("Quotation not found"), frappe.DoesNotExistError)
#   quotation = quotation.pop()

#   quotation["doctype_fields"], quotation["all_fields"] = get_doctype_fields("Quotation", name)
#   quotation["doctype"] = "Quotation"
#   quotation["_form_script"] = get_form_script('Quotation')
#   quotation["_assign"] = get_assigned_users("Quotation", quotation.name)
#   return quotation

@frappe.whitelist()
def get_quotation(name):
    Quotation = frappe.qb.DocType("Quotation")

    # Fetch the Quotation document
    query = frappe.qb.from_(Quotation).select("*").where(Quotation.name == name).limit(1)
    quotation = query.run(as_dict=True)
    
    if not len(quotation):
        frappe.throw(_("Quotation not found"), frappe.DoesNotExistError)
    
    quotation = quotation.pop()

    # Fetch doctype fields and other metadata
    doctype_fields, all_fields = get_doctype_fields("Quotation", name)
    meta = frappe.get_meta("Quotation")

    # Initialize dictionaries to store metadata and data
    items_fields = []
    items_data = []

    # Find the 'items' table field in the doctype meta
    for field in meta.fields:
        if field.fieldname == 'items' and field.fieldtype == 'Table':
            child_table_name = field.options
            child_table_fields = frappe.get_meta(child_table_name).fields
            items_fields = [
                {
                    "fieldname": child_field.fieldname,
                    "fieldtype": child_field.fieldtype,
                    "label": child_field.label,
                    "hidden": child_field.hidden,
                    "reqd": child_field.reqd,
                    "options": child_field.options,
                    "read_only": child_field.read_only,
                    "placeholder": child_field.default,
                }
                for child_field in child_table_fields
            ]
            
            # Fetch actual data for the 'items' table
            items_data = frappe.get_all(child_table_name, filters={'parent': name}, fields=["*"])
            break

    # Add the items fields and data to the quotation dictionary
    quotation["items_fields"] = items_fields
    quotation["items_data"] = items_data

    # Optionally include other fields if needed
    quotation["doctype_fields"] = doctype_fields
    quotation["all_fields"] = all_fields
    quotation["doctype"] = "Quotation"
    quotation["_form_script"] = get_form_script('Quotation')
    quotation["_assign"] = get_assigned_users("Quotation", quotation.name)

    return quotation
@frappe.whitelist()
def get_item_variant():
  item_variant = frappe.get_list("Item", filters={"has_variants": 1})
  item_names = [item['name'] for item in item_variant]
  return item_names


@frappe.whitelist(allow_guest=True)
def save_quotation(data):
    try:
        data = frappe.parse_json(data)
        
        # Define the doctype where the dynamic fields will be added
        doctype = "Quotation"

        # Initialize dictionaries for main doc and child table data
        main_doc_data = {}
        child_table_data = []

        # Get the meta for the doctype
        meta = frappe.get_meta(doctype)

        for fieldname, field_info in data.items():
            value = field_info['value']

            # Check if the field is in the main doctype fields
            if meta.has_field(field_info['name']):
                main_doc_data[field_info['name']] = value
            else:
                # If the field is not in the main doctype, add it to the child table data
                # Use the field label as the key instead of the fieldname
                child_table_data.append({
                    'attribute': field_info['label'],  # Use label as the key
                    'attribute_value': value
                })

        # Create a new document for your target DocType
        doc = frappe.get_doc({
            "doctype": doctype,
            **main_doc_data
        })

        # Add attributes to the child table
        for child in child_table_data:
            doc.append('item_variant_attribute', child)

        # Save the document to the database
        doc.insert()
        frappe.db.commit()

        return {
            "status": "success",
            "message": _("Document saved successfully"),
            "docname": doc.name
        }
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), _("Failed to save quotation"))
        return {
            "status": "error",
            "message": str(e)
        }