class ImageBuilder:

    def build(
        self,
        data,
        output_file
    ):

        with open(
            output_file,
            "w",
            encoding="utf-8"
        ) as f:

            f.write("# IMAGE PROMPTS\n\n")

            for key, value in data.items():

                if "IMAGE" in key.upper():

                    f.write(f"## {key}\n\n")

                    f.write(value)

                    f.write("\n\n")

        print(f"Image Prompt Saved : {output_file}")

        return output_file


builder = ImageBuilder()