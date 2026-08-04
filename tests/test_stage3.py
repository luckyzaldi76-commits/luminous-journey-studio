from services.stage1_service import Stage1Service
from services.stage3_service import Stage3Service


stage1 = Stage1Service()
stage3 = Stage3Service()

script = stage1.generate(
    gospel="Matthew 14:13-21",
    language="English",
    audience="Adults",
)

result = stage3.generate(script)

print(result)