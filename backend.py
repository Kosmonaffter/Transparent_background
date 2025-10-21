from PIL import Image


def make_background_transparent(
    input_path: str,
    output_path: str,
    color_to_transparent: tuple[int, int, int] = (255, 255, 255),
) -> None:
    image = Image.open(input_path).convert('RGBA')

    datas = image.getdata()

    new_data = []
    for item in datas:
        if (
            item[0] == color_to_transparent[0]
            and item[1] == color_to_transparent[1]
            and item[2] == color_to_transparent[2]
        ):
            new_data.append((255, 255, 255, 0))
        else:
            new_data.append(item)
    image.putdata(new_data)
    image.save(output_path, 'PNG')
