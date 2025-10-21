import tkinter as tk
from PIL import Image, ImageTk
from tkinter import filedialog, messagebox, ttk

from backend import make_background_transparent


class ConverterApp(tk.Tk):
    """Класс создаёт окно и запускает make_background_transparent."""
    def __init__(self):
        super().__init__()

        style = ttk.Style()
        style.theme_use('clam')

        self.iconbitmap(r'D:\Dev\Transparent_background\icon\Icon_apps_T.ico')
        self.title('ConvertImagesTransparent - Сделать фон прозрачным')
        self.geometry('600x400')
        # self.attributes("-alpha", 0.9)
        self.file_path_var = tk.StringVar()

        # Создаем Notebook
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill='both')
        # Создаем фреймы для вкладок
        self.tab_main = ttk.Frame(self.notebook)
        self.tab_about = ttk.Frame(self.notebook)
        # Добавляем вкладки в Notebook
        self.notebook.add(self.tab_main, text='Главная')
        self.notebook.add(self.tab_about, text='About')
        # Создаем отдельный фрейм для всех виджетов на главной вкладке
        self.main_frame = ttk.Frame(self.tab_main)
        self.main_frame.grid(row=0, column=0, sticky='nsew')

        # Наполняем вкладку About информацией
        about_text = (
            'ConvertImagesTransparent\n\n'
            'Приложение для удаления белого фона с изображений.\n\n'
            'Автор: Telegram: @kosmonafftsb\n'
            'Email: kosmonaffter@yandex.ru\n'
            '© 2025'
        )
        label_about = ttk.Label(
            self.tab_about,
            text=about_text,
            justify='left',
            font=('Arial', 12),
            padding=10,
            anchor='nw',
        )
        label_about.pack(expand=True, fill='both')

        ttk.Label(
            self.main_frame,
            text='Выберите изображение\nна белом фоне:',
        ).grid(
            row=0,
            column=0,
            padx=5,
            pady=5,
            sticky='w',
        )

        ttk.Entry(
            self.main_frame,
            textvariable=self.file_path_var,
            width=50,
        ).grid(
            row=0,
            column=1,
            padx=5,
            pady=5,
        )

        ttk.Button(
            self.main_frame,
            text='Обзор...',
            command=self.select_file,
        ).grid(
            row=0,
            column=2,
            padx=5,
            pady=5,
        )

        ttk.Button(
            self.main_frame,
            text='Поехали!',
            command=self.make_transparent,
        ).grid(
            row=1,
            column=1,
            pady=20,
        )
        tk.Label(
            self.main_frame,
            text="@2025 kosmonaffter@yandex.ru",
            font=("Arial", 8),
            foreground="red",
        ).grid(
            row=4,
            column=0,
            columnspan=3,
            sticky="w",
            padx=5,
            pady=5,
        )

        self.image_label = ttk.Label(self.main_frame)
        self.image_label.grid(row=2, column=0, columnspan=3, pady=10)
        self.slide_images = [
            r'D:\Dev\Transparent_background\images\image_1.png',
            r'D:\Dev\Transparent_background\images\image_2.png',
        ]
        self.current_image_index = 0
        # Запускаем цикл смены изображений
        self.show_next_image()

    def select_file(self):
        path = filedialog.askopenfilename(
            filetypes=[
                ('Image files', '*.png *.jpg *.bmp *.ico'),
            ],
        )
        if path:
            self.file_path_var.set(path)

    def make_transparent(self):
        input_path = self.file_path_var.get()
        if not input_path:
            messagebox.showwarning(
                'Внимание',
                'Выберите файл!',
            )
            return

        output_path = (
            input_path.rsplit('.', 1)[0] + '_transparent.png'
        )

        try:
            make_background_transparent(
                input_path,
                output_path,
            )
        except Exception as exc:
            messagebox.showerror(
                'Ошибка',
                f'Не удалось обработать изображение:\n{exc}',
            )
        else:
            messagebox.showinfo(
                'Успех',
                f'Файл сохранён с прозрачным фоном:\n{output_path}',
            )

    def show_next_image(self):
        # Загружаем следующий рисунок из списка
        image_path = self.slide_images[self.current_image_index]
        image = Image.open(image_path)
        # при необходимости изменяем размер
        image = image.resize((500, 200), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(image)

        # Обновляем Label с картинкой
        self.image_label.configure(image=photo)
        # сохраняем ссылку чтоб картинка не пропала
        self.image_label.image = photo  # type: ignore

        # Обновляем индекс для следующего изображения
        self.current_image_index = (
            self.current_image_index + 1
        ) % len(self.slide_images)

        # Запускаем следующий вызов через 3000 мс (3 секунды)
        self.after(3000, self.show_next_image)


if __name__ == '__main__':
    app = ConverterApp()
    app.mainloop()
