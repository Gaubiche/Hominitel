class TemplateElement:
    def __init__(self, minitel, content, inverse=False):
        self.minitel = minitel
        self.content = content
        self.content_to_display = None
        self.last_displayed = [], False
        self.height = None
        self.inverse = inverse

    def get_content(self):
        return self.content() if callable(self.content) else self.content

    def get_inverse(self):
        return self.inverse() if callable(self.inverse) else self.inverse

    def prepare_content(self, width):
        content = self.get_content()
        inverse = self.get_inverse()
        self.content_to_display = content
        self.inverse = inverse
        self.lines = [content[i:i+width] for i in range(0, len(content), width)]
        return len(self.lines)

    def prepare_update(self, width):
        content = self.get_content()
        inverse = self.get_inverse()
        lines = [content[i:i+width] for i in range(0, len(content), width)]
        last_displayed_lines, last_inverse_state = self.last_displayed
        lines_to_update = set()
        if len(lines) > len(last_displayed_lines):
            lines_to_update = {i + len(last_displayed_lines) for i in range(len(lines) - len(last_displayed_lines))}
        if len(lines) < len(last_displayed_lines):
            lines_to_update = {i + len(lines) for i in range(len(last_displayed_lines) - len(lines))}
        for i, line in enumerate(lines):
            if len(last_displayed_lines)<=i or line != last_displayed_lines[i] or inverse != last_inverse_state:
                lines_to_update.add(i)
        self.content_to_display = content
        self.inverse = inverse
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
        if self.get_inverse():
            self.minitel.inverse()
        self.minitel._print('{:<{width}}'.format(self.lines[element_line], width=width))
        self.last_displayed = self.lines, self.inverse

    def update(self, new_position, width=40):
        current_content = self.content_to_display
        if new_position is not None and new_position != self.position:
            self.position = new_position
        if current_content != self.last_displayed:
            self.clear_old_content()
            lines = [current_content[i:i+width] for i in range(0, len(current_content), width)]
            for i, line in enumerate(lines):
                self.minitel.vtab(self.position + i)
                if self.get_inverse():
                    self.minitel.inverse()
                self.minitel._print(line.ljust(width))
            self.last_displayed = current_content