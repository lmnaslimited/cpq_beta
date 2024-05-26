import re
import frappe

@frappe.whitelist()
def get_items_with_attributes_from_content(content):
    # Extract attributes from content
    search_attributes = extract_attributes_from_content(content)

    # Query items with the extracted attributes
    items = []
    if search_attributes:
        items = get_items_with_attributes(search_attributes)

    return {
        "attributes": search_attributes if search_attributes else {},
        "items": items if items else []
    }

def extract_attributes_from_content(content):
    # Fetch all item variant attributes
    variant_attributes = frappe.get_all('Item Variant Attribute', fields=["attribute"])
    # Convert the list of dicts to a list of attribute names
    attribute_names = [attr['attribute'] for attr in variant_attributes]

    attributes = {}
    for line in content:
        for attribute in attribute_names:
            # Escape special characters in the attribute name for regex
            escaped_attribute = re.escape(attribute)
            # Define patterns to search for the attribute value
            patterns = [
                rf"{escaped_attribute}\s*:\s*(\S+)",  # e.g., "attribute: value"
                rf"{escaped_attribute}\s+is\s+(\S+)",  # e.g., "attribute is value"
                rf"with\s+{escaped_attribute}\s+(\S+)",  # e.g., "with attribute value"
                rf"^{escaped_attribute}\s+(\S+)",  # e.g., "attribute value" at the start of the line
                rf"{escaped_attribute}\s+as\s+(\S+)",  # e.g., "attribute as value"
                rf"\b{escaped_attribute}\b\s*[:=]\s*(\S+)",  # e.g., "attribute: value" or "attribute = value"
            ]
            for pattern in patterns:
                match = re.search(pattern, line, re.IGNORECASE)
                if match:
                    value = match.group(1)
                    attributes[attribute] = value
                    break  # Stop if a match is found
    return attributes

def get_items_with_attributes(search_attributes):
    subqueries = []
    params = []
    
    # Build subqueries for each attribute
    for attribute, value in search_attributes.items():
        subquery = """
            SELECT parent AS name
            FROM `tabItem Variant Attribute`
            WHERE attribute = %s AND attribute_value = %s
        """
        subqueries.append(subquery)
        params.extend([attribute, value])
    
    # Join the subqueries using INTERSECT
    query = " INTERSECT ".join(subqueries)
    
    # Execute the query
    items = frappe.db.sql(query, tuple(params), as_dict=True)

    return items