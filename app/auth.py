import sqlite3
import hashlib
import tkinter as tk
from tkinter import ttk, messagebox
import os

class AuthManager:
    def __init__(self, db_name="market_auth.db"):
        self.db_name = db_name
        self.init_database()
        self.create_default_admin()
    
    def init_database(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT DEFAULT 'user',
                full_name TEXT,
                email TEXT,
                created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP,
                is_active BOOLEAN DEFAULT 1
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    def create_default_admin(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # Admin kullanıcısı var mı kontrol et
        cursor.execute("SELECT COUNT(*) FROM users WHERE role = 'admin'")
        admin_count = cursor.fetchone()[0]
        
        if admin_count == 0:
            # Varsayılan admin oluştur
            admin_password = self.hash_password("admin123")
            cursor.execute('''
                INSERT INTO users (username, password_hash, role, full_name, email)
                VALUES (?, ?, ?, ?, ?)
            ''', ("admin", admin_password, "admin", "Sistem Yöneticisi", "admin@market.com"))
            conn.commit()
        
        conn.close()
    
    def authenticate(self, username, password):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        password_hash = self.hash_password(password)
        cursor.execute('''
            SELECT id, username, role, full_name, is_active 
            FROM users 
            WHERE username = ? AND password_hash = ?
        ''', (username, password_hash))
        
        user = cursor.fetchone()
        
        if user and user[4]:  # is_active kontrolü
            # Son giriş zamanını güncelle
            cursor.execute('''
                UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = ?
            ''', (user[0],))
            conn.commit()
            conn.close()
            return {
                'id': user[0],
                'username': user[1],
                'role': user[2],
                'full_name': user[3]
            }
        
        conn.close()
        return None
    
    def create_user(self, username, password, role, full_name, email):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        try:
            password_hash = self.hash_password(password)
            cursor.execute('''
                INSERT INTO users (username, password_hash, role, full_name, email)
                VALUES (?, ?, ?, ?, ?)
            ''', (username, password_hash, role, full_name, email))
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            conn.close()
            return False
    
    def get_all_users(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, username, role, full_name, email, created_date, last_login, is_active
            FROM users
            ORDER BY created_date DESC
        ''')
        
        users = cursor.fetchall()
        conn.close()
        return users
    
    def update_user_status(self, user_id, is_active):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('UPDATE users SET is_active = ? WHERE id = ?', (is_active, user_id))
        conn.commit()
        conn.close()

class LoginWindow:
    def __init__(self, on_success_callback):
        self.auth_manager = AuthManager()
        self.on_success_callback = on_success_callback
        self.current_user = None
        
        self.create_login_window()
    
    def create_login_window(self):
        self.login_root = tk.Tk()
        self.login_root.title("Market Sistemi - Giriş")
        self.login_root.geometry("450x600")
        self.login_root.configure(bg='#1e3c72')
        self.login_root.resizable(False, False)
        
        # Pencereyi ortala
        self.center_window()
        
        # Ana çerçeve
        main_frame = tk.Frame(self.login_root, bg='#1e3c72')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=40)
        
        # Logo ve başlık
        title_frame = tk.Frame(main_frame, bg='#1e3c72')
        title_frame.pack(pady=(0, 40))
        
        # Logo (büyük emoji)
        logo_label = tk.Label(title_frame, text="🏪", font=('Arial', 80), 
                             bg='#1e3c72', fg='white')
        logo_label.pack()
        
        title_label = tk.Label(title_frame, text="MARKET YÖNETİM SİSTEMİ", 
                              font=('Arial', 18, 'bold'), bg='#1e3c72', fg='white')
        title_label.pack(pady=(10, 0))
        
        subtitle_label = tk.Label(title_frame, text="Güvenli Giriş", 
                                 font=('Arial', 12), bg='#1e3c72', fg='#a8c8ff')
        subtitle_label.pack(pady=(5, 0))
        
        # Giriş formu çerçevesi
        form_frame = tk.Frame(main_frame, bg='white', relief=tk.RAISED, bd=2)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # İç çerçeve
        inner_frame = tk.Frame(form_frame, bg='white')
        inner_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        # Kullanıcı adı
        tk.Label(inner_frame, text="👤 Kullanıcı Adı", font=('Arial', 12, 'bold'), 
                bg='white', fg='#333').pack(anchor='w', pady=(0, 5))
        
        self.username_entry = tk.Entry(inner_frame, font=('Arial', 14), relief=tk.FLAT, 
                                      bd=5, bg='#f8f9fa')
        self.username_entry.pack(fill=tk.X, pady=(0, 20), ipady=8)
        self.username_entry.insert(0, "admin")  # Varsayılan
        
        # Şifre
        tk.Label(inner_frame, text="🔒 Şifre", font=('Arial', 12, 'bold'), 
                bg='white', fg='#333').pack(anchor='w', pady=(0, 5))
        
        self.password_entry = tk.Entry(inner_frame, font=('Arial', 14), show='*', 
                                      relief=tk.FLAT, bd=5, bg='#f8f9fa')
        self.password_entry.pack(fill=tk.X, pady=(0, 30), ipady=8)
        self.password_entry.insert(0, "admin123")  # Varsayılan
        
        # Giriş butonu
        login_btn = tk.Button(inner_frame, text="🚀 GİRİŞ YAP", command=self.login,
                             bg='#28a745', fg='white', font=('Arial', 14, 'bold'),
                             relief=tk.FLAT, pady=12, cursor='hand2')
        login_btn.pack(fill=tk.X, pady=(0, 15))
        
        # Yeni kullanıcı butonu
        new_user_btn = tk.Button(inner_frame, text="➕ Yeni Kullanıcı Oluştur", 
                                command=self.show_register_window,
                                bg='#007bff', fg='white', font=('Arial', 12, 'bold'),
                                relief=tk.FLAT, pady=8, cursor='hand2')
        new_user_btn.pack(fill=tk.X, pady=(0, 10))
        
        # Bilgi etiketi
        info_label = tk.Label(inner_frame, 
                             text="Varsayılan: admin / admin123", 
                             font=('Arial', 10), bg='white', fg='#666')
        info_label.pack(pady=(10, 0))
        
        # Enter tuşu ile giriş
        self.login_root.bind('<Return>', lambda e: self.login())
        
        # Focus ayarla
        self.username_entry.focus()
    
    def center_window(self):
        self.login_root.update_idletasks()
        width = self.login_root.winfo_width()
        height = self.login_root.winfo_height()
        x = (self.login_root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.login_root.winfo_screenheight() // 2) - (height // 2)
        self.login_root.geometry(f'{width}x{height}+{x}+{y}')
    
    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username or not password:
            messagebox.showerror("Hata", "Kullanıcı adı ve şifre gereklidir!")
            return
        
        user = self.auth_manager.authenticate(username, password)
        
        if user:
            self.current_user = user
            self.login_root.destroy()
            self.on_success_callback(user)
        else:
            messagebox.showerror("Hata", "Kullanıcı adı veya şifre hatalı!")
            self.password_entry.delete(0, tk.END)
            self.password_entry.focus()
    
    def show_register_window(self):
        register_window = tk.Toplevel(self.login_root)
        register_window.title("Yeni Kullanıcı Oluştur")
        register_window.geometry("400x550")
        register_window.configure(bg='white')
        register_window.resizable(False, False)
        
        # Ana çerçeve
        main_frame = tk.Frame(register_window, bg='white')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        # Başlık
        tk.Label(main_frame, text="👥 YENİ KULLANICI OLUŞTUR", 
                font=('Arial', 16, 'bold'), bg='white', fg='#333').pack(pady=(0, 30))
        
        # Form alanları
        fields = [
            ("👤 Kullanıcı Adı *", "username"),
            ("🔒 Şifre *", "password"),
            ("👨‍💼 Ad Soyad *", "full_name"),
            ("📧 E-posta", "email"),
        ]
        
        entries = {}
        
        for label_text, field_name in fields:
            tk.Label(main_frame, text=label_text, font=('Arial', 11, 'bold'), 
                    bg='white', fg='#333').pack(anchor='w', pady=(10, 5))
            
            if field_name == 'password':
                entry = tk.Entry(main_frame, font=('Arial', 12), show='*', 
                               relief=tk.FLAT, bd=5, bg='#f8f9fa')
            else:
                entry = tk.Entry(main_frame, font=('Arial', 12), 
                               relief=tk.FLAT, bd=5, bg='#f8f9fa')
            
            entry.pack(fill=tk.X, pady=(0, 5), ipady=6)
            entries[field_name] = entry
        
        # Rol seçimi
        tk.Label(main_frame, text="🎭 Rol *", font=('Arial', 11, 'bold'), 
                bg='white', fg='#333').pack(anchor='w', pady=(10, 5))
        
        role_var = tk.StringVar(value="user")
        role_frame = tk.Frame(main_frame, bg='white')
        role_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Radiobutton(role_frame, text="👤 Kullanıcı", variable=role_var, value="user",
                      bg='white', font=('Arial', 11)).pack(side=tk.LEFT, padx=(0, 20))
        tk.Radiobutton(role_frame, text="👨‍💼 Yönetici", variable=role_var, value="admin",
                      bg='white', font=('Arial', 11)).pack(side=tk.LEFT)
        
        def create_user():
            username = entries['username'].get().strip()
            password = entries['password'].get().strip()
            full_name = entries['full_name'].get().strip()
            email = entries['email'].get().strip()
            role = role_var.get()
            
            if not all([username, password, full_name]):
                messagebox.showerror("Hata", "Zorunlu alanları doldurun!")
                return
            
            if len(password) < 6:
                messagebox.showerror("Hata", "Şifre en az 6 karakter olmalıdır!")
                return
            
            success = self.auth_manager.create_user(username, password, role, full_name, email)
            
            if success:
                messagebox.showinfo("Başarılı", "Kullanıcı başarıyla oluşturuldu!")
                register_window.destroy()
            else:
                messagebox.showerror("Hata", "Bu kullanıcı adı zaten kullanımda!")
        
        # Butonlar
        btn_frame = tk.Frame(main_frame, bg='white')
        btn_frame.pack(fill=tk.X, pady=(20, 0))
        
        tk.Button(btn_frame, text="💾 Oluştur", command=create_user,
                 bg='#28a745', fg='white', font=('Arial', 12, 'bold'),
                 relief=tk.FLAT, pady=8, cursor='hand2').pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Button(btn_frame, text="❌ İptal", command=register_window.destroy,
                 bg='#dc3545', fg='white', font=('Arial', 12, 'bold'),
                 relief=tk.FLAT, pady=8, cursor='hand2').pack(side=tk.RIGHT)
    
    def run(self):
        self.login_root.mainloop()