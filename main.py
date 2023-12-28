import tkinter as tk
from tkinter import messagebox
from tkinter import PhotoImage  # Resim eklemek için PhotoImage kullanılır
from PIL import Image, ImageTk
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from passlib.hash import sha256_crypt
import anasayfa

# SQLite veritabanı oluşturma
engine = create_engine('sqlite:///user_credentials.db', echo=False)
Base = declarative_base()

# Kullanıcı bilgilerini temsil eden veritabanı tablosu
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)

Base.metadata.create_all(engine)

# Tkinter uygulaması oluşturma
app = tk.Tk()
app.title("Login")
app.geometry("1000x600")

# Arka plan resmini eklemek için ImageTk kullanımı
bg_image = Image.open("images/bg1.png")  # Arka plan resmi dosyasının adını ve yolunu belirtin
bg_image = bg_image.resize((1000, 600), Image.LANCZOS)  # Resmi pencere boyutuna uygun olarak yeniden boyutlandırın
bg_image = ImageTk.PhotoImage(bg_image)

bg_label = tk.Label(app, image=bg_image)
bg_label.place(relwidth=1, relheight=1)


# Giriş bilgileri giriş kutuları
bg_color = "#ebe4d4"
username_label = tk.Label(app, text="Kullanıcı Adı:", font=("Helvetica", 16), bg=bg_color)
username_label.place(x=100,y=250)

username_entry = tk.Entry(app, font=("Helvetica", 16), bg=bg_color)
username_entry.place(x=100,y=300)

password_label = tk.Label(app, text="Şifre:", font=("Helvetica", 16), bg=bg_color)
password_label.place(x=100,y=350)

password_entry = tk.Entry(app, show="*", font=("Helvetica", 16), bg=bg_color)
password_entry.place(x=100,y=400)

# Kullanıcıyı veritabanına kaydetme ve giriş işlemi
def save_user():
    username = username_entry.get()
    password = password_entry.get()

    # Şifreyi güvenli bir şekilde hashleme
    hashed_password = sha256_crypt.hash(password)

    # SQLAlchemy ile kullanıcı bilgilerini veritabanına kaydetme
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        new_user = User(username=username, password=hashed_password)
        session.add(new_user)
        session.commit()
        session.close()
        messagebox.showinfo("Başarılı", "Kullanıcı başarıyla kaydedildi.")
    except:
        messagebox.showerror("Hata", "Kullanıcı kayıt edilemedi!")

def login():
    global app
    username = username_entry.get()
    password = password_entry.get()

    # SQLAlchemy ile kullanıcı bilgilerini veritabanından sorgulama
    Session = sessionmaker(bind=engine)
    session = Session()

    user = session.query(User).filter_by(username=username).first()

    if user and sha256_crypt.verify(password, user.password):
        messagebox.showinfo("Başarılı", "Giriş başarılı!")
        liste = app.place_slaves()
        for l in liste:
            l.destroy()
        # anasayfayı projeye aktarıyoruz
        anasayfa.make_widgets(app)
                
    else:
        messagebox.showerror("Hata", "Kullanıcı adı veya şifre yanlış!")

    session.close()

# Kaydet ve Giriş butonları
save_button = tk.Button(app, text="Kaydet", command=save_user, font=("Helvetica", 16))
save_button.place(x=100,y=450)

login_button = tk.Button(app, text="Giriş   ", command=login, font=("Helvetica", 16))
login_button.place(x=250,y=450)


# Tkinter uygulamasını başlatma
app.mainloop()

