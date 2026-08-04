from services.stage1_service import Stage1Service

service = Stage1Service()

result = service.generate(
    gospel="Matthew 14:13-21",
    language="English",
    audience="Adults",
)

print(result)