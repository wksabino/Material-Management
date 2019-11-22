from tkinter import *
import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    return conn

def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def main():
    database = r"C:\sqlite\db\management.db"

    sql_create_inventory_table = """ CREATE TABLE IF NOT EXISTS P_MAT_INVENTORY (
                                        order_id integer PRIMARY KEY,
                                        project_id integer NOT NULL,
                                        mat_id integer NOT NULL,
                                        ordered_date text NOT NULL,
                                        supplier_name text,
                                        tot_units integer NOT NULL,
                                        unit_cost integer NOT NULL,
                                        received_date text,
                                        transfer_date text
                                    ); """

    sql_create_projects_table = """CREATE TABLE IF NOT EXISTS P_PROJECTS (
                                    project_id integer PRIMARY KEY,
                                    project_name text NOT NULL,
                                    FOREIGN KEY (project_id) REFERENCES P_MAT_INVENTORY (project_id)
                                );"""

    sql_create_materials_table = """CREATE TABLE IF NOT EXISTS P_MATERIALS (
                                    mat_id integer PRIMARY KEY,
                                    mat_name text NOT NULL,
                                    FOREIGN KEY (mat_id) REFERENCES P_MAT_INVENTORY (mat_id)
                                );"""

    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        # create inventory table
        create_table(conn, sql_create_inventory_table)

        # create projects table
        create_table(conn, sql_create_projects_table)

        # create materials table
        create_table(conn, sql_create_materials_table)
    else:
        print("Error! cannot create the database connection.")

def main_login_screen():
    global login_screen
    global login_frame
    global username_verify, password_verify

    login_screen = Tk()
    login_screen.geometry('350x250')
    login_screen.title('MATERIAL MANAGEMENT')

    login_frame = Frame(login_screen, width=300, height=250)
    login_frame.place(x=40, y=0)

    username_verify = StringVar()
    password_verify = StringVar()

    username_label = Label(login_frame, text='Username:').place(x=20, y=60)
    username_verify = Entry(login_frame, textvariable=username_verify)
    username_verify.place(x=100, y=60)

    password_label = Label(login_frame, text='Password:').place(x=20, y=90)
    password_verify = Entry(login_frame, textvariable=password_verify, show='*')
    password_verify.place(x=100, y=90)

    Button(login_frame, text='Login', command=login_verify).place(x=50, y=120, height=30, width=50)
    Button(login_frame, text='Exit', command=login_screen.destroy).place(x=120, y=120, height=30, width=50)

    login_screen.mainloop()

def login_verify():
    global username1

    username1 = username_verify.get()
    password1 = password_verify.get()
    username_verify.delete(0,END)
    password_verify.delete(0,END)

    if not username1 == 'admin':
        user_not_found()
    else:
        if password1 == 'admin':
            login_frame.destroy()
            login_success()
        else:
            password_not_recognised()

def login_success():
    success_frame = Frame(login_screen, width=350, height=250)
    success_frame.pack()

    Button(success_frame, text='PROJECTS', command='projects').place(x=50, y=80, height=30, width=100)
    Button(success_frame, text='SUPPLIERS', command=suppliers).place(x=190, y=80, height=30, width=100)

def password_not_recognised():
    global passwordnot_screen
    passwordnot_screen = Tk()
    passwordnot_screen.title('Login')
    passwordnot_screen.geometry('150x50')
    Label(passwordnot_screen, text='Invalid Password').pack()
    Button(passwordnot_screen, text='Ok', command=passwordnot_screen.destroy).pack()

def user_not_found():
    global usernot_screen
    usernot_screen = Tk()
    usernot_screen.title('Login')
    usernot_screen.geometry('150x50')
    Label(usernot_screen, text='User Not Found').pack()
    Button(usernot_screen, text='Ok', command=usernot_screen.destroy).pack()

def suppliers():
    global suppliers_screen

    suppliers_screen = Tk()
    suppliers_screen.geometry('1000x650')
    suppliers_screen.title('SUPPLIERS PAGE')

    shop_cost_label = Label(suppliers_screen, text='Total Shop Cost:').place(x=20, y=60)
    Button(suppliers_screen, text='Order', command='suppliers_order').place(x=80, y=90, height=30, width=100)
    Button(suppliers_screen, text='Exit', command=suppliers_exit).place(x=20, y=600, height=30, width=70)

def suppliers_exit():
    suppliers_screen.destroy()

if __name__ == '__main__':
    create_connection(r"C:\sqlite\db\management.db")
    main()
    main_login_screen()