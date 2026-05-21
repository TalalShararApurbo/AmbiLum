def get_contrasting_text_color(hex_color):
    """Returns 'black' or 'white' depending on the luminance of the hex_color."""
    if not hex_color or len(hex_color) != 7:
        return "black"
    try:
        r = int(hex_color[1:3], 16)
        g = int(hex_color[3:5], 16)
        b = int(hex_color[5:7], 16)
        luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
        return "black" if luminance > 0.5 else "white"
    except Exception:
        return "black"
