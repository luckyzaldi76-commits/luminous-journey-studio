# Luminous Journey Studio

AI-powered devotional production pipeline for Luminous Journey.

---

## Features

- Multi-stage production pipeline
- Gemini AI
- OpenRouter AI
- Automatic fallback
- Automatic retry
- Parallel processing
- Markdown templates
- Structured parser
- Validation
- Export engine

---

## Project Structure

```
engine/
providers/
services/
templates/
config/
exports/
logs/
tests/
```

---

## Pipeline

```
Stage 1
    │
    ▼
Devotional Script

    │
    ▼
Stage 2
SEO + Hashtags

    │
    ▼
Stage 3
Image Prompts

    │
    ▼
Stage 4
Metadata

    │
    ▼
Builder

    │
    ▼
Exporter
```

---

## AI Providers

Supported:

- Gemini
- OpenRouter

Automatic fallback:

```
Gemini
    │
    ▼
Retry

    │
Success?
    │
 No
    ▼
OpenRouter
```

---

## Installation

```bash
git clone https://github.com/luckyzaldi76-commits/luminous-journey-studio.git

cd luminous-journey-studio

pip install -r requirements.txt
```

---

## Configuration

Create:

```
.env
```

Example:

```text
GEMINI_API_KEY=...

OPENROUTER_API_KEY=...

AI_PROVIDER=gemini
```

---

## Run

```bash
python -m tests.test_engine
```

---

## Output

```
exports/

    devotional.md

    devotional.docx

    metadata.txt
```

---

## Current Version

v1.0.0

---

## License

Private project.

Copyright © Luminous Journey.