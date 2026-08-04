from services.production_pipeline import ProductionPipeline


def main():

    pipeline = ProductionPipeline("openrouter")

    result = pipeline.generate("Say hello in one sentence.")

    print(result)


if __name__ == "__main__":
    main()