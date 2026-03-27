import tkinter as tk 

# Класс круга
class CCircle:
    
    
    RADIUS = 30  # постоянный радиус
    
    # Конструктор сохранения координат круга
    def __init__(self, x, y):
        
        self.x = x                      
        self.y = y                     
        self.is_selected = False        # выделен ли круг (False - нет, True - да)
        
    def draw(self, canvas, canvas_id=None):
        
        # Вычисляем координаты прямоугольника, в который вписан круг
        x1 = self.x - self.RADIUS        
        y1 = self.y - self.RADIUS       
        x2 = self.x + self.RADIUS        
        y2 = self.y + self.RADIUS        

        # Выбираем цвета в зависимости от выделения
        if self.is_selected:
            fill_color = "#ffcccc"       
            outline_color = "red"        
            width = 3                    
        else:
            fill_color = "#6495ed"      
            outline_color = "black"      
            width = 1                    
        
        # Если круг уже существует - обновляем, иначе создаём новый
        if canvas_id:
            canvas.coords(canvas_id, x1, y1, x2, y2)
            canvas.itemconfig(canvas_id, fill=fill_color, outline=outline_color, width=width)
            return canvas_id
        else:
            return canvas.create_oval(x1, y1, x2, y2, fill=fill_color, outline=outline_color, width=width)
    
    def contains_point(self, x, y):
        #Проверяет, попала ли точка (x, y) в круг
        dx = x - self.x
        dy = y - self.y
        return dx*dx + dy*dy <= self.RADIUS * self.RADIUS
    
    def set_selected(self, selected):
        self.is_selected = selected


# Класс контейнер
class CircleContainer:
    
    def __init__(self):
        self._circles = []          # список для хранения кругов (приватный)
    
    def add(self, circle):
        # Добавляет круг в контейнер
        self._circles.append(circle)
    
    def remove(self, circle):
        # Удаляет круг из контейнера
        if circle in self._circles:
            self._circles.remove(circle)
    
    def get_all(self):
        # Возвращает список всех кругов
        return self._circles.copy()
    
    def get_count(self):
        # Возвращает количество кругов
        return len(self._circles)
    
    def clear(self):
        # Очищает контейнер
        self._circles.clear()


# Класс Circles
class CirclesApp:
    
    def __init__(self):

        # Создаём главное окно
        self.root = tk.Tk()
        self.root.title("Круги на форме - Лабораторная работа 3 часть №1")
        self.root.geometry("700x550")
        self.root.minsize(500, 400)
        
        # Создаём контейнер для хранения кругов
        self.container = CircleContainer()
        
        # Словарь для связи объекта круга с его ID на canvas
        self.circle_ids = {}
        
        # Флаг нажатой клавиши Ctrl
        self.ctrl_pressed = False
        
        # Создаём элементы интерфейса
        self.setup_ui()
        
        # Привязываем обработчики событий
        self.bind_events()
        
    def setup_ui(self):
        
        # Верхняя панель с подсказками команд
        info_frame = tk.Frame(self.root, bg="#f0f0f0")
        info_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.info_label = tk.Label(
            info_frame,
            text="Двойной клик - создать круг | Клик - выделить | Ctrl+Клик - добавить к выделению | Delete - удалить выделенные",
            bg="#f0f0f0",
            font=("Arial", 9)
        )
        self.info_label.pack(side=tk.LEFT, padx=5)
        
        # Панель с кнопками
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.clear_btn = tk.Button(btn_frame, text="Снять выделение", command=self.clear_selection)
        self.clear_btn.pack(side=tk.LEFT, padx=5)
        
        self.clear_all_btn = tk.Button(btn_frame, text="Очистить всё", command=self.clear_all)
        self.clear_all_btn.pack(side=tk.LEFT, padx=5)
        
        # Статусная строка внизу
        self.status_label = tk.Label(
            self.root,
            text="Кругов: 0 | Выделено: 0",
            bg="#e0e0e0",
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        self.status_label.pack(fill=tk.X, side=tk.BOTTOM)
        
        # Область для рисования 
        self.canvas = tk.Canvas(self.root, bg="white", relief=tk.SUNKEN, borderwidth=1)
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
    def bind_events(self):
        
        # События мыши на canvas
        self.canvas.bind("<Button-1>", self.on_mouse_click)           
        self.canvas.bind("<Double-Button-1>", self.on_double_click)   
        
        # События клавиатуры
        self.root.bind("<KeyPress-Control_L>", self.on_ctrl_press)    
        self.root.bind("<KeyPress-Control_R>", self.on_ctrl_press)
        self.root.bind("<KeyRelease-Control_L>", self.on_ctrl_release)
        self.root.bind("<KeyRelease-Control_R>", self.on_ctrl_release)
        self.root.bind("<Delete>", self.on_delete)                    
        
        # Событие изменения размера окна
        self.canvas.bind("<Configure>", self.on_resize)
        
        # Устанавливаем фокус на canvas для обработки клавиш
        self.canvas.focus_set()
    
    def on_mouse_click(self, event):
        
        x, y = event.x, event.y
        
        # Находим все круги, в которые попал клик
        hit_circles = []
        for circle in self.container.get_all():
            if circle.contains_point(x, y):
                hit_circles.append(circle)
        
        # Если кликнули на круг(и)
        if hit_circles:
            if self.ctrl_pressed:
                # Ctrl нажат: инвертируем выделение (добавляем/убираем)
                circle = hit_circles[0]
                circle.set_selected(not circle.is_selected)
            else:
                # Ctrl не нажат: выделяем только первый круг, остальные снимаем
                for circle in self.container.get_all():
                    if circle in hit_circles:
                        circle.set_selected(circle == hit_circles[0])
                    else:
                        circle.set_selected(False)
        else:
            # Кликнули на пустое место - снимаем выделение со всех
            for circle in self.container.get_all():
                circle.set_selected(False)
        
        # Перерисовываем и обновляем статус
        self.update_canvas()
        self.update_status()
    
    def on_double_click(self, event):
    
        x, y = event.x, event.y
        
        # Создаём новый круг
        circle = CCircle(x, y)
        
        # Добавляем в контейнер
        self.container.add(circle)
        
        # Рисуем на canvas и запоминаем ID
        circle_id = circle.draw(self.canvas)
        self.circle_ids[circle] = circle_id
        
        # Обновляем статус
        self.update_status()
    
    def on_ctrl_press(self, event):
        
        self.ctrl_pressed = True
    
    def on_ctrl_release(self, event):
        
        self.ctrl_pressed = False
    
    def on_delete(self, event):
        
        # Собираем выделенные круги
        circles_to_remove = []
        for circle in self.container.get_all():
            if circle.is_selected:
                circles_to_remove.append(circle)
        
        # Удаляем каждый выделенный круг
        for circle in circles_to_remove:
            # Удаляем с canvas
            if circle in self.circle_ids:
                self.canvas.delete(self.circle_ids[circle])
                del self.circle_ids[circle]
            # Удаляем из контейнера
            self.container.remove(circle)
        
        # Перерисовываем и обновляем статус
        self.update_canvas()
        self.update_status()
    
    def on_resize(self, event):
    
        self.update_canvas()
    
    def clear_selection(self):
       
        for circle in self.container.get_all():
            circle.set_selected(False)
        self.update_canvas()
        self.update_status()
    
    def clear_all(self):
        
        self.canvas.delete("all")
        self.container.clear()
        self.circle_ids.clear()
        self.update_status()
    
    def update_canvas(self):
        
        for circle in self.container.get_all():
            if circle in self.circle_ids:
                circle_id = self.circle_ids[circle]
                # Перерисовываем круг
                x1 = circle.x - circle.RADIUS
                y1 = circle.y - circle.RADIUS
                x2 = circle.x + circle.RADIUS
                y2 = circle.y + circle.RADIUS
                self.canvas.coords(circle_id, x1, y1, x2, y2)
                
                # Обновляем цвета в зависимости от выделения
                if circle.is_selected:
                    fill_color = "#ffcccc"
                    outline_color = "red"
                    width = 3
                else:
                    fill_color = "#6495ed"
                    outline_color = "black"
                    width = 1
                
                self.canvas.itemconfig(circle_id, fill=fill_color, outline=outline_color, width=width)
    
    # Обнвление статусной строки
    def update_status(self):
        
        count = self.container.get_count()
        selected = sum(1 for c in self.container.get_all() if c.is_selected)
        self.status_label.config(text=f"Кругов: {count} | Выделено: {selected}")
    
    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = CirclesApp()
    app.run()