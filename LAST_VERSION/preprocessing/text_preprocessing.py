def validate_content(text):
    "Valida si una cadena es suficiente para considerarse texto"
    photo_foot = [
        "TapScanner",
        "CamScanner"
    ]
    invalid_options = [
        "  ",
        "   "
    ]

    photo = False
    for option in photo_foot:
        if text.__contains__(option):
            photo = True
            break

    if not photo:
        for option in (invalid_options + photo_foot):
            text = text.replace(option, "")
        if text.isspace():
            text = ""

    return ("" if photo else text), photo


def is_valid_text(text):
    return (not text.isspace()) and len(text) > 0
