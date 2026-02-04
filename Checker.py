import tkinter as tk
from tkinter import filedialog, ttk, messagebox, scrolledtext, simpledialog
import requests
import threading
from concurrent.futures import ThreadPoolExecutor
import socks
from collections import Counter
from time import time

# Constants
TEST_URL = "https://api.ipify.org"
COUNTRY_API = "http://ip-api.com/json/"

class EntryScreen:
    def __init__(self, root):
        self.root = root
        root.title("Hoşgeldiniz")
        root.geometry("600x350")
        root.configure(bg="#0d0b16")

        tk.Label(root, text="🔥 Hoşgeldiniz Dostlarım 🔥", fg="#c77dff", bg="#0d0b16",
                 font=("Segoe UI", 18, "bold")).pack(pady=15)
        tk.Label(root, text="Proxy Checker V.3 - Ultimate Edition", fg="#9d4edd", bg="#0d0b16",
                 font=("Segoe UI", 14)).pack(pady=5)
        tk.Label(root, text="⚡ Powered by youmean25 ⚡", fg="#7b2cbf", bg="#0d0b16",
                 font=("Segoe UI", 11, "italic")).pack(pady=5)
        tk.Label(root, text="Discord: youmean25", fg="#5a189a", bg="#0d0b16",
                 font=("Segoe UI", 10)).pack(pady=5)

        theme_frame = tk.Frame(root, bg="#0d0b16")
        theme_frame.pack(pady=10)
        tk.Label(theme_frame, text="Tema:", fg="white", bg="#0d0b16",
                font=("Segoe UI", 9)).pack(side="left", padx=5)
        
        self.theme_var = tk.StringVar(value="Mor")
        for theme in ["Mor", "Mavi", "Yeşil", "Kırmızı"]:
            tk.Radiobutton(theme_frame, text=theme, variable=self.theme_var,
                          value=theme, bg="#0d0b16", fg="white",
                          selectcolor="#5a189a", font=("Segoe UI", 9)).pack(side="left", padx=3)

        tk.Button(root, text="▶ Başla", bg="#7b2cbf", fg="white",
                  font=("Segoe UI", 14, "bold"), width=15, height=2,
                  command=self.start_checker).pack(pady=20)

    def start_checker(self):
        theme = self.theme_var.get()
        self.root.destroy()
        root = tk.Tk()
        ProxyCheckerGUI(root, theme)
        root.mainloop()

class ProxyCheckerGUI:
    def __init__(self, root, theme="Mor"):
        self.root = root
        self.theme = theme
        self.colors = self.get_theme_colors(theme)
        
        root.title("Proxy Checker V.3 - Powered by youmean25")
        root.geometry("1100x700")
        root.configure(bg=self.colors['bg'])

        self.proxies = []
        self.results = []
        self.done = 0
        self.lock = threading.Lock()
        self.executor = None
        self.start_time = None
        self.country_stats = Counter()
        self.is_running = False
        self.stop_flag = False
        self.update_counter = 0

        self.build_ui()

    def get_theme_colors(self, theme):
        themes = {
            "Mor": {'bg': '#0d0b16', 'primary': '#7b2cbf', 'secondary': '#5a189a', 'text': '#c77dff', 'accent': '#9d4edd'},
            "Mavi": {'bg': '#03045e', 'primary': '#0077b6', 'secondary': '#023e8a', 'text': '#90e0ef', 'accent': '#00b4d8'},
            "Yeşil": {'bg': '#081c15', 'primary': '#2d6a4f', 'secondary': '#1b4332', 'text': '#95d5b2', 'accent': '#52b788'},
            "Kırmızı": {'bg': '#1a0000', 'primary': '#9d0208', 'secondary': '#6a040f', 'text': '#ffb3c1', 'accent': '#e85d75'}
        }
        return themes.get(theme, themes["Mor"])

    def build_ui(self):
        # Üst panel
        top_panel = tk.Frame(self.root, bg=self.colors['bg'])
        top_panel.pack(fill="x", pady=5)

        left_frame = tk.Frame(top_panel, bg=self.colors['bg'])
        left_frame.pack(side="left", padx=5)

        tk.Button(left_frame, text="📁 Dosya Ekle", bg=self.colors['secondary'], fg="white",
                  font=("Segoe UI", 9), command=self.load_file).pack(side="left", padx=2)

        tk.Button(left_frame, text="🔗 GitHub", bg=self.colors['secondary'], fg="white",
                  font=("Segoe UI", 9), command=self.load_github).pack(side="left", padx=2)

        tk.Button(left_frame, text="📋 Çoklu Yapıştır", bg=self.colors['secondary'], fg="white",
                  font=("Segoe UI", 9), command=self.paste_proxies).pack(side="left", padx=2)

        tk.Button(left_frame, text="📋 Hızlıları Kopyala", bg=self.colors['accent'], fg="white",
                  font=("Segoe UI", 9), command=self.copy_fast_proxies).pack(side="left", padx=2)

        right_frame = tk.Frame(top_panel, bg=self.colors['bg'])
        right_frame.pack(side="right", padx=5)

        tk.Label(right_frame, text="Tip:", fg="white", bg=self.colors['bg'],
                 font=("Segoe UI", 8)).pack(side="left", padx=2)

        self.ptype = ttk.Combobox(right_frame, values=["http", "https", "socks4", "socks5"], width=8)
        self.ptype.set("http")
        self.ptype.pack(side="left", padx=2)

        # Hız ayarı
        speed_container = tk.Frame(right_frame, bg=self.colors['bg'])
        speed_container.pack(side="left", padx=(14, 2))
        
        tk.Label(speed_container, text="Hız (ms):", fg="#00ff88", bg=self.colors['bg'],
                 font=("Segoe UI", 8, "bold")).pack(side="top", anchor="w")
        
        speed_frame = tk.Frame(speed_container, bg=self.colors['bg'])
        speed_frame.pack(side="top")
        
        self.speed_var = tk.IntVar(value=1500)
        self.speed_slider = tk.Scale(speed_frame, from_=500, to=5000, orient="horizontal",
                                     variable=self.speed_var, length=120, bg=self.colors['bg'],
                                     fg="white", highlightthickness=0, troughcolor=self.colors['secondary'],
                                     activebackground=self.colors['primary'], showvalue=False)
        self.speed_slider.pack(side="left")
        
        self.speed_label = tk.Label(speed_frame, text="1500", fg="#00ff88", bg=self.colors['bg'],
                                   font=("Segoe UI", 9, "bold"), width=5)
        self.speed_label.pack(side="left", padx=2)
        
        def update_speed_label(val):
            self.speed_label.config(text=str(int(float(val))))
        
        self.speed_slider.config(command=update_speed_label)

        # Threads ayarı
        thread_container = tk.Frame(right_frame, bg=self.colors['bg'])
        thread_container.pack(side="left", padx=(14, 2))
        
        tk.Label(thread_container, text="Threads:", fg="#00ff88", bg=self.colors['bg'],
                 font=("Segoe UI", 8, "bold")).pack(side="top", anchor="w")
        
        thread_frame = tk.Frame(thread_container, bg=self.colors['bg'])
        thread_frame.pack(side="top")
        
        self.thread_var = tk.IntVar(value=80)

        self.thread_slider = tk.Scale(
            thread_frame,
            from_=10,
            to=200,
            orient="horizontal",
            variable=self.thread_var,
            length=120,
            bg=self.colors['bg'],
            fg="white",
            highlightthickness=0,
            troughcolor=self.colors['secondary'],
            activebackground=self.colors['primary'],
            showvalue=False
        )
        self.thread_slider.pack(side="left")

        self.thread_label = tk.Label(
            thread_frame,
            text="80",
            fg="#00ff88",
            bg=self.colors['bg'],
            font=("Segoe UI", 9, "bold"),
            width=4
        )
        self.thread_label.pack(side="left", padx=2)

        def update_thread_label(val):
            self.thread_label.config(text=str(int(float(val))))

        self.thread_slider.config(command=update_thread_label)

        # Kontrol butonları
        control_frame = tk.Frame(self.root, bg=self.colors['bg'])
        control_frame.pack(fill="x", pady=5)

        self.start_btn = tk.Button(control_frame, text="▶ Başlat", bg=self.colors['primary'], fg="white",
                  font=("Segoe UI", 10, "bold"), width=12, command=self.start)
        self.start_btn.pack(side="left", padx=5)

        self.stop_btn = tk.Button(control_frame, text="⏹ Durdur", bg="#dc143c", fg="white",
                  font=("Segoe UI", 10, "bold"), width=12, state="disabled", command=self.stop)
        self.stop_btn.pack(side="left", padx=5)

        tk.Button(control_frame, text="🗑 Temizle", bg="#3c096c", fg="white",
                  font=("Segoe UI", 9), command=self.clear).pack(side="left", padx=2)

        self.progress = ttk.Progressbar(control_frame, length=350, mode='determinate')
        self.progress.pack(side="left", padx=10)

        # Ana container
        main_container = tk.Frame(self.root, bg=self.colors['bg'])
        main_container.pack(fill="both", expand=True, padx=5, pady=5)

        left_panel = tk.Frame(main_container, bg=self.colors['bg'], width=650)
        left_panel.pack(side="left", fill="both", expand=True, padx=5)

        self.output_title = tk.Label(left_panel, text="⚡ Hazır | Yüklü: 0", fg=self.colors['text'], bg=self.colors['bg'],
                 font=("Segoe UI", 11, "bold"))
        self.output_title.pack(pady=5)

        self.out = scrolledtext.ScrolledText(left_panel, height=20, bg="#1a1626", fg="white",
                                             font=("Consolas", 9), insertbackground="white", state="disabled")
        self.out.pack(fill="both", expand=True)
        self.out.tag_config("ok", foreground="#00ff88")
        self.out.tag_config("slow", foreground="#ffcc00")
        self.out.tag_config("veryslow", foreground="#ff6b6b")

        # Sağ panel
        right_panel = tk.Frame(main_container, bg=self.colors['bg'], width=350)
        right_panel.pack(side="right", fill="both", padx=5)

        tk.Label(right_panel, text="📊 İstatistikler", fg=self.colors['text'], bg=self.colors['bg'],
                 font=("Segoe UI", 11, "bold")).pack(pady=5)

        self.stats_text = scrolledtext.ScrolledText(right_panel, height=15, bg="#1a1626", fg="white",
                                                    font=("Consolas", 9), state="normal")
        self.stats_text.pack(fill="both", expand=True, pady=5)
        self.stats_text.tag_config("header", foreground="#c77dff", font=("Consolas", 9, "bold"))
        self.stats_text.tag_config("good", foreground="#00ff88")
        self.stats_text.tag_config("warn", foreground="#ffcc00")

        # Export bölümü
        export_frame = tk.Frame(right_panel, bg=self.colors['bg'])
        export_frame.pack(fill="x", pady=5)

        tk.Label(export_frame, text="Export Format:", fg="white", bg=self.colors['bg'],
                font=("Segoe UI", 8)).pack(side="left", padx=2)
        self.export_format = ttk.Combobox(export_frame, values=["ip:port", "user:pass@ip:port", "ip:port:user:pass"], width=18)
        self.export_format.set("ip:port")
        self.export_format.pack(side="left", padx=2)
        tk.Button(export_frame, text="💾 Export", bg=self.colors['accent'], fg="white",
                 font=("Segoe UI", 8), command=self.custom_export).pack(side="left", padx=2)

    def load_file(self):
        path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if path:
            try:
                with open(path, encoding="utf-8") as f:
                    lines = [l.strip() for l in f if ":" in l]
                    self.proxies = lines  # Normal dosya ekleme (öncekiler temizlenir)
                    self.output_title.config(text=f"⚡ Hazır | Yüklü: {len(self.proxies)}")
                    messagebox.showinfo("Başarılı", f"✅ {len(lines)} proxy yüklendi!")
            except Exception as e:
                messagebox.showerror("Hata", f"Dosya okunamadı: {e}")

    def load_github(self):
        url = simpledialog.askstring("GitHub URL", "Proxy listesi URL'sini girin:")
        if url:
            try:
                r = requests.get(url, timeout=10)
                lines = [l.strip() for l in r.text.split("\n") if ":" in l]
                self.proxies = lines  # Normal dosya ekleme (öncekiler temizlenir)
                self.output_title.config(text=f"⚡ Hazır | Yüklü: {len(self.proxies)}")
                messagebox.showinfo("Başarılı", f"✅ {len(lines)} proxy yüklendi!")
            except Exception as e:
                messagebox.showerror("Hata", f"GitHub'dan yüklenemedi: {e}")

    def paste_proxies(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Çoklu Yapıştır")
        dialog.geometry("500x400")
        dialog.configure(bg=self.colors['bg'])

        tk.Label(dialog, text="Proxy listesini yapıştırın (her satıra bir proxy):",
                fg="white", bg=self.colors['bg'], font=("Segoe UI", 10)).pack(pady=5)

        text_box = scrolledtext.ScrolledText(dialog, height=15, bg="#1a1626", fg="white",
                                            font=("Consolas", 9))
        text_box.pack(fill="both", expand=True, padx=10, pady=5)

        def save_paste():
            content = text_box.get("1.0", "end-1c")
            lines = [l.strip() for l in content.split("\n") if ":" in l]
            self.proxies.extend(lines)
            self.output_title.config(text=f"⚡ Hazır | Yüklü: {len(self.proxies)}")
            messagebox.showinfo("Başarılı", f"✅ {len(lines)} proxy eklendi!")
            dialog.destroy()

        tk.Button(dialog, text="✅ Ekle", bg=self.colors['primary'], fg="white",
                 font=("Segoe UI", 10), command=save_paste).pack(pady=5)

    def copy_fast_proxies(self):
        if not self.results:
            messagebox.showwarning("Uyarı", "Önce test yapın!")
            return

        fast_list = "\n".join([p[0] for p in self.results])
        self.root.clipboard_clear()
        self.root.clipboard_append(fast_list)
        messagebox.showinfo("Kopyalandı", f"✅ {len(self.results)} hızlı proxy kopyalandı!")

    def clear(self):
        self.stop_flag = True
        self.is_running = False

        if self.executor:
            self.executor.shutdown(wait=False)

        self.proxies.clear()
        self.results.clear()
        self.done = 0
        self.country_stats.clear()

        self.output_title.config(text="⚡ Hazır | Yüklü: 0")
        self.out.config(state="normal")
        self.out.delete("1.0", "end")
        self.out.config(state="disabled")
        self.stats_text.delete("1.0", "end")
        self.progress['value'] = 0

        self.start_btn.config(state="normal")
        self.stop_btn.config(state="disabled")

        messagebox.showinfo("Temizlendi", "✨ Tüm veriler temizlendi!")

    def start(self):
        if not self.proxies:
            messagebox.showwarning("Uyarı", "Önce proxy ekleyin!")
            return

        if self.is_running:
            messagebox.showwarning("Uyarı", "Zaten çalışıyor!")
            return

        self.is_running = True
        self.stop_flag = False
        self.done = 0
        self.results.clear()
        self.country_stats.clear()
        self.update_counter = 0

        self.out.config(state="normal")
        self.out.delete("1.0", "end")
        self.out.config(state="disabled")
        self.stats_text.delete("1.0", "end")

        self.progress['maximum'] = len(self.proxies)
        self.progress['value'] = 0

        self.start_btn.config(state="disabled")
        self.stop_btn.config(state="normal")

        self.start_time = time()
        threads = self.thread_var.get()
        self.executor = ThreadPoolExecutor(max_workers=threads)

        for proxy in self.proxies:
            if self.stop_flag:
                break
            self.executor.submit(self.check_proxy, proxy)

    def stop(self):
        self.stop_flag = True
        self.is_running = False

        if self.executor:
            self.executor.shutdown(wait=False)

        self.start_btn.config(state="normal")
        self.stop_btn.config(state="disabled")

        self.out.config(state="normal")
        self.out.insert("end", "\n🍵 Test durduruldu!\n", "slow")
        self.out.see("end")
        self.out.config(state="disabled")

        self.save_results()
        messagebox.showinfo("Durduruldu", "⏸ Test durduruldu!")

    def save_results(self):
        if self.results:
            with open("hizli.txt", "w", encoding="utf-8") as f:
                for p, ping, c in sorted(self.results, key=lambda x: x[1]):
                    f.write(f"{p}\n")

    def check_proxy(self, proxy):
        if self.stop_flag:
            return

        try:
            ptype = self.ptype.get().lower()
            ip, port = proxy.split(":")
            port = int(port)
            t0 = time()
            max_ping = self.speed_var.get()

            # Proxy testi
            if ptype in ["socks4", "socks5"]:
                s = socks.socksocket()
                s.set_proxy(socks.SOCKS5 if ptype == "socks5" else socks.SOCKS4, ip, port)
                s.settimeout(5)
                s.connect(("www.google.com", 443))
                s.close()
            else:
                test_proxies = {
                    "http": f"{ptype}://{proxy}",
                    "https": f"{ptype}://{proxy}"
                }
                requests.get(TEST_URL, proxies=test_proxies, timeout=5)

            if self.stop_flag:
                return

            ping = int((time() - t0) * 1000)

            # Ülke bilgisi
            country = "?"
            try:
                if not self.stop_flag:
                    country_resp = requests.get(COUNTRY_API + ip, timeout=2)
                    country = country_resp.json().get("country", "?")
            except:
                pass

            if self.stop_flag:
                return

            # Kaydet
            with self.lock:
                if ping <= max_ping:
                    self.results.append((proxy, ping, country))
                    self.country_stats[country] += 1
                    
                    if not self.stop_flag:
                        tag = "ok" if ping < 500 else "slow" if ping < 1500 else "veryslow"
                        self.root.after(0, lambda: self.update_output(proxy, ping, country, tag))

        except Exception as e:
            pass

        if not self.stop_flag:
            with self.lock:
                self.done += 1
                self.root.after(0, lambda: self.progress.config(value=self.done))
                
                self.update_counter += 1
                if self.update_counter % 10 == 0:
                    self.root.after(0, self.update_stats_panel)

                if self.done >= len(self.proxies):
                    self.root.after(0, self.finish)

    def update_output(self, proxy, ping, country, tag):
        self.out.config(state="normal")
        self.out.insert("end", f"✅ {proxy} | {ping}ms | {country}\n", tag)
        self.out.see("end")
        self.out.config(state="disabled")

    def update_stats_panel(self):
        self.stats_text.delete("1.0", "end")
        
        self.stats_text.insert("end", "━━━ GENEL ━━━\n", "header")
        self.stats_text.insert("end", f"Toplam: {len(self.proxies)}\n")
        self.stats_text.insert("end", f"Çalışan: {len(self.results)}\n", "good")
        self.stats_text.insert("end", f"Başarısız: {self.done - len(self.results)}\n\n")
        
        if self.results:
            all_pings = [p[1] for p in self.results]
            avg_ping = sum(all_pings) / len(all_pings)
            self.stats_text.insert("end", f"Ort. Ping: {avg_ping:.0f} ms\n\n")
        
        if self.results:
            self.stats_text.insert("end", "━━━ EN HIZLI 10 ━━━\n", "header")
            top10 = sorted(self.results, key=lambda x: x[1])[:10]
            for i, (p, ping, c) in enumerate(top10, 1):
                self.stats_text.insert("end", f"{i}. {p} | {ping}ms | {c}\n", "good")
            self.stats_text.insert("end", "\n")
        
        if self.country_stats:
            self.stats_text.insert("end", "━━━ ÜLKELER ━━━\n", "header")
            for country, count in self.country_stats.most_common(5):
                self.stats_text.insert("end", f"{country}: {count}\n")

    def finish(self):
        if self.stop_flag:
            return

        if self.executor:
            self.executor.shutdown(wait=True)

        self.is_running = False
        self.start_btn.config(state="normal")
        self.stop_btn.config(state="disabled")

        if len(self.results) == 0:
            messagebox.showinfo("Bilgi", "❌ Hiç çalışan proxy bulunamadı!")
            return

        self.out.config(state="normal")
        self.out.insert("end", "\n🎉 Test tamamlandı!\n", "ok")
        self.out.see("end")
        self.out.config(state="disabled")

        self.save_results()
        messagebox.showinfo("Tamamlandı", f"🎉 {len(self.results)} çalışan proxy bulundu!")

    def custom_export(self):
        if not self.results:
            messagebox.showwarning("Uyarı", "Önce test yapın!")
            return
        
        export_type = self.export_format.get()
        file_name = simpledialog.askstring("Dosya Adı", "Dosya adını girin:", parent=self.root)
        
        if not file_name:
            messagebox.showwarning("Uyarı", "Geçerli bir dosya adı girin!")
            return

        try:
            if export_type == "user:pass@ip:port":
                with open(f"{file_name}_userpass.txt", "w", encoding="utf-8") as f:
                    for p, _, _ in self.results:
                        f.write(f"user:pass@{p}\n")
                messagebox.showinfo("Export", f"✅ {file_name}_userpass.txt oluşturuldu!")
            
            elif export_type == "ip:port:user:pass":
                with open(f"{file_name}_format2.txt", "w", encoding="utf-8") as f:
                    for p, _, _ in self.results:
                        f.write(f"{p}:user:pass\n")
                messagebox.showinfo("Export", f"✅ {file_name}_format2.txt oluşturuldu!")
            
            else:
                with open(f"{file_name}_simple.txt", "w", encoding="utf-8") as f:
                    for p, _, _ in self.results:
                        f.write(f"{p}\n")
                messagebox.showinfo("Export", f"✅ {file_name}_simple.txt oluşturuldu!")

        except Exception as e:
            messagebox.showerror("Hata", f"Export hatası: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    EntryScreen(root)
    root.mainloop()