from luminous.infrastructure.parsers.parser_service import ParserService


sample = """
# TITLE

Luminous Journey

# SCRIPT

This is line 1.

This is line 2.

# SEO

SEO Description

# HASHTAGS

#faith
#jesus
"""

result = ParserService.parse(sample)

for key, value in result.items():

    print("=" * 60)

    print(key)

    print("-" * 60)

    print(value)