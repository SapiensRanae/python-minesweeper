import tkinter as tk
from tkinter import *
from random import shuffle
from tkinter.messagebox import *
from datetime import datetime

s_played = 0
temp = ''


class my_buttone(tk.Button):
    def __init__(self, master, x, y, number, *arg, **kwargs):
        super(my_buttone, self).__init__(master, width=3, font='calibri 15 bold', *arg, **kwargs)
        self.x = x
        self.y = y
        self.number = number
        self.is_mine = False
        self.count_bomb = 0
        self.is_open = False
        self.MM = False

    def __repr__(self):  # вивід в консоль
        return f'{self.x} {self.y} {self.number} {self.is_mine}'

    def set_color(self, color, relief='groove'):  # налштування кнопки
        self.config(text=self.count_bomb, disabledforeground=color, fg=color, relief=relief)


class minesweeper_class():
    window = tk.Tk()
    window.title('Сапер')
    
    window.iconphoto(False, tk.PhotoImage(file='icon.png'))

    rows = 10
    colums = 10
    time = False
    mines = 10

    # автоматично запускається при визові
    def __init__(self):
        # self.rows = 9
        # self.colums = 8
        # self.mines = 7
        self.GAME_OVER = False
        self.Firs_click = True
        self.buttons = []  # присвоєння buttons до кожного нового екземляру


        self.m_count = self.mines
        self.timer =Label(self.window, text=f'0 c', font='Times 30')
        self.timer.grid(column=0, row=self.rows + 1, columnspan=4,stick='w')





        for i in range(self.rows + 2):
            RAM = []
            for r in range(self.colums + 2):
                btn = my_buttone(self.window, x=i, y=r, number=0)
                btn.config(command=lambda a=btn: self.click(a))
                btn.bind('<Button-3>', self.r_click)
                RAM.append(btn)

            self.buttons.append(RAM)

    def tick(self):

        global s_played, temp
        temp = self.window.after(1000, self.tick)

        self.timer.configure(text = f'{s_played} c')
        s_played += 1



    # відмальовує весь інтерфейс
    def create_widgets(self):

        # створення меню
        m_menu = tk.Menu(self.window)
        self.window.config(menu=m_menu)

        setins_menu = tk.Menu(m_menu, tearoff=0)
        setins_menu.add_command(label='Почати гру', command=self.restart)
        setins_menu.add_command(label='Налаштування', command=self.settings)
        setins_menu.add_command(label='Вийти', command=self.window.destroy)
        m_menu.add_cascade(label='Меню', menu=setins_menu)

        # відмальовка кнопок та присвоєня індивідуального номера
        count = 1
        for i in range(1, self.rows + 1):
            for r in range(1, self.colums + 1):
                btn = self.buttons[i][r]
                btn.number = count
                count += 1
                btn.grid(column=i, row=r, stick='NWES')
        for i in range(1, self.rows + 1):
            tk.Grid.rowconfigure(self.window, i, weight=1)
        for r in range(1, self.colums + 1):
            tk.Grid.columnconfigure(self.window, r, weight=1)

        tk.Label(self.window, text=f'{self.m_count} мін', font='Times 30').grid(column=4, row=self.rows + 1,
                                                                                columnspan=3,
                                                                                stick='wnse'
                                                                                )
        self.end_btn = tk.Button(self.window, text='Завершити гру', font='calibri 15 bold', disabledforeground='Gray', fg='RED', command = lambda :self.end_game(), state='disabled')
        self.end_btn.grid(column=7, row=self.rows + 1, stick='NWES', columnspan=3)
    # перезапуск
    def restart(self):

        global s_played
        s_played = 0
        self.timer.configure(text = '0 c')

        [child.destroy() for child in self.window.winfo_children()]  # видалення всього
        self.__init__()

        self.create_widgets()

    # Окреме вікно з налаштуваннями
    def settings(self):
        win_settings = tk.Toplevel(self.window)
        win_settings.wm_title('Налаштування')

        # текст біля полів вводу
        tk.Label(win_settings, text='Кількість рядків').grid(row=0, column=0)
        tk.Label(win_settings, text='Кількість стовпців').grid(row=1, column=0)
        tk.Label(win_settings, text='Кількість мін').grid(row=2, column=0)

        # поля вводу
        r_entry = tk.Entry(win_settings)
        r_entry.grid(row=0, column=1, padx=20, pady=20)
        r_entry.insert(0, self.rows)

        c_entry = tk.Entry(win_settings)
        c_entry.grid(row=1, column=1, padx=20, pady=20)
        c_entry.insert(0, self.rows)

        m_entry = tk.Entry(win_settings)
        m_entry.grid(row=2, column=1, padx=20, pady=20)
        m_entry.insert(0, self.mines)

        tk.Button(win_settings, text='Прийняти', command=lambda: self.change_settings(r_entry, c_entry, m_entry)).grid(
            row=4,
            column=1,
            padx=20,
            pady=20)

    # прийняти зміни
    def change_settings(self, r_entry, c_entry, m_entry):
        try:

            if int(r_entry.get()) > 40:
                showerror('ПОМИЛКА', 'Існує обмеження до 40 клітинок ')
                return
            if int(c_entry.get()) > 40:
                showerror('ПОМИЛКА', 'Існує обмеження до 40 клітинок ')
                return
            if  (int(m_entry.get())/(int(r_entry.get())*int(c_entry.get())))*100 > 60:
                showerror('ПОМИЛКА', 'Існує обмеження до 60% мін від усьго ігрового поля ')
                return 

            if int(r_entry.get()) < 0:
                self.rows = int(r_entry.get())*-1
            else:
                self.rows = int(r_entry.get())

            if int(c_entry.get()) < 0:
                self.colums = int(c_entry.get())*-1
            else:
                self.colums = int(c_entry.get())
                
            if int(m_entry.get()) < 0:
                self.mines = int(m_entry.get())*-1
            else:
                self.mines = int(m_entry.get())
            self.restart()
        except ValueError:
            showerror('ПОМИЛКА', 'Ви ввели неправильне значення ')
            return

    # обробка кліку
    def click(self, btn: my_buttone):

        if self.GAME_OVER:
            return

        if self.Firs_click:
            self.set_mines(btn.number)
            self.count_m()
            #self.print_buttuns()
            if self.time == False:
                self.time = True
                self.tick()

            # print(self.create_mines())
            self.Firs_click = False
        if btn.is_mine:
            btn.config(text='*', disabledforeground='red', fg='red')
            btn.is_open = True
            self.GAME_OVER = True
            self.window.after_cancel(temp)
            self.time = False
            showinfo('GAME OVER', 'Пощастить пізніше')
            for i in range(self.rows + 2):
                for r in range(self.colums + 2):
                    btn = self.buttons[i][r]
                    if btn.is_mine:
                        if btn.MM:
                            btn.config(text='*', disabledforeground='blue')
                        else:
                            btn.config(text='*', disabledforeground='black')

        # присвоєння кольору
        else:
            match btn.count_bomb:
                case 0:
                    btn.config(bg='#e0e0e0', relief='flat')
                    self.nulls_search(btn)
                case 1:
                    btn.set_color('blue')
                case 2:
                    btn.set_color('Green')
                case 3:
                    btn.set_color('Red')
                case 4:
                    btn.set_color('Purple')
                case 5:
                    btn.set_color('Maroon')
                case 6:
                    btn.set_color('Turquoise')
                case 7:
                    btn.set_color('Black')
                case 8:
                    btn.set_color('Gray')
            btn.is_open = True
        btn.config(state='disabled')

    def r_click(self, event):

        if self.GAME_OVER:
            return
        if self.Firs_click:
            showinfo('', f'Ви ще не зробили жодного кліку, Ви не можете знати де знаходяться міни')
            return

        btn = event.widget
        if btn['state'] == 'normal':
            if self.m_count > 0:
                btn.set_color('RED')
                btn.config(text='🚩', state='disabled', relief='raised')
                self.m_count -= 1
                btn.MM = True
                tk.Label(self.window, text=f'{self.m_count} мін', font='Times 30').grid(column=4, row=self.rows + 1,
                                                                                        columnspan=3,
                                                                                        stick='wnes'
                                                                                        )

        elif btn['state'] == 'disabled':
            if btn.MM == True:
                btn.MM = False
                btn.config(text='', state='normal', relief='raised')
                self.m_count += 1
                tk.Label(self.window, text=f'{self.m_count} мін', font='Times 30').grid(column=4, row=self.rows + 1,
                                                                                        columnspan=3,
                                                                                        stick='wnse'
                                                                                        )
        if self.m_count:

            self.end_btn.config(state='disabled')

        else:
            self.end_btn.config(state='normal')

    def end_game(self):


        # print('hi')
        a = 0
        for i in range(1, self.rows + 1):
            for r in range(1, self.colums + 1):
                btn = self.buttons[i][r]
                if not btn.is_mine:
                    continue
                else:
                    if btn.MM:
                        a+=1
                        if a == self.mines:
                            self.end_btn.config(state='disabled')
                            self.window.after_cancel(temp)
                            self.time = False
                            showinfo('ВИ ВИГРАЛИ', f'Ви виграли за {s_played} секунд')
                    else:
                        btn.config(text='*', disabledforeground='red', fg='red')
                        btn.is_open = True
                        self.GAME_OVER = True

                        for i in range(1, self.rows + 1):
                            for r in range(1, self.colums + 1):
                                btn = self.buttons[i][r]
                                if btn.is_mine:
                                    if btn.MM:
                                        btn.config(text='*', disabledforeground='blue')
                                    else:
                                        btn.config(text='*', disabledforeground='black')

        if self.GAME_OVER:
            self.window.after_cancel(temp)
            self.time = False
            self.end_btn.config(state='disabled')
            showinfo('GAME OVER', 'Пощастить пізніше')


    # відкриття всіз нулів
    def nulls_search(self, btn: my_buttone):

        line = [btn]
        while line:
            cur_btn = line.pop()
            if cur_btn.count_bomb:
                match cur_btn.count_bomb:


                    case 1:
                        cur_btn.set_color('blue')
                    case 2:
                        cur_btn.set_color('Green')
                    case 3:
                        cur_btn.set_color('Red')
                    case 4:
                        cur_btn.set_color('Purple')
                    case 5:
                        cur_btn.set_color('Maroon')
                    case 6:
                        cur_btn.set_color('Turquoise')
                    case 7:
                        cur_btn.set_color('Black')
                    case 8:
                        cur_btn.set_color('Gray')
            else:
                cur_btn.config(text='', bg='#e0e0e0', relief='flat')
            if cur_btn.MM:
                self.m_count+= 1
            cur_btn.is_open = True
            cur_btn.config(state='disabled')

            if cur_btn.count_bomb == 0:

                x, y = cur_btn.x, cur_btn.y
                for xi in [-1, 0, 1]:
                    for yi in [-1, 0, 1]:
                        next_btn = self.buttons[x + xi][y + yi]
                        if not next_btn.is_open and 1 <= next_btn.x <= self.rows and 1 <= next_btn.y <= self.colums and next_btn not in line:
                            line.append(next_btn)
        tk.Label(self.window, text=f'{self.m_count} мін', font='Times 30').grid(column=4, row=self.rows + 1,
                                                                                columnspan=3,
                                                                                stick='wnse'
                                                                                )
    # пошук мін навколо одднієї кнопки
    def count_m(self):
        for i in range(1, self.rows + 1):
            for r in range(1, self.colums + 1):
                btn = self.buttons[i][r]
                count_bombs = 0
                if not btn.is_mine:
                    for row in [-1, 0, 1]:
                        for col in [-1, 0, 1]:
                            btn_n = self.buttons[i + row][r + col]
                            if btn_n.is_mine:
                                count_bombs += 1
                btn.count_bomb = count_bombs

    def start(self):
        # self.open()
        self.create_widgets()
        # спрощення коду

        self.window.mainloop()

    def print_buttuns(self):
        print('--------------')
        for r in range(1, self.colums + 1):
            for i in range(1, self.rows + 1):
                btn = self.buttons[i][r]
                if btn.is_mine:
                    print('M', end='')
                else:
                    print(btn.count_bomb, end='')

            print()

    # створення мін
    def create_mines(self, ntu):
        a = list(range(1, self.colums * self.rows + 1))
        a.remove(ntu)
        shuffle(a)
        return a[:self.mines]

    # присвоєння мін
    def set_mines(self, number):
        i_mines = self.create_mines(number)

        for i in range(1, self.rows + 1):
            for r in range(1, self.colums + 1):
                btn = self.buttons[i][r]

                if btn.number in i_mines:
                    btn.is_mine = True

    # відкриття всіх кнопок (для розробника)
    def open(self):
        for i in range(self.rows + 2):
            for r in range(self.colums + 2):
                btn = self.buttons[i][r]

                # присвоєння кольору
                if btn.is_mine:
                    btn.config(text='*', background='red', disabledforeground='black')
                else:
                    match btn.count_bomb:
                        case 0:
                            btn.config(bg='#e0e0e0', relief='flat')

                        case 1:
                            btn.set_color('blue')
                        case 2:
                            btn.set_color('Green')
                        case 3:
                            btn.set_color('Red')
                        case 4:
                            btn.set_color('Purple')
                        case 5:
                            btn.set_color('Maroon')
                        case 6:
                            btn.set_color('Turquoise')
                        case 7:
                            btn.set_color('Black')
                        case 8:
                            btn.set_color('Gray')

                btn.config(state='disabled')


# game = minesweeper() # екземляр класу


minesweeper = minesweeper_class()
minesweeper.start()
