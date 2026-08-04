from services.builder_service import BuilderService

sample = """
# TITLE

Walking with Jesus

# SCRIPT

This is script.

# SEO

SEO Description

# HASHTAGS

#faith
#jesus

# IMAGE_PROMPTS

Prompt 1

Prompt 2

# METADATA

Author=Luminous
"""

result = BuilderService.build(sample)

for key, value in result.items():

    print("=" * 60)
    print(key.upper())
    print("-" * 60)
    print(value)