import ast

def restructure_llm_output(raw_data, video_info):
    # Remove Markdown code block syntax if present
    if raw_data.startswith("```") and raw_data.endswith("```"):
        lines = raw_data.split('\n')
        json_like_data = '\n'.join(lines[1:-1])
    else:
        json_like_data = raw_data

    
    # Parse the string as a Python literal
    data = ast.literal_eval(json_like_data)

    # Create the new structure
    restructured_data = {
        "title": data.get("title", ""),
        "shortDescription": data.get("shortDescription", ""),
        "subtopics": {},
        "sources" : video_info
    }

    # Move all other keys into subtopics
    for key, value in data.items():
        if key not in ["title", "shortDescription"]:
            restructured_data["subtopics"][key] = value

    return restructured_data