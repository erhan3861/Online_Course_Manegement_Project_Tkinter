import tkinter as tk
from PIL import Image, ImageTk
import pandas as pd

class Courses():
    def __init__(self, root):
        # Veri setini yükle
        self.data = pd.read_csv('coursera_dataset.csv')

        # tkinter penceresini oluştur
        self.root = root
        self.root.geometry("1366x768+0+0")
        self.root.title("Kurs İnceleme Uygulaması")

        # Ana pencereyi sarmalayacak bir çerçeve oluştur
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Kurs butonlarını içerecek bir çerçeve oluşturun
        self.button_frame = tk.Frame(self.main_frame, width=220)
        self.button_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Kurs bilgilerini gösterecek bir LabelFrame oluşturun
        self.info_frame = tk.LabelFrame(self.main_frame, text="Kurs Bilgileri", width=400, height=400)
        self.info_frame.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.course_items = ["Course Name", "University", "Difficulty Level", "Course Rating", "Course URL", "Course Description", "Skills", "Specialized"]

        self.course_buttons = {}

        # Kurs arama için giriş alanı
        self.search_entry = tk.Entry(self.info_frame)
        self.search_entry.pack()

        # Arama düğmesi
        self.search_button = tk.Button(self.info_frame, text="Kursları Ara", command= self.search_courses)
        self.search_button.pack()

        # Enter tuşuna basıldığında arama yapmak için olay dinleyiciyi (event listener) ekleyin
        self.search_entry.bind("<Return>", self.search_courses)

    def create_course_buttons(self, keyword):
        for widget in self.button_frame.winfo_children():
            widget.destroy()  # Önceki kurs butonlarını temizle

        for index, row in self.data.iterrows():
            course_name = row['Course Name']

            if keyword.lower() in course_name.lower():
                btn_single_course = tk.Label(self.button_frame, width=70, height = 7, bd=3, relief="raised")
                btn_single_course.pack(fill = tk.BOTH, padx=5, pady=5)

                try:
                # Resim dosyasının yolu, kurs adına bağlı olarak ayarlanmalıdır.
                    image_path = f'images/{course_name}/img0.png' # Bu örnekte "images" klasöründen resimleri alıyoruz.
                    img = Image.open(image_path)

                except:  # if there is error use default image
                    image_path = "images/python.png"
                    img = Image.open(image_path)
                
                # Resmi aç ve istediğiniz boyuta yeniden boyutlandır
                
                img = img.resize((100, 100), Image.Resampling.LANCZOS)  # Özel boyutlandırmayı burada ayarlayabilirsiniz
                img = ImageTk.PhotoImage(img)

                # Resim etiketi oluşturun ve ekrana yerleştirin
                image_label = tk.Label(btn_single_course, image=img)
                image_label.image = img
                image_label.pack(side=tk.LEFT, padx=5, pady=5)

                # Kurs adı ve derecelendirmeyi içeren etiketi oluşturun ve ekrana yerleştirin
                course_info_label = tk.Label(btn_single_course, text=f"{course_name}\nRating: {row['Course Rating']}", justify=tk.LEFT)
                course_info_label.pack(side=tk.LEFT, padx=5, pady=5)

                # Kurs butonunu oluşturun
                command = lambda name=course_name: self.show_course_details(name)
                button = tk.Button(btn_single_course, text="Daha Fazla Bilgi", width=15, command=command, justify=tk.RIGHT)
                button.pack(side=tk.RIGHT, padx=5, pady=5)

                # Kurs butonunu sözlüğe ekleyin
                self.course_buttons[course_name] = btn_single_course       

    def show_course_details(self, course_name):
        # seçilen kurs
        selected_course = self.data[self.data['Course Name'] == course_name].iloc[0]

        # Kurs ayrıntılarını görüntülemek için istediğiniz işlemi yapabilirsiniz.
        for widget in self.info_frame.winfo_children():
            if widget not in [self.search_button, self.search_entry]:
                widget.destroy()  # Önceki kurs bilgilerini temizle
        
        for column in self.course_items:
            label = tk.Label(self.info_frame, text=f"{column}: {selected_course[column]}", wraplength=300)
            label.pack(fill=tk.BOTH, expand=True)


    def search_courses(self, event=None):
        keyword = self.search_entry.get().lower()
        
        for key in self.course_buttons:
            self.course_buttons[key].destroy()

        self.course_buttons.clear()
        
        self.create_course_buttons(keyword)


if __name__ == '__main__':

    root = tk.Tk()

    courses = Courses(root)

    root.mainloop()
