import json

def is_list_of_strings(obj):
    return isinstance(obj, list) and all(isinstance(item, str) for item in obj)

def restructure_data(input_data, video_info):
    
    output = {
        "title": "",
        "shortDescription": "",
        "subtopics": {},
        "sources" : video_info,
    }
    
    # Identify and categorize fields
    string_fields = []
    list_fields = []
    other_fields = []
    
    for key, value in input_data.items():
        if isinstance(value, str):
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
            output["subtopics"][key] = [value]
        elif is_list_of_strings(value):
            output["subtopics"][key] = value
        else:
            # For other types, convert to string and wrap in a list
            output["subtopics"][key] = [str(value)]
    
    return output


