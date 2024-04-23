import cv2
import pathlib
import pyautogui
from tkinter import *
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

class SketchImage:
    def __init__(self, root):
        self.window = root
        self.window.geometry("940x580")
        self.window.title('Sketch Creator')
        self.window.configure(bg="#fafafa")

        self.width = 700
        self.height = 440

        self.Image_Path = ''
        self.SketchImg = ''

        # Stylish font
        self.font_style = ("Helvetica", 12, "bold")

        # Menu
        self.menubar = Menu(self.window, font=self.font_style)
        self.window.config(menu=self.menubar)

        # File menu
        file_menu = Menu(self.menubar, tearoff=0, font=self.font_style)
        self.menubar.add_cascade(label='File', menu=file_menu)
        file_menu.add_command(label='Open Image', command=self.Open_Image)
        file_menu.add_separator()
        file_menu.add_command(label='Exit', command=self.Exit)

        # Sketch menu
        sketch_menu = Menu(self.menubar, tearoff=0, font=self.font_style)
        self.menubar.add_cascade(label='Sketch', menu=sketch_menu)
        sketch_menu.add_command(label='Create Sketch', command=self.CreateSketch)

        # Save menu
        save_menu = Menu(self.menubar, tearoff=0, font=self.font_style)
        self.menubar.add_cascade(label='Save', menu=save_menu)
        save_menu.add_command(label='Save Image', command=self.Save_Image)

        # Canvas frame
        self.canvas_frame = Frame(self.window, bg="#fafafa")
        self.canvas_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)

        # Canvas for displaying image
        self.canvas = Canvas(self.canvas_frame, bg="white", width=self.width, height=self.height)
        self.canvas.pack(fill=BOTH, expand=True)

        # Adjustments frame
        self.adjustments_frame = Frame(self.window, bg="#fafafa")
        self.adjustments_frame.pack(fill=X, padx=20)

        # Parameters sliders
        self.thickness_slider = Scale(self.adjustments_frame, from_=1, to=10, orient=HORIZONTAL, length=200, label="Line Thickness", bg="#fafafa", font=self.font_style)
        self.thickness_slider.set(5)
        self.thickness_slider.pack(side=LEFT, padx=10)

        self.contrast_slider = Scale(self.adjustments_frame, from_=1, to=100, orient=HORIZONTAL, length=200, label="Contrast", bg="#fafafa", font=self.font_style)
        self.contrast_slider.set(50)
        self.contrast_slider.pack(side=LEFT, padx=10)

        self.brightness_slider = Scale(self.adjustments_frame, from_=-100, to=100, orient=HORIZONTAL, length=200, label="Brightness", bg="#fafafa", font=self.font_style)
        self.brightness_slider.set(0)
        self.brightness_slider.pack(side=LEFT, padx=10)

        self.artistic_effect_slider = Scale(self.adjustments_frame, from_=0, to=100, orient=HORIZONTAL, length=200, label="Artistic Effect", bg="#fafafa", font=self.font_style)
        self.artistic_effect_slider.set(0)
        self.artistic_effect_slider.pack(side=LEFT, padx=10)

    def Open_Image(self):
        self.Clear_Screen()
        self.Image_Path = filedialog.askopenfilename(title="Select an Image", filetypes=(("Image files", "*.jpg *.jpeg *.png"),))
        if len(self.Image_Path) != 0:
            self.Show_Image(self.Image_Path)

    def Show_Image(self, Img):
        try:
            image = Image.open(Img)
            resized_image = image.resize((self.width, self.height))
            self.img = ImageTk.PhotoImage(resized_image)
            self.canvas.create_image(0, 0, anchor=NW, image=self.img)
        except Exception as e:
            messagebox.showerror("Error", f"Error while opening image: {str(e)}")

    def CreateSketch(self):
        if len(self.Image_Path) == 0:
            messagebox.showerror("Error", "No image selected.")
            return

        try:
            Img = cv2.imread(self.Image_Path)
            Img = cv2.resize(Img, (740, 480))
            GrayImg = cv2.cvtColor(src=Img, code=cv2.COLOR_BGR2GRAY)
            InvertImg = cv2.bitwise_not(GrayImg)

            # Adjusting parameters
            thickness = self.thickness_slider.get()
            contrast = self.contrast_slider.get() / 50.0
            brightness = self.brightness_slider.get()
            artistic_effect = self.artistic_effect_slider.get() / 100.0

            # Applying adjustments
            SmoothImg = cv2.medianBlur(src=InvertImg, ksize=thickness)
            IvtSmoothImg = cv2.bitwise_not(SmoothImg)
            self.SketchImg = cv2.divide(cv2.addWeighted(GrayImg, contrast, brightness, 0, artistic_effect), IvtSmoothImg, scale=250)
            cv2.imshow("Result Image", self.SketchImg)
            cv2.waitKey()
            cv2.destroyAllWindows()
        except Exception as e:
            messagebox.showerror("Error", f"Error while creating sketch: {str(e)}")

    def Save_Image(self):
        if len(self.SketchImg) == 0:
            messagebox.showerror("Error", "No sketch image to save.")
            return

        try:
            filename = pyautogui.prompt("Enter the filename to be saved")
            filename = filename + pathlib.Path(self.Image_Path).suffix
            cv2.imwrite(filename, self.SketchImg)
        except Exception as e:
            messagebox.showerror("Error", f"Error while saving image: {str(e)}")

    def Clear_Screen(self):
        self.canvas.delete("all")

    def Exit(self):
        self.window.destroy()

if __name__ == "__main__":
    root = Tk()
    SketchImage(root)
    root.mainloop()
