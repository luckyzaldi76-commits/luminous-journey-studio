def save_response(
    text,
    output_file
):

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(text)

    print(f"Saved : {output_file}")

    return output_file