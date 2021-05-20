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
current_charge_level = 5



class Photo_system:
    def __init__(self, photo,f_photo):
        self.photo = photo
        self.f_photo = f_photo

    def take_photo(self):
        # Включаем первую камеру
        #start = time.clock()
        cap = cv2.VideoCapture(0)
        # "Прогреваем" камеру, чтобы снимок не был тёмным
        for i in range(30):
            cap.read()
        # Делаем снимок
        ret, frame = cap.read()
        # Записываем в файл
        cv2.imwrite(self.photo, frame)
        # Отключаем камеру
        cap.release()
       # end = time.clock()
       # total = (end - start)*100
       #  global current_charge_level
       #  current_charge_level = current_charge_level- total*0.1

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
        global current_charge_level
        current_charge_level = current_charge_level - total * 0.1



class Antenna:

    signal = ''
    def __init__(self, signal):
        self.signal = signal

    def accept_signal(self):
        print("accepted signal %d" % Antenna.signal)
        total = random.randint(0,5)
        global current_charge_level
        current_charge_level = current_charge_level - total * 0.1
    def send_signal(self):
        print("Sended signal", self.signal)
        total = randint(0, 5)
        global current_charge_level
        current_charge_level = current_charge_level - total * 0.1


class Exploration_system:
    def __init__(self, res):
        self.res = res
    def explore(self):
        if self.res == 'drill':
            k= random.randrange(1, 100)
            if k%2==0:
                messagebox.showinfo('There are:', 'Iron Ore')
            elif k%3==0:
                messagebox.showinfo('There are:', 'Coal')
            else:
                messagebox.showinfo('There are:', 'Nothing')

        if self.res == 'apxs':
            k = random.randrange(100,1000)
            if k % 2 == 0:
                messagebox.showinfo('There are:', '60% - He; 15% - N')
            elif k % 3 == 0:
                messagebox.showinfo('There are:', '23% - Ne; 70% - Li')
            else:
                messagebox.showinfo('There are:', '10% - O; 80% - C')
        else:
            print("Error")





class Info_proc_system:
    def __init__(self, signal):
        self.signal = signal
    def parse_signal(self):
        print("parsed")
        res = base64.b64encode(self.signal)
        f = open("info.txt", "w")
        f.writelines(res)
        f.close()
        return res

    def unparse_signal(self):
        res = self
        print("unparsed")


class Energy_system:
    def __init__(self,charge_level):
        self.charge_level = charge_level

    def reduce_charge_level(self):
        coef=[0.1,0.2,0.1,0.2,0.3,]
        coef_c = coef[0]
        coef_e = coef[1]
        coef_a = coef[2]
        coef_i = coef[3]
        coef_m = coef[4]
    def get_charge_level(self):
        print("Current level: ", self)

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


if __name__ == "__main__":

    root = Tk()
    canvas = Canvas(root, width=400, height=400)
    canvas.grid()
    item1 = canvas.create_rectangle(10, 10, 30, 30, fill="red")

    def create_window_move():
        def clicked():
            res = txt1.get()
            res1= txt2.get()
            window.destroy()
            p = Movement_system(0, 0)
            p.move_object(canvas, item1,( int(res),int(res1)), 25)

        window = Toplevel(root)
        lbl = Label(window, text="new x")
        lbl.grid(column=1, row=1)
        lbl = Label(window, text="new y")
        lbl.grid(column=2, row=1)
        txt1 = Entry(window, width=10)
        txt1.grid(column=1, row=2)
        txt2 = Entry(window, width=10)
        txt2.grid(column=2, row=2)
        btn = Button(window, text="Send!", command = clicked)
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
            p = Photo_system(res,res1)
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
            p=Exploration_system('drill')
            p.explore()

        def clicked_1():
            p = Exploration_system('apxs')
            p.explore()

        window = Toplevel(root)
        btn = Button(window, text="Drill!", command=clicked)
        btn.grid(column=0, row=1)
        btn = Button(window, text="APXS!", command=clicked_1)
        btn.grid(column=1, row=1)

    btn = Button(root, text="Take photo", command=create_window_photo)
    btn.grid(column=1, row=1)

    btn = Button(root, text="Put filter", command=create_window_filter)
    btn.grid(column=2, row=1)

    btn = Button(root, text="Move rover!", command =create_window_move)
    btn.grid(column=3, row=1)

    btn = Button(root, text="Explore!", command = create_window_ex)
    btn.grid(column=5, row=1)



    btn = Button(root, text="Get signal!")
    btn.grid(column=4, row=1)


    btn = Button(root, text="Check Energy!")
    btn.grid(column=6, row=1)



    root.mainloop()
