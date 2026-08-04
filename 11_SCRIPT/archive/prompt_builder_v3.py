from core.template_loader import load_template


def build_prompt(reading):

    role = load_template("templates/role.txt")
    structure = load_template("templates/structure.txt")
    language = load_template("templates/language.txt")
    output = load_template("templates/output.txt")
    json_rule = load_template("templates/json.txt")
    schema = load_template("schemas/response_schema.txt")

    return f"""
{role}

{structure}

{language}

{output}

{json_rule}

{schema}

TODAY'S READING

Date:
{reading.date}

Reading I:
{reading.reading1}

Reading II:
{reading.reading2 or "None"}

Gospel:
{reading.gospel}
"""