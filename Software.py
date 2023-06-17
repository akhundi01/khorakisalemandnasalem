from tkinter import *  # کتابخونه تکینتر رو اضافه کن
from PIL import Image, ImageTk
from tkinter.messagebox import *
import speech_recognition as sr
from time import *
from pyttsx3 import *
from notifypy import *
from datetime import *
from openpyxl import Workbook
import sqlite3
import os  # کتابخونه های اس کیو لایت سه و او اس رو اضافه کن


boolan = True


class MainApp(Tk):  # ساخت یک کلاس و ارث بری از کتابخونه ی تکینتر
    def __init__(self):  # ساخت تابع اینشیالایزر یا سازنده
        global boolan
        super().__init__()
        if boolan == True:
            n = Notify()
            n.title = "خوش آمدگویی"
            n.message = 'به نرم افزار خوش آمدید.'
            n.icon = "Icon.ico"
            n.send()  # ارسال اعلان بر اساس اطلاعاتی که داده شده
            boolan = False
        else:
            pass

        self.title("خوراکی‌های‌ سالم و ناسالم")  # قرار دادن عنوان پنجره
        # طول و عرض نرم افزار تغییر نکنید
        self.resizable(width=False, height=False)
        self.iconbitmap('Icon.ico')  # قرار دادن آیکون نرم افزار

        # ساخت تابع که وظیفه بسته شدن برنامه را دارد
        def exit_mainapp(event): self.destroy()

        image = ImageTk.PhotoImage(Image.open('img/D1.jpg'))
        # گذاشتن برچسب که عکسی را نشان می دهد
        self.label = Label(self, image=image)

        self.open_learn = Button(self, text='آموزش', bg="#00cde8", padx=30, bd=0, pady=10, font=(
            'B Titr', 8), fg='white')  # ساخت باتن یا کلید که از فونت بی تیتر استفاده می کند و متن و اندازه و غیره آن مشخص شده است

        self.open_game = Button(self, text='بازی', bg="#ffcf00", padx=30, bd=0, pady=10, font=(
            'B Titr', 8), fg='white')  # ساخت باتن

        self.open_designers = Button(
            self, text='طراحان', bg="#065381", fg='white', command=lambda: self.open_designers_func(), padx=30, bd=0, pady=10, font=(
                'B Titr', 8))

        self.btn_open_assistant = Button(self, text='دستیار صوتی', padx=27, pady=10, font=(
            'B Titr', 8), fg='white', bd=0, command=lambda: self.assistant(), bg="#fe2635")

        # قرار داردن مختصات قرارگیری دکمه ها و برچسب ها و غیره
        self.open_learn.place(y=260, x=338)
        self.open_game.place(y=340, x=338)
        self.open_designers.place(y=180, x=275)
        self.btn_open_assistant.place(x=270, y=425)

        self.label.pack()

        # هنگامی روی باتن مورد نظر کلیک شد این تابع فراخوانی شود
        self.open_learn.config(command=self.open_learn_func)
        self.open_game.config(command=self.open_game_func)

        # هنگامی که این کلید ها روی کیبرد فشار داده شده  تابعه ای اجرا شود
        self.bind('<Control-w>', exit_mainapp)
        self.mainloop()

    def open_learn_func(self):
        self.destroy()  # پنجره رو ببند
        LearnApp()  # و این کلاس رو اجرا کن

    def open_game_func(self):
        self.destroy()
        GUI()

    def open_designers_func(self):
        Designers()

    def assistant(self):
        try:  # چک می کنه هنگامی که خطای ساختاری داد برنامه متوقف نشه
            r = sr.Recognizer()
            with sr.Microphone() as source:
                r.pause_threshold = 1
                r.adjust_for_ambient_noise(source)
                audio = r.listen(source)
                # حرفی که می زنیم رو به زبان فارسی تشخیص بده
                text = r.recognize_google(audio, language='fa-IR')
                # گذاشتن شرط ها
                if text == 'سلام':
                    speak("Hello")
                elif text == 'اسمت چیه':
                    speak('else')
                elif text == 'آموزش' or text == "وارد بخش آموزش شو" or text == 'بخش آموزش رو باز کن' or text == 'بخش اول' or text == 'اول' or text == 'اولی':
                    self.destroy()
                    LearnApp()
                elif text == 'ساعت' or text == "ساعت چنده":
                    d = datetime.now()
                    showinfo("زمان", "{}".format(
                        d.strftime("%H : %M : %S         ")))
                elif text == 'بازی' or text == "وارد بخش بازی شو" or text == 'بخش بازی رو باز کن' or text == 'بخش سوم' or text == 'سوم' or text == 'آخری':
                    self.destroy()
                    GUI()
                    MainApp()
                elif text == 'خداحافظ' or text == "ببند" or text == "بسته شو" or text == 'خارج شو':
                    self.destroy()
                elif text == 'رایانه خاموش' or text == "رایانه رو خاموش کن":
                    os.system('Shutdown /s') if askyesno("پرسش",
                                                         "آیا از خاموش کردن رایانه اطمینان دارید؟") == YES else showinfo("", ".عملیات لغو شد")
                else:
                    showinfo('', ".ببخشید من جوابی برای این سوال ندارم")
        except:
            # نشان دادن جعبه پیام
            showerror(
                '', '.لطفا میکروفون به رایانه خود متصل کنید یا با من صحبت کنید')


class LearnApp(Tk):  # پنجره ای رو می سازه که چند اسلاید رو نشان می ده
    count = 1

    def __init__(self):
        self.zero_all()  # فراخوانی تابع مورد نظر
        super().__init__()

        self.iconbitmap('Icon.ico')
        self.title('آموزش')
        self.resizable(width=False, height=False)

        def right(event): self.right_picture()
        def left(event): self.left_picture()

        def open_mainapp(event):
            self.destroy()
            MainApp()

        self.logo_App = ImageTk.PhotoImage(Image.open('img/A1.jpg'))
        self.logo1 = ImageTk.PhotoImage(Image.open('img/right.png'))
        self.logo2 = ImageTk.PhotoImage(Image.open('img/left.png'))
        self.logo3 = ImageTk.PhotoImage(Image.open('img/home.png'))
        self.back_logo = ImageTk.PhotoImage(Image.open('img/back.png'))

        self.label = Label(self, image=self.logo_App)
        self.right_btn = Button(self, image=self.logo1, bg='white',
                                width=55, pady=20, command=lambda: self.right_picture())
        self.left_btn = Button(self, image=self.logo2, bg='white',
                               width=50, pady=20, command=lambda: self.left_picture())
        self.home_btn = Button(self, image=self.logo3,
                               command=lambda: self.open_MainApp())
        self.back_btn = Button(self, image=self.back_logo,
                               command=lambda: self.back_func())

        self.label.pack()
        self.right_btn.place(x=938, y=310, rely=.4)
        self.left_btn.place(x=7.5, y=560)
        self.home_btn.place(x=5, y=5)
        self.back_btn.place(y=5, x=54)

        self.left_btn['border'] = 0.5  # ضخامت باتن رو مشخص می کنه
        self.right_btn['border'] = 0.5

        self.bind('<Right>', right)
        self.bind("<Left>", left)
        self.bind('<Control-w>', open_mainapp)
        self.mainloop()
        MainApp()

    def right_picture(self):
        LearnApp.count += 1
        if LearnApp.count < 9:
            print(LearnApp.count)
            self.logo = ImageTk.PhotoImage(Image.open(
                'img/A{}.jpg'.format(LearnApp.count)))
            self.label.config(image=self.logo)
            self.label.pack()
        else:
            self.destroy()
            MainApp()

    def left_picture(self):
        LearnApp.count -= 1
        if LearnApp.count < 22:
            self.logo = ImageTk.PhotoImage(Image.open(
                'img/A{}.jpg'.format(LearnApp.count)))
            self.label.config(image=self.logo)
            self.label.pack()
        else:
            self.destroy()
            MainApp()

    def back_func(self):  # تابعی که اولین اسلاید رو نشون می ده
        self.logo = ImageTk.PhotoImage(Image.open('img/A1.jpg'))
        self.label.config(image=self.logo)
        LearnApp.count = 1

    def open_MainApp(self):
        self.destroy()
        MainApp()

    def zero_all(self):
        LearnApp.count = 1


class Designers(Tk):  # پنجره ای که نام برنامه نویس ها و غیره را نشان می دهد و مانند کلاس های دیگر از کلاس تی کی استفاده می کند
    def __init__(self):
        super().__init__()

        self.title('طراحان')
        self.iconbitmap("Icon.ico")

        self.geometry("300x400")  # طول و عرض صفحه را مشخص می کند
        self.resizable(height=False, width=False)
        self.config(bg="#065381")  # رنگ بک گراند صفحه

        Label(self, text=':برنامه نویس ', font=('B Titr', 11),
              bg='#065381', fg='white').place(x=200, y=125)
        Label(self, text=':برنامه نویس ', font=('B Titr', 11),
              bg='#065381', fg='white').place(x=200, y=80)
        Label(self, text=':دبیر راهنما ', font=('B Titr', 11),
              bg='#065381', fg='white').place(x=200, y=45)
        Label(self, text=':مدرسه ', font=('B Titr', 11),
              bg='#065381', fg='white').place(x=200, y=10)  # برجسب ها

        Label(self, text="شاهد کردکوی", font=('B Titr', 11),
              bg='#065381', fg='white').place(x=111, y=10)
        Label(self, text="دکتر احمد مهرانی", font=('B Titr', 11),
              bg='#065381', fg='white').place(x=90, y=45)
        Label(self, text="محمدحسین آخوندی", font=('B Titr', 11),
              bg='#065381', fg='white').place(x=75, y=80)
        Label(self,  text="حسن دودانگی", font=('B Titr', 11),
              bg='#065381', fg='white').place(x=110, y=125)

        self.mainloop()  # تا وقتی کاربر برنامه رو نبست کد ها اجرا شن


class GUI(Tk):
    def __init__(self):
        super().__init__()

        self.create_db()  # تابعی را فراخوانی می کند

        self.title("بازی")
        self.resizable(width=False, height=False)
        self.iconbitmap('Icon.ico')

        bg = ImageTk.PhotoImage(Image.open("img\\H1.jpg"))
        bg_lbl = Label(self, image=bg)  # بک گراند صفحه رو نمایش می دهد
        bg_lbl.pack()

        btn_1 = Button(self, bd=0, bg="#010101", text="ایجاد حساب", fg="white", padx=60, font=(
            "B Titr", 11), command=lambda: self.run_register())
        btn_2 = Button(self, text="ورود‌ به حساب", bd=0, bg="#7eff02", padx=60, font=(
            "B Titr", 11), command=lambda: self.run_login())

        # i1, i3 = PhotoImage(file="img\\11.png"), PhotoImage(file="img\\33.png")
        # self.img_btn1, self.img_btn2 = Button(self, image=i1), Button(self, image=i3)

        level1_btn = Button(self, text="بازی اول", font=(
            "B Titr", 8), padx=7, pady=10, bg="#57901b", bd=0, fg="white")
        level2_btn = Button(self, text='بازی دوم', font=(
            "B Titr", 8), padx=7, pady=10, bg="#f67b11", bd=0, fg="white")

        m = Menu(self)  # ساخت منو
        # قرار دادن چند گزینه در منو
        m.add_command(label="ایجاد حساب", command=self.run_register)
        m.add_command(label="ورود به حساب", command=self.run_login)
        m.add_command(label="امتیازات", command=self.run_scoreuser)
        m.add_command(label="راهنما", command=self.run_guide)

        # self.img_btn1.config(command=lambda: self.func('level 1'))# هنگامی کاربر روی کلید مورد نظر کلیک کرد تابعی که بهش داده شده احرا شن
        # self.img_btn2.config(command=lambda: self.func('level 2'))

        level1_btn.config(command=lambda: self.func('level 1'))
        level2_btn.config(command=lambda: self.func('level 2'))

        # مکان قرار گیری باتن ها منو و غیره
        # self.img_btn2.place(x=530, y=215)
        # self.img_btn1.place(x=115, y=215)

        btn_1.place(x=180, y=63)
        btn_2.place(x=430, y=63)

        level1_btn.place(x=150, y=375)
        level2_btn.place(x=577, y=375)

        self.config(menu=m)

        self.mainloop()
        # بعد از بسته شدن این پنجره پنجره ای دیگه باز بشه
        MainApp()

    def run_register(self):
        self.destroy()  # این پنجره رو می بنده
        RegisterUser()
        GUI()

    def run_login(self):
        self.destroy()
        LoginUser()
        GUI()

    def run_guide(self):
        self.destroy()
        GuideApp()
        GUI()

    def run_scoreuser(self):
        self.destroy()
        ScoreUser()
        GUI()

    def func(self, x):
        if x == "level 1":
            if len(LoginUser.loginlist) == 0:
                showwarning(
                    "", "برای اسفاده از این بازی ابتدا به حساب خود وارد شوید")
            else:
                self.destroy()
                G1()
        elif x == "level 2":
            self.destroy()
            G2()
            GUI()

    def create_db(self):

        conn = sqlite3.connect('db.db')
        cur = conn.cursor()
        cur.execute(
            "CREATE TABLE IF NOT EXISTS my_table(name text,username text,psw text);")  # جدولی را در دیتابیس ایجاد می کند
        conn.commit()
        conn.close()


class RegisterUser(Tk):
    def __init__(self):
        super().__init__()

        self.title("ایجاد حساب")
        self.geometry("400x300")
        self.iconbitmap('Icon.ico')
        self.resizable(False, False)

        self.v_fname, self.v_username, self.v_psw = StringVar(), StringVar(), StringVar()

        self.lbl_fisrtname = Label(self, text=' : نام ', font=('B Titr', 11))
        self.lbl_username = Label(
            self, text=' : نام کاربری', font=('B Titr', 11))
        self.lbl_psw = Label(self, text=' : رمز عبور ', font=('B Titr', 11),)

        self.e_fname = Entry(self, width=32, bd=2,
                             justify='right', textvariable=self.v_fname)  # گرفتن ورودی از کاربرد و ورودی را در متغیری می ریزد
        self.e_username = Entry(self, width=32, bd=2,
                                justify='right', textvariable=self.v_username)
        self.e_psw = Entry(self, width=32, bd=2,
                           justify='right', show="*", textvariable=self.v_psw)

        self.save_user_btn = Button(self, text="ثبت", font=(
            'B Titr', 9), width=10, bd=2, command=lambda: self.save_user_func())

        # مختصات قرار گیری برچسب ها و غیره
        self.lbl_fisrtname.place(x=300, y=5)
        self.lbl_username.place(x=300, y=40)
        self.lbl_psw.place(x=300, y=75)
        self.e_fname.place(x=100, y=12)
        self.e_username.place(x=100, y=51)
        self.e_psw.place(x=100, y=82)
        self.save_user_btn.place(x=155, y=160)

        self.mainloop()

    def save_user_func(self):
        # اگر همه ورودی ها پر شده باشد کد های درونش را اجرا می کند
        if len(self.v_fname.get()) > 0 and len(self.v_username.get()) > 0 and len(self.v_psw.get()) > 0:

            conn = sqlite3.connect("db.db")
            cur = conn.cursor()
            cur.execute("SELECT * FROM my_table WHERE username = ? or psw = ?",
                        (self.v_username.get(), self.v_psw.get(),))
            fet = cur.fetchall()  # اطلاعات این جدول را در این متغیر می ریزد
            if fet:
                # چک می کنه که آیا اطلاعات از قبل وجو داشت یا خیر
                showwarning(
                    "", "متاسفانه نام کاربری شما قبلا در سیستم ثبت شده است")
            else:  # اگر از قبل وجود نداشت این کدا ها اجرا میشوند
                conn = sqlite3.connect("db.db")
                cur = conn.cursor()
                cur.execute("INSERT INTO my_table VALUES (:name,:username,:psw)", {
                            'name': self.v_fname.get(), "username": self.v_username.get(), "psw": self.v_psw.get()})  # اطلاعات را در ستون های مشخص شده می ریزد
                conn.commit()
                conn.close()

                conn = sqlite3.connect('db.db')
                cur = conn.cursor()
                cur.execute(
                    f"CREATE TABLE IF NOT EXISTS {self.v_username.get()}(level text, score text)")  # و جدولی برای نام کاربری داده شده می سازد
                conn.commit()  # کوئری ها را اجرا می کند
                conn.close()  # و دیتا بیس را می بندد

                # و در آخر پیامی را نشان می دهد
                showinfo("تبریک", "ثبت نام با موفقیت انجام شد")

            self.v_fname.set('')  # و ورودی ها را خالی می کند
            self.v_username.set('')
            self.v_psw.set('')

        # اگر هر یک از ورودی ها خالی باشد پیام خاصی را نشان می دهد
        elif len(self.v_fname.get()) == 0:
            showwarning("هشدار", "لطفا نام خود را وارد کنید")
        elif len(self.v_username.get()) == 0:
            showwarning("هشدار", "لطفا نام کاربری :  خود را وارد کنید")
        elif len(self.v_psw.get()) == 0:
            showwarning("هشدار", "لطفا رمز عبور خود را وارد کنید")


class LoginUser(Tk):
    b = False
    loginlist = []

    def __init__(self):
        super().__init__()
        self.loginlist.clear()

        self.title("ورود به حساب")
        self.iconbitmap("Icon.ico")
        self.geometry("400x300")
        self.resizable(width=False, height=False)

        self.v_username, self.v_psw = StringVar(), StringVar()
        self.lbl_username = Label(
            self, text=' : نام کاربری', font=('B Titr', 11))
        self.lbl_psw = Label(self, text=' : رمز عبور ', font=('B Titr', 11))

        self.e_username = Entry(self, width=32, bd=2,
                                justify='right', textvariable=self.v_username)
        self.e_psw = Entry(self, width=32, bd=2, justify='right',
                           show="*", textvariable=self.v_psw)

        self.btn_re = Button(self, text="ورود", command=lambda: self.login(), font=(
            'B Titr', 9), width=10, bd=2)

        self.show_user_btn = Button(self, text='نمایش کاربران', font=(
            'B Titr', 9), width=10, bd=2, command=lambda: self.show_list_user())

        self.li = Listbox(self, width=35, height=17,
                          justify='right', font=('Tahoma', 10, 'bold'), bd=2)  # ساخت لیست باکس

        self.lbl_username.place(x=300, y=10)
        self.lbl_psw.place(x=300, y=44)
        self.e_username.place(x=100, y=17)
        self.e_psw.place(x=100, y=51)
        self.show_user_btn.place(x=5, y=259)
        self.btn_re.place(x=150, y=120)
        self.show_user_btn.place(x=5, y=259)

        self.mainloop()

    def view(self):
        # اطلاعاتی که از قبل در لیست باکس ذخیره شده بود را پاک می کند
        self.li.delete(0, 'end')
        conn = sqlite3.connect('db.db')
        cur = conn.cursor()
        cur.execute('SELECT name FROM my_table')
        row = cur.fetchall()
        for r in row:
            for i in r:
                # و هر کدام را به لیست باکس اضافه می کند
                self.li.insert('end', i)

    def show_list_user(self):
        if LoginUser.b == False:
            self.geometry('700x300')  # اندازه صفحه را تغییر می دهد
            self.li.place(x=400)
            self.view()
            LoginUser.b = True
        elif LoginUser.b == True:
            self.geometry('400x300')
            LoginUser.b = False

    def login(self):
        if len(self.v_username.get()) > 0 and len(self.v_psw.get()) > 0:
            conn = sqlite3.connect('db.db')
            cur = conn.cursor()
            cur.execute('SELECT * FROM my_table WHERE username = ?  AND psw = ?',
                        (self.v_username.get(), self.v_psw.get(),))

            result = cur.fetchall()

            if result:  # اگر اطلاعات درست باشد این کد ها را اجرا می کند
                for r in result:
                    showinfo('خوش آمد گویی',
                             '{} خوش آمدید'.format(r[0]))
                LoginUser.loginlist.append('{}'.format(self.v_username.get()))
                # و یک فایل تکست درست می کند و نام کاربری را در آن میریزد
                f = open("file.txt", 'w+')
                f.write(f"{self.v_username.get()}")
                f.close()

                self.v_username.set("")
                self.v_psw.set("")
            else:
                conn = sqlite3.connect('db.db')
                cur = conn.cursor()
                cur.execute("SELECT * FROM my_table WHERE username = ?",
                            (self.v_username.get(), ))
                fet = cur.fetchall()
                if not fet:
                    showwarning(
                        "هشدار", "نام کاربری وارد شده در سیستم موجود نمی باشد")
                else:
                    showerror("", "رمزعبور نادرست است")
        else:
            # چک می کند که آیا همه ورودی ها پر شده یا خیر
            if len(self.v_username.get()) == 0:
                showwarning('هشدار', 'لطفا نام کاربری :  خود را وارد کنید')
            elif len(self.v_psw.get()) == 0:
                showwarning("هشدار", "لطفا رمز عبور خود را وارد کنید")
            else:
                conn = sqlite3.connect('db.db')
                cur = conn.cursor()
                cur.execute(
                    "SLELCT * FROM my_table WHERE username = ?", (self.v_username.get(), ))
                fet = cur.fetchall()
                if not fet:
                    print('Hello')


class ScoreUser(Tk):  # پنجره ای که امتیازات را نشان می دهد
    def __init__(self):
        super().__init__()

        self.title('امتیازکاربران')
        self.geometry("700x450")
        self.iconbitmap('Icon.ico')
        self.resizable(False, False)
        self.config(bg="#1a75ff")

        self.e = StringVar()  # متغیری می سازد

        self.li = Listbox(self, width=75, height=13, justify='right', font=(
            'B Titr', 10), bg="#1a75ff", fg='white')  # ساخت لیست باکس
        Label(self, text=" : نام کاربری", font=("B Titr", 13),
              bg="#1a75ff", fg="white").place(x=600, y=5)
        self.entry = Entry(self, width=50, bd=2, justify='right',
                           textvariable=self.e)  # گرفتن ورودی
        self.btn = Button(self, text="جستوجو", bd=2, font=(
            "B Titr", 9), padx=40, command=lambda: self.view(), bg='#1a75ff', fg='white')
        b = ImageTk.PhotoImage(Image.open("img\\print.png"))
        Button(self, image=b, command=lambda: self.func_print()).place(x=5, y=395)

        # مکان قرارگیری دکمه ها و غیره
        self.entry.place(x=260, y=17)
        self.li.place(x=232, y=120)
        self.btn.place(x=360, y=60)

        self.mainloop()
        # پس از بسته شدن این کلاس را اجرا می کند
        GUI()

    def view(self):
        def view_list(x):
            li = list()

            self.li.delete(0, 'end')  # اطلاعات قبلی موجود را پاک می کند
            conn = sqlite3.connect("db.db")
            cur = conn.cursor()  # اطلاعات را از این جدول واکشی می کند
            cur.execute(f"SELECT level, score FROM {x}")
            fet = cur.fetchall()

            var = 0
            for i in fet:
                var += 2
                for r in i:
                    li.append(r)

                    def show_level():
                        if str(li[-2 + var]) == "doz 1":
                            return "دوز مرحله اول"
                        if str(li[-2 + var]) == "doz 2":
                            return "دوز مرحله دوم"
                        if str(li[-2 + var]) == "doz 3":
                            return "دوز مرحله سوم"
                        if int(li[-2+var]) == 11:
                            return "مرحله اول "
                        if int(li[-2+var]) == 22:
                            return "مرحله دوم "
                        if int(li[-2+var]) == 33:
                            return "مرحله سوم "
                        if int(li[-2+var]) == 1:
                            return "مرحله اول "
                        if int(li[-2+var]) == 2:
                            return "مرحله دوم "
                        if int(li[-2+var]) == 3:
                            return "مرحله سوم "

                # print(li[-2 + var],"                   ",li[-1 + var])
                # امتیاز و مرحله را به لیست باکس اضافه می کند
                self.li.insert(
                    "end", f"{li[-1+var]}                                                                                                                    {show_level()}")

        def search():
            if len(self.e.get()) > 0:
                view_list(self.e.get())
            else:
                showwarning('! هشدار', 'لطفا نام کاربر را وارد کنید')
        search()

    def func_print(self):
        # ساخت فایل دیتا بیس
        workbook = Workbook()
        sheet = workbook.active

        # برقراری ارتباط با دیتابیس
        conn = sqlite3.connect('db.db')
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM {self.e.get()}")
        fet = cur.fetchall()
        mylist = list()

        # قرارگیری اطلاعات در مختصات داده شده
        sheet["A1"] = f"{self.e.get()}"
        sheet["B1"] = "نام کاربری : "
        sheet["A2"] = "مرحله"
        sheet["B2"] = " امتیاز شما"

        v1 = 1
        v2 = 2
        for r in fet:
            # اطلاعات را از دیتابیس می گیرد و به فایل اکسل اضافه می کند
            for i in r:
                mylist.append(i)
            sheet[f"B{3+v1}"] = f"{mylist[-1+v2]}"
            sheet[f"A{3+v1}"] = f"{mylist[-2+v2]}"

            v1 += 1  # هر دفعه یک واحد به این متغیر اضافه می کند
            v2 += 2

        # فایل اکسل را ذخیره می کند
        workbook.save(filename=f"{self.e.get()}.xlsx")

        # و آن را اجرا می کند و چاپ می کند
        os.startfile(f'{self.e.get()}.xlsx', 'print')


class GuideApp(Tk):  # ساخت پنجره ای که راهنمای نرم افزار است

    def __init__(self):
        super().__init__()

        self.title("راهنما")
        self.geometry("400x400")
        self.iconbitmap("Icon.ico")
        self.resizable(width=False, height=False)
        self.config(bg="white")

        logo_r = ImageTk.PhotoImage(Image.open("img\\R.jpg"))
        l_r = Label(self, image=logo_r, font=("B titr", 15),
                    bd=0)  # ساخت برچسب که ضخامت آن صفر است

        logo_space = ImageTk.PhotoImage(Image.open("img\\space.jpg"))
        l_space = Label(self, image=logo_space, bg='white')

        Label(self, text="آغاز بازی و شروع مجدد بازی   :  ",
              font=("B titr", 12), bg='white').place(x=100, y=33)
        Label(self, text="پرش پرنده به بالا    :  ", font=(
            "B titr", 12), bg='white').place(x=170, y=142)

        # مختصات قرارگیری آنها
        l_r.place(x=300, y=1)
        l_space.place(x=295, y=110)

        self.mainloop()


class G1(Tk):
    def __init__(self):
        super().__init__()

        self.title("بازی اول")
        self.resizable(False, False)
        self.iconbitmap("Icon.ico")

        self.logo = ImageTk.PhotoImage(Image.open("img/H3.jpg"))
        Label(self, image=self.logo).pack()

        btn1, btn2, btn3 = Button(self, text="مرحله اول", bg="#57901b", font=("B Titr", 8), bd=0, padx=7, pady=10, fg="white"), Button(self, text="مرحله دوم", bg="#7b1b0d",  font=(
            "B Titr", 8), bd=0, padx=7, fg="white", pady=10), Button(self, text="مرحله سوم", bg="#f67b11", font=("B Titr", 8), padx=7, pady=10, fg="white", bd=0)

        btn1.config(command=lambda: self.open_game_1())
        btn2.config(command=lambda: self.open_game_2())
        btn3.config(command=lambda: self.open_game_3())

        btn1.place(x=149, y=375)
        btn2.place(x=370, y=375)
        btn3.place(x=576, y=375)

        self.mainloop()
        GUI()

    def open_game_1(self):
        self.destroy()
        import game_1_1

    def open_game_2(self):
        self.destroy()
        import game_1_2

    def open_game_3(self):
        self.destroy()
        import game_1_3


class G2(Tk):
    user1list, user2list = [], []

    def __init__(self):
        G2.user1list.clear()
        G2.user2list.clear()

        super().__init__()

        self.iconbitmap("Icon.ico")
        self.title("بازی اول")
        self.resizable(False, False)

        self.logo = ImageTk.PhotoImage(Image.open("img/H2.jpg"))
        Label(self, image=self.logo).pack()

        user_1 = Button(self, bd=0, bg="#7eff02", text="کاربر اول", fg="black", padx=60, font=(
            "B Titr", 11), command=lambda: self.open_login_1())
        user_2 = Button(self, bd=0, bg="#010101", text="کاربر دوم", fg="white", padx=60, font=(
            "B Titr", 11), command=lambda: self.open_login_2())

        btn1, btn2, btn3 = Button(self, text="مرحله اول", bg="#57901b", font=("B Titr", 8), bd=0, padx=7, pady=10, fg="white", command=lambda: self.func("1")), Button(self, text="مرحله دوم", bg="#7b1b0d",  font=(
            "B Titr", 8), bd=0, padx=7, fg="white", pady=10, command=lambda: self.func("2")), Button(self, text="مرحله سوم", bg="#f67b11", font=("B Titr", 8), padx=7, pady=10, fg="white", bd=0, command=lambda: self.func("3"))

        user_1.place(x=438, y=63)
        user_2.place(x=180, y=63)
        btn1.place(x=149, y=375)
        btn2.place(x=370, y=375)
        btn3.place(x=576, y=375)

        self.mainloop()
        GUI()

    def open_login_1(self):
        self.destroy()
        LoginUser()
        l = LoginUser.loginlist[len(
            LoginUser.loginlist) - 1: len(LoginUser.loginlist)]
        for i in l:
            file = open("file1.txt", 'w+')
            file.write(f"{i}")
            file.close()
        G2()

    def open_login_2(self):
        self.destroy()
        LoginUser()
        l2 = LoginUser.loginlist[len(
            LoginUser.loginlist) - 1: len(LoginUser.loginlist)]
        for i2 in l2:
            file = open("file2.txt", 'w+')
            file.write(f"{i2}")
            file.close()
        G2()

    def func(self, x):
        file_1 = open("file1.txt", "r")
        read_file_1 = file_1.read()
        file_1.close()

        # --------------------------------------

        file_2 = open("file2.txt", "r")
        read_file_2 = file_2.read()
        file_2.close()

        if x == "1":
            if len(str(read_file_1)) == 0:
                showwarning("هشدار", "")
            if len(str(read_file_2)) == 0:
                showwarning("هشدار", "")
            else:
                self.destroy()
                import game_2_1 as g
                g.app()
                G2()
        elif x == "2":
            if len(str(read_file_1)) == 0:
                showwarning("هشدار", "")
            if len(str(read_file_2)) == 0:
                showwarning("هشدار", "")
            if len(str(read_file_1)) != 0 and len(str(read_file_2)) != 0:
                self.destroy()
                import game_2_2 as g
                g.app()
                G2()
        elif x == "3":
            if len(str(read_file_1)) == 0:
                showwarning("هشدار", "")
            if len(str(read_file_2)) == 0:
                showwarning("هشدار", "")
            if len(str(read_file_1)) != 0 and len(str(read_file_2)) != 0:
                self.destroy()
                import game_2_3 as g3
                g3.app()
                G2()
