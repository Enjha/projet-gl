import os 
import shutil
import fnmatch

from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from app.models.music import Music
from app.models.playlist import Playlist
from mutagen.mp3 import MP3
from pygame import mixer

# Classe permettant la gestion des musiques dans la librairie
class Library (object):
 
    # Chemin pour les fichiers/dossiers de musiques et playlists.
    global LIBRARY_PATH, PLAYLISTS_PATH
    LIBRARY_PATH = "ressources/songs"
    PLAYLISTS_PATH = "ressources/playlists"

    # Liste de playlists et musiques.
    playlist_list = []
    music_list = []
    current_music = ()

    # Constructeur
    def __init__(self):
        self.init_music_list()
        self.init_playlists_list()
    
    # Initialise les liste de musiques et de playlists en allant chercher directemment dans les fichiers/dossiers.
    def init_music_list(self):
        pattern = "*.mp3" 
        music_list = []
        for root, dirs, files, in os.walk(LIBRARY_PATH):
            for filename in fnmatch.filter(files, pattern): 
                music=self.create_music_by_name(filename)
                music_list.append(music)
        self.music_list = music_list

    # Initialise la liste des playlists en fonctions des fichiers
    def init_playlists_list(self):
        dir_list = os.listdir(PLAYLISTS_PATH)
        for file in dir_list:
            self.playlist_list.append(Playlist(file.replace(".txt", ""), self))

    # Getter pour les liste de musiques et de playlists.
    def get_music_list(self):
        return self.music_list
    
    def get_playlist_list(self):
        return self.playlist_list
    #Getter pour la musique actuellement en écoute. 
    def get_current_music(self):
        return self.current_music
    
    def set_current_music(self, music):
        self.current_music = music

    # Obtenir la musique suivante à la courante
    def get_next_music(self, music):
        size = len(self.music_list)
        for i in range(size):
            if(self.music_list[i].get_title() == music.get_title()):
                if(i < size-1):
                    return self.music_list[i+1]
                else:
                    return self.music_list[0]   

    # Obtenir la musique précédente à la courante
    def get_previous_music(self, music):
        size = len(self.music_list)
        for i in range(size):
            if(self.music_list[i].equals(music)):
                if(i > 0):
                    return self.music_list[i-1]
                else:
                    return self.music_list[size-1] 

    # Ajouter et supprimer une playlist à la liste des playlists
    def add_playlist(self, playlist):
        self.playlist_list.append(playlist)

    def remove_playlist(self, playlist):
        self.playlist_list.remove(playlist)   

    # Vérifie que le titre de la musique est présente dans la librairie.
    def is_music_exist(self, name):
        for music in self.music_list:
            if name == music.get_title():
                return True
        return False

    # Créer un objet Music en récupérant son temps
    def create_music_by_name(self, name):
        audio = MP3(LIBRARY_PATH+"\\"+name)
        audio_info = audio.info
        duration = int(audio_info.length)
        music = Music(name.replace(".mp3", "") , duration, self)
        return music

    # Methode d'import de fichier en .mp3
    def import_music(self, music_space):
        # Ouvrir la fenêtre de dialogue pour importer des fichiers .mp3
        songs=filedialog.askopenfilenames(initialdir="songs/",title="Importer fichier audio", filetypes=(("mp3 Files","*.mp3"),))
        # Parcourir la selection
        for song in songs:
            # Recupérer le nom de la musique dans le chemin
            song_split = song.split("/")
            song_rename = song_split[len(song_split)-1]
            # Si elle a déjà été importé alors empêcher le re-import et afficher une pop-in
            if(os.path.exists(LIBRARY_PATH+"/"+ song_rename)):
                messagebox.showinfo("Information", song_rename+" a déjà été importé",icon='warning')
            # Si non, on l'ajoute à l'interface et dans le dossier
            else:
                shutil.copy(song, LIBRARY_PATH)    
                music = self.create_music_by_name(song_rename)
                self.music_list.append(music)
                music_space.insert(END,music.get_title())
    
    # Méthode de suppression d'une musique présente dans la librairie  
    def delete_music(self, music_space): 
        name=music_space.get("anchor")+".mp3"
        name_music_test = music_space.get("anchor")
        if(os.path.exists(LIBRARY_PATH+"/"+ name)):
            result = messagebox.askquestion("Confirmation", "Voulez-vous supprimer "+name+" ?", icon='warning')
            if result == 'yes':
                # Suppression de la musique sur l'affichage
                music_space.delete("anchor")
                # Suppression de la musique dans le dossier songs
                os.remove(LIBRARY_PATH+"/"+ name)
                # Suppression de la musique dans la liste des musiques de l'objet
                for music in self.get_music_list():
                    if(music.get_title() == name):
                        self.get_playlist_list().remove(music)         
                for playlist in self.get_playlist_list():
                    for music in playlist.music_list:
                        if(music.get_title() == name):
                            playlist.remove_music(playlist, name)    
        else:
           messagebox.showinfo(name +" n'existe pas.", icon='warning')

    # Méthode permettant de jouer une musique
    def play_music(self, music_clicked):
        # Charger la musique et la jouer 
        self.set_current_music(music_clicked)
        mixer.music.load(LIBRARY_PATH + "\\" + music_clicked.get_title() + ".mp3")
        mixer.music.play()

    # Méthode permettant d'arrêter la lecture d'une quelconque musique
    def stop_music(self, music_space):
        mixer.music.stop()
        music_space.select_clear('active')

    # Renvoie une musique grâce au nom
    def find_music_by_name(self, name):
        for music in self.get_music_list():
            if(music.get_title() == name):
                return music

    # Renvoie une playlist grâce au nom
    def find_playlist_by_title(self, title):
        for playlist in self.get_playlist_list():
            if(playlist.get_title() == title):
                return playlist            