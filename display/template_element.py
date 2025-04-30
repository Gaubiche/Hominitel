class TemplateElement:
    def __init__(self, minitel, content, inverse=False):
        self.minitel = minitel
        self.content = content
        self.content_to_display = None
        self.last_displayed = []
        self.height = None
        self.inverse = inverse

    def get_content(self):
        return self.content() if callable(self.content) else self.content

    def get_inverse(self):
        return self.inverse() if callable(self.inverse) else self.inverse

    def prepare_content(self, width):
        content = self.get_content()
        inverse = self.get_inverse()
        self.inverse_to_display = inverse
        self.lines = [content[i:i+width] for i in range(0, len(content), width)]
        return len(self.lines)

    def prepare_update(self, width):
        content = self.get_content()
        inverse = self.get_inverse()
        lines = [content[i:i+width] for i in range(0, len(content), width)]
        lines_to_update = set()
        if len(lines) > len(self.last_displayed):
            lines_to_update = {i + len(self.last_displayed) for i in range(len(lines) - len(self.last_displayed))}
        if len(lines) < len(self.last_displayed):
            lines_to_update = {i + len(lines) for i in range(len(self.last_displayed) - len(lines))}
        for i, line in enumerate(lines):
            if len(self.last_displayed)<=i or line != self.last_displayed[i]["line"] or inverse != self.last_displayed[i]["inversed"]:
                lines_to_update.add(i)
        self.inverse_to_display = inverse
        self.lines = lines
        return lines_to_update, len(self.lines)

    def clear_zone(self, x, y, width):
        # self.minitel.pos()
        # for i in range(self.height):
        #     self.minitel.vtab(self.position + i)
        #     self.minitel._print(" " * width)
        pass

    def display(self, x, y, width, element_line):
        self.clear_zone(x, y, width)
        self.minitel.pos(y, x)
        if self.inverse_to_display:
            self.minitel.inverse()
        self.minitel._print('{:<{width}}'.format(self.lines[element_line], width=width))
        if len(self.last_displayed)<=element_line:
            self.last_displayed.append({"line": self.lines[element_line], "inversed": self.inverse_to_display, "x": x, "y": y})
        else:
            self.last_displayed[element_line] = {"line": self.lines[element_line], "inversed": self.inverse_to_display, "x": x, "y": y}


    def update(self, x, y, width, element_line):
        if len(self.last_displayed)<=element_line or self.last_displayed[element_line] != {"line": self.lines[element_line], "inversed": self.inverse_to_display, "x": x, "y": y}:
            self.display(x, y, width, element_line)
            if len(self.last_displayed)<=element_line:
                self.last_displayed.append({"line": self.lines[element_line], "inversed": self.inverse_to_display, "x": x, "y": y})
            else:
                self.last_displayed[element_line] = {"line": self.lines[element_line], "inversed": self.inverse_to_display, "x": x, "y": y}