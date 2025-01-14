import tkinter as tk
from tkinter import filedialog, messagebox, Menu, ttk, Label

# Fonctionnalités principales
def open_file():
    file_path = filedialog.askopenfilename(
        filetypes=[("Fichiers texte", "*.txt"), ("Tous les fichiers", "*.*")]
    )
    if file_path:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
        text_input.delete("1.0", tk.END)
        text_input.insert(tk.END, content)

def save_text():
    text = text_input.get("1.0", tk.END).strip()
    if not text:
        messagebox.showwarning("Attention", "Veuillez entrer du texte avant d'enregistrer.")
        return
    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Fichiers texte", "*.txt"), ("Tous les fichiers", "*.*")]
    )
    if file_path:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(text)
        messagebox.showinfo("Succès", "Texte enregistré avec succès !")

def quit_app():
    if messagebox.askyesno("Quitter", "Voulez-vous vraiment quitter ?"):
        app.destroy()


def toggle_theme():
    global dark_mode
    dark_mode = not dark_mode
    apply_theme()

def apply_theme():
    colors = {
        "bg": "#1C1C1C" if dark_mode else "#FFFFFF",
        "fg": "#FFD700" if dark_mode else "#000000",
        "text_bg": "#333333" if dark_mode else "#F5F5F5",
        "text_fg": "#FFD700" if dark_mode else "#000000",
    }
    # Appliquer les couleurs à la fenêtre principale et aux widgets compatibles
    app.configure(bg=colors["bg"])
    text_input.configure(bg=colors["text_bg"], fg=colors["text_fg"])
    stats_label.configure(bg=colors["bg"], fg=colors["fg"])
    encoding_label.configure(bg=colors["bg"], fg=colors["fg"])  # Ajout pour le label d'encodage

def clear_text():
    text_input.delete("1.0", tk.END)

def copy_to_clipboard():
    text = text_input.get("1.0", tk.END).strip()
    if text:
        app.clipboard_clear()
        app.clipboard_append(text)
        messagebox.showinfo("Succès", "Texte copié dans le presse-papiers !")
    else:
        messagebox.showwarning("Attention", "Aucun texte à copier.")


def update_stats(event=None):
    text = text_input.get("1.0", tk.END).strip()
    word_count = len(text.split())
    char_count = len(text)
    reading_time = round(word_count / 200, 2)  # Estimation de 200 mots par minute
    stats_label.config(
        text=f"Mots : {word_count} | Caractères : {char_count} | Temps de lecture : {reading_time} min"
    )


def highlight_syntax(event=None):
    text = text_input.get("1.0", tk.END)
    for tag in text_input.tag_names():
        text_input.tag_delete(tag)

    syntax_colors = {
        "&#": "green",
        "//": "orange",
        "!": "blue",
        "$": "red",
    }

    for symbol, color in syntax_colors.items():
        start_idx = "1.0"
        while True:
            start_idx = text_input.search(symbol, start_idx, tk.END, nocase=True)
            if not start_idx:
                break
            line_start = f"{start_idx.split('.')[0]}.0"
            line_end = f"{start_idx.split('.')[0]}.end"
            text_input.tag_add(symbol, line_start, line_end)
            text_input.tag_config(symbol, foreground=color)
            start_idx = line_end

# Fonctionnalité pour afficher les infos d'aide sur la syntaxe
def show_help():
    syntax_info = """
    Informations sur la syntaxe mise en évidence :
    - "&#" : Couleur verte
    - "//" : Couleur orange
    - "!" : Couleur bleue
    - "$" : Couleur rouge

    Ces symboles peuvent être utilisés pour organiser et identifier
    différents types d'informations dans le texte.
    """
    messagebox.showinfo("Aide - Syntaxe", syntax_info)

# Fonctionnalité pour afficher les infos sur l'éditeur
def show_about():
    about_info = """
    Éditeur de texte "Text-Or" version 1.4
    Développé par Prince MOUNANGA en Python avec Tkinter.
    """
    messagebox.showinfo("À propos", about_info)

def show_context_menu(event):
    context_menu.tk_popup(event.x_root, event.y_root)


def toggle_fullscreen():
    app.attributes("-fullscreen", not app.attributes("-fullscreen"))


def exit_fullscreen():
    app.attributes("-fullscreen", False)

def update_scrollbar():
    """
    Affiche ou masque la barre de défilement en fonction du contenu de la zone de texte.
    """
    text_height = text_input.count("1.0", tk.END, "pixels")[1]
    visible_height = text_frame.winfo_height()

    if text_height > visible_height:
        scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)  # Affiche la barre de défilement
    else:
        scroll_bar.pack_forget()  # Masque la barre de défilement

def on_text_change(event=None):
    """
    Met à jour les statistiques, applique la mise en évidence syntaxique,
    et ajuste la visibilité de la barre de défilement.
    """
    update_stats()
    highlight_syntax()
    update_scrollbar()

# Création de la fenêtre principale
app = tk.Tk()
app.title("Text-Or")
app.geometry("800x600")
app.iconbitmap("app.ico")  # Remplacer par le chemin vers ton fichier .ico
app.resizable(True, True)

# Variables et état
dark_mode = True

# Zone de texte avec barre de défilement
text_frame = tk.Frame(app)
text_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

scroll_bar = ttk.Scrollbar(text_frame)
text_input = tk.Text(
    text_frame,
    wrap=tk.WORD,
    undo=True,
    font=("Courier", 12),
    yscrollcommand=scroll_bar.set,
)
scroll_bar.config(command=text_input.yview)
scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)
text_input.pack(expand=True, fill=tk.BOTH)
text_input.bind("<KeyRelease>", lambda e: (update_stats(), highlight_syntax()))
text_input.bind("<Button-3>", show_context_menu)

# Frame pour l'encodage et les statistiques
info_frame = tk.Frame(app)
info_frame.pack(fill=tk.X, padx=10, pady=5)

# Label pour le type d'encodage, aligné à gauche
encoding_label = tk.Label(info_frame, text="UTF-8", anchor="w", font=("Helvetica", 10))
encoding_label.pack(side="left")  # Un peu d'espace à droite

# Label pour les statistiques, aligné à droite
stats_label = tk.Label(info_frame, text="", anchor="e", font=("Helvetica", 10))
stats_label.pack(side="right", expand=True, fill=tk.X)

# Menu principal
menu_bar = Menu(app)
app.config(menu=menu_bar)

# Menu "Fichier"
file_menu = Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Ouvrir", command=open_file)
file_menu.add_command(label="Enregistrer", command=save_text)
file_menu.add_separator()
file_menu.add_command(label="Quitter", command=quit_app)
menu_bar.add_cascade(label="Fichier", menu=file_menu)

# Menu "Affichage"
view_menu = Menu(menu_bar, tearoff=0)
view_menu.add_command(label="Plein écran", command=toggle_fullscreen)
view_menu.add_command(label="Réduire l'écran", command=exit_fullscreen)
view_menu.add_command(label="Mode clair/sombre", command=toggle_theme)
menu_bar.add_cascade(label="Affichage", menu=view_menu)

# Menu "Édition"
edit_menu = Menu(menu_bar, tearoff=0)
edit_menu.add_command(label="Effacer", command=clear_text)
edit_menu.add_command(label="Copier", command=copy_to_clipboard)
menu_bar.add_cascade(label="Édition", menu=edit_menu)

# Menu "Aide" avec sous-menus pour Aide et À propos
help_menu = Menu(menu_bar, tearoff=0)
help_menu.add_command(label="Ecriture syntaxique", command=show_help)
help_menu.add_command(label="À propos", command=show_about)
menu_bar.add_cascade(label="Aide", menu=help_menu)

# Menu contextuel
context_menu = Menu(app, tearoff=0)
context_menu.add_command(label="Couper", command=lambda: app.event_generate("<<Cut>>"))
context_menu.add_command(label="Copier", command=lambda: app.event_generate("<<Copy>>"))
context_menu.add_command(label="Coller", command=lambda: app.event_generate("<<Paste>>"))

# Appliquer le thème initial
apply_theme()

# Lancement de l'application
app.mainloop()
