class ScriptBuilder:

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

            for key, value in data.items():

                f.write(f"# {key}\n\n")

                f.write(value.strip())

                f.write("\n\n")

        print(f"Script Saved : {output_file}")

        return output_file


builder = ScriptBuilder()