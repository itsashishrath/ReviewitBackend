import json
import re
import ast

def safe_eval(s):
    try:
        return ast.literal_eval(s)
    except:
        return s

def extract_key_value_pairs(text):
    # This regex looks for patterns like "'key': value" or "key: value"
    pattern = r"(?:['\"]?([^:\n'\"]+)['\"]?:\s*([^,\n}]+))"
    matches = re.findall(pattern, text)
    return {k.strip(): safe_eval(v.strip()) for k, v in matches}

def is_list_of_strings(obj):
    return isinstance(obj, list) and all(isinstance(item, str) for item in obj)

def restructure_data(input_data):
    # If input_data is a string, try to parse it
    if isinstance(input_data, str):
        try:
            input_data = json.loads(input_data)
        except json.JSONDecodeError:
            # If JSON parsing fails, try to extract key-value pairs
            input_data = extract_key_value_pairs(input_data)

    output = {
        "title": "",
        "shortDescription": "",
        "subtopics": {}
    }
    
    # Identify and categorize fields
    string_fields = []
    list_fields = []
    other_fields = []
    
    for key, value in input_data.items():
        if isinstance(value, str):
            # Check if the string value looks like a list
            if value.strip().startswith('[') and value.strip().endswith(']'):
                try:
                    value = safe_eval(value)
                    if is_list_of_strings(value):
                        list_fields.append(key)
                        input_data[key] = value  # Update the input_data with the parsed list
                        continue
                except:
                    pass
            string_fields.append(key)
        elif is_list_of_strings(value):
            list_fields.append(key)
        else:
            other_fields.append(key)
    
    # Assign title and shortDescription
    if "title" in string_fields:
        output["title"] = input_data["title"]
        string_fields.remove("title")
    elif string_fields:
        output["title"] = input_data[string_fields[0]]
        string_fields = string_fields[1:]
    
    if "shortDescription" in string_fields:
        output["shortDescription"] = input_data["shortDescription"]
        string_fields.remove("shortDescription")
    elif string_fields:
        output["shortDescription"] = input_data[string_fields[0]]
        string_fields = string_fields[1:]
    
    # Assign remaining fields to subtopics
    for key in list_fields + string_fields + other_fields:
        value = input_data[key]
        if isinstance(value, str):
            # Try to parse string values that look like lists
            if value.strip().startswith('[') and value.strip().endswith(']'):
                try:
                    parsed_value = safe_eval(value)
                    if is_list_of_strings(parsed_value):
                        output["subtopics"][key] = parsed_value
                        continue
                except:
                    pass
            output["subtopics"][key] = [value]
        elif is_list_of_strings(value):
            output["subtopics"][key] = value
        else:
            # For other types, convert to string and wrap in a list
            output["subtopics"][key] = [str(value)]
    
    return output

# Test the function with various input formats, including potential syntax errors
test_inputs = [
    # Well-formed dictionary
    {
        "title": "Google Pixel 9 Pro Review",
        "shortDescription": "Latest flagship smartphone from Google.",
        "Camera Quality": ["Great main camera", "Improved ultrawide"],
        "Battery Life": "Excellent all-day battery",
        "Performance": 95,
        "Pros": ["Fast charging", "Water resistant"],
        "Cons": ["Expensive", "Large camera bump"]
    },
    # String with syntax errors
    """
    {
        'Product Name': 'iPhone 15 Pro',
        'Overview': "Apple's latest premium smartphone.",
        'Camera': 'Triple-lens system with LiDAR',
        'Battery': ['All-day battery life', 'Fast charging supported',
        'Processor': 'A16 Bionic chip',
        'Advantages': ['Powerful performance', 'Premium build quality'],
        'Disadvantages': 'High price point'
    """,
    # String with lists represented as strings
    """
    {
        'title': 'Samsung Galaxy S22 Review',
        'shortDescription': 'Samsung's latest flagship phone',
        'Display': '6.1-inch Dynamic AMOLED 2X',
        'Camera': "['50MP wide', '12MP ultrawide', '10MP telephoto']",
        'Battery': '3,700 mAh',
        'Pros': "['Compact design', 'Bright display', 'Versatile camera system']",
        'Cons': "['Average battery life', 'Slower charging than competitors']"
    }
    """,

    """
    {
        'title': 'Google Pixel 9 Pro Review', 
        'shortDescription': 'The Google Pixel 9 Pro is the latest flagship smartphone from Google boasting significant improvements in hardware, software, and AI features, making it a compelling contender in the high-end market.',
        'Camera Quality':[  'The camera bump is significantly larger than previous models, offering a triple camera system with a 50MP main camera, a 48MP ultrawide camera, and a 48MP 5x telephoto camera (1, 3).',
                            'Add Me feature allows the user to be included in group photos by taking multiple photos and merging them (2).', 
                            'The main camera sensor is larger than the Pixel 8 Pro, potentially resulting in shallower depth of field (2).', 
                    'Google has redesigned the HDR Plus image pipeline for improved photo quality (1).', 
                    'Video boost allows videos to be upscaled to 8K and captures 30MP stills from videos (1).', 
                    'The front-facing camera has been upgraded to 42MP, significantly higher than the Pixel 8 Pro (1).', 
                    'The camera system is said to be better at maintaining consistent colors across lenses while filming videos (1).'], 
        'Battery Life': [
                    'The Pixel 9 Pro XL boasts a longer battery life thanks to a dual-chip architecture, offering up to 36 hours in battery saver mode (2).'], 
        'Performance': ['The Pixel 9 Pro utilizes the new Tensor G4 chip, which is more powerful and efficient, leading to faster web browsing and app launching (2).', 
                'Gemini Live allows for conversations with the assistant, providing a more interactive experience (2).'], 
        'Build Quality': ['The Pixel 9 Pro features a flat-edged design with polished glass back and matte metal sides (2).', 
                  'The phone feels heavier than previous models, giving it a more solid feel (2).', 
                  'The Pixel 9 Pro is made from 100 recycled aluminum, making it more environmentally friendly (3).', 
                  'The phone features Gorilla Glass Victus 2, offering improved scratch resistance (3).', 
                  'The Pixel 9 Pro XL boasts a high level of durability, passing a bend test with minimal flex (3).', 
                  'The camera bump is extremely large, prompting concerns about its size and functionality (3).'], 
        'Display': ['The Pixel 9 Pro features a 6.8-inch, 120Hz Super Actua display, with a peak brightness of 3,000 nits (3).', 
            'The display is extremely bright and resilient to heat (3).', 
            'The Pixel 9 Pro Fold offers a 6.3-inch outer screen and an 8-inch inner screen, both brighter than previous models (2).', 
            'The Pixel 9 Pro Fold features thin bezels and a premium design with soft-touch matte glass and metal rails (2).'], 
        'Pros': ['Improved camera features and performance (1, 2).', 'Faster performance with the new Tensor G4 chip (2).', 
         'Enhanced AI features, including Gemini Live and Pixel Studio (2).', 
         'More durable design with flat edges and Gorilla Glass Victus 2 (2, 3).', 
         'Brighter and larger displays on both the Pixel 9 Pro and Pixel 9 Pro Fold (2, 3).', 
         'Longer battery life in the Pixel 9 Pro XL thanks to dual-chip architecture (2).', 
         'Improved hardware design with a more premium feel (2).'], 
        'Cons': ['The camera bump is extremely large and could be a potential issue for users (3).', 
         'The Pixel 9 Pro Fold's camera bump is even larger than the regular Pixel 9 Pro (2).', 
         'The phone is expensive, with the Pixel 9 Pro starting at $999 (2).', 
         'The Pixel 9 Pro Fold is priced at $1,799, which is comparable to other foldable phones (2).',
        'The lack of an SD card slot in the Pixel 9 Pro (3).', 
        'Some users may find the button placement to be unusual (3).'], 

        'Overall': 'The Google Pixel 9 Pro is a significant improvement over its predecessor, offering compelling features and performance. The phone boasts a strong camera system, a powerful processor, and impressive AI capabilities. However, the large camera bump and the phone's high price tag might be drawbacks for some users. Overall, the Pixel 9 Pro is a powerful and well-rounded flagship smartphone that is sure to appeal to a wide range of users.'
    }
    """
]

for i, test_input in enumerate(test_inputs, 1):
    print(f"\nTest Input {i}:")
    print(test_input)
    print("\nRestructured Output:")
    restructured = restructure_data(test_input)
    print(json.dumps(restructured, indent=2))