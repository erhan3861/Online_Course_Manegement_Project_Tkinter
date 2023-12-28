import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from PIL import Image, ImageTk
from sqlalchemy import create_engine, Column, Integer, String, DateTime, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

# SQLAlchemy ile veritabanı bağlantısını oluştur
engine = create_engine('sqlite:///app_usage.db', echo=False)
Base = declarative_base()

class UserUsage(Base):
    __tablename__ = 'register'

    id = Column(Integer, primary_key=True)
    username = Column(String)
    name = Column(String)
    surname = Column(String)
    number = Column(String)
    login_time = Column(DateTime)
    profile_picture_path = Column(String)
    # eklemek istedğimiz ilave verileri buraya yazıyoruz

Base.metadata.create_all(engine)

class StudentRegistrationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Öğrenci Kaydı Uygulaması")

        # Kullanıcı Adı Etiketi ve Giriş Alanı
        self.username_label = tk.Label(root, text="Kullanıcı Adı:")
        self.username_label.pack()
        self.username_entry = tk.Entry(root)
        self.username_entry.pack()

        # İsim ve Soyisim Etiketi ve Giriş Alanları
        self.name_label = tk.Label(root, text="İsim:")
        self.name_label.pack()
        self.name_entry = tk.Entry(root)
        self.name_entry.pack(pady=10)

        self.surname_label = tk.Label(root, text="Soyisim:")
        self.surname_label.pack()
        self.surname_entry = tk.Entry(root)
        self.surname_entry.pack(pady=10)

        # Öğrenci Numarası Etiketi ve Giriş Alanı
        self.number_label = tk.Label(root, text="Öğrenci Numarası:")
        self.number_label.pack()
        self.number_entry = tk.Entry(root)
        self.number_entry.pack(pady=10)

        # Profil Resmi Ekleme Alanı
        self.image_path = None
        self.image_label = tk.Label(root, text="Profil Resmi: Yok")
        self.image_label.pack()

        self.browse_button = tk.Button(root, text="Select Photo", command=self.browse_image)
        self.browse_button.pack(pady=10)

        # Kayıt Düğmesi
        self.register_button = tk.Button(root, text="Register", command=self.register_student)
        self.register_button.pack(pady=10)

        # Profil Resmi Gösterme Label'i
        self.profile_picture_label = tk.Label(root, text="Profil Resmi: Yok")
        self.profile_picture_label.pack(pady=10)

    def browse_image(self):
        # Kullanıcıya resim seçme penceresi aç
        file_path = filedialog.askopenfilename(title="Profil Resmi Seç", filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif")])

        if file_path:
            self.image_path = file_path
            self.image_label.config(text=f"Profil Resmi: {os.path.basename(file_path)}")

    def register_student(self):
        # Kullanıcı adı, isim, soyisim, öğrenci numarası ve profil resmini al
        username = self.username_entry.get()

        # SQLAlchemy ile kullanıcı bilgilerini veritabanına kaydetme
        Session = sessionmaker(bind=engine)
        session = Session()
        
        if session.query(UserUsage).filter_by(username=username).first():
            messagebox.showerror("Hata", "Kullanıcı adı kayıtlıdır")
            return 

        name = self.name_entry.get()
        surname = self.surname_entry.get()
        number = self.number_entry.get()
        # ödev1 sorgulama ekle

        if username and name and surname and number:
            # Kullanıcı adını, adını, soyadını, öğrenci numarasını, kayıt zamanını ve profil resim yolu veritabanına kaydet
            new_entry = UserUsage(
                username=username,
                name=name,
                surname=surname,
                number=number,
                login_time=datetime.now(),
                profile_picture_path=self.save_profile_picture(username)
            )

            session = sessionmaker(bind=engine)()
            session.add(new_entry)
            session.commit()

            # Başarı mesajını göster
            success_message = tk.Label(self.root, text="Kayıt Başarılı!", fg="green")
            success_message.pack()
        else:
            # Bilgilerin eksik olduğu hata mesajını göster
            error_message = tk.Label(self.root, text="Lütfen tüm bilgileri girin", fg="red")
            error_message.pack()

    def save_profile_picture(self, username):
        # Kullanıcının adına göre profil resmini kaydet ve dosya yolu geri döndür
        user_folder = "profiles"
        if not os.path.exists(user_folder):
            os.makedirs(user_folder, exist_ok=True)

        if self.image_path:
            destination_path = os.path.join(user_folder, f"{username}.png")
            Image.open(self.image_path).save(destination_path)

            img = Image.open(destination_path)
            img = img.resize((300, 300), Image.LANCZOS)
            img = ImageTk.PhotoImage(img)

            self.profile_picture_label.config(image=img)
            self.profile_picture_label.image = img # referans gönderiyoruz

            # Kaydı göster mesajını göster
            record_message = tk.Label(self.root, text=self.username_entry.get(), fg="green")
            record_message.pack()

            return destination_path
        else:
            return None

if __name__ == "__main__":
    root = tk.Tk()
    app = StudentRegistrationApp(root)
    root.mainloop()
