from core.template_loader import load_template


def build_prompt(reading):

    role = load_template("role.txt")
    structure = load_template("structure.txt")
    language = load_template("language.txt")
    output = load_template("output.txt")

    return f"""
{role}

{structure}

{language}

{output}

Today's Reading

Date:
{reading.date}

Reading I:
{reading.reading1}

Reading II:
{reading.reading2 or "None"}

Gospel:
{reading.gospel}
"""