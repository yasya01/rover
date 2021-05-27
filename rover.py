import math
import random
import sys, pygame
from tkinter import *
import time
import cv2
from PIL import Image
from tkinter.ttk import Combobox
from tkinter import messagebox
import base64
from datetime import datetime
current_charge_level = 100


class Energy_system:
    def __init__(self, charge_level):
        self.charge_level = charge_level

    def reduce_charge_level(self, funk_name):
        global current_charge_level
        if funk_name == "drill" or funk_name == "apxs" or funk_name == "photo":
            if current_charge_level < 11:
                self.produce_charge_level()
            else:
                current_charge_level = current_charge_level - 10

        elif funk_name == 'move':
            if current_charge_level < 16:
                self.produce_charge_level()
            else:
                current_charge_level = current_charge_level - 15
        elif funk_name == 'filter':
            if current_charge_level < 6:
                self.produce_charge_level()
            else:
                current_charge_level = current_charge_level - 5
        else:
            messagebox.showinfo("Error")

    def get_charge_level(self):
        global current_charge_level
        messagebox.showinfo("E_level: ", [current_charge_level, " %"])

    def produce_charge_level(self):
        time.sleep(5)
        global current_charge_level
        current_charge_level = 100
        messagebox.showinfo("Full charged")


class Info_proc_system:
    def __init__(self, funk_name):
        self.funk_name = funk_name
    def parse_signal(self):
        current_datetime = datetime.now()
        message = self.funk_name+str(current_datetime)
        message_bytes = message.encode('ascii')
        base64_bytes = base64.b64encode(message_bytes)
        res = base64_bytes.decode('ascii')
        f = open("info.txt", "a")
        f.writelines([res, "\n"])
        f.close()

    def unparse_signal(self):
        res = "info.txt"
        file1 = open(res, "r")
        while True:
            line = file1.readline()
            if not line:
                break
            base64_bytes = line.encode('ascii')
            message_bytes = base64.b64decode(base64_bytes)
            message = message_bytes.decode('ascii')
            f = open('de_info.txt', "a")
            f.writelines([message, "\n"])
            f.close()
        file1.close


class Photo_system:
    def __init__(self, photo,f_photo):
        self.photo = photo
        self.f_photo = f_photo

    def take_photo(self):
        cap = cv2.VideoCapture(0)
        for i in range(30):
            cap.read()
        ret, frame = cap.read()
        cv2.imwrite(self.photo, frame)
        cap.release()
        p = Info_proc_system('take_photo')
        p.parse_signal()
        global current_charge_level
        k = Energy_system(current_charge_level)
        k.reduce_charge_level('photo')

    def white_black(self, brightness):
        source = Image.open(self.photo)
        result = Image.new('RGB', source.size)
        separator = 255/brightness/2*3
        for x in range(source.size[0]):
            for y in range(source.size[1]):
                r, g, b = source.getpixel((x, y))
                total = r + g + b
                if total > separator:
                    result.putpixel((x, y), (255, 255, 255))
                else:
                    result.putpixel((x, y), (0, 0, 0))
        result.save(self.f_photo, "JPEG")
        p = Info_proc_system('white_black')
        p.parse_signal()
        global current_charge_level
        k = Energy_system(current_charge_level)
        k.reduce_charge_level('filter')


class Exploration_system:
    def __init__(self, res):
        self.res = res
    def explore(self):
        global current_charge_level
        if self.res == 'drill':
            k= random.randrange(1, 100)
            if k%2==0:
                messagebox.showinfo('There are:', 'Iron Ore')
            elif k%3==0:
                messagebox.showinfo('There are:', 'Coal')
            else:
                messagebox.showinfo('There are:', 'Nothing')

            k = Energy_system(current_charge_level)
            k.reduce_charge_level('drill')


        if self.res == 'apxs':
            k = random.randrange(100,1000)
            if k % 2 == 0:
                messagebox.showinfo('There are:', '60% - He; 15% - N')
            elif k % 3 == 0:
                messagebox.showinfo('There are:', '23% - Ne; 70% - Li')
            else:
                messagebox.showinfo('There are:', '10% - O; 80% - C')

            k = Energy_system(current_charge_level)
            k.reduce_charge_level('apxs')

        else:
            print("Error")
        p = Info_proc_system('explore')
        p.parse_signal()





class Movement_system:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move_object(self,canvas, object_id, destination, speed=50):
        dest_x, dest_y = destination
        coords = canvas.coords(object_id)
        current_x = coords[0]
        current_y = coords[1]
        new_x, new_y = current_x, current_y
        delta_x = delta_y = 0
        if current_x < dest_x:
            delta_x = 1
        elif current_x > dest_x:
            delta_x = -1
        if current_y < dest_y:
            delta_y = 1
        elif current_y > dest_y:
            delta_y = -1

        if (delta_x, delta_y) != (0, 0):
            canvas.move(object_id, delta_x, delta_y)

        if (new_x, new_y) != (dest_x, dest_y):
            canvas.after(speed, self.move_object, canvas, object_id, destination, speed)


def rover():
    root = Tk()
    root.title("Mars")
    canvas = Canvas(root, width=400, height=400)
    canvas.grid()
    item1 = canvas.create_rectangle(10, 10, 30, 30, fill="red")

    def create_window_move():
        def clicked():
            res = txt1.get()
            res1 = txt2.get()
            window.destroy()
            p = Movement_system(0, 0)
            p.move_object(canvas, item1, (int(res), int(res1)), 25)
            f = Info_proc_system('move_object')
            f.parse_signal()
            global current_charge_level
            k = Energy_system(current_charge_level)
            k.reduce_charge_level('move')

        window = Toplevel(root)
        lbl = Label(window, text="new x")
        lbl.grid(column=1, row=1)
        lbl = Label(window, text="new y")
        lbl.grid(column=2, row=1)
        txt1 = Entry(window, width=10)
        txt1.grid(column=1, row=2)
        txt2 = Entry(window, width=10)
        txt2.grid(column=2, row=2)
        btn = Button(window, text="Send!", command=clicked)
        btn.grid(column=3, row=2)

    def create_window_photo():
        def clicked():
            res = txt1.get()
            window.destroy()
            p = Photo_system(res, '')
            p.take_photo()

        window = Toplevel(root)
        lbl = Label(window, text="Put photo name")
        lbl.grid(column=1, row=1)
        txt1 = Entry(window, width=10)
        txt1.grid(column=1, row=2)
        btn = Button(window, text="Send!", command=clicked)
        btn.grid(column=3, row=2)

    def create_window_filter():
        def clicked():
            res = txt1.get()
            res1 = txt2.get()
            res2 = txt3.get()
            window.destroy()
            p = Photo_system(res, res1)
            p.white_black(int(res2))

        window = Toplevel(root)
        lbl = Label(window, text="photo name")
        lbl.grid(column=1, row=1)
        lbl = Label(window, text="new filtered photo name")
        lbl.grid(column=2, row=1)
        lbl = Label(window, text="brightness")
        lbl.grid(column=3, row=1)
        txt1 = Entry(window, width=10)
        txt1.grid(column=1, row=2)
        txt2 = Entry(window, width=10)
        txt2.grid(column=2, row=2)
        txt3 = Entry(window, width=10)
        txt3.grid(column=3, row=2)
        btn = Button(window, text="Send!", command=clicked)
        btn.grid(column=4, row=2)

    def create_window_ex():
        def clicked():
            p = Exploration_system('drill')
            p.explore()

        def clicked_1():
            p = Exploration_system('apxs')
            p.explore()

        window = Toplevel(root)
        btn = Button(window, text="Drill!", command=clicked)
        btn.grid(column=0, row=1)
        btn = Button(window, text="APXS!", command=clicked_1)
        btn.grid(column=1, row=1)

    def create_window_info():
        p = Info_proc_system('info')
        p.unparse_signal()
        window = Toplevel(root)
        listbox = Listbox(window)
        listbox.grid(row=1, column=0, columnspan=2, padx=20, pady=20)
        listbox.insert(END, "History of commands")
        with open('de_info.txt', 'r') as file:
            lst = file.readlines()
        for item in lst:
            listbox.insert(END, item)

    def create_window_energy():
        global current_charge_level
        p = Energy_system(current_charge_level)
        p.get_charge_level()

    btn = Button(root, text="Take photo", command=create_window_photo)
    btn.grid(column=1, row=1)

    btn = Button(root, text="Put filter", command=create_window_filter)
    btn.grid(column=2, row=1)

    btn = Button(root, text="Move rover!", command=create_window_move)
    btn.grid(column=3, row=1)

    btn = Button(root, text="Explore!", command=create_window_ex)
    btn.grid(column=5, row=1)

    btn = Button(root, text="Info!", command=create_window_info)
    btn.grid(column=4, row=1)

    btn = Button(root, text="Check Energy!", command=create_window_energy)
    btn.grid(column=6, row=1)

    root.mainloop()


if __name__ == "__main__":
    rover()
