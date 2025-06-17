from hominitel.minitel.minitel import minitel

class DisplayMode:
    WIDE = {"width": 40, "column_nb": 1, "column_spacing": 0}
    TWO_COLUMNS = {"width": 18, "column_nb": 2, "column_spacing": 2}

class RenderRegistry:
    def __init__(self, display_mode=DisplayMode.WIDE, top=1, bottom=39):
        self.elements = []
        self.top = top
        self.bottom = bottom
        self.height = bottom - top
        self.display_mode=display_mode
        self.init_display_map()
        self.last_total_height = 0

    def register(self, element):
        self.elements.append(element)

    def init_display_map(self):
        self.display_map = {i: {j: (None, 0) for j in range(self.display_mode["column_nb"])} for i in range(25)}

    def display(self):
        h = 0
        self.init_display_map()
        for template_element in self.elements:
            if h > self.height * self.display_mode["column_nb"]:
                break
            height = template_element.prepare_content(self.display_mode["width"])
            for i in range(height):
                self.display_map[h][h//self.height] = (template_element, i)
                h+=1
        self.last_total_height = h
        for i in self.display_map.keys():
            for j, el in self.display_map[i].items():
                template_element = el[0]
                inner_line = el[1]
                if template_element != None:
                    template_element.display(1+j*(self.display_mode["width"] + self.display_mode["column_spacing"]), i + self.top, self.display_mode["width"], inner_line)

    def update(self):
        h = 0
        new_total_height = 0
        
        # Calculate new total height needed for all elements
        for template_element in self.elements:
            if h > self.height * self.display_mode["column_nb"]:
                break
            _, height = template_element.prepare_update(self.display_mode["width"])
            new_total_height = max(new_total_height, h + height)
            h += height
        
        # Clear any lines that are no longer needed (if new height is less than old height)
        if new_total_height < self.last_total_height:
            for i in range(new_total_height, min(self.last_total_height, self.height * self.display_mode["column_nb"])):
                for j in range(self.display_mode["column_nb"]):
                    if i < 25:  # Safety check
                        minitel.pos(i + self.top, 1 + j*(self.display_mode["width"] + self.display_mode["column_spacing"]))
                        minitel.print(" " * self.display_mode["width"])
        
        self.last_total_height = new_total_height
        
        # Now update the elements
        h = 0
        for template_element in self.elements:
            if h > self.height * self.display_mode["column_nb"]:
                break
            lines_to_update, height = template_element.prepare_update(self.display_mode["width"])
            for i in range(height):
                if i in lines_to_update:
                    self.display_map[h][h//self.height] = (template_element, i)
                else:
                    self.display_map[h][h//self.height] = (template_element, -1)
                h+=1
        for i in self.display_map.keys():
            for j, el in self.display_map[i].items():
                template_element = el[0]
                inner_line = el[1]
                if template_element != None and inner_line != -1:
                    # Check if this is a selection-only update
                    if hasattr(template_element, 'selection_indicator') and template_element.selection_indicator:
                        # Try to update only the selection indicator first
                        if not template_element.update_selection_only(1+j*(self.display_mode["width"] + self.display_mode["column_spacing"]), i + self.top, self.display_mode["width"], inner_line):
                            # Fallback to full update if selection-only update didn't perform any changes
                            template_element.display(1+j*(self.display_mode["width"] + self.display_mode["column_spacing"]), i + self.top, self.display_mode["width"], inner_line)
                    else:
                        template_element.display(1+j*(self.display_mode["width"] + self.display_mode["column_spacing"]), i + self.top, self.display_mode["width"], inner_line)
