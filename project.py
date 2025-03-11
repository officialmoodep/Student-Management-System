from tkinter import *
from tkinter import messagebox
import sqlite3
import os

# مسیر ذخیره دیتابیس در دسکتاپ
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
db_path = os.path.join(desktop_path, "project.db")

# ایجاد دیتابیس و جدول جدید در دسکتاپ
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fname TEXT NOT NULL,
    lname TEXT NOT NULL,
    course TEXT,
    password TEXT NOT NULL
)
""")
conn.commit()

# شمارنده برای شماره‌گذاری کاربران
counter = 1

# تابع بازنشانی شمارنده
def reset_counter():
    global counter
    cursor.execute("SELECT * FROM students")
    data = cursor.fetchall()
    if not data:  # اگر دیتابیس خالی است
        counter = 1  # شمارنده را از 1 شروع می‌کنیم
    else:
        counter = 1  # اگر داده‌ها موجود باشند، شمارنده را از 1 شروع می‌کنیم

# تابع اضافه کردن اطلاعات
def add_entry():
    global counter
    if fname_var.get() and lname_var.get() and password_var.get():
        cursor.execute("INSERT INTO students (fname, lname, course, password) VALUES (?, ?, ?, ?)",
                       (fname_var.get(), lname_var.get(), course_var.get(), password_var.get()))
        conn.commit()
        show_entries()
        clear_fields()
    else:
        messagebox.showwarning("خطا", "لطفاً نام، نام خانوادگی و رمز عبور را وارد کنید.")

# تابع نمایش اطلاعات
def show_entries():
    global counter
    listbox.delete(0, END)
    cursor.execute("SELECT * FROM students")
    data = cursor.fetchall()

    reset_counter()  # استفاده از تابع برای بازنشانی شمارنده

    for row in data:
        listbox.insert(END, f"{counter} - {row[0]} - {row[1]} {row[2]} - {row[3]}")
        counter += 1  # شمارنده برای هر رکورد افزایش می‌یابد

# تابع حذف اطلاعات انتخاب‌شده
def delete_entry():
    global counter
    try:
        selected = listbox.get(ACTIVE)
        if selected:
            # جدا کردن ID از رکورد انتخاب‌شده
            student_id = selected.split(" - ")[1]
            cursor.execute("DELETE FROM students WHERE id=?", (student_id,))
            conn.commit()

            reset_counter()  # بازنشانی شمارنده بعد از حذف رکورد

            show_entries()
        else:
            messagebox.showwarning("خطا", "لطفاً یک مورد را انتخاب کنید.")
    except Exception as e:
        messagebox.showerror("خطا", f"مشکلی پیش آمد: {str(e)}")

# تابع خالی کردن ورودی‌ها
def clear_fields():
    fname_var.set("")
    lname_var.set("")
    course_var.set("")
    password_var.set("")

# تابع ورود به سامانه
def login():
    cursor.execute("SELECT * FROM students WHERE password=?", (login_var.get(),))
    user = cursor.fetchone()
    if user:
        messagebox.showinfo("ورود موفق", f"خوش آمدید {user[1]} {user[2]}!")
    else:
        messagebox.showerror("خطا", "رمز ورود اشتباه است.")

# تابع خروج از برنامه
def exit_program():
    root.destroy()

# طراحی رابط کاربری
root = Tk()
root.title("مدیریت ثبت‌نام آموزشگاه")
root.geometry("600x500")

# فیلدهای ورود اطلاعات
Label(root, text="نام:").grid(row=0, column=0, padx=5, pady=5, sticky=W)
Label(root, text="نام خانوادگی:").grid(row=1, column=0, padx=5, pady=5, sticky=W)
Label(root, text="نام دوره:").grid(row=0, column=2, padx=5, pady=5, sticky=W)
Label(root, text="رمز ورود:").grid(row=1, column=2, padx=5, pady=5, sticky=W)

fname_var = StringVar()
lname_var = StringVar()
course_var = StringVar()
password_var = StringVar()
login_var = StringVar()

Entry(root, textvariable=fname_var).grid(row=0, column=1, padx=5, pady=5)
Entry(root, textvariable=lname_var).grid(row=1, column=1, padx=5, pady=5)
Entry(root, textvariable=course_var).grid(row=0, column=3, padx=5, pady=5)
Entry(root, textvariable=password_var, show="*").grid(row=1, column=3, padx=5, pady=5)

# لیست‌باکس برای نمایش کاربران
listbox = Listbox(root, width=70)
listbox.grid(row=2, column=0, columnspan=4, padx=5, pady=5)

# دکمه‌ها
Button(root, text="مشاهده همه", width=20, command=show_entries).grid(row=3, column=3, padx=5, pady=5, sticky=E)
Button(root, text="اضافه کردن", width=20, command=add_entry).grid(row=4, column=3, padx=5, pady=5, sticky=E)
Button(root, text="خالی کردن ورودی‌ها", width=20, command=clear_fields).grid(row=5, column=3, padx=5, pady=5, sticky=E)
Button(root, text="حذف کردن", width=20, command=delete_entry).grid(row=6, column=3, padx=5, pady=5, sticky=E)
Button(root, text="خروج", width=20, command=exit_program).grid(row=7, column=3, padx=5, pady=5, sticky=E)

# ورود به سامانه
Label(root, text="رمز ورود به سامانه:").grid(row=8, column=0, padx=5, pady=5, sticky=W)
Entry(root, textvariable=login_var, show="*").grid(row=8, column=1, padx=5, pady=5)
Button(root, text="ورود به سامانه", command=login).grid(row=8, column=2, padx=5, pady=5)

root.mainloop()