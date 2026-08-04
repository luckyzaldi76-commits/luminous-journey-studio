from services.stage1_service import Stage1Service
from services.stage2_service import Stage2Service


stage1 = Stage1Service()
stage2 = Stage2Service()

script = stage1.generate(
    gospel="Matthew 14:13-21",
    language="English",
    audience="Adults",
)

result = stage2.generate(script)

print(result)