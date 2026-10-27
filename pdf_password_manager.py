import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pypdf import PdfReader, PdfWriter
import os
import sys
import ctypes


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath('.')
    return os.path.join(base_path, relative_path)

try:
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('Theo.PDFPasswordManager.1')
except Exception:
    pass


def choisir_fichier():
    fichier = filedialog.askopenfilename(filetypes=[('PDF', '*.pdf')])
    if fichier:
        entree_pdf.delete(0, tk.END)
        entree_pdf.insert(0, fichier)


def afficher_champs(*args):
    mode = action.get()

    if mode == 'Ajouter':
        label_actuel.grid_remove()
        entree_actuel.grid_remove()
        label_nouveau.config(text='Nouveau mot de passe')

    elif mode == 'Modifier':
        label_actuel.grid(row=2, column=0, sticky='w', padx=5, pady=5)
        entree_actuel.grid(row=2, column=1, sticky='ew', padx=5, pady=5)
        label_nouveau.config(text='Nouveau mot de passe')

    elif mode == 'Supprimer':
        label_actuel.grid_remove()
        entree_actuel.grid_remove()
        label_nouveau.config(text='Mot de passe actuel')



def executer():
    try:
        pdf = entree_pdf.get().strip()
        if not os.path.exists(pdf):
            raise Exception('Fichier PDF introuvable.')

        mode = action.get()
        nouveau = entree_nouveau.get().strip()
        actuel = entree_actuel.get().strip()

        if mode in ('Ajouter', 'Modifier') and not nouveau:
            raise Exception('Le nouveau mot de passe ne peut pas être vide.')

        try:
            reader = PdfReader(pdf)
        except Exception:
            raise Exception('Le fichier sélectionné n\'est pas un PDF valide.')

        writer = PdfWriter()

        if mode == 'Ajouter':
            for page in reader.pages:
                writer.add_page(page)
            writer.encrypt(nouveau)
            sortie = pdf.replace('.pdf', '_protege.pdf')

        elif mode == 'Modifier':
            if not reader.is_encrypted:
                raise Exception('Le PDF n\'est pas protégé.')
            if reader.decrypt(actuel) == 0:
                raise Exception('Mot de passe actuel incorrect.')

            for page in reader.pages:
                writer.add_page(page)
            writer.encrypt(nouveau)
            sortie = pdf.replace('.pdf', '_modifie.pdf')

        elif mode == 'Supprimer':
            if not reader.is_encrypted:
                raise Exception('Le PDF n\'est pas protégé.')
            if reader.decrypt(nouveau) == 0:
                raise Exception('Mot de passe incorrect.')

            for page in reader.pages:
                writer.add_page(page)
            sortie = pdf.replace('.pdf', '_sans_mdp.pdf')

        if os.path.exists(sortie):
            if not messagebox.askyesno('Confirmation', f'Le fichier existe déjà :\n{sortie}\n\nVoulez-vous le remplacer ?'):
                return

        with open(sortie, 'wb') as f:
            writer.write(f)

        entree_actuel.delete(0, tk.END)
        entree_nouveau.delete(0, tk.END)
        messagebox.showinfo('Succès', f'PDF créé :\n{sortie}')

    except Exception as e:
        entree_actuel.delete(0, tk.END)
        entree_nouveau.delete(0, tk.END)
        messagebox.showerror('Erreur', str(e))


root = tk.Tk()
try:
    root.iconbitmap(resource_path('icon.ico'))
except Exception:
    pass
root.title('Gestionnaire de mots de passe PDF')
root.geometry('720x320')
root.minsize(650, 280)

root.columnconfigure(1, weight=1)

frame = ttk.Frame(root, padding=10)
frame.pack(fill='both', expand=True)
frame.columnconfigure(1, weight=1)

action = tk.StringVar(value='Ajouter')
action.trace_add('write', afficher_champs)


ttk.Label(frame, text='Action').grid(row=0, column=0, sticky='w', padx=5, pady=5)
ttk.Combobox(frame, textvariable=action, values=['Ajouter', 'Modifier', 'Supprimer'], state='readonly').grid(row=0, column=1, sticky='ew', padx=5, pady=5)


ttk.Label(frame, text='PDF source').grid(row=1, column=0, sticky='w', padx=5, pady=5)
entree_pdf = ttk.Entry(frame)
entree_pdf.grid(row=1, column=1, sticky='ew', padx=5, pady=5)
ttk.Button(frame, text='Parcourir', command=choisir_fichier).grid(row=1, column=2, padx=5, pady=5)

label_actuel = ttk.Label(frame, text='Mot de passe actuel')
label_actuel.grid(row=2, column=0, sticky='w', padx=5, pady=5)
entree_actuel = ttk.Entry(frame, show='*')
entree_actuel.grid(row=2, column=1, sticky='ew', padx=5, pady=5)

label_nouveau = ttk.Label(frame, text='Nouveau mot de passe')
label_nouveau.grid(row=3, column=0, sticky='w', padx=5, pady=5)
entree_nouveau = ttk.Entry(frame, show='*')
entree_nouveau.grid(row=3, column=1, sticky='ew', padx=5, pady=5)

def basculer_mdp():
    caractere = '' if voir_mdp.get() else '*'
    entree_actuel.config(show=caractere)
    entree_nouveau.config(show=caractere)

voir_mdp = tk.BooleanVar(value=False)
ttk.Checkbutton(frame, text='Afficher les mots de passe', variable=voir_mdp, command=basculer_mdp).grid(row=4, column=1, sticky='w', padx=5, pady=5)


ttk.Button(frame, text='Exécuter', command=executer).grid(row=10, column=1, pady=15)

afficher_champs()
root.mainloop()
