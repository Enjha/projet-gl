from tkinter import *
from tkinter import font
from app.layouts.playlists_layout import *

class LibraryLayout : 

    # Constructeur
    def __init__(self, window, library, player_layout):
        self.window = window
        self.library = library
        self.player_layout = player_layout
    # Affiche le layout de la librairie
    def show(self):
        font_text_button = font.Font(size=15, family=('Sans Serif'))
        # Espace afficahnt les musiques
        music_list = self.library.get_music_list()

        # Affiche les playlist lors d'un click
        def on_click_playlist():
            musics_frame.destroy()
            top_buttons.destroy()
            PlaylistsLayout(self.window, self.library, self).show()

        # Permet de lever l'event quand on clique sur une musique
        def on_click_music(event):
            supp_button.place(anchor = 'e', height= 40, width=210, x=self.window.winfo_height()+150,y=40)

        # Lorsqu'on double click sur une musique
        def on_double_click_music(event):
            music_clicked = self.library.find_music_by_name(music_space.get("anchor"))
            #On la joue et la déclare comme la musique courante
            self.library.set_current_music(music_clicked)
            self.library.play_music(music_clicked)
            if(len(self.window.children) <= 2):
                self.player_layout.show()  
                
        # Paquer les boutons   
        top_buttons = Frame(self.window, width=self.window.winfo_width(), height=80, bg="#141414")
        top_buttons.pack(side=TOP)
        # Boutons permettant l'import, la suppression, et aller aux playlists
        import_button = Button(top_buttons, text="Importer des musiques", activebackground="#0be881", bg="#05c46b", fg="white", command=lambda : self.library.import_music(music_space))
        playlist_button = Button(top_buttons, text="Accéder aux playlists", activebackground="#0be881", bg="#05c46b", fg="white", command=lambda : on_click_playlist())
        supp_button = Button(top_buttons,text="🗑️ Supprimer", activebackground='#ff5e57', bg='#ff3f34', fg ='white', borderwidth=0, command=lambda : self.library.delete_music(music_space))
       
        import_button['font'] = font_text_button
        playlist_button['font'] = font_text_button
        supp_button['font'] = font_text_button
       
        import_button.place(anchor = 'w', height= 40, width=210, x=20, y=40)
        playlist_button.place(anchor = 'w', height= 40, width=210, x=300, y=40)
        supp_button.place_forget()
        
        musics_frame = Frame(self.window, width= 900, height= 400, bg="#141414")
        musics_frame.pack(padx= (30,30) ,pady=(20,40))
        
        music_space = Listbox(musics_frame, fg="white",width=70,height=17, bg="#202020",font=('helvetica',18), selectbackground="#4b4b4b", relief=FLAT, selectforeground="white", highlightthickness=0, activestyle=NONE)
        music_space.pack(padx=10, pady=10)
        
        # Initialise la liste des musiques sur l'affichage
        for music in music_list: 
            music_space.insert('end', music.get_title()) 
            
        music_space.bind("<Double-Button>", on_double_click_music)
        music_space.bind("<Button>", on_click_music)
        
        
    def get_player_layout(self):
        return self.player_layout

    def clear(self):
        self.destroy()