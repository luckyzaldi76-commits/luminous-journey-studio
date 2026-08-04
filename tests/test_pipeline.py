from pathlib import Path

from services.production_pipeline import ProductionPipeline


pipeline = ProductionPipeline("openrouter")

prompt = """
Return exactly this format.

# TITLE

Test Title

# SCRIPT

Hello from GPT.

# SEO

SEO Description

# HASHTAGS

#faith
#jesus

# IMAGE_PROMPTS

Jesus walking on water

# METADATA

Author=Luminous
"""

result = pipeline.generate(
    prompt,
    Path("exports/pipeline"),
)

print(result)