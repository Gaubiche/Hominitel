from hominitel.minitel.minitel import minitel

class TemplateElement:
    def __init__(self, content, selection_indicator=None):
        self.content = content
        self.content_to_display = None
        self.last_displayed = []
        self.height = None
        self.selection_indicator = selection_indicator

    def get_content(self):
        return self.content() if callable(self.content) else self.content

    def get_selection_indicator(self):
        return self.selection_indicator() if callable(self.selection_indicator) else self.selection_indicator

    def prepare_content(self, width):
        content = self.get_content()
        indicator = self.get_selection_indicator()
        # Ensure indicator is a string
        if indicator is None:
            indicator = ""
        else:
            indicator = str(indicator)
        self.indicator_to_display = indicator
        # Add indicator to content if provided
        if indicator:
            content = indicator + content
        self.lines = [content[i:i+width] for i in range(0, len(content), width)]
        return len(self.lines)

    def prepare_update(self, width):
        content = self.get_content()
        indicator = self.get_selection_indicator()
        # Ensure indicator is a string
        if indicator is None:
            indicator = ""
        else:
            indicator = str(indicator)
        # Add indicator to content if provided
        if indicator:
            content = indicator + content
        lines = [content[i:i+width] for i in range(0, len(content), width)]
        lines_to_update = set()
        if len(lines) > len(self.last_displayed):
            lines_to_update = {i + len(self.last_displayed) for i in range(len(lines) - len(self.last_displayed))}
        if len(lines) < len(self.last_displayed):
            lines_to_update = {i + len(lines) for i in range(len(self.last_displayed) - len(lines))}
        for i, line in enumerate(lines):
            if len(self.last_displayed)<=i or line != self.last_displayed[i]["line"] or indicator != self.last_displayed[i]["indicator"]:
                lines_to_update.add(i)
        self.indicator_to_display = indicator
        self.lines = lines
        return lines_to_update, len(self.lines)

    def clear_zone(self, x, y, width):
        # self.minitel.pos()
        # for i in range(self.height):
        #     self.minitel.vtab(self.position + i)
        #     self.minitel.print(" " * width)
        pass

    def display(self, x, y, width, element_line):
        current_line = self.lines[element_line]
        
        # Check if we need to clear anything
        if len(self.last_displayed) > element_line:
            last_line = self.last_displayed[element_line]["line"]
            
            # If the new line is shorter than the old one, we need to clear the excess
            if len(current_line) < len(last_line):
                # Display the new content first
                minitel.pos(y, x)
                minitel.print('{:<{width}}'.format(current_line, width=width))
                
                # Then clear any remaining characters from the old line
                if len(current_line) < len(last_line):
                    minitel.pos(y, x + len(current_line))
                    minitel.print(" " * (len(last_line) - len(current_line)))
            else:
                # New line is same length or longer, just display normally
                minitel.pos(y, x)
                minitel.print('{:<{width}}'.format(current_line, width=width))
        else:
            # First time displaying this line, just display normally
            minitel.pos(y, x)
            minitel.print('{:<{width}}'.format(current_line, width=width))
        
        if len(self.last_displayed)<=element_line:
            self.last_displayed.append({"line": self.lines[element_line], "indicator": self.indicator_to_display, "x": x, "y": y})
        else:
            self.last_displayed[element_line] = {"line": self.lines[element_line], "indicator": self.indicator_to_display, "x": x, "y": y}

    def update(self, x, y, width, element_line):
        if len(self.last_displayed)<=element_line or self.last_displayed[element_line] != {"line": self.lines[element_line], "indicator": self.indicator_to_display, "x": x, "y": y}:
            self.display(x, y, width, element_line)
            if len(self.last_displayed)<=element_line:
                self.last_displayed.append({"line": self.lines[element_line], "indicator": self.indicator_to_display, "x": x, "y": y})
            else:
                self.last_displayed[element_line] = {"line": self.lines[element_line], "indicator": self.indicator_to_display, "x": x, "y": y}

    def update_selection_only(self, x, y, width, element_line):
        """Updates only the selection indicator part of the line"""
        if self.selection_indicator and len(self.last_displayed) > element_line:
            indicator = self.get_selection_indicator()
            # Ensure indicator is a string
            if indicator is None:
                indicator = ""
            else:
                indicator = str(indicator)
            last_indicator = self.last_displayed[element_line]["indicator"]
            
            # Check if only the indicator changed
            if indicator != last_indicator:
                # Get the current line content
                current_line = self.lines[element_line] if element_line < len(self.lines) else ""
                
                # Only update the indicator part without clearing first
                minitel.pos(y, x)
                minitel.print('{:<{width}}'.format(current_line[:2], width=2))
                
                # Update the stored indicator
                self.last_displayed[element_line]["indicator"] = indicator
                return True  # Indicate that update was performed
        return False  # Indicate that no update was needed or performed