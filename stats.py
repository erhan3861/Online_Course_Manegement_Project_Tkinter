import tkinter as tk
import matplotlib.pyplot as plt # görselleştirme
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg # tkinter görselleştirme sınıfı
from sqlalchemy import create_engine, Column, Integer, DateTime, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import sys

# Define the UserUsage class outside the UserStatsApp class
engine = create_engine('sqlite:///app_usage.db', echo=False)
Base = declarative_base()

class UserUsage(Base):
    __tablename__ = 'user_usage'

    id = Column(Integer, primary_key=True)
    username = Column(String)
    login_time = Column(DateTime)

Base.metadata.create_all(engine)

class UserStatsApp:
    def __init__(self, root): # otomatik çalışıyor
        self.root = root
        self.root.title("App User Login Time Statistics")
        self.root.geometry("1366x768") # ilave kod ile otomatik hesaplama


        # Global variables for Matplotlib figure and canvas
        self.fig, self.ax = plt.subplots()
        self.canvas = None

        # SQLAlchemy setup
        self.engine = create_engine('sqlite:///app_usage.db', echo=False)
        Base = declarative_base()

        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

        # Entry widget for the user to enter their name
        self.user_name_label = tk.Label(root, text="Enter Your Username:")
        self.user_name_label.pack()
        self.user_name_entry = tk.Entry(root)
        self.user_name_entry.pack()

        # Option menu to select time granularity
        self.time_granularity_label = tk.Label(root, text="Time Granularity:")
        self.time_granularity_label.pack()
        # optionmenu kodları
        self.granularity_var = tk.StringVar(value="Hours")
        self.granularity_options = ["Hours", "Minutes", "Seconds"]
        self.time_granularity_menu = tk.OptionMenu(root, self.granularity_var, *self.granularity_options)
        self.time_granularity_menu.pack()

        # Button to update user login time statistics based on the selected time granularity
        self.update_button = tk.Button(root, text="Update Statistics", command=self.update_statistics)
        self.update_button.pack()

    def update_statistics(self):
        username = self.user_name_entry.get() # kullanıcıdan aldığımız username
        user = self.session.query(UserUsage).filter(UserUsage.username == username).first()

        if user:
            login_time = datetime.now()
            new_user = UserUsage(username=username, login_time=login_time)
            self.session.add(new_user)
            self.session.commit()

            login_times = [row.login_time for row in self.session.query(UserUsage).filter(UserUsage.username == username)]
            self.ax.clear()

            if self.granularity_var.get() == "Hours":
                time_format = "%H"
            elif self.granularity_var.get() == "Minutes":
                time_format = "%M"
            else:
                time_format = "%S"

            login_time_strings = [time.strftime(time_format) for time in login_times]

            # figure
            self.fig.set_size_inches(10, 6)
            self.ax.hist(login_time_strings, bins=20, edgecolor='black')
            self.ax.set_xlabel("Login Time")
            self.ax.set_ylabel("Frequency")
            self.ax.set_title(f"Login Time Statistics for User '{username}'")

            if self.canvas:
                self.canvas.get_tk_widget().pack_forget()
            self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
            self.canvas.get_tk_widget().pack()

        else:
            tk.Label(self.root, text=f"User '{username}' does not exist. Please register first.").pack()
            login_time = datetime.now()
            new_user = UserUsage(username=username, login_time=login_time)
            self.session.add(new_user) # ekle
            self.session.commit() # kaydet
    

if __name__ == "__main__":
    root = tk.Tk()
    app = UserStatsApp(root)
    root.mainloop()
