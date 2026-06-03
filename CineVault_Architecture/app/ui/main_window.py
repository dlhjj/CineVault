
import tkinter as tk
from tkinter import ttk, messagebox

from app.database.database import init_database
from app.services.movie_service import MovieService

class CineVaultApp:

    def __init__(self):
        init_database()

        self.root = tk.Tk()
        self.root.title('CineVault')
        self.root.geometry('1100x700')
        self.root.configure(bg='#1e1e1e')

        self.build_ui()
        self.load_movies()

    def build_ui(self):

        header = tk.Frame(self.root, bg='#252526', height=70)
        header.pack(fill='x')

        tk.Label(
            header,
            text='🎬 CineVault',
            bg='#252526',
            fg='white',
            font=('Segoe UI', 24, 'bold')
        ).pack(side='left', padx=20, pady=15)

        content = tk.Frame(self.root, bg='#1e1e1e')
        content.pack(fill='both', expand=True, padx=15, pady=15)

        sidebar = tk.Frame(content, bg='#2d2d30', width=280)
        sidebar.pack(side='left', fill='y')

        tk.Label(
            sidebar,
            text='Добавить фильм',
            bg='#2d2d30',
            fg='white',
            font=('Segoe UI', 14, 'bold')
        ).pack(pady=15)

        self.title_entry = tk.Entry(sidebar)
        self.title_entry.pack(fill='x', padx=15, pady=5)

        self.genre_entry = tk.Entry(sidebar)
        self.genre_entry.pack(fill='x', padx=15, pady=5)

        self.rating_entry = tk.Entry(sidebar)
        self.rating_entry.pack(fill='x', padx=15, pady=5)

        self.watched_var = tk.BooleanVar()

        tk.Checkbutton(
            sidebar,
            text='Просмотрен',
            variable=self.watched_var,
            bg='#2d2d30',
            fg='white',
            selectcolor='#2d2d30'
        ).pack(pady=10)

        tk.Button(
            sidebar,
            text='Добавить',
            command=self.add_movie,
            bg='#0e639c',
            fg='white'
        ).pack(fill='x', padx=15)

        self.stats_label = tk.Label(
            sidebar,
            text='',
            bg='#2d2d30',
            fg='#8fd18f'
        )
        self.stats_label.pack(pady=20)

        right = tk.Frame(content, bg='#1e1e1e')
        right.pack(side='right', fill='both', expand=True, padx=(10,0))

        self.search_entry = tk.Entry(right)
        self.search_entry.pack(fill='x', pady=(0,10))
        self.search_entry.bind('<KeyRelease>', lambda e: self.load_movies())

        self.tree = ttk.Treeview(
            right,
            columns=('id','title','genre','rating','watched'),
            show='headings'
        )

        for col, text in [
            ('id','ID'),
            ('title','Название'),
            ('genre','Жанр'),
            ('rating','Рейтинг'),
            ('watched','Статус')
        ]:
            self.tree.heading(col, text=text)

        self.tree.pack(fill='both', expand=True)

        tk.Button(
            right,
            text='Удалить выбранный фильм',
            command=self.delete_movie
        ).pack(pady=10)

    def add_movie(self):
        try:
            MovieService.add_movie(
                self.title_entry.get(),
                self.genre_entry.get(),
                float(self.rating_entry.get()),
                self.watched_var.get()
            )
            self.load_movies()

        except Exception as error:
            messagebox.showerror('Ошибка', str(error))

    def load_movies(self):

        for item in self.tree.get_children():
            self.tree.delete(item)

        movies = MovieService.get_movies(
            self.search_entry.get()
        )

        watched_count = sum(movie[4] for movie in movies)

        self.stats_label.config(
            text=f'Фильмов: {len(movies)}\nПросмотрено: {watched_count}'
        )

        for movie in movies:

            self.tree.insert(
                '',
                'end',
                values=(
                    movie[0],
                    movie[1],
                    movie[2],
                    movie[3],
                    'Да' if movie[4] else 'Нет'
                )
            )

    def delete_movie(self):

        selected = self.tree.selection()

        if not selected:
            return

        movie_id = self.tree.item(selected[0])['values'][0]

        MovieService.delete_movie(movie_id)
        self.load_movies()

    def run(self):
        self.root.mainloop()
