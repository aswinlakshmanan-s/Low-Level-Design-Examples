# Flyweight class to hold style info
class Style:
    def __init__(self, font_name: str, font_size: int, bold: bool, italic: bool):
        self.font_name = font_name
        self.font_size = font_size
        self.bold = bold
        self.italic = italic

    def __repr__(self):
        return f"Style({self.font_name}, {self.font_size}, Bold={self.bold}, Italic={self.italic})"

# Factory to share styles
class StyleFactory:
    def __init__(self):
        self._styles = {}

    def get_style(self, font_name: str, font_size: int, bold: bool, italic: bool) -> Style:
        key = (font_name, font_size, bold, italic)
        if key not in self._styles:
            self._styles[key] = Style(font_name, font_size, bold, italic)
        return self._styles[key]

# Character holds text + reference to shared style
class Character:
    def __init__(self, ch: str, style: Style):
        self.ch = ch
        self.style = style

    def __repr__(self):
        return f"'{self.ch}'({self.style})"

# Document stores characters in lines
class Document:
    def __init__(self):
        self.lines = []  # list of list of Character

    def add_char(self, line_number: int, ch: str, style: Style):
        while len(self.lines) <= line_number:
            self.lines.append([])
        self.lines[line_number].append(Character(ch, style))

    def delete_last_char(self, line_number: int):
        if 0 <= line_number < len(self.lines) and self.lines[line_number]:
            self.lines[line_number].pop()

    def read_line(self, line_number: int) -> str:
        if 0 <= line_number < len(self.lines):
            return ''.join(char.ch for char in self.lines[line_number])
        return ""

    def print_debug(self):
        for i, line in enumerate(self.lines):
            print(f"Line {i}:", line)

# Sample usage
if __name__ == "__main__":
    factory = StyleFactory()
    doc = Document()

    style1 = factory.get_style("Arial", 12, False, False)
    style2 = factory.get_style("Arial", 12, True, False)

    doc.add_char(0, 'H', style1)
    doc.add_char(0, 'e', style1)
    doc.add_char(0, 'l', style1)
    doc.add_char(0, 'l', style1)
    doc.add_char(0, 'o', style2)

    doc.add_char(1, 'W', style2)
    doc.add_char(1, 'o', style1)
    doc.add_char(1, 'r', style1)
    doc.add_char(1, 'l', style1)
    doc.add_char(1, 'd', style2)

    print("\nText Output:")
    print(doc.read_line(0))  # Hello
    print(doc.read_line(1))  # World

    print("\nDebug View:")
    doc.print_debug()
