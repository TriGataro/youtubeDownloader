import os
from tkinter.filedialog import askdirectory
from pytube import YouTube,Playlist
from tkinter import *
from tkinter import messagebox
import webbrowser

root=Tk()
root.title("Youtube Downloader in Python ")
root.iconbitmap(r'youtube_icon.ico')
root.geometry("650x260")

logPath = StringVar()
selectedFormat=StringVar()
selectedFormat.set(".mp4")
folder=""  
e=Entry(root,width=100,borderwidth=5,)
e.grid( row=2, column=0,columnspan=4,padx=10,pady=20)
e.config(fg="blue")
logPath.set("Seleccione carpeta de descarga")

def make_textmenu(root):
	global the_menu
	the_menu = Menu(root, tearoff=0)
	the_menu.add_command(label="Cortar")
	the_menu.add_command(label="Copiar")
	the_menu.add_command(label="Pegar")
	the_menu.add_separator()
	the_menu.add_command(label="Selecionar todo")

def callback_select_all(event):
	# select text after 50ms
	root.after(50, lambda:event.widget.select_range(0, 'end'))

def show_textmenu(event):
	e_widget = event.widget
	the_menu.entryconfigure("Cortar",command=lambda: e_widget.event_generate("<<Cut>>"))
	the_menu.entryconfigure("Copiar",command=lambda: e_widget.event_generate("<<Copy>>"))
	the_menu.entryconfigure("Pegar",command=lambda: e_widget.event_generate("<<Paste>>"))
	the_menu.entryconfigure("Selecionar todo",command=lambda: e_widget.select_range(0, 'end'))
	the_menu.tk.call("tk_popup", the_menu, event.x_root, event.y_root)

def openFolder():
     global folder    
     if(folder==""):
        importanInfo(f"Seleccione carpeta de descarga")
        selectFolder()
     else:
        os.startfile(folder)
 
def selectFolder():
     global folder    
     folder=askdirectory(title="Seleccione carpeta de descarga") 
     logPath.set(folder)

def openBrowser(link):
     webbrowser.open(link)
def downloadEvent():
    full_Path=""
    new_name=""
    fileFormat=selectedFormat.get()
    global folder
    if folder=="":
        openFolder()
    else:  
        url=e.get()
        if(url==""):
            e.focus_set()
            importanInfo(f"Url Vacía")
        else:
            try:            
                if url.lower().startswith('https://www.youtube.com'):
                    if '/playlist?' in url:
                        importanInfo(f"Playlist encontrada")
                        playlist= Playlist(url)
                        for yt in playlist.videos:
                            downloadFile(yt,fileFormat)
                    else:
                        yt=YouTube(url)
                        downloadFile(yt,fileFormat)
                else:
                    importanInfo(f"Url no es de youtube")
            except Exception as err:
                importanInfo(f"Error al descargar: {err}")   
                clear()

def downloadFile(yt, format):
     
     if format==".mp3":
           video = yt.streams.filter(only_audio=True).first()
     else:
           video = yt.streams.get_highest_resolution()
         
     full_Path= f"{folder}\{video.default_filename}"     
     new_name=full_Path.replace(".mp4",format)

     if not os.path.isfile(new_name):
        #importanInfo(f"Descargando en formato {format}\nAutor:{yt.author}\nVistas:{yt.views},\n Esto puede tomar varios minutos dependiendo de la duracion del video")
        try:
            video.download(folder)
            os.rename(full_Path,new_name)
            importanInfo(f"Archivo descargado:{yt.title}")
            #os.startfile(new_name)
        except Exception as e:
            importanInfo(f"Error al descargar: {e}")    
     else:
        importanInfo(f"Archivo {os.path.basename(new_name)} ya descargado")
     
def clear():
    e.delete(0,END)
    
def importanInfo(info):
    messagebox.showinfo("Información",info)

make_textmenu(root)
e.focus_set()
root.bind_class("Entry", "<Button-3><ButtonRelease-3>", show_textmenu)
root.bind_class("Entry", "<Control-a>", callback_select_all)

rdb_mp4=Radiobutton(root,text="MP4 (Video)",variable=selectedFormat,value=".mp4")
rdb_mp3=Radiobutton(root,text="MP3 (Música)",variable=selectedFormat,value=".mp3")
button_path=Button(root,text="Ubicación Descarga",padx=5,pady=5,command=selectFolder, bg="#808080",fg="#FFFFFF")
button_open=Button(root,text="Abrir Descarga",padx=5,pady=5,command=openFolder,bg="#808080",fg="#FFFFFF")
button_download=Button(root,text="Descargar",padx=5,pady=5,command=downloadEvent, bg="#00FFFF")
button_goyoutube=Button(root,text="Ir a Youtube",padx=5,pady=5,command=lambda:openBrowser("https://www.youtube.com"), bg="#ffffff",fg="#000000")
button_gogithub=Button(root,text="Github",padx=0,pady=0, borderwidth=0,command=lambda:openBrowser("https://github.com/TriGataro"))
button_clear=Button(root,text="Limpiar",padx=5,pady=5,command=clear, bg="#00FFFF")
label_path=Label(root, textvariable=logPath,padx=10,pady=10,fg="#DC143C")


label_path.grid(row=0,column=0)

rdb_mp4.grid(row=1,column=0)
rdb_mp3.grid(row=1,column=1)

button_download.grid(row=3,column=0)
button_clear.grid(row=3,column=3)
button_goyoutube.grid(row=1,column=3)

button_gogithub.grid(row=4,column=1)
button_path.grid(row=5,column=0)
button_open.grid(row=5,column=3)


root.mainloop()