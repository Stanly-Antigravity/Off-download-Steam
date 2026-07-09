import os
import sys
import subprocess
import winreg
import tkinter as tk
import customtkinter as ctk
import tkinter.messagebox as messagebox
from customtkinter import filedialog
from PIL import Image

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Appearance Settings (Premium Dark Theme)
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

class SteamManagerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Steam Download Manager PRO")
        self.geometry("550x680")
        self.resizable(False, False)
        
        # Premium Fonts
        self.font_title = ctk.CTkFont(family="Tahoma", size=24, weight="bold")
        self.font_bold = ctk.CTkFont(family="Tahoma", size=15, weight="bold")
        self.font_normal = ctk.CTkFont(family="Tahoma", size=13)
        
        icon_path = resource_path("icon.png")
        
        # Set Window Icon
        icon_ico_path = resource_path("icon.ico")
        if os.path.exists(icon_ico_path):
            try:
                self.iconbitmap(icon_ico_path)
            except Exception as e:
                print("Icon load error:", e)
                
        # Header Frame
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(pady=(25, 10))
        
        # Display Logo Image
        if os.path.exists(icon_path):
            try:
                logo_img = ctk.CTkImage(light_image=Image.open(icon_path), dark_image=Image.open(icon_path), size=(90, 90))
                self.logo_label = ctk.CTkLabel(self.header_frame, image=logo_img, text="")
                self.logo_label.pack(pady=(0, 10))
            except Exception as e:
                print("Logo image load error:", e)
                
        self.title_label = ctk.CTkLabel(self.header_frame, text="مدیریت دانلود استیم", font=self.font_title, text_color="#3498DB")
        self.title_label.pack()
        
        # Path Selection Frame (Card Style)
        self.path_var = ctk.StringVar(value=self.get_steam_path())
        self.path_var.trace_add("write", self.check_status) # Auto update status when path changes
        
        self.path_frame = ctk.CTkFrame(self, corner_radius=12, fg_color="#212429", border_width=1, border_color="#34495E")
        self.path_frame.pack(pady=10, padx=20, fill="x")
        
        self.path_label = ctk.CTkLabel(self.path_frame, text=": مسیر پوشه استیم یا کتابخانه بازی‌ها", font=self.font_bold)
        self.path_label.pack(anchor="e", padx=15, pady=(10, 0))
        
        self.path_inner_frame = ctk.CTkFrame(self.path_frame, fg_color="transparent")
        self.path_inner_frame.pack(fill="x", padx=15, pady=(5, 15))
        
        # Browse Button
        self.btn_browse = ctk.CTkButton(self.path_inner_frame, text="انتخاب پوشه", font=self.font_normal, width=100, corner_radius=8, command=self.browse_folder, fg_color="#2980B9", hover_color="#1F618D")
        self.btn_browse.pack(side="left", padx=(0, 10))
        
        self.path_entry = ctk.CTkEntry(self.path_inner_frame, textvariable=self.path_var, justify="left", font=ctk.CTkFont(size=12), corner_radius=8)
        self.path_entry.pack(side="left", fill="x", expand=True)
        
        # Workshop Card
        self.ws_frame = ctk.CTkFrame(self, corner_radius=15, fg_color="#1E2024", border_width=1, border_color="#E67E22")
        self.ws_frame.pack(pady=10, padx=20, fill="x")
        
        self.ws_label = ctk.CTkLabel(self.ws_frame, text="ورک شاپ (Workshop)", font=self.font_bold, text_color="#E67E22")
        self.ws_label.pack(pady=(15, 0))
        
        self.ws_desc = ctk.CTkLabel(self.ws_frame, text="مسدودسازی دانلود مادها و مپ‌های ورک‌شاپ", font=self.font_normal, text_color="#95A5A6")
        self.ws_desc.pack(pady=0)
        
        # Workshop Status
        self.ws_status_label = ctk.CTkLabel(self.ws_frame, text="وضعیت: در حال بررسی...", font=self.font_bold)
        self.ws_status_label.pack(pady=(5, 0))
        
        self.ws_btn_frame = ctk.CTkFrame(self.ws_frame, fg_color="transparent")
        self.ws_btn_frame.pack(pady=(10, 15), fill="x", padx=20)
        
        self.btn_block_ws = ctk.CTkButton(self.ws_btn_frame, text="مسدود کردن", font=self.font_bold, corner_radius=8, fg_color="#E74C3C", hover_color="#C0392B", command=lambda: self.toggle_access("workshop", False))
        self.btn_block_ws.pack(side="left", padx=10, expand=True, fill="x")
        
        self.btn_unblock_ws = ctk.CTkButton(self.ws_btn_frame, text="فعال کردن", font=self.font_bold, corner_radius=8, fg_color="#2ECC71", hover_color="#27AE60", command=lambda: self.toggle_access("workshop", True))
        self.btn_unblock_ws.pack(side="right", padx=10, expand=True, fill="x")
        
        # All Games Card
        self.game_frame = ctk.CTkFrame(self, corner_radius=15, fg_color="#1E2024", border_width=1, border_color="#9B59B6")
        self.game_frame.pack(pady=10, padx=20, fill="x")
        
        self.game_label = ctk.CTkLabel(self.game_frame, text="کل بازی ها (All Games)", font=self.font_bold, text_color="#9B59B6")
        self.game_label.pack(pady=(15, 0))
        
        self.game_desc = ctk.CTkLabel(self.game_frame, text="مسدودسازی دانلود و آپدیت تمامی بازی‌های استیم", font=self.font_normal, text_color="#95A5A6")
        self.game_desc.pack(pady=0)
        
        # All Games Status
        self.game_status_label = ctk.CTkLabel(self.game_frame, text="وضعیت: در حال بررسی...", font=self.font_bold)
        self.game_status_label.pack(pady=(5, 0))
        
        self.game_btn_frame = ctk.CTkFrame(self.game_frame, fg_color="transparent")
        self.game_btn_frame.pack(pady=(10, 15), fill="x", padx=20)
        
        self.btn_block_game = ctk.CTkButton(self.game_btn_frame, text="مسدود کردن", font=self.font_bold, corner_radius=8, fg_color="#E74C3C", hover_color="#C0392B", command=lambda: self.toggle_access("games", False))
        self.btn_block_game.pack(side="left", padx=10, expand=True, fill="x")
        
        self.btn_unblock_game = ctk.CTkButton(self.game_btn_frame, text="فعال کردن", font=self.font_bold, corner_radius=8, fg_color="#2ECC71", hover_color="#27AE60", command=lambda: self.toggle_access("games", True))
        self.btn_unblock_game.pack(side="right", padx=10, expand=True, fill="x")
        
        # Footer
        self.footer = ctk.CTkLabel(self, text="Designed for Game Centers | Premium Edition", font=ctk.CTkFont(size=11), text_color="#7F8C8D")
        self.footer.pack(side="bottom", pady=15)
        
        # Initial check
        self.check_status()

    def get_steam_path(self):
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Valve\Steam")
            path, _ = winreg.QueryValueEx(key, "SteamPath")
            return path.replace("/", "\\")
        except FileNotFoundError:
            return "C:\\Program Files (x86)\\Steam"

    def browse_folder(self):
        folder = filedialog.askdirectory(title="انتخاب پوشه استیم یا کتابخانه بازی‌ها")
        if folder:
            self.path_var.set(folder.replace("/", "\\"))

    def check_status(self, *args):
        base_path = self.path_var.get()
        if not os.path.exists(base_path):
            self.ws_status_label.configure(text="وضعیت: مسیر نامعتبر ❌", text_color="#95A5A6")
            self.game_status_label.configure(text="وضعیت: مسیر نامعتبر ❌", text_color="#95A5A6")
            return
            
        ws_path = os.path.join(base_path, "steamapps", "workshop", "downloads")
        game_path = os.path.join(base_path, "steamapps", "downloading")
        
        self.update_status_label(self.ws_status_label, ws_path)
        self.update_status_label(self.game_status_label, game_path)

    def update_status_label(self, label, path):
        if not os.path.exists(path):
            label.configure(text="وضعیت: آزاد 🟢 (پوشه دانلود خالیست)", text_color="#2ECC71")
            return
            
        try:
            # Try writing a temporary file to check if blocked
            test_file = os.path.join(path, "test_status.tmp")
            with open(test_file, "w") as f:
                f.write("t")
            os.remove(test_file)
            label.configure(text="وضعیت: فعال 🟢", text_color="#2ECC71")
        except PermissionError:
            label.configure(text="وضعیت: مسدود 🔴", text_color="#E74C3C")
        except Exception:
            label.configure(text="وضعیت: نامشخص ⚪", text_color="#95A5A6")

    def toggle_access(self, target, unblock=False):
        base_path = self.path_var.get()
        if not os.path.exists(base_path):
            messagebox.showerror("خطا", "مسیر نامعتبر است! لطفاً آدرس صحیح پوشه استیم را انتخاب کنید.")
            return
            
        if target == "workshop":
            target_path = os.path.join(base_path, "steamapps", "workshop", "downloads")
        else:
            target_path = os.path.join(base_path, "steamapps", "downloading")
            
        os.makedirs(target_path, exist_ok=True)
        
        if unblock:
            cmd = f'icacls "{target_path}" /remove:d Everyone /C /Q'
            msg = "دانلود با موفقیت فعال (باز) شد."
        else:
            cmd = f'icacls "{target_path}" /deny Everyone:(W,WD,AD) /C /Q'
            msg = "دانلود با موفقیت مسدود (بسته) شد."
            
        try:
            subprocess.run(cmd, shell=True, check=True, creationflags=subprocess.CREATE_NO_WINDOW)
            messagebox.showinfo("موفقیت", msg)
            self.check_status() # Update labels
        except subprocess.CalledProcessError:
            messagebox.showerror("خطا", "عملیات با خطا مواجه شد.\nلطفاً برنامه را با کلیک راست و 'Run as Administrator' اجرا کنید.")

if __name__ == "__main__":
    app = SteamManagerApp()
    app.mainloop()
