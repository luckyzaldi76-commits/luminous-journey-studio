from pathlib import Path

from engine.production_engine import ProductionEngine


engine = ProductionEngine()

prompt = """
Return exactly this format.

# TITLE

Engine Test

# SCRIPT

Production Engine Running.

# SEO

SEO

# HASHTAGS

#engine
#pipeline

# IMAGE_PROMPTS

Sunrise over Galilee

# METADATA

Version=1
"""

result = engine.run(
    prompt,
    Path("exports/engine"),
)

print(result)