from core.template_loader import load_template


def build_prompt(reading, part):

    role = load_template("templates/role.txt")
    language = load_template("templates/language.txt")
    output = load_template("templates/output.txt")

    part_prompt = load_template(f"templates/part{part}.txt")

    return f"""
{role}

{language}

{output}

{part_prompt}

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