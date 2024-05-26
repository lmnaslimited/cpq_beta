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
                rf"(\S+)\s+{escaped_attribute}",  # e.g., "value attribute"
                rf"{escaped_attribute}\s+is\s+(\S+)",  # e.g., "attribute is value"
                rf"with\s+{escaped_attribute}\s+(\S+)",  # e.g., "with attribute value"
                rf"^{escaped_attribute}\s+(\S+)",  # e.g., "attribute value" at the start of the line
                rf"{escaped_attribute}\s+as\s+(\S+)",  # e.g., "attribute as value"
                rf"\b{escaped_attribute}\b\s*[:=]\s*(\S+)",  # e.g., "attribute: value" or "attribute = value"     
                rf"{escaped_attribute}\s+can\s+be\s+(\S+)",  # e.g., "attribute can be value"
            ]
            for pattern in patterns:
                match = re.search(pattern, line, re.IGNORECASE)
                if match:
                    value = match.group(1)
                   
                    # Check if the value is not a negative word
                    negative_words = ['not', 'is', 'isn\'t', 'doesn\'t','and', 'the', 'a', 'was', 'were']
                    if value.lower() not in negative_words:
                        if attribute not in attributes:
                            attributes[attribute.strip()] = value.strip()
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

    if not items:
        return []

    # Fetch item prices and join them with items
    item_names = [item['name'] for item in items]
    item_prices = frappe.get_all('Item Price', filters={'item_code': ['in', item_names]}, fields=['item_code', 'price_list_rate'])

    # Create a dictionary to map item codes to their prices
    item_price_map = {item['item_code']: item['price_list_rate'] for item in item_prices}

    # Append the price to the item details
    for item in items:
        item['price'] = item_price_map.get(item['name'], 'Price not available')


    return items