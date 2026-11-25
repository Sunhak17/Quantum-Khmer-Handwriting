import matplotlib.font_manager as fm

PREFERRED_KHMER_FONTS = [
    "Noto Sans Khmer",
    "Khmer OS",
    "Khmer UI",
    "Khmer OS System",
    "Khmer OS Content",
    "Khmer OS Battambang-Kh Auto",
    "Leelawadee UI",
    "Noto Serif Khmer",
]


def khmer_font_name():
    available = {f.name for f in fm.fontManager.ttflist}
    for name in PREFERRED_KHMER_FONTS:
        if name in available:
            return name
    for f in fm.fontManager.ttflist:
        if "khmer" in f.name.lower():
            return f.name
    return None


def khmer_font_prop():
    name = khmer_font_name()
    return fm.FontProperties(family=name) if name else None
