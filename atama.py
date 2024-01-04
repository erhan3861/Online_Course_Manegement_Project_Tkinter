import pandas as pd
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, text
from sqlalchemy.orm import sessionmaker
import tkinter as tk
from tkinter import ttk, messagebox

class Atama:
    def __init__(self):
        self.engine = create_engine('sqlite:///app_usage.db', echo=False)
        self.connection = self.engine.connect()
        self.metadata = MetaData()
        
        # Tabloyu tanımla
        self.secilen_kurslar = Table('atamalar', self.metadata,
                                     Column('id', Integer, primary_key=True),
                                     Column('kullanici_id', Integer),
                                     Column('isim', String),
                                     Column('kurs_adi', String))
        
        # Tabloyu oluştur
        self.metadata.create_all(self.engine)
        
        # CSV dosyasından kurs isimlerini DataFrame'e yükle
        self.df_kurslar = pd.read_csv("dataset.csv")

    def ara_kullanici(self, username):
        query = text(f"SELECT * FROM register WHERE username = '{username}'")
        result = self.connection.execute(query).fetchone()
        return result

    def ara_isim(self, name):
        query = text(f"SELECT * FROM register WHERE name = '{name}'")
        result = self.connection.execute(query).fetchone()
        return result

    def kurs_ara(self, id, kurs):
        query = text(f"SELECT * FROM atamalar WHERE kullanici_id = '{id}' and kurs_adi = '{kurs}'")
        result = self.connection.execute(query).fetchone()
        return result

    def goster_secim(self):
        kullanici_adi = self.entry_kullanici.get()
        isim = self.entry_isim.get()
        kurs_secimi = self.combo_kurs.get()

        # Kullanıcı adını veritabanında ara
        kullanici = self.ara_kullanici(kullanici_adi)
        aranan_isim = self.ara_isim(isim)

        if kullanici:
            # Kullanıcı adı bulundu, seçimleri göster
            messagebox.showinfo("Seçimler", f"Kullanıcı Adı: {kullanici.username}\nİsim: {kullanici.name}\nSeçilen Kurs: {kurs_secimi}")
        elif aranan_isim:
            messagebox.showinfo("Seçimler", f"Kullanıcı adı: {aranan_isim.username}\nİsim: {aranan_isim.name}\nSeçilen Kurs: {kurs_secimi}")
        else:
            messagebox.showerror("Hata", "Kullanıcı adı bulunamadı!")

    def kaydet(self):
        kullanici_adi = self.entry_kullanici.get()
        if not kullanici_adi:
            messagebox.showerror("Hata", "Kayıt için kullanıcı adı girmelisiniz.")
            return # kaydet tuşu çalışmıyor

        isim = self.entry_isim.get()
        kurs_secimi = self.combo_kurs.get()

        # Kullanıcı adını veritabanında ara
        kullanici = self.ara_kullanici(kullanici_adi)
        isim = self.ara_isim(isim)

        Session = sessionmaker(bind=self.engine)
        session = Session()

        if kullanici:
            # Daha önceden aynı kurs atanmışsa geri dön
            if self.kurs_ara(kullanici.id, kurs_secimi):
                messagebox.showerror("Hata", "Kullanıcı bu kursa önceden kayıt olmuştur")
                return
            
            # Seçilen kursu ayrı bir tabloya kaydet
            session.execute(self.secilen_kurslar.insert().values(kullanici_id=kullanici.id, isim=kullanici.name, kurs_adi=kurs_secimi))

            messagebox.showinfo("Başarı", "Seçimler başarıyla kaydedildi!")
        else:
            messagebox.showerror("Hata", "Kullanıcı adı bulunamadı!")

        session.commit()

    def baslat(self, root):
        # Tkinter arayüzünü oluştur
        self.root = root
        self.root.title("Kullanıcı ve Kurs Seçimi")
        # Kullanıcı adı giriş alanı
        label_kullanici = tk.Label(self.root, text="Kullanıcı Adı:")
        label_kullanici.pack(padx=10, pady=5)
        self.entry_kullanici = tk.Entry(self.root)
        self.entry_kullanici.pack(padx=10, pady=10)

        # İsim giriş alanı
        label_isim = tk.Label(self.root, text="İsim:")
        label_isim.pack(padx=10, pady=5)
        self.entry_isim = tk.Entry(self.root)
        self.entry_isim.pack(padx=10, pady=10)

        # Kurs seçimi için liste kutusu
        label_kurs = tk.Label(self.root, text="Kurs Seçimi:")
        label_kurs.pack(padx=10, pady=5)
        kurslar = self.df_kurslar['Course Name'].tolist()
        self.combo_kurs = ttk.Combobox(self.root, values=kurslar, state="readonly")
        self.combo_kurs.pack(padx=10, pady=10)

        # Göster ve Kaydet düğmeleri
        button_goster = tk.Button(self.root, text="Göster", command=self.goster_secim)
        button_goster.pack(padx=10, pady=10)

        button_kaydet = tk.Button(self.root, text="Kaydet", command=self.kaydet)
        button_kaydet.pack(padx=10, pady=10)

        # Tkinter ana döngüsünü başlat
        self.root.mainloop()

if __name__ == "__main__":
    # Uygulamayı başlat
    root = tk.Tk()
    atama_app = Atama()
    atama_app.baslat(root)
