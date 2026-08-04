from pathlib import Path

from services.builder_service import BuilderService
from services.exporter_service import ExporterService


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

data = BuilderService.build(sample)

ExporterService.export(
    Path("exports/demo"),
    data,
)

print("Export OK")