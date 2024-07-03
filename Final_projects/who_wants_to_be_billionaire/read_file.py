import tkinter as tk
from tkinter import ttk

def read_players_from_file(filename):
    players = []
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if line:  # Пропускаем пустые строки
                    player_data = line.split(',')  # Предполагаем формат "Имя игрока,Выигрыш"
                    if len(player_data) == 2:
                        players.append((player_data[0], player_data[1]))
                    else:
                        print(f"Неверный формат строки: {line}")
    except FileNotFoundError:
        print(f"Файл {filename} не найден")
    return players

def add_player():
    new_player_name = entry_name.get()
    new_player_score = entry_score.get()

    if new_player_name and new_player_score:
        # Добавляем нового игрока в таблицу
        tree.insert("", tk.END, values=(new_player_name, new_player_score))
        # Добавляем нового игрока в файл
        with open(filename, 'a', encoding='utf-8') as file:
            file.write(f"{new_player_name},{new_player_score}\n")
    else:
        print("Введите имя игрока и выигрыш")

# Создаем файл и записываем начальные данные, если он не существует
def create_initial_file(filename):
    initial_data = [
        ("Имя игрока 1", "1000000 рублей"),
        ("Имя игрока 2", "500000 рублей"),
        ("Имя игрока 3", "250000 рублей"),
        ("Имя игрока 4", "125000 рублей"),
        ("Имя игрока 5", "64000 рублей"),
    ]

    with open(filename, 'w', encoding='utf-8') as file:
        for player in initial_data:
            file.write(f"{player[0]},{player[1]}\n")

root = tk.Tk()
root.title("Таблица топ игроков - Кто хочет стать миллионером?")

# Проверяем, существует ли файл, и создаем его, если нет
filename = "top_players.txt"
create_initial_file(filename)

# Создание виджета Treeview (таблицы)
tree = ttk.Treeview(root, columns=("Имя игрока", "Выигрыш"), show="headings")
tree.heading("Имя игрока", text="Имя игрока")
tree.heading("Выигрыш", text="Выигрыш")

# Чтение данных из текстового файла
top_players = read_players_from_file(filename)

# Обновление таблицы с данными из файла
for player in top_players:
    tree.insert("", tk.END, values=player)

# Упаковка виджета Treeview
tree.pack(expand=True, fill="both")

# Виджеты для добавления нового игрока
frame_add_player = tk.Frame(root)
frame_add_player.pack(pady=10)

label_name = tk.Label(frame_add_player, text="Имя игрока:")
label_name.grid(row=0, column=0, padx=5, pady=5)
entry_name = tk.Entry(frame_add_player)
entry_name.grid(row=0, column=1, padx=5, pady=5)

label_score = tk.Label(frame_add_player, text="Выигрыш:")
label_score.grid(row=1, column=0, padx=5, pady=5)
entry_score = tk.Entry(frame_add_player)
entry_score.grid(row=1, column=1, padx=5, pady=5)

button_add = tk.Button(frame_add_player, text="Добавить игрока", command=add_player)
button_add.grid(row=2, columnspan=2, padx=5, pady=10)

root.mainloop()
