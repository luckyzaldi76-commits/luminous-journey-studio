from services.stage4_service import Stage4Service


stage4 = Stage4Service()

result = stage4.generate(
    gospel="Matthew 14:13-21",
    language="English",
    audience="Adults",
)

print(result)