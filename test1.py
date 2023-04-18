import math
from tkinter import *
from tkinter import filedialog

import numpy as np
from PIL import Image, ImageDraw, ImageTk, ImageFont


class Application(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.choose_image_button = Button(self)
        self.choose_image_button["text"] = "Выбрать изображение"
        self.choose_image_button["command"] = self.choose_image
        self.choose_image_button.pack()

        self.radius_entry_label = Label(self, text="Радиус круга:")
        self.radius_entry_label.pack()
        self.radius_entry = Entry(self)
        self.radius_entry.pack()

        self.nails_entry_label = Label(self, text="Количество гвоздей:")
        self.nails_entry_label.pack()
        self.nails_entry = Entry(self)
        self.nails_entry.pack()

        self.generate_button = Button(self)
        self.generate_button["text"] = "Сгенерировать круговую картинку"
        self.generate_button["command"] = self.generate_circle_image
        self.generate_button.pack()

        # self.image_canvas = Canvas(self, width=500, height=500)
        # self.image_canvas.pack()

    def choose_image(self):
        self.filename = filedialog.askopenfilename(title="Select file", filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))
        self.image = Image.open(self.filename).convert("L")

        # self.image_canvas.delete("all")
        # self.image_canvas.image = ImageTk.PhotoImage(self.image)
        # self.image_canvas.create_image(0, 0, anchor=NW, image=self.image_canvas.image)

    def pinCoords(self, radius, x0, y0, numPins=100, offset=0):
        alpha = np.linspace(0 + offset, 2 * np.pi + offset, numPins + 1)

        if (x0 == None) or (y0 == None):
            x0 = radius + 1
            y0 = radius + 1

        coords = []
        for angle in alpha[0:-1]:
            x = int(x0 + radius * np.cos(angle))
            y = int(y0 + radius * np.sin(angle))

            coords.append((x, y))
        return coords
    

    def bresenham_line(self, x0, y0, x1, y1):
        """Возвращает список кортежей с координатами пикселей на линии между двумя точками"""
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy
        line = [(x0, y0)]
        while x0 != x1 or y0 != y1:
            e2 = err * 2
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy
            line.append((x0, y0))
        return line
    def get_line_points(self, start_point, end_point):

        # создание списка для хранения координат точек на линии
        line_points = []

        # вычисление координат для линии
        dx = abs(end_point[0] - start_point[0])
        dy = abs(end_point[1] - start_point[1])
        x, y = start_point

        # определение направления движения линии
        if start_point[0] < end_point[0]:
            x_step = 1
        else:
            x_step = -1

        if start_point[1] < end_point[1]:
            y_step = 1
        else:
            y_step = -1

        # вычисление координат каждой точки на линии
        if dx > dy:
            ai = (dy - dx) * 2
            bi = dy * 2
            d = bi - dx

            while x != end_point[0]:
                # сохранение координат текущей точки
                line_points.append((x, y))

                # обновление координат и параметра d
                if d >= 0:
                    x += x_step
                    y += y_step
                    d += ai
                else:
                    d += bi
                    x += x_step
        else:
            ai = (dx - dy) * 2
            bi = dx * 2
            d = bi - dy

            while y != end_point[1]:
                # сохранение координат текущей точки
                line_points.append((x, y))

                # обновление координат и параметра d
                if d >= 0:
                    x += x_step
                    y += y_step
                    d += ai
                else:
                    d += bi
                    y += y_step

            # сохранение координат последней точки
            line_points.append((x, y))

        # возвращение списка координат точек на линии
        return line_points
    def get_line_lightness(self, line):
        lightness = []
        for pixel in line:
            lightness.append(self.image.getpixel(pixel))
        return sum(lightness) / len(lightness)

    def right(self):
            radius = int(self.radius_entry.get())
            num_nails = int(self.nails_entry.get())
            num_lines = 300
            width = self.image.width
            height = self.image.height
            circle_image = Image.new('RGBA', (width, height), (255, 255, 255, 255))
            draw = ImageDraw.Draw(circle_image)
            nail_positions = self.pinCoords(radius, width / 2, height / 2, num_nails)
            next_value = (nail_positions[0][0],nail_positions[0][1])
            for i in range(num_lines):
                draw1 = ImageDraw.Draw(self.image)
                list2 = []
                maxlist1 = []
                coords = []
                next_value = ()
                height = self.image.height
                pixels = self.image.load() # create the pixel map
                for i in range(len(nail_positions)):
                    for j in range(len(nail_positions)):
                        list2 = []
                        if i == j:
                            continue
                        list_temp = self.get_line_points((nail_positions[i][0],nail_positions[i][1]),(nail_positions[j][0],nail_positions[j][1]))
                        for g in range(len(list_temp)):
                            list2.append(pixels[list_temp[g][0],list_temp[g][1]])
                        maxlist1.append(sum(list2))
                        coords.append(((nail_positions[i][0],nail_positions[i][1]),(nail_positions[j][0],nail_positions[j][1])))
                index, max_value = max(enumerate(maxlist1), key=lambda i_v: i_v[1])
                print(index, max_value)
                print(coords[index])
                next_value = (coords[index][1][0], coords[index][1][1])
                draw.line((coords[index][0][0],coords[index][0][1],coords[index][1][0],coords[index][1][1]), fill=(0, 0, 0, 200))
                draw1.line((coords[index][0][0],coords[index][0][1],coords[index][1][0],coords[index][1][1]), fill=(0))
            circle_image.show()
    def generate_circle_image(self):
        self.right()
                 
        radius = int(self.radius_entry.get())
        num_nails = int(self.nails_entry.get())
        width = self.image.width
        height = self.image.height

        nail_positions = self.pinCoords(radius, width / 2, height / 2, num_nails)
        # print(nail_positions)
        circle_image = Image.new('RGBA', (width, height), (255, 255, 255, 255))
        draw = ImageDraw.Draw(circle_image)
        for i in range(num_nails):
            x = nail_positions[i][0]
            y = nail_positions[i][1]
            draw.point((x, y), fill=0)
        pixels = []
        for i in range(len(nail_positions)):
            pixels.append(self.get_line_lightness(self.bresenham_line(nail_positions[i][0], nail_positions[i][1], nail_positions[i][0], nail_positions[i][1])))
        next_nail = []
        for i in range(len(nail_positions)):
            next_nail.append((nail_positions[i], pixels[i], i))
        next_nail  = sorted(next_nail, key=lambda x: x[1])
        for i in range(len(nail_positions) - 1):
            x = next_nail[i][0][0]
            y = next_nail[i][0][1]
            x1 = next_nail[i + 1][0][0]
            y1 = next_nail[i + 1][0][1]
            # print(self.get_line_points((x, y),(x1, y1)))
            draw.line((x, y, x1, y1), fill=(0, 0, 0, 128))
            
        numbered_image = Image.new('RGB', (width, height), (255, 255, 255))
        draw = ImageDraw.Draw(numbered_image)
        font = ImageFont.truetype("Roboto-Thin.ttf", 10)
        for i in range(len(nail_positions)):
            draw.text(next_nail[i][0], str(next_nail[i][2]), font=font, fill=(0, 0, 0))

        circle_image.show()
        numbered_image.show()
        instruction_text = "\n".join([f"{i + 1}. Перевязать нить с гвоздика {next_nail[i][2]} на гвоздик {next_nail[i + 1][2]}" for i in range(len(next_nail) - 1)])
        instruction_text += f"\n{num_nails}. Завязать конец нити на последний гвоздик"
        instruction_window = Toplevel(self)
        instruction_window.title("Инструкция по плетению")
        instruction_label = Label(instruction_window, text=instruction_text)
        instruction_label.pack()
    
    
                  
            
            
            # for i in range(width): # for every pixel:
            #     for j in range(height):
            #         if pixels[i,j] != (255, 0, 0):
            #             # change to black if not red
            #             pixels[i,j] = (0, 0 ,0)
if __name__ == '__main__':
    root = Tk()
    app = Application(master=root)
    app.mainloop()