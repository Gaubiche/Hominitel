import random
from lib import upynitel
from machine import UART
from display.template_element import TemplateElement


class DisplayMode:
    WIDE = {"width": 40, "column_nb": 1, "column_spacing": 0}
    TWO_COLUMNS = {"width": 18, "column_nb": 2, "column_spacing": 2}

class DisplayRegistry:
    def __init__(self, display_mode=DisplayMode.WIDE, top=1, bottom=39):
        self.elements = []
        self.top = top
        self.bottom = bottom
        self.display_mode=display_mode
        self.init_display_map()

    def register(self, element):
        self.elements.append(element)

    def init_display_map(self):
        self.display_map = {i: {j: (None, 0) for j in range(self.display_mode["column_nb"])} for i in range(25)}

    def display(self):
        h = 0
        self.init_display_map()
        for template_element in self.elements:
            if h > 24 * self.display_mode["column_nb"]:
                break
            height = template_element.prepare_content(self.display_mode["width"])
            for i in range(height):
                self.display_map[h][h//24] = (template_element, i)
                h+=1
        for i in self.display_map.keys():
            for j, el in self.display_map[i].items():
                template_element = el[0]
                inner_line = el[1]
                if template_element != None:
                    template_element.display(1+j*(self.display_mode["width"] + self.display_mode["column_spacing"]), i, self.display_mode["width"], inner_line)

    def update(self):
        h = 0
        for template_element in self.elements:
            if h > 24 * self.display_mode["column_nb"]:
                break
            lines_to_update, height = template_element.prepare_update(self.display_mode["width"])
            for i in range(height):
                if i in lines_to_update:
                    self.display_map[h][h//24] = (template_element, i)
                else:
                    self.display_map[h][h//24] = (template_element, -1)
                h+=1
        for i in self.display_map.keys():
            for j, el in self.display_map[i].items():
                print(lines_to_update)
                if j in lines_to_update:
                    template_element = el[0]
                    inner_line = el[1]
                    if template_element != None and inner_line != -1:
                        template_element.display(1+j*(self.display_mode["width"] + self.display_mode["column_spacing"]), i, self.display_mode["width"], inner_line)

