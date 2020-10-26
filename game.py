from tkinter import *
import time # время 
import random # random

tk = Tk() # окно с игровым полем
tk.title('Game') # заголовок окна
tk.resizable(0, 0) # запрет на изменение разрешения экрана
tk.wm_attributes('-topmost', 1) # поверх всех окон

canvas = Canvas(tk, width=500, height=400, highlightthickness=0) # создаём полотно 400*500
canvas.pack() # у каждого элемента свои координаты
tk.update() # обновление окна с холстом


class Ball: # шарик
    # конструктор
    def __init__(self, canvas, paddle, score, color): # все параметры для мяча
        self.canvas = canvas
        self.paddle = paddle
        self.score = score

        self.id = canvas.create_oval(10,10, 25, 25, fill=color) # круг с радиусом 15 пикселей
        self.canvas.move(self.id, 245, 100) # помещаем круг на полотно с координатами 245 * 100
        
        starts = [-2, -1, 1, 2] # список возможных направлений для старта
        random.shuffle(starts) # shuffle = перемешиваем список

        self.x = starts[0] # выбираем вектор движения для шарика
        self.y = -2 # в начале всегда падает вниз, поэтому - 2

        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width() # шарик узнаёт свою высоту и ширину

        self.hit_bottom = False # св-во, которое отвечает за касание шарика дна (ну или проигрыша)

    
    # касание о платформу
    # pos[x1, y1, x2, y2] - левая верхняя (x1, y1) и правая нижняя точки (x2, y2)
    def hit_paddle(self, pos):
        paddle_pos = self.canvas.coords(self.paddle.id) # получаем координаты платформы

        if pos[2] >= paddle_pos[0] and pos[0] <= paddle_pos[2]: # если координаты касания совпадают с координатой платформы
            if pos[3] >= paddle_pos[1] and pos[3] <= paddle_pos[3]:
                self.score.hit() # увеличиваем счёт
                return True # успешное касание
        return False # касания не было


    # отрисовка шарика
    def draw(self):
        self.canvas.move(self.id, self.x, self.y) # передвигаем шарик на x и y
        pos = self.canvas.coords(self.id) # новые координаты шарика

        if pos[1] <= 0: # если шарик падает сверху
            self.y = 2 # задаём падение на следущем шаге

        if pos[3] >= self.canvas_height: # коснулись дна правой нижней клеткой
            self.hit_bottom = True
            canvas.create_text(250, 120, text='Вы проиграли', font=('Courier', 30), fill='red') # выводим сообщение о конце игры и кол-во очков

        if self.hit_paddle(pos) == True: # если было касание платформы
            self.y = -2 # отправляем шар наверх

        if pos[0] <= 0: # касание левой стенки
            self.x = 2 # двигаем вправо
        
        if pos[2] >= self.canvas_width: # касание правой стенки
            self.x = -2 # двигаемся влево



class Paddle:
    # конструктор
    def __init__(self, canvas, color):
        self.canvas = canvas # рисуем на нашем полотне
        self.id = canvas.create_rectangle(0, 0, 100, 10, fill=color) # прямоугольник 10 * 100 пикселей

        start_1 = [40, 60, 90, 120, 150, 180, 200] # возможные стартовые значения
        random.shuffle(start_1) # перемешиваем их

        self.starting_point_x = start_1[0] # выбираем первое из перемешанных
        self.canvas.move(self.id, self.starting_point_x, 300) # стартовое положение: рандом * 300

        self.x = 0 # платформа никуда не двигается

        self.canvas_width = self.canvas.winfo_width() # платформа узнаёт свою ширину

        # задаём обработчик нажатий
        # если нажата стрелка вправо: выполняем turn_right()
        self.canvas.bind_all('<KeyPress-Right>', self.turn_right)
        # влево: выполняем trun_left()
        self.canvas.bind_all('<KeyPress-Left>', self.turn_left)

        self.started = False # пока игра не началась
        self.canvas.bind_all('<KeyPress-Return>', self.start_game) # стартуем!


    # двигаемся вправо
    def turn_right(self, event):
        self.x = 2 # смещаемся на 2 пикселя вправо

    # двигаемся влево
    def turn_left(self, event):
        self.x = -2 # двигаем на 2 пикселя влево

    # игра начинается
    def start_game(self, event):
        self.started = True # меняем переменную, которая отвечает за старт

    # метод, отвечающий за движение платформы
    def draw(self):
        self.canvas.move(self.id, self.x, 0) # сдвигаем платформу на заданное кол-во пикселей
        pos = self.canvas.coords(self.id) # обновлённые координаты платформы

        # если упёрлись в левую границу полотна
        if pos[0] <= 0:
            self.x = 0 # тупо останавливаемся

        # если упёрлись в правую границу
        if pos[2] >= self.canvas_width:
            self.x = 0 # также тупо останавливаемся



class Score: # очОчки
    # конструктор
    def __init__(self, canvas, color):
        self.score = 0 # 0 очков в начальный момент
        self.canvas = canvas # полотно, где отобразим очки

        self.id = canvas.create_text(450, 10, text=self.score, font=('Courier', 15), fill=color) # наш счёт в координате 450 * 10

    def hit(self):
        self.score += 1 # увелчиваем счёт на 1
        self.canvas.itemconfig(self.id, text=self.score) # пишем новое значение счёта




score = Score(canvas, 'green') # создаём зелёный счёт
paddle = Paddle(canvas, 'White') # создаём белую платформу
ball = Ball(canvas, paddle, score, 'red') # создаём красный шарик

# пока шарик не коснулся дна
while not ball.hit_bottom:
    # если игра началась и платформа может двигаться
    if paddle.started == True:
        ball.draw() # двигаем шарик
        paddle.draw() # двигаем платформу

    tk.update_idletasks() # обновляем всё игровое поле, чтобы всё закончило рисоваться
    tk.update() # обновляем всё игровое поле, которое уже отроботало свой алгоритм
    time.sleep(0.01) # замираем на сотую секунду для плавности XD

time.sleep(3) # даём три секунды на осознание поражения