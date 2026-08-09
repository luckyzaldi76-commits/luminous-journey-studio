from luminous.infrastructure.templates.template_loader import TemplateLoader


def main():

    prompt = TemplateLoader.load(

        "stage1.md",

        gospel="Matthew 14:13-21",

        language="English",

        audience="Adults",

    )

    assert prompt

    assert "Matthew 14:13-21" in prompt

    assert "English" in prompt

    assert "Adults" in prompt

    print()

    print("=" * 60)

    print("TEMPLATE LOADER TEST PASSED")

    print("=" * 60)

    print()

    print(prompt[:500])

    print()

    print("=" * 60)

    print("END")

    print("=" * 60)


if __name__ == "__main__":

    main()