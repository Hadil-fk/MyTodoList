import tkinter as tk
from tkinter import messagebox


class My_todo:
    def __init__(self, root):
        self.root = root
        self.root.title("To_Do_List")
        self.root.geometry("450x1000")
        self.root.config(bg="black")
        self.tasks = []

        # Label d'accueil
        self.l = tk.Label(root, text="Welcome to your To-Do List", font=("Arial", 20), fg="white", bg="darkblue")
        self.l.place(x=50,y=10)

        # Champ de saisie
        self.t = tk.Entry(root, width=20)
        self.t.place(x=160,y=70)

        # Boutons
        self.b = tk.Button(root, text="+", command=self.add, bg="white", fg="black")  # Ajouter tâche
        self.b.place(x=300,y=70)
        self.s = tk.Button(root, text="Supprimer tout", command=self.clear_all, bg="white", fg="black")  # Supprimer tout
        self.s.place(x=160, y=400)
        self.save = tk.Button(root, text="Save", command=self.save_tasks, bg="white", fg="black")  # Enregistrer
        self.save.place(x=280, y=400)

        # Cadre des tâches
        self.f = tk.Frame(root)
        self.f.place(x=160, y=150)

        # Charger les tâches
        self.load_tasks()
    #ajouter une tache
    def add(self):
        text = self.t.get().strip()
        if text:
            var = tk.BooleanVar()  # Suivre l'état de la case à cocher
            self.create_task_widget(text, var)
            self.tasks.append((text, var))
            self.t.delete(0, tk.END)  # Vider le champ de saisie
            self.update()  # Mise à jour immédiate du fichier
        else:
            messagebox.showwarning("Erreur", "Veuillez entrer une tâche valide.")
    #widget pour la tache
    def create_task_widget(self, text, var):
        itemframe = tk.Frame(self.f,bg="black") #creation du cadre
        itemframe.pack(anchor="w", pady=5)#alignee a gauche et 5px autour de lui
        check = tk.Checkbutton(itemframe, text=text, variable=var) #checkbutton dans le cadre 
        check.pack(side="left") #au gauche du cadre
        remove_btn = tk.Button(itemframe, text="Remove", command=lambda: self.remove(itemframe, text))
        remove_btn.pack(side="left") 
        return itemframe #retourner le cadre
#supprimer tache
    def remove(self, itemframe, text):
        self.tasks = [(t, v) for t, v in self.tasks if t != text] #liste du tuple
        itemframe.destroy() #detruit le cadre
        # Mettre à jour le fichier
        self.update()
#supprimer toutes les taches
    def clear_all(self):
        for widget in self.f.winfo_children():#retourne une liste de tous les widgets
            widget.destroy()# Supprime chaque widget
        self.tasks.clear() #supprime tout le continu du liste
        self.update()  # Mise à jour du fichier
#Réécrire le fichier avec les tâches actuelles
    def update(self):
        with open("tasks.txt", "w") as f:#ouvrir le fichier en mode ecriture
            for text, var in self.tasks:#parcours de la liste
                status = "done" if var.get() else "pending" #if True la case est cochée
                f.write(f"{text}|{status}\n") #la forme du tache
#Enregistrer les tâches
    def save_tasks(self):
        self.update()#'écrire les données au bon format
        messagebox.showinfo("Tâches enregistrées", "Les tâches ont été sauvegardées avec succès.")
        #(le titre de la boite,le msg affiché à l'utilisateur)
# Charger les taches depuis le fichier
    def load_tasks(self):
        try: #lire le fichier quelque soit l'eureurs
            with open("tasks.txt", "r") as file: # ouvrir le fichier en mode lecture
                for line in file:
                    text, status = line.strip().split("|") #supprime les espaces et separe la ligne 
                    var = tk.BooleanVar(value=(status == "done")) # if status done : True
                    self.create_task_widget(text, var) #ajouter un wisget
                    self.tasks.append((text, var)) #ajouter la tache a la liste sous forme de tuple
        except FileNotFoundError:# Si le fichier n'existe pas l'exécution continue sans erreur
            pass


# Main application
if __name__ == "__main__": #Si le script est exécuté directement le code sera execute
    root = tk.Tk() #fenetre principale
    app = My_todo(root) # instance de la classe 
    root.mainloop()
