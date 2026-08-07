from services.template_loader import TemplateLoader


prompt = TemplateLoader.load(
    "stage1.md",
    gospel="Matthew 14:13-21",
    language="English",
    audience="Adults",
)

print(prompt)