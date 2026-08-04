from core.prompt_reader import load_prompt


def build_prompt(reading):

    master_prompt = load_prompt()

    return f"""{master_prompt}

==================================================
TODAY'S READING
==================================================

Date:
{reading.date}

Reading I:
{reading.reading1}

Reading II:
{reading.reading2 or "None"}

Gospel:
{reading.gospel}

==================================================

Generate the complete production package according to all instructions above.
"""