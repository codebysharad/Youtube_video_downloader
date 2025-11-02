from tkinter import *
import customtkinter as ct
from PIL import Image
import requests
from io import BytesIO
import os
import yt_dlp
import threading
from datetime import datetime

class app:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Video Downloader")
        self.root.geometry("900x600")
        self.root.minsize(800, 500)
        self.root.eval('tk::PlaceWindow . center')  # Center window on 

        ct.set_appearance_mode("dark")
        ct.set_default_color_theme("blue")

        # ---------------- Responsive Layout ----------------
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=0)  # sidebar fixed
        self.root.grid_columnconfigure(1, weight=1)  # main expands

        # Sidebar
        self.sidebar_Frame = ct.CTkFrame(self.root)
        self.sidebar_Frame.grid(row=0, column=0, sticky='ns', padx=5, pady=5)
        self.sidebar_Frame.grid_rowconfigure(5, weight=1)
        self.sidebar_Frame.grid_columnconfigure(0, weight=1)

        self.butn1 = ct.CTkButton(self.sidebar_Frame, text="Home", command=self.Home)
        self.butn1.grid(row=0, column=0, sticky='ew', padx=15, pady=10)

        self.butn2 = ct.CTkButton(self.sidebar_Frame, text="Downloads", command=self.Downloads)
        self.butn2.grid(row=1, column=0, sticky='ew', padx=15, pady=10)

        self.butn3 = ct.CTkButton(self.sidebar_Frame, text="Settings", command=self.Settings)
        self.butn3.grid(row=2, column=0, sticky='ew', padx=15, pady=10)

        self.butn4 = ct.CTkButton(self.sidebar_Frame, text="About", command=self.About)
        self.butn4.grid(row=3, column=0, sticky='ew', padx=15, pady=10)

        # ---------------- Main Content Area ----------------
        self.MainFrame = ct.CTkFrame(self.root)
        self.MainFrame.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)
        self.MainFrame.grid_rowconfigure(0, weight=0)
        self.MainFrame.grid_rowconfigure(1, weight=1)
        self.MainFrame.grid_rowconfigure(2, weight=0)
        self.MainFrame.grid_columnconfigure(0, weight=1)

        self.lable = ct.CTkLabel(self.MainFrame, text="YouTube Downloader", font=("Helvetica", 40))
        self.lable.grid(row=0, column=0, sticky='n', padx=5, pady=10)

        # URL + Search Section
        self.content_container = ct.CTkFrame(self.MainFrame, fg_color="transparent")
        self.content_container.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)
        self.content_container.grid_rowconfigure(0, weight=1)
        self.content_container.grid_rowconfigure(1, weight=1)
        self.content_container.grid_columnconfigure(0, weight=1)

        self.url_entry = ct.CTkEntry(self.content_container, placeholder_text='Enter Video URL...',
                                     width=500, height=40, font=ct.CTkFont(size=18))
        self.url_entry.grid(row=0, column=0, padx=10, pady=(0, 20), sticky="n")

        self.button_container = ct.CTkFrame(self.content_container, fg_color="transparent")
        self.button_container.grid(row=1, column=0, padx=10, pady=10, sticky="n")

        self.search_btn = ct.CTkButton(self.button_container, text="Search",
                                       command=self.create_download_view, font=ct.CTkFont(size=20),
                                       height=40, width=150)
        self.search_btn.pack(side='left', padx=(0, 10))

        # Footer
        self.FooterFrame = ct.CTkFrame(self.MainFrame, fg_color="transparent")
        self.FooterFrame.grid(row=2, column=0, sticky='sew', pady=(0, 10))
        self.footer_label = ct.CTkLabel(self.FooterFrame, text="Status: Ready", text_color="gray70")
        self.footer_label.pack()

    # ---------------- Functions ----------------
    def create_download_view(self):
        self.info_container = ct.CTkFrame(self.MainFrame, width=400)
        self.info_container.grid(row=3, column=0, padx=10, pady=(0, 20), ipadx=50, ipady=10, sticky="n")
        self.info_container.grid_columnconfigure(0, weight=1)
        self.info_container.grid_columnconfigure(1, weight=1)

        self.text_block = ct.CTkFrame(self.info_container, fg_color="transparent")
        self.text_block.grid(row=0, column=1, sticky="nsew")
        self.text_block.grid_columnconfigure(1, weight=1)

        self.Url = self.url_entry.get().strip()
        print(f"Video Url: {self.Url}")

        self.image_label = ct.CTkLabel(self.info_container, text="Loading Info", font=ct.CTkFont(size=20))
        self.image_label.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        threading.Thread(target=self.Load_info, daemon=True).start()

    def Load_info(self):
        try:
            self.dlp_Opt = {'skip_download': True, 'quiet': True}
            with yt_dlp.YoutubeDL(self.dlp_Opt) as ydl:
                self.info_dict = ydl.extract_info(self.Url, download=False)
                self.formats = self.info_dict.get("formats", [])
                self.resolutions = sorted({f"{f['height']}p" for f in self.formats if f.get("height")},
                                          key=lambda x: int(x.replace('p', '')), reverse=True)
                self.title = self.info_dict.get('title')
                self.uploader = self.info_dict.get('uploader')
                self.duration_seconds = self.info_dict.get('duration')
                self.views = self.info_dict.get('view_count')
                self.image_url = self.info_dict.get('thumbnail')

            self.text_block.after(0, self.populate_info)
        except Exception as e:
            self.image_label.configure(text=f"Error loading info: {e}")

    def populate_info(self):
        self.Vidtitle = ct.CTkLabel(self.text_block, text=f"Title : {self.title}", anchor='w')
        self.Vidtitle.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

        self.Viduploader = ct.CTkLabel(self.text_block, text=f"Uploader : {self.uploader}", anchor='w')
        self.Viduploader.grid(row=2, column=1, padx=5, pady=5, sticky="nsew")

        self.Viddur = ct.CTkLabel(self.text_block, text=f"Duration : {self.duration_seconds}", anchor='w')
        self.Viddur.grid(row=3, column=1, padx=5, pady=5, sticky="nsew")

        self.Vidview = ct.CTkLabel(self.text_block, text=f"Views : {self.views}", anchor='w')
        self.Vidview.grid(row=4, column=1, padx=5, pady=5, sticky="nsew")

        self.option_menu = ct.CTkOptionMenu(master=self.text_block, values=self.resolutions)
        self.option_menu.grid(row=5, column=1, padx=5, pady=5, sticky="ew")
        self.option_menu.set(self.resolutions[0])

        self.label_status = ct.CTkLabel(master=self.text_block, text="")
        self.label_status.grid(row=6, column=1, padx=5, pady=5, sticky="nsew")

        self.label_result = ct.CTkLabel(master=self.text_block, text="")
        self.label_result.grid(row=7, column=1, padx=5, pady=5, sticky="nsew")

        self.downBtn = ct.CTkFrame(self.info_container, fg_color="transparent")
        self.downBtn.grid(row=2, column=0, columnspan=2, pady=10, sticky="ew")

        self.VideoDown = ct.CTkButton(self.downBtn, text="Download Video",
                                      command=self.downloadVideo, font=ct.CTkFont(size=20),
                                      height=40, width=150)
        self.VideoDown.pack(side='left', padx=(0, 10))

        self.AudioDown = ct.CTkButton(self.downBtn, text="Download Audio",
                                      command=self.downloadAudio, font=ct.CTkFont(size=20),
                                      height=40, width=150)
        self.AudioDown.pack(side='left')

        self.progressbar = ct.CTkProgressBar(self.text_block, width=400)
        self.progressbar.grid(row=8, column=1, padx=5, pady=5, sticky="ew")
        self.progressbar.set(0)

        try:
            response = requests.get(self.image_url)
            response.raise_for_status()
            image_data = BytesIO(response.content)
            pil_image = Image.open(image_data)
            self.tk_image = ct.CTkImage(pil_image, size=(150, 150))
            self.image_label.configure(image=self.tk_image, text="")
        except Exception as e:
            self.image_label.configure(text=f"Error loading image: {e}")

    def print_selected_resolution(self):
        self.selected = self.option_menu.get()
        self.label_result.configure(text=f"🎥 Selected Resolution: {self.selected}")
        print("Selected Resolution:", self.selected)
        return self.selected

    def on_progress(self, d):
        if d['status'] == 'downloading':
            percent = d.get('_percent_str', '0.0%').strip().replace('%', '')
            try:
                progress = float(percent)
            except ValueError:
                progress = 0.0
            self.progressbar.set(progress / 100)
        elif d['status'] == 'finished':
            self.progressbar.set(1.0)

    def task(self):
        url = self.Url.strip()
        res = self.print_selected_resolution().strip().lower()
        if not url:
            self.label_status.configure(text="⚠️ Please enter a YouTube URL")
            return
        self.label_status.configure(text="⏳ Fetching info...")
        try:
            ydl_opts = {
                'format': f'bestvideo[height={res[:-1]}]+bestaudio/best' if 'p' in res else 'best',
                'merge_output_format': 'mp4',
                'outtmpl': '%(title)s.%(ext)s',
                'quiet': True,
                'progress_hooks': [self.on_progress]
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                title = info.get("title", "Unknown Title")
                self.label_status.configure(text=f"🎬 Downloading: {title} ({res})")
                ydl.download([url])
            self.label_status.configure(text=f"✅ Download complete: {title}.mp4")
        except Exception as e:
            self.label_status.configure(text=f"❌ Error: {e}")

    def task2(self):
        url = self.Url.strip()
        if not url:
            self.label_status.configure(text="⚠️ Please enter a YouTube URL")
            return
        self.label_status.configure(text="⏳ Fetching audio info...")
        try:
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'outtmpl': '%(title)s.%(ext)s',
                'quiet': True,
                'progress_hooks': [self.on_progress],
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                title = info.get("title", "Unknown Title")
                self.label_status.configure(text=f"🎧 Downloading: {title}")
                ydl.download([url])
            self.label_status.configure(text=f"✅ Audio download complete: {title}.mp3")
        except Exception as e:
            self.label_status.configure(text=f"❌ Error: {e}")

    def HistoryWrite(self):
        with open('YoutubeDownload.txt','a') as f:
            self.now = datetime.now()
            self.formatted_time = self.now.strftime("%d-%m-%Y %H:%M:%S")
            f.write(f'''{self.title}  {self.formatted_time}  \n ''')


    def downloadVideo(self):
        threading.Thread(target=self.task, daemon=True).start()
        self.HistoryWrite()

    def downloadAudio(self):
        threading.Thread(target=self.task2, daemon=True).start()
        self.HistoryWrite()

    # ---------------- Sidebar Functions ----------------
    def Home(self):
        for widget in self.MainFrame.winfo_children():
            widget.destroy()
        self.__init__(self.root)

    def Downloads(self):
        for widget in self.MainFrame.winfo_children():
            widget.destroy()
        self.lable = ct.CTkLabel(self.MainFrame, text="📂 Downloaded Files", font=("Helvetica", 30))
        self.lable.pack(pady=20)
        download_dir = os.getcwd()
        files = [f for f in os.listdir(download_dir) if f.endswith(('.mp4', '.mp3'))]
        for f in files:
            ct.CTkLabel(self.MainFrame, text=f, anchor='w').pack(pady=2, padx=10)

    def Settings(self):
        for widget in self.MainFrame.winfo_children():
            widget.destroy()
        self.lable = ct.CTkLabel(self.MainFrame, text="⚙️ Settings", font=("Helvetica", 30))
        self.lable.pack(pady=20)
        self.path_label = ct.CTkLabel(self.MainFrame, text=f"Current Download Folder: {os.getcwd()}")
        self.path_label.pack(pady=10)
        self.theme_option = ct.CTkOptionMenu(self.MainFrame, values=["Light", "Dark", "System"], command=self.change_theme)
        self.theme_option.pack(pady=10)
        self.theme_option.set("Dark")

    def change_theme(self, choice):
        ct.set_appearance_mode(choice.lower())

    def About(self):
        for widget in self.MainFrame.winfo_children():
            widget.destroy()
        self.lable = ct.CTkLabel(self.MainFrame, text="About", font=("Helvetica", 30))
        self.lable.pack(pady=20)
        about_text = """
        🎬 YouTube Downloader App
        Version: 1.0
        Developed by: Code by Sharad
        Built using Major: Python, CustomTkinter, yt-dlp
        Built using Major: PIL , io , requests, threadings,datetime
        """
        ct.CTkLabel(self.MainFrame, text=about_text, justify="left").pack(padx=20)


if __name__ == "__main__":
    yt_app = ct.CTk()
    yt_DLP_app = app(yt_app)
    yt_app.mainloop()
