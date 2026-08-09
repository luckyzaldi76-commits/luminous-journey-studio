# Luminous Journey Studio

AI-powered devotional production pipeline for Luminous Journey.

---

# Features

- Workflow Runtime
- Workflow Registry
- Scheduler
- Event Bus
- Pipeline Context
- Multi-stage Production
- Gemini Provider
- OpenRouter Provider
- Mock Provider
- Automatic Provider Fallback
- Retry Policy
- Markdown Templates
- Structured Parser
- Validation
- Builder
- Export Engine
- CLI
- Parallel Task Execution

---

# Architecture

```
CLI
 │
 ▼
Production Engine
 │
 ▼
Workflow Registry
 │
 ▼
Runtime
 │
 ▼
Scheduler
 │
 ▼
Pipeline Context
 │
 ▼
Tasks
 │
 ├── Script
 ├── SEO
 ├── Image
 └── Metadata
 │
 ▼
Builder
 │
 ▼
Exporter
```

---

# Project Structure

```
config/

engine/

exports/

luminous/
    container/
    context/
    domain/
    kernel/
    tasks/
    workflows/

providers/

services/

templates/

tests/

run.py
```

---

# Workflow

```
Script
   │
   ├───────────────┐
   ▼               ▼
SEO           Image Prompts
   │               │
   └──────┬────────┘
          ▼
      Metadata
          │
          ▼
       Builder
          │
          ▼
       Exporter
```

---

# AI Providers

Supported:

- Gemini
- OpenRouter
- Mock

Provider selection:

```
USE_MOCK=True

        │
        ▼

      Mock

        │

        ▼

Completed
```

or

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

# Installation

```bash
git clone https://github.com/luckyzaldi76-commits/luminous-journey-studio.git

cd luminous-journey-studio

pip install -r requirements.txt
```

---

# Configuration

Create:

```text
.env
```

Example:

```text
AI_PROVIDER=auto

USE_MOCK=False

GEMINI_API_KEY=xxxxxxxx

OPENROUTER_API_KEY=xxxxxxxx
```

---

# Run Workflow

```bash
python run.py daily_gospel --gospel "Matthew 14:13-21"
```

or

```bash
python run.py daily_gospel \
    --gospel "Matthew 14:13-21" \
    --language English \
    --audience Adults
```

---

# Run Tests

```bash
python -m tests.test_runtime

python -m tests.test_template_loader

python -m tests.run_all
```

---

# Export Files

```
exports/

script.txt

response.md

seo.json

metadata.json

image_prompts.md

runtime.json
```

---

# Current Version

```
v0.5.0
```

Runtime Architecture Edition.

---

# License

Private Project.

Copyright © Luminous Journey.