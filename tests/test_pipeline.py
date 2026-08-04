from services.production_pipeline import ProductionPipeline

pipeline = ProductionPipeline("gemini")

response = pipeline.generate("Say Hello")

print(response)