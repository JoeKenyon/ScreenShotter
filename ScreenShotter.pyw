from PIL import ImageGrab
import tkinter as tk
import pyautogui
import win32api
  
class GUI:
    def __init__(self, master):
        global coords, image
        self.master = master
        self.master.geometry("600x250")
        master.title("ScreenShotter 0.0.1")
        
        self.label = tk.Label(master)
        
        self.areaBtn = tk.Button(master, text="Select Area", command=lambda: GUI.grab_area(self.label))
        
        coords = tk.StringVar()

        self.areaBtn.pack(side=tk.LEFT)
        self.label.pack(side=tk.LEFT)
        #print("2")
        
        
    def stuff():
        #print("#################")
        box = coords.get()
        #print(box)
        box = box.replace(",","(")
        box = box.replace(")","")
        box = box.split("(")
        del box[0]
        for i in range(len(box)):
            box[i] = int(box[i])
        #print(box)
        try:
            im=ImageGrab.grab(bbox=(box[0],box[1],box[2],box[3]))
            im.save("image.png", "PNG")
        except Exception as e:
            print(e)
            
        
    def grab_area(selflabel):
        pressed = False
        started = False
        
        winpos = (0,0)
        first = (0,0)
        last = (0,0)
        
        window = tk.Toplevel(root)
        state_left = win32api.GetKeyState(0x01)
        window.overrideredirect(1)
        window.wm_attributes('-alpha',0.5)
        window.geometry("100x100")
         
        while True:
            
            a = win32api.GetKeyState(0x01)
            mouse = pyautogui.position()

            if a != state_left:  # Button state changed
                state_left = a
                if a < 0:
                    pressed = True
                else:
                    pressed = False
                    
            try:        
                if pressed:
                    if not started:
                        first = mouse
                    started = True
                    winposdif = (mouse[0] - winpos[0], mouse[1] - winpos[1])
                    winsize = str(winposdif[0])+ "x" + str(winposdif[1])
                    window.geometry(winsize)
                    
                elif not pressed:
                    if started:
                        last = mouse # end of square
                        coords.set(str(first)+str(last))
                        window.destroy()
                        GUI.stuff()

                        selflabel.image = tk.PhotoImage(file="image.png")
                        selflabel['image'] = selflabel.image

                        selflabel.pack()
                        
                        
                        
                        break
                    
                    winpos = (mouse[0], mouse[1])
                    window.geometry("+" + str(mouse[0])+ "+" + str(mouse[1]))
                    started = False
                    
            except Exception as e:
                print(e)
                break
                
            window.update_idletasks()
            window.update()


root = tk.Tk()
my_gui = GUI(root)
root.mainloop()
