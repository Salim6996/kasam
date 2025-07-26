import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime
import sqlite3
from database import Database

class MarketApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Market Yönetim Sistemi")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f0f0')
        
        # İkon ayarla - Bu satırı ekleyin
        try:
            self.root.iconphoto(True, tk.PhotoImage(file="ikon.png"))
        except:
            pass  # İkon dosyası bulunamazsa hata vermez
        
        # Veritabanı bağlantısı
        self.db = Database()
        # Ana stil ayarları
        self.setup_styles()
        # Ana pencere oluştur
        self.create_main_window()
        # İlk sayfa olarak ürün listesini göster
        self.show_products()
    
    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        # Özel stiller
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'), background='#f0f0f0')
        style.configure('Header.TLabel', font=('Arial', 12, 'bold'), background='#f0f0f0')
        style.configure('Custom.Treeview', font=('Arial', 10))
        style.configure('Custom.Treeview.Heading', font=('Arial', 10, 'bold'))
    
    def create_main_window(self):
        # Ana çerçeve
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Başlık
        title_label = ttk.Label(main_frame, text="🏪 MARKET YÖNETİM SİSTEMİ", style='Title.TLabel')
        title_label.pack(pady=(0, 20))
        
        # Menü çerçevesi
        menu_frame = tk.Frame(main_frame, bg='#e0e0e0', relief=tk.RAISED, bd=2)
        menu_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Menü butonları
        buttons = [
            ("📦 Ürünler", self.show_products, '#4CAF50'),
            ("💰 Satış", self.show_sales, '#2196F3'),
            ("📊 Stok", self.show_stock, '#FF9800'),
            ("📈 Raporlar", self.show_reports, '#9C27B0'),
            ("⚙️ Ayarlar", self.show_settings, '#607D8B')
        ]
        
        for text, command, color in buttons:
            btn = tk.Button(menu_frame, text=text, command=command, 
                          font=('Arial', 12, 'bold'), bg=color, fg='white',
                          padx=20, pady=10, relief=tk.FLAT, cursor='hand2')
            btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        # İçerik çerçevesi
        self.content_frame = tk.Frame(main_frame, bg='white', relief=tk.SUNKEN, bd=2)
        self.content_frame.pack(fill=tk.BOTH, expand=True)
    
    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def show_products(self):
        self.clear_content()
        
        # Ürünler sayfası başlığı
        title_frame = tk.Frame(self.content_frame, bg='white')
        title_frame.pack(fill=tk.X, padx=20, pady=10)
        
        ttk.Label(title_frame, text="📦 ÜRÜN YÖNETİMİ", style='Title.TLabel').pack(side=tk.LEFT)
        
        # Butonlar çerçevesi
        btn_frame = tk.Frame(title_frame, bg='white')
        btn_frame.pack(side=tk.RIGHT)
        
        tk.Button(btn_frame, text="➕ Yeni Ürün", command=self.add_product_window,
                 bg='#4CAF50', fg='white', font=('Arial', 10, 'bold'), padx=15).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="✏️ Düzenle", command=self.edit_product,
                 bg='#2196F3', fg='white', font=('Arial', 10, 'bold'), padx=15).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="🗑️ Sil", command=self.delete_product,
                 bg='#f44336', fg='white', font=('Arial', 10, 'bold'), padx=15).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="🔄 Yenile", command=self.refresh_products,
                 bg='#FF9800', fg='white', font=('Arial', 10, 'bold'), padx=15).pack(side=tk.LEFT, padx=5)
        
        # Arama çerçevesi
        search_frame = tk.Frame(self.content_frame, bg='white')
        search_frame.pack(fill=tk.X, padx=20, pady=(0, 10))
        
        ttk.Label(search_frame, text="🔍 Ara:", font=('Arial', 10)).pack(side=tk.LEFT, padx=(0, 5))
        self.search_entry = tk.Entry(search_frame, font=('Arial', 10), width=30)
        self.search_entry.pack(side=tk.LEFT, padx=(0, 10))
        self.search_entry.bind('<KeyRelease>', self.search_products)
        
        tk.Button(search_frame, text="Temizle", command=self.clear_search,
                 bg='#9E9E9E', fg='white', font=('Arial', 9)).pack(side=tk.LEFT)
        
        # Ürün listesi
        list_frame = tk.Frame(self.content_frame, bg='white')
        list_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        # Treeview oluştur
        columns = ('ID', 'Ürün Adı', 'Barkod', 'Fiyat', 'Stok', 'Kategori')
        self.products_tree = ttk.Treeview(list_frame, columns=columns, show='headings', style='Custom.Treeview')
        
        # Sütun başlıkları
        for col in columns:
            self.products_tree.heading(col, text=col)
            self.products_tree.column(col, width=120, anchor='center')
        
        # Kaydırma çubukları
        v_scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.products_tree.yview)
        h_scrollbar = ttk.Scrollbar(list_frame, orient=tk.HORIZONTAL, command=self.products_tree.xview)
        self.products_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Yerleştir
        self.products_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Çift tıklama olayı
        self.products_tree.bind('<Double-1>', lambda e: self.edit_product())
        
        # Ürünleri yükle
        self.refresh_products()
    
    def refresh_products(self):
        # Mevcut verileri temizle
        for item in self.products_tree.get_children():
            self.products_tree.delete(item)
        
        # Veritabanından ürünleri getir
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, name, barcode, price, stock, category 
            FROM products 
            ORDER BY name
        ''')
        products = cursor.fetchall()
        conn.close()
        
        # Ürünleri ekle
        for product in products:
            id, name, barcode, price, stock, category = product
            # Stok durumuna göre renk
            tags = []
            if stock <= 5:
                tags = ['low_stock']
            elif stock <= 0:
                tags = ['no_stock']
            
            self.products_tree.insert('', tk.END, values=(
                id, name, barcode or 'N/A', f'{price:.2f} ₺', stock, category or 'N/A'
            ), tags=tags)
        
        # Renk etiketleri
        self.products_tree.tag_configure('low_stock', background='#ffeb3b')
        self.products_tree.tag_configure('no_stock', background='#ffcdd2')
    
    def search_products(self, event=None):
        search_term = self.search_entry.get().lower()
        
        # Mevcut verileri temizle
        for item in self.products_tree.get_children():
            self.products_tree.delete(item)
        
        # Veritabanından ara
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, name, barcode, price, stock, category 
            FROM products 
            WHERE LOWER(name) LIKE ? OR LOWER(barcode) LIKE ? OR LOWER(category) LIKE ?
            ORDER BY name
        ''', (f'%{search_term}%', f'%{search_term}%', f'%{search_term}%'))
        products = cursor.fetchall()
        conn.close()
        
        # Sonuçları ekle
        for product in products:
            id, name, barcode, price, stock, category = product
            tags = []
            if stock <= 5:
                tags = ['low_stock']
            elif stock <= 0:
                tags = ['no_stock']
            
            self.products_tree.insert('', tk.END, values=(
                id, name, barcode or 'N/A', f'{price:.2f} ₺', stock, category or 'N/A'
            ), tags=tags)
        
        self.products_tree.tag_configure('low_stock', background='#ffeb3b')
        self.products_tree.tag_configure('no_stock', background='#ffcdd2')
    
    def clear_search(self):
        self.search_entry.delete(0, tk.END)
        self.refresh_products()
    
    def add_product_window(self):
        # Yeni pencere oluştur
        add_window = tk.Toplevel(self.root)
        add_window.title("Yeni Ürün Ekle")
        add_window.geometry("400x500")
        add_window.configure(bg='white')
        add_window.resizable(False, False)
        
        # Ana çerçeve
        main_frame = tk.Frame(add_window, bg='white', padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Başlık
        ttk.Label(main_frame, text="➕ YENİ ÜRÜN EKLE", style='Title.TLabel').pack(pady=(0, 20))
        
        # Form alanları
        fields = [
            ("Ürün Adı *", "name"),
            ("Barkod", "barcode"),
            ("Fiyat *", "price"),
            ("Stok Miktarı *", "stock"),
            ("Kategori", "category"),
            ("Açıklama", "description")
        ]
        
        entries = {}
        
        for label_text, field_name in fields:
            frame = tk.Frame(main_frame, bg='white')
            frame.pack(fill=tk.X, pady=5)
            
            label = tk.Label(frame, text=label_text, font=('Arial', 10, 'bold'), 
                           bg='white', width=15, anchor='w')
            label.pack(side=tk.LEFT)
            
            if field_name == 'description':
                entry = tk.Text(frame, height=3, width=25, font=('Arial', 10))
            else:
                entry = tk.Entry(frame, font=('Arial', 10), width=25)
            entry.pack(side=tk.RIGHT, fill=tk.X, expand=True)
            entries[field_name] = entry
        
        # Butonlar
        btn_frame = tk.Frame(main_frame, bg='white')
        btn_frame.pack(fill=tk.X, pady=20)
        
        def save_product():
            try:
                name = entries['name'].get().strip()
                barcode = entries['barcode'].get().strip()
                price = float(entries['price'].get())
                stock = int(entries['stock'].get())
                category = entries['category'].get().strip()
                description = entries['description'].get('1.0', tk.END).strip()
                
                if not name:
                    messagebox.showerror("Hata", "Ürün adı gereklidir!")
                    return
                
                if price < 0:
                    messagebox.showerror("Hata", "Fiyat negatif olamaz!")
                    return
                
                if stock < 0:
                    messagebox.showerror("Hata", "Stok negatif olamaz!")
                    return
                
                # Veritabanına ekle
                conn = self.db.get_connection()
                cursor = conn.cursor()
                
                cursor.execute('''
                    INSERT INTO products (name, barcode, price, stock, category, description)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (name, barcode or None, price, stock, category or None, description or None))
                
                # Stok hareketi kaydet
                product_id = cursor.lastrowid
                cursor.execute('''
                    INSERT INTO stock_movements (product_id, movement_type, quantity, reason)
                    VALUES (?, 'IN', ?, 'İlk stok girişi')
                ''', (product_id, stock))
                
                conn.commit()
                conn.close()
                
                messagebox.showinfo("Başarılı", "Ürün başarıyla eklendi!")
                add_window.destroy()
                self.refresh_products()
                
            except ValueError:
                messagebox.showerror("Hata", "Fiyat ve stok sayısal değer olmalıdır!")
            except sqlite3.IntegrityError:
                messagebox.showerror("Hata", "Bu barkod zaten kullanımda!")
            except Exception as e:
                messagebox.showerror("Hata", f"Bir hata oluştu: {str(e)}")
        
        tk.Button(btn_frame, text="💾 Kaydet", command=save_product,
                 bg='#4CAF50', fg='white', font=('Arial', 12, 'bold'), padx=30).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="❌ İptal", command=add_window.destroy,
                 bg='#f44336', fg='white', font=('Arial', 12, 'bold'), padx=30).pack(side=tk.RIGHT, padx=10)
    
    def edit_product(self):
        selected = self.products_tree.selection()
        if not selected:
            messagebox.showwarning("Uyarı", "Lütfen düzenlenecek ürünü seçin!")
            return
        
        item = self.products_tree.item(selected[0])
        product_id = item['values'][0]
        
        # Ürün bilgilerini getir
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
        product = cursor.fetchone()
        conn.close()
        
        if not product:
            messagebox.showerror("Hata", "Ürün bulunamadı!")
            return
        
        # Düzenleme penceresi
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Ürün Düzenle")
        edit_window.geometry("400x500")
        edit_window.configure(bg='white')
        edit_window.resizable(False, False)
        
        main_frame = tk.Frame(edit_window, bg='white', padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text="✏️ ÜRÜN DÜZENLE", style='Title.TLabel').pack(pady=(0, 20))
        
        # Form alanları
        fields = [
            ("Ürün Adı *", "name", product[1]),
            ("Barkod", "barcode", product[2] or ""),
            ("Fiyat *", "price", str(product[3])),
            ("Stok Miktarı *", "stock", str(product[4])),
            ("Kategori", "category", product[5] or ""),
            ("Açıklama", "description", product[6] or "")
        ]
        
        entries = {}
        
        for label_text, field_name, default_value in fields:
            frame = tk.Frame(main_frame, bg='white')
            frame.pack(fill=tk.X, pady=5)
            
            label = tk.Label(frame, text=label_text, font=('Arial', 10, 'bold'), 
                           bg='white', width=15, anchor='w')
            label.pack(side=tk.LEFT)
            
            if field_name == 'description':
                entry = tk.Text(frame, height=3, width=25, font=('Arial', 10))
                entry.insert('1.0', default_value)
            else:
                entry = tk.Entry(frame, font=('Arial', 10), width=25)
                entry.insert(0, default_value)
            entry.pack(side=tk.RIGHT, fill=tk.X, expand=True)
            entries[field_name] = entry
        
        # Butonlar
        btn_frame = tk.Frame(main_frame, bg='white')
        btn_frame.pack(fill=tk.X, pady=20)
        
        def update_product():
            try:
                name = entries['name'].get().strip()
                barcode = entries['barcode'].get().strip()
                price = float(entries['price'].get())
                stock = int(entries['stock'].get())
                category = entries['category'].get().strip()
                description = entries['description'].get('1.0', tk.END).strip()
                
                if not name:
                    messagebox.showerror("Hata", "Ürün adı gereklidir!")
                    return
                
                if price < 0:
                    messagebox.showerror("Hata", "Fiyat negatif olamaz!")
                    return
                
                if stock < 0:
                    messagebox.showerror("Hata", "Stok negatif olamaz!")
                    return
                
                # Stok değişikliği kontrol et
                old_stock = product[4]
                stock_diff = stock - old_stock
                
                conn = self.db.get_connection()
                cursor = conn.cursor()
                
                cursor.execute('''
                    UPDATE products 
                    SET name=?, barcode=?, price=?, stock=?, category=?, description=?, updated_date=CURRENT_TIMESTAMP
                    WHERE id=?
                ''', (name, barcode or None, price, stock, category or None, description or None, product_id))
                
                # Stok değişikliği varsa hareket kaydet
                if stock_diff != 0:
                    movement_type = 'IN' if stock_diff > 0 else 'OUT'
                    cursor.execute('''
                        INSERT INTO stock_movements (product_id, movement_type, quantity, reason)
                        VALUES (?, ?, ?, 'Manuel düzenleme')
                    ''', (product_id, movement_type, abs(stock_diff)))
                
                conn.commit()
                conn.close()
                
                messagebox.showinfo("Başarılı", "Ürün başarıyla güncellendi!")
                edit_window.destroy()
                self.refresh_products()
                
            except ValueError:
                messagebox.showerror("Hata", "Fiyat ve stok sayısal değer olmalıdır!")
            except Exception as e:
                messagebox.showerror("Hata", f"Bir hata oluştu: {str(e)}")
        
        tk.Button(btn_frame, text="💾 Güncelle", command=update_product,
                 bg='#2196F3', fg='white', font=('Arial', 12, 'bold'), padx=30).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="❌ İptal", command=edit_window.destroy,
                 bg='#f44336', fg='white', font=('Arial', 12, 'bold'), padx=30).pack(side=tk.RIGHT, padx=10)
    
    def delete_product(self):
        selected = self.products_tree.selection()
        if not selected:
            messagebox.showwarning("Uyarı", "Lütfen silinecek ürünü seçin!")
            return
        
        item = self.products_tree.item(selected[0])
        product_id = item['values'][0]
        product_name = item['values'][1]
        
        result = messagebox.askyesno("Onay", f"'{product_name}' ürünü silmek istediğinizden emin misiniz?")
        if result:
            try:
                conn = self.db.get_connection()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
                conn.commit()
                conn.close()
                
                messagebox.showinfo("Başarılı", "Ürün başarıyla silindi!")
                self.refresh_products()
                
            except Exception as e:
                messagebox.showerror("Hata", f"Bir hata oluştu: {str(e)}")
    
    def show_sales(self):
        self.clear_content()
        
        # Satış sayfası
        title_frame = tk.Frame(self.content_frame, bg='white')
        title_frame.pack(fill=tk.X, padx=20, pady=10)
        
        ttk.Label(title_frame, text="💰 SATIŞ İŞLEMLERİ", style='Title.TLabel').pack(side=tk.LEFT)
        
        # Ana çerçeve
        main_frame = tk.Frame(self.content_frame, bg='white')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Sol panel - Satış yapma
        left_frame = tk.LabelFrame(main_frame, text="🛒 Yeni Satış", font=('Arial', 12, 'bold'),
                                  bg='white', padx=10, pady=10)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Ürün arama
        search_frame = tk.Frame(left_frame, bg='white')
        search_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(search_frame, text="Ürün Ara:", font=('Arial', 10, 'bold'), bg='white').pack(anchor='w')
        self.sale_search_entry = tk.Entry(search_frame, font=('Arial', 12), width=30)
        self.sale_search_entry.pack(fill=tk.X, pady=2)
        self.sale_search_entry.bind('<KeyRelease>', self.search_products_for_sale)
        
        # Ürün listesi (satış için)
        self.sale_products_listbox = tk.Listbox(left_frame, font=('Arial', 10), height=8)
        self.sale_products_listbox.pack(fill=tk.X, pady=5)
        self.sale_products_listbox.bind('<Double-Button-1>', self.add_to_cart)
        
        # Miktar girişi
        qty_frame = tk.Frame(left_frame, bg='white')
        qty_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(qty_frame, text="Miktar:", font=('Arial', 10, 'bold'), bg='white').pack(side=tk.LEFT)
        self.quantity_entry = tk.Entry(qty_frame, font=('Arial', 12), width=10)
        self.quantity_entry.pack(side=tk.LEFT, padx=5)
        self.quantity_entry.insert(0, "1")
        
        tk.Button(qty_frame, text="🛒 Sepete Ekle", command=self.add_to_cart,
                 bg='#4CAF50', fg='white', font=('Arial', 10, 'bold')).pack(side=tk.RIGHT)
        
        # Sağ panel - Sepet
        right_frame = tk.LabelFrame(main_frame, text="🛍️ Sepet", font=('Arial', 12, 'bold'),
                                   bg='white', padx=10, pady=10)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Sepet listesi
        cart_columns = ('Ürün', 'Adet', 'Fiyat', 'Toplam')
        self.cart_tree = ttk.Treeview(right_frame, columns=cart_columns, show='headings', height=10)
        
        for col in cart_columns:
            self.cart_tree.heading(col, text=col)
            self.cart_tree.column(col, width=100, anchor='center')
        
        self.cart_tree.pack(fill=tk.BOTH, expand=True)
        
        # Sepet butonları
        cart_btn_frame = tk.Frame(right_frame, bg='white')
        cart_btn_frame.pack(fill=tk.X, pady=5)
        
        tk.Button(cart_btn_frame, text="🗑️ Seçili Sil", command=self.remove_from_cart,
                 bg='#f44336', fg='white', font=('Arial', 9)).pack(side=tk.LEFT, padx=5)
        tk.Button(cart_btn_frame, text="🧹 Sepeti Temizle", command=self.clear_cart,
                 bg='#FF9800', fg='white', font=('Arial', 9)).pack(side=tk.LEFT, padx=5)
        
        # Toplam ve satış
        total_frame = tk.Frame(right_frame, bg='white')
        total_frame.pack(fill=tk.X, pady=10)
        
        self.total_label = tk.Label(total_frame, text="TOPLAM: 0.00 ₺", 
                                   font=('Arial', 16, 'bold'), bg='white', fg='#4CAF50')
        self.total_label.pack()
        
        tk.Button(total_frame, text="💳 SATIŞ TAMAMLA", command=self.complete_sale,
                 bg='#2196F3', fg='white', font=('Arial', 14, 'bold'), pady=10).pack(fill=tk.X, pady=5)
        
        # Sepet verilerini tutacak liste
        self.cart_items = []
        
        # İlk ürün listesini yükle
        self.load_products_for_sale()
    
    def load_products_for_sale(self):
        self.sale_products_listbox.delete(0, tk.END)
        
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, name, price, stock 
            FROM products 
            WHERE stock > 0
            ORDER BY name
        ''')
        products = cursor.fetchall()
        conn.close()
        
        for product in products:
            id, name, price, stock = product
            display_text = f"{name} - {price:.2f}₺ (Stok: {stock})"
            self.sale_products_listbox.insert(tk.END, display_text)
            
        # Ürün verilerini sakla
        self.sale_products_data = products
    
    def search_products_for_sale(self, event=None):
        search_term = self.sale_search_entry.get().lower()
        self.sale_products_listbox.delete(0, tk.END)
        
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, name, price, stock 
            FROM products 
            WHERE (LOWER(name) LIKE ? OR LOWER(barcode) LIKE ?) AND stock > 0
            ORDER BY name
        ''', (f'%{search_term}%', f'%{search_term}%'))
        products = cursor.fetchall()
        conn.close()
        
        for product in products:
            id, name, price, stock = product
            display_text = f"{name} - {price:.2f}₺ (Stok: {stock})"
            self.sale_products_listbox.insert(tk.END, display_text)
            
        self.sale_products_data = products
    
    def add_to_cart(self, event=None):
        selection = self.sale_products_listbox.curselection()
        if not selection:
            messagebox.showwarning("Uyarı", "Lütfen bir ürün seçin!")
            return
        
        try:
            quantity = int(self.quantity_entry.get())
            if quantity <= 0:
                messagebox.showerror("Hata", "Miktar 0'dan büyük olmalıdır!")
                return
        except ValueError:
            messagebox.showerror("Hata", "Geçerli bir miktar girin!")
            return
        
        selected_index = selection[0]
        product = self.sale_products_data[selected_index]
        id, name, price, stock = product
        
        if quantity > stock:
            messagebox.showerror("Hata", f"Yetersiz stok! Mevcut: {stock}")
            return
        
        # Sepette zaten var mı kontrol et
        for i, item in enumerate(self.cart_items):
            if item['id'] == id:
                new_quantity = item['quantity'] + quantity
                if new_quantity > stock:
                    messagebox.showerror("Hata", f"Toplam miktar stoğu aşıyor! Mevcut: {stock}")
                    return
                self.cart_items[i]['quantity'] = new_quantity
                self.cart_items[i]['total'] = new_quantity * price
                break
        else:
            # Yeni ürün ekle
            self.cart_items.append({
                'id': id,
                'name': name,
                'price': price,
                'quantity': quantity,
                'total': quantity * price
            })
        
        self.update_cart_display()
        self.quantity_entry.delete(0, tk.END)
        self.quantity_entry.insert(0, "1")
    
    def update_cart_display(self):
        # Sepeti temizle
        for item in self.cart_tree.get_children():
            self.cart_tree.delete(item)
        
        # Yeni verileri ekle
        total_amount = 0
        for item in self.cart_items:
            self.cart_tree.insert('', tk.END, values=(
                item['name'], item['quantity'], f"{item['price']:.2f}₺", f"{item['total']:.2f}₺"
            ))
            total_amount += item['total']
        
        self.total_label.config(text=f"TOPLAM: {total_amount:.2f} ₺")
    
    def remove_from_cart(self):
        selected = self.cart_tree.selection()
        if not selected:
            messagebox.showwarning("Uyarı", "Silinecek ürünü seçin!")
            return
        
        # Seçili öğenin indeksini bul
        item_index = self.cart_tree.index(selected[0])
        del self.cart_items[item_index]
        self.update_cart_display()
    
    def clear_cart(self):
        self.cart_items = []
        self.update_cart_display()
    
    def complete_sale(self):
        if not self.cart_items:
            messagebox.showwarning("Uyarı", "Sepet boş!")
            return
        
        total_amount = sum(item['total'] for item in self.cart_items)
        
        result = messagebox.askyesno("Satış Onayı", 
                                   f"Toplam tutar: {total_amount:.2f} ₺\n\nSatışı tamamlamak istiyor musunuz?")
        
        if result:
            try:
                conn = self.db.get_connection()
                cursor = conn.cursor()
                
                # Her ürün için satış kaydı oluştur
                for item in self.cart_items:
                    # Satış kaydı
                    cursor.execute('''
                        INSERT INTO sales (product_id, quantity, unit_price, total_price)
                        VALUES (?, ?, ?, ?)
                    ''', (item['id'], item['quantity'], item['price'], item['total']))
                    
                    # Stok güncelle
                    cursor.execute('''
                        UPDATE products SET stock = stock - ? WHERE id = ?
                    ''', (item['quantity'], item['id']))
                    
                    # Stok hareketi kaydet
                    cursor.execute('''
                        INSERT INTO stock_movements (product_id, movement_type, quantity, reason)
                        VALUES (?, 'OUT', ?, 'Satış')
                    ''', (item['id'], item['quantity']))
                
                conn.commit()
                conn.close()
                
                messagebox.showinfo("Başarılı", f"Satış tamamlandı!\nToplam: {total_amount:.2f} ₺")
                
                # Sepeti temizle ve ürün listesini güncelle
                self.clear_cart()
                self.load_products_for_sale()
                
            except Exception as e:
                messagebox.showerror("Hata", f"Satış sırasında hata oluştu: {str(e)}")
    
    def show_stock(self):
        self.clear_content()
        
        # Stok sayfası başlığı
        title_frame = tk.Frame(self.content_frame, bg='white')
        title_frame.pack(fill=tk.X, padx=20, pady=10)
        
        ttk.Label(title_frame, text="📊 STOK YÖNETİMİ", style='Title.TLabel').pack(side=tk.LEFT)
        
        # Butonlar
        btn_frame = tk.Frame(title_frame, bg='white')
        btn_frame.pack(side=tk.RIGHT)
        
        tk.Button(btn_frame, text="📦 Stok Ekle", command=self.add_stock_window,
                 bg='#4CAF50', fg='white', font=('Arial', 10, 'bold'), padx=15).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="📤 Stok Çıkar", command=self.remove_stock_window,
                 bg='#FF9800', fg='white', font=('Arial', 10, 'bold'), padx=15).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="⚠️ Düşük Stok", command=self.show_low_stock,
                 bg='#f44336', fg='white', font=('Arial', 10, 'bold'), padx=15).pack(side=tk.LEFT, padx=5)
        
        # Ana içerik çerçevesi
        content_frame = tk.Frame(self.content_frame, bg='white')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Sol panel - Stok listesi
        left_frame = tk.LabelFrame(content_frame, text="📋 Stok Durumu", font=('Arial', 12, 'bold'),
                                  bg='white', padx=10, pady=10)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Stok listesi
        stock_columns = ('ID', 'Ürün Adı', 'Kategori', 'Stok', 'Fiyat', 'Değer')
        self.stock_tree = ttk.Treeview(left_frame, columns=stock_columns, show='headings')
        
        for col in stock_columns:
            self.stock_tree.heading(col, text=col)
            self.stock_tree.column(col, width=100, anchor='center')
        
        # Kaydırma çubuğu
        stock_scrollbar = ttk.Scrollbar(left_frame, orient=tk.VERTICAL, command=self.stock_tree.yview)
        self.stock_tree.configure(yscrollcommand=stock_scrollbar.set)
        
        self.stock_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        stock_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Sağ panel - Stok hareketleri
        right_frame = tk.LabelFrame(content_frame, text="📈 Son Stok Hareketleri", 
                                   font=('Arial', 12, 'bold'), bg='white', padx=10, pady=10)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Stok hareketleri listesi
        movement_columns = ('Tarih', 'Ürün', 'İşlem', 'Miktar', 'Sebep')
        self.movements_tree = ttk.Treeview(right_frame, columns=movement_columns, show='headings')
        
        for col in movement_columns:
            self.movements_tree.heading(col, text=col)
            self.movements_tree.column(col, width=90, anchor='center')
        
        movements_scrollbar = ttk.Scrollbar(right_frame, orient=tk.VERTICAL, command=self.movements_tree.yview)
        self.movements_tree.configure(yscrollcommand=movements_scrollbar.set)
        
        self.movements_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        movements_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Verileri yükle
        self.refresh_stock_data()
    
    def refresh_stock_data(self):
        # Stok listesini güncelle
        for item in self.stock_tree.get_children():
            self.stock_tree.delete(item)
        
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, name, category, stock, price, (stock * price) as value
            FROM products
            ORDER BY stock ASC
        ''')
        
        products = cursor.fetchall()
        total_value = 0
        
        for product in products:
            id, name, category, stock, price, value = product
            total_value += value
            
            # Stok durumuna göre renk
            tags = []
            if stock <= 0:
                tags = ['no_stock']
            elif stock <= 5:
                tags = ['low_stock']
            
            self.stock_tree.insert('', tk.END, values=(
                id, name, category or 'N/A', stock, f'{price:.2f}₺', f'{value:.2f}₺'
            ), tags=tags)
        
        self.stock_tree.tag_configure('low_stock', background='#ffeb3b')
        self.stock_tree.tag_configure('no_stock', background='#ffcdd2')
        
        # Stok hareketlerini güncelle
        for item in self.movements_tree.get_children():
            self.movements_tree.delete(item)
        
        cursor.execute('''
            SELECT sm.movement_date, p.name, sm.movement_type, sm.quantity, sm.reason
            FROM stock_movements sm
            JOIN products p ON sm.product_id = p.id
            ORDER BY sm.movement_date DESC
            LIMIT 20
        ''')
        
        movements = cursor.fetchall()
        for movement in movements:
            date, name, type, quantity, reason = movement
            type_text = "GİRİŞ" if type == "IN" else "ÇIKIŞ"
            date_text = date[:16] if date else ""
            
            self.movements_tree.insert('', tk.END, values=(
                date_text, name[:15], type_text, quantity, reason[:15]
            ))
        
        conn.close()
    
    def add_stock_window(self):
        # Stok ekleme penceresi
        stock_window = tk.Toplevel(self.root)
        stock_window.title("Stok Ekle")
        stock_window.geometry("400x300")
        stock_window.configure(bg='white')
        
        main_frame = tk.Frame(stock_window, bg='white', padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text="📦 STOK EKLE", style='Title.TLabel').pack(pady=(0, 20))
        
        # Ürün seçimi
        tk.Label(main_frame, text="Ürün:", font=('Arial', 10, 'bold'), bg='white').pack(anchor='w')
        
        product_var = tk.StringVar()
        product_combo = ttk.Combobox(main_frame, textvariable=product_var, width=50, state='readonly')
        
        # Ürünleri yükle
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM products ORDER BY name")
        products = cursor.fetchall()
        conn.close()
        
        product_combo['values'] = [f"{p[0]} - {p[1]}" for p in products]
        product_combo.pack(fill=tk.X, pady=5)
        
        # Miktar
        tk.Label(main_frame, text="Eklenecek Miktar:", font=('Arial', 10, 'bold'), bg='white').pack(anchor='w', pady=(10, 0))
        quantity_entry = tk.Entry(main_frame, font=('Arial', 12))
        quantity_entry.pack(fill=tk.X, pady=5)
        
        # Sebep
        tk.Label(main_frame, text="Sebep:", font=('Arial', 10, 'bold'), bg='white').pack(anchor='w', pady=(10, 0))
        reason_entry = tk.Entry(main_frame, font=('Arial', 12))
        reason_entry.pack(fill=tk.X, pady=5)
        reason_entry.insert(0, "Stok ekleme")
        
        def save_stock():
            if not product_var.get():
                messagebox.showerror("Hata", "Lütfen ürün seçin!")
                return
            
            try:
                product_id = int(product_var.get().split(' - ')[0])
                quantity = int(quantity_entry.get())
                reason = reason_entry.get().strip() or "Stok ekleme"
                
                if quantity <= 0:
                    messagebox.showerror("Hata", "Miktar 0'dan büyük olmalıdır!")
                    return
                
                conn = self.db.get_connection()
                cursor = conn.cursor()
                
                # Stok güncelle
                cursor.execute("UPDATE products SET stock = stock + ? WHERE id = ?", (quantity, product_id))
                
                # Hareket kaydet
                cursor.execute('''
                    INSERT INTO stock_movements (product_id, movement_type, quantity, reason)
                    VALUES (?, 'IN', ?, ?)
                ''', (product_id, quantity, reason))
                
                conn.commit()
                conn.close()
                
                messagebox.showinfo("Başarılı", f"{quantity} adet stok eklendi!")
                stock_window.destroy()
                self.refresh_stock_data()
                
            except ValueError:
                messagebox.showerror("Hata", "Geçerli bir miktar girin!")
            except Exception as e:
                messagebox.showerror("Hata", f"Bir hata oluştu: {str(e)}")
        
        # Butonlar
        btn_frame = tk.Frame(main_frame, bg='white')
        btn_frame.pack(fill=tk.X, pady=20)
        
        tk.Button(btn_frame, text="💾 Kaydet", command=save_stock,
                 bg='#4CAF50', fg='white', font=('Arial', 12, 'bold'), padx=30).pack(side=tk.LEFT)
        tk.Button(btn_frame, text="❌ İptal", command=stock_window.destroy,
                 bg='#f44336', fg='white', font=('Arial', 12, 'bold'), padx=30).pack(side=tk.RIGHT)
    
    def remove_stock_window(self):
        # Stok çıkarma penceresi
        stock_window = tk.Toplevel(self.root)
        stock_window.title("Stok Çıkar")
        stock_window.geometry("400x300")
        stock_window.configure(bg='white')
        
        main_frame = tk.Frame(stock_window, bg='white', padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text="📤 STOK ÇIKAR", style='Title.TLabel').pack(pady=(0, 20))
        
        # Ürün seçimi
        tk.Label(main_frame, text="Ürün:", font=('Arial', 10, 'bold'), bg='white').pack(anchor='w')
        
        product_var = tk.StringVar()
        product_combo = ttk.Combobox(main_frame, textvariable=product_var, width=50, state='readonly')
        
        # Stoklu ürünleri yükle
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, stock FROM products WHERE stock > 0 ORDER BY name")
        products = cursor.fetchall()
        conn.close()
        
        product_combo['values'] = [f"{p[0]} - {p[1]} (Stok: {p[2]})" for p in products]
        product_combo.pack(fill=tk.X, pady=5)
        
        # Miktar
        tk.Label(main_frame, text="Çıkarılacak Miktar:", font=('Arial', 10, 'bold'), bg='white').pack(anchor='w', pady=(10, 0))
        quantity_entry = tk.Entry(main_frame, font=('Arial', 12))
        quantity_entry.pack(fill=tk.X, pady=5)
        
        # Sebep
        tk.Label(main_frame, text="Sebep:", font=('Arial', 10, 'bold'), bg='white').pack(anchor='w', pady=(10, 0))
        reason_entry = tk.Entry(main_frame, font=('Arial', 12))
        reason_entry.pack(fill=tk.X, pady=5)
        reason_entry.insert(0, "Stok çıkarma")
        
        def remove_stock():
            if not product_var.get():
                messagebox.showerror("Hata", "Lütfen ürün seçin!")
                return
            
            try:
                product_info = product_var.get()
                product_id = int(product_info.split(' - ')[0])
                current_stock = int(product_info.split('Stok: ')[1].split(')')[0])
                quantity = int(quantity_entry.get())
                reason = reason_entry.get().strip() or "Stok çıkarma"
                
                if quantity <= 0:
                    messagebox.showerror("Hata", "Miktar 0'dan büyük olmalıdır!")
                    return
                
                if quantity > current_stock:
                    messagebox.showerror("Hata", f"Yetersiz stok! Mevcut: {current_stock}")
                    return
                
                conn = self.db.get_connection()
                cursor = conn.cursor()
                
                # Stok güncelle
                cursor.execute("UPDATE products SET stock = stock - ? WHERE id = ?", (quantity, product_id))
                
                # Hareket kaydet
                cursor.execute('''
                    INSERT INTO stock_movements (product_id, movement_type, quantity, reason)
                    VALUES (?, 'OUT', ?, ?)
                ''', (product_id, quantity, reason))
                
                conn.commit()
                conn.close()
                
                messagebox.showinfo("Başarılı", f"{quantity} adet stok çıkarıldı!")
                stock_window.destroy()
                self.refresh_stock_data()
                
            except ValueError:
                messagebox.showerror("Hata", "Geçerli bir miktar girin!")
            except Exception as e:
                messagebox.showerror("Hata", f"Bir hata oluştu: {str(e)}")
        
        # Butonlar
        btn_frame = tk.Frame(main_frame, bg='white')
        btn_frame.pack(fill=tk.X, pady=20)
        
        tk.Button(btn_frame, text="💾 Kaydet", command=remove_stock,
                 bg='#FF9800', fg='white', font=('Arial', 12, 'bold'), padx=30).pack(side=tk.LEFT)
        tk.Button(btn_frame, text="❌ İptal", command=stock_window.destroy,
                 bg='#f44336', fg='white', font=('Arial', 12, 'bold'), padx=30).pack(side=tk.RIGHT)
    
    def show_low_stock(self):
        # Düşük stok uyarısı penceresi
        low_stock_window = tk.Toplevel(self.root)
        low_stock_window.title("Düşük Stok Uyarısı")
        low_stock_window.geometry("600x400")
        low_stock_window.configure(bg='white')
        
        main_frame = tk.Frame(low_stock_window, bg='white', padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text="⚠️ DÜŞÜK STOK UYARISI", style='Title.TLabel').pack(pady=(0, 20))
        
        # Eşik değeri girişi
        threshold_frame = tk.Frame(main_frame, bg='white')
        threshold_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(threshold_frame, text="Minimum stok seviyesi:", font=('Arial', 10, 'bold'), bg='white').pack(side=tk.LEFT)
        threshold_entry = tk.Entry(threshold_frame, font=('Arial', 10), width=10)
        threshold_entry.pack(side=tk.LEFT, padx=5)
        threshold_entry.insert(0, "5")
        
        def refresh_low_stock():
            try:
                threshold = int(threshold_entry.get())
                
                # Listeyi temizle
                for item in low_stock_tree.get_children():
                    low_stock_tree.delete(item)
                
                # Düşük stoklu ürünleri getir
                conn = self.db.get_connection()
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT id, name, category, stock, price
                    FROM products
                    WHERE stock <= ?
                    ORDER BY stock ASC
                ''', (threshold,))
                
                products = cursor.fetchall()
                conn.close()
                
                for product in products:
                    id, name, category, stock, price = product
                    tags = []
                    if stock <= 0:
                        tags = ['no_stock']
                    elif stock <= 2:
                        tags = ['critical_stock']
                    else:
                        tags = ['low_stock']
                    
                    low_stock_tree.insert('', tk.END, values=(
                        id, name, category or 'N/A', stock, f'{price:.2f}₺'
                    ), tags=tags)
                
                low_stock_tree.tag_configure('no_stock', background='#ffcdd2')
                low_stock_tree.tag_configure('critical_stock', background='#ffab91')
                low_stock_tree.tag_configure('low_stock', background='#ffeb3b')
                
            except ValueError:
                messagebox.showerror("Hata", "Geçerli bir eşik değeri girin!")
        
        tk.Button(threshold_frame, text="🔄 Yenile", command=refresh_low_stock,
                 bg='#2196F3', fg='white', font=('Arial', 10)).pack(side=tk.LEFT, padx=5)
        
        # Düşük stok listesi
        low_stock_columns = ('ID', 'Ürün Adı', 'Kategori', 'Stok', 'Fiyat')
        low_stock_tree = ttk.Treeview(main_frame, columns=low_stock_columns, show='headings')
        
        for col in low_stock_columns:
            low_stock_tree.heading(col, text=col)
            low_stock_tree.column(col, width=100, anchor='center')
        
        low_stock_scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=low_stock_tree.yview)
        low_stock_tree.configure(yscrollcommand=low_stock_scrollbar.set)
        
        low_stock_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        low_stock_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # İlk yükleme
        refresh_low_stock()
    
    def show_reports(self):
        self.clear_content()
        
        # Raporlar sayfası başlığı
        title_frame = tk.Frame(self.content_frame, bg='white')
        title_frame.pack(fill=tk.X, padx=20, pady=10)
        
        ttk.Label(title_frame, text="📈 RAPORLAR", style='Title.TLabel').pack(side=tk.LEFT)
        
        # Ana çerçeve
        main_frame = tk.Frame(self.content_frame, bg='white')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Sol panel - Hızlı istatistikler
        left_frame = tk.LabelFrame(main_frame, text="📊 Hızlı İstatistikler", 
                                  font=('Arial', 12, 'bold'), bg='white', padx=15, pady=15)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        # İstatistikleri hesapla
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        # Toplam ürün sayısı
        cursor.execute("SELECT COUNT(*) FROM products")
        total_products = cursor.fetchone()[0]
        
        # Toplam stok değeri
        cursor.execute("SELECT SUM(stock * price) FROM products")
        total_stock_value = cursor.fetchone()[0] or 0
        
        # Bugünkü satışlar
        cursor.execute('''
            SELECT COUNT(*), COALESCE(SUM(total_price), 0)
            FROM sales 
            WHERE DATE(sale_date) = DATE('now')
        ''')
        today_sales_count, today_sales_total = cursor.fetchone()
        
        # Bu ayki satışlar
        cursor.execute('''
            SELECT COUNT(*), COALESCE(SUM(total_price), 0)
            FROM sales 
            WHERE DATE(sale_date) >= DATE('now', 'start of month')
        ''')
        month_sales_count, month_sales_total = cursor.fetchone()
        
        # Düşük stoklu ürün sayısı
        cursor.execute("SELECT COUNT(*) FROM products WHERE stock <= 5")
        low_stock_count = cursor.fetchone()[0]
        
        conn.close()
        
        # İstatistik kartları
        stats = [
            ("📦 Toplam Ürün", str(total_products), '#4CAF50'),
            ("💰 Stok Değeri", f"{total_stock_value:.2f}₺", '#2196F3'),
            ("🛒 Bugünkü Satış", f"{today_sales_count} adet", '#FF9800'),
            ("💵 Bugünkü Ciro", f"{today_sales_total:.2f}₺", '#9C27B0'),
            ("📈 Aylık Satış", f"{month_sales_count} adet", '#00BCD4'),
            ("💸 Aylık Ciro", f"{month_sales_total:.2f}₺", '#4CAF50'),
            ("⚠️ Düşük Stok", f"{low_stock_count} ürün", '#f44336')
        ]
        
        for title, value, color in stats:
            card_frame = tk.Frame(left_frame, bg=color, relief=tk.RAISED, bd=2)
            card_frame.pack(fill=tk.X, pady=5)
            
            tk.Label(card_frame, text=title, font=('Arial', 10, 'bold'), 
                    bg=color, fg='white').pack(pady=2)
            tk.Label(card_frame, text=value, font=('Arial', 12, 'bold'), 
                    bg=color, fg='white').pack(pady=2)
        
        # Sağ panel - Detaylı raporlar
        right_frame = tk.Frame(main_frame, bg='white')
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Rapor butonları
        report_buttons_frame = tk.Frame(right_frame, bg='white')
        report_buttons_frame.pack(fill=tk.X, pady=(0, 10))
        
        report_buttons = [
            ("📅 Günlük Satış Raporu", self.daily_sales_report),
            ("🏆 En Çok Satan Ürünler", self.best_selling_report),
            ("📊 Kategori Raporu", self.category_report),
            ("💰 Gelir Raporu", self.revenue_report)
        ]
        
        for i, (text, command) in enumerate(report_buttons):
            row = i // 2
            col = i % 2
            
            btn = tk.Button(report_buttons_frame, text=text, command=command,
                           bg='#2196F3', fg='white', font=('Arial', 11, 'bold'),
                           padx=20, pady=15, width=25)
            btn.grid(row=row, column=col, padx=5, pady=5, sticky='ew')
        
        report_buttons_frame.grid_columnconfigure(0, weight=1)
        report_buttons_frame.grid_columnconfigure(1, weight=1)
        
        # Rapor görüntüleme alanı
        self.report_display_frame = tk.LabelFrame(right_frame, text="📋 Rapor Sonuçları", 
                                                 font=('Arial', 12, 'bold'), bg='white')
        self.report_display_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        # Varsayılan mesaj
        tk.Label(self.report_display_frame, text="Rapor görmek için yukarıdaki butonları kullanın", 
                font=('Arial', 12), bg='white', fg='gray').pack(expand=True)
    
    def daily_sales_report(self):
        # Rapor alanını temizle
        for widget in self.report_display_frame.winfo_children():
            widget.destroy()
        
        # Tarih seçimi
        date_frame = tk.Frame(self.report_display_frame, bg='white')
        date_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(date_frame, text="Tarih (YYYY-MM-DD):", font=('Arial', 10, 'bold'), bg='white').pack(side=tk.LEFT)
        date_entry = tk.Entry(date_frame, font=('Arial', 10), width=15)
        date_entry.pack(side=tk.LEFT, padx=5)
        date_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))
        
        def show_daily_report():
            date = date_entry.get()
            
            # Mevcut raporu temizle
            for widget in report_tree_frame.winfo_children():
                widget.destroy()
            
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT p.name, SUM(s.quantity) as total_qty, SUM(s.total_price) as total_revenue
                FROM sales s
                JOIN products p ON s.product_id = p.id
                WHERE DATE(s.sale_date) = ?
                GROUP BY p.id, p.name
                ORDER BY total_revenue DESC
            ''', (date,))
            
            sales = cursor.fetchall()
            conn.close()
            
            if not sales:
                tk.Label(report_tree_frame, text=f"{date} tarihinde satış yapılmamış.",
                        font=('Arial', 12), bg='white').pack(expand=True)
                return
            
            # Rapor tablosu
            columns = ('Ürün Adı', 'Satış Adedi', 'Toplam Gelir')
            report_tree = ttk.Treeview(report_tree_frame, columns=columns, show='headings', height=10)
            
            for col in columns:
                report_tree.heading(col, text=col)
                report_tree.column(col, width=150, anchor='center')
            
            total_qty = 0
            total_revenue = 0
            
            for sale in sales:
                name, qty, revenue = sale
                total_qty += qty
                total_revenue += revenue
                report_tree.insert('', tk.END, values=(name, qty, f'{revenue:.2f}₺'))
            
            # Toplam satır
            report_tree.insert('', tk.END, values=('TOPLAM', total_qty, f'{total_revenue:.2f}₺'), tags=['total'])
            report_tree.tag_configure('total', background='#e8f5e8', font=('Arial', 10, 'bold'))
            
            # Kaydırma çubuğu
            scrollbar = ttk.Scrollbar(report_tree_frame, orient=tk.VERTICAL, command=report_tree.yview)
            report_tree.configure(yscrollcommand=scrollbar.set)
            
            report_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        tk.Button(date_frame, text="📊 Rapor Oluştur", command=show_daily_report,
                 bg='#4CAF50', fg='white', font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=5)
        
        # Rapor tablosu için çerçeve
        report_tree_frame = tk.Frame(self.report_display_frame, bg='white')
        report_tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # İlk yükleme
        show_daily_report()
    
    def best_selling_report(self):
        # Rapor alanını temizle
        for widget in self.report_display_frame.winfo_children():
            widget.destroy()
        
        # En çok satan ürünler raporu
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT p.name, SUM(s.quantity) as total_sold, SUM(s.total_price) as total_revenue
            FROM sales s
            JOIN products p ON s.product_id = p.id
            GROUP BY p.id, p.name
            ORDER BY total_sold DESC
            LIMIT 10
        ''')
        
        products = cursor.fetchall()
        conn.close()
        
        if not products:
            tk.Label(self.report_display_frame, text="Henüz satış yapılmamış.",
                    font=('Arial', 12), bg='white').pack(expand=True)
            return
        
        tk.Label(self.report_display_frame, text="🏆 EN ÇOK SATAN 10 ÜRÜN", 
                font=('Arial', 14, 'bold'), bg='white').pack(pady=10)
        
        # Rapor tablosu
        columns = ('Sıra', 'Ürün Adı', 'Toplam Satış', 'Toplam Gelir')
        report_tree = ttk.Treeview(self.report_display_frame, columns=columns, show='headings', height=12)
        
        for col in columns:
            report_tree.heading(col, text=col)
            report_tree.column(col, width=150, anchor='center')
        
        for i, product in enumerate(products, 1):
            name, sold, revenue = product
            report_tree.insert('', tk.END, values=(i, name, sold, f'{revenue:.2f}₺'))
        
        # Kaydırma çubuğu
        scrollbar = ttk.Scrollbar(self.report_display_frame, orient=tk.VERTICAL, command=report_tree.yview)
        report_tree.configure(yscrollcommand=scrollbar.set)
        
        report_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def category_report(self):
        # Rapor alanını temizle
        for widget in self.report_display_frame.winfo_children():
            widget.destroy()
        
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT 
                COALESCE(p.category, 'Kategorisiz') as category,
                COUNT(p.id) as product_count,
                SUM(p.stock) as total_stock,
                AVG(p.price) as avg_price,
                SUM(p.stock * p.price) as stock_value
            FROM products p
            GROUP BY p.category
            ORDER BY product_count DESC
        ''')
        
        categories = cursor.fetchall()
        conn.close()
        
        if not categories:
            tk.Label(self.report_display_frame, text="Henüz ürün eklenmemiş.",
                    font=('Arial', 12), bg='white').pack(expand=True)
            return
        
        tk.Label(self.report_display_frame, text="📊 KATEGORİ RAPORU", 
                font=('Arial', 14, 'bold'), bg='white').pack(pady=10)
        
        # Rapor tablosu
        columns = ('Kategori', 'Ürün Sayısı', 'Toplam Stok', 'Ort. Fiyat', 'Stok Değeri')
        report_tree = ttk.Treeview(self.report_display_frame, columns=columns, show='headings', height=12)
        
        for col in columns:
            report_tree.heading(col, text=col)
            report_tree.column(col, width=120, anchor='center')
        
        total_products = 0
        total_stock = 0
        total_value = 0
        
        for category in categories:
            cat_name, count, stock, avg_price, value = category
            total_products += count
            total_stock += stock or 0
            total_value += value or 0
            
            report_tree.insert('', tk.END, values=(
                cat_name, count, stock or 0, f'{avg_price:.2f}₺', f'{value:.2f}₺'
            ))
        
        # Toplam satır
        report_tree.insert('', tk.END, values=(
            'TOPLAM', total_products, total_stock, '-', f'{total_value:.2f}₺'
        ), tags=['total'])
        report_tree.tag_configure('total', background='#e8f5e8', font=('Arial', 10, 'bold'))
        
        # Kaydırma çubuğu
        scrollbar = ttk.Scrollbar(self.report_display_frame, orient=tk.VERTICAL, command=report_tree.yview)
        report_tree.configure(yscrollcommand=scrollbar.set)
        
        report_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def revenue_report(self):
        # Rapor alanını temizle
        for widget in self.report_display_frame.winfo_children():
            widget.destroy()
        
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        # Son 30 günün gelir raporu
        cursor.execute('''
            SELECT 
                DATE(sale_date) as sale_day,
                COUNT(*) as transaction_count,
                SUM(total_price) as daily_revenue
            FROM sales
            WHERE sale_date >= DATE('now', '-30 days')
            GROUP BY DATE(sale_date)
            ORDER BY sale_day DESC
        ''')
        
        daily_revenues = cursor.fetchall()
        conn.close()
        
        if not daily_revenues:
            tk.Label(self.report_display_frame, text="Son 30 günde satış yapılmamış.",
                    font=('Arial', 12), bg='white').pack(expand=True)
            return
        
        tk.Label(self.report_display_frame, text="💰 SON 30 GÜN GELİR RAPORU", 
                font=('Arial', 14, 'bold'), bg='white').pack(pady=10)
        
        # Rapor tablosu
        columns = ('Tarih', 'İşlem Sayısı', 'Günlük Gelir')
        report_tree = ttk.Treeview(self.report_display_frame, columns=columns, show='headings', height=12)
        
        for col in columns:
            report_tree.heading(col, text=col)
            report_tree.column(col, width=150, anchor='center')
        
        total_transactions = 0
        total_revenue = 0
        
        for revenue in daily_revenues:
            day, count, revenue_amount = revenue
            total_transactions += count
            total_revenue += revenue_amount
            
            report_tree.insert('', tk.END, values=(day, count, f'{revenue_amount:.2f}₺'))
        
        # Toplam satır
        report_tree.insert('', tk.END, values=(
            'TOPLAM', total_transactions, f'{total_revenue:.2f}₺'
        ), tags=['total'])
        report_tree.tag_configure('total', background='#e8f5e8', font=('Arial', 10, 'bold'))
        
        # Kaydırma çubuğu
        scrollbar = ttk.Scrollbar(self.report_display_frame, orient=tk.VERTICAL, command=report_tree.yview)
        report_tree.configure(yscrollcommand=scrollbar.set)
        
        report_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def show_settings(self):
        self.clear_content()
        
        # Ayarlar sayfası
        title_frame = tk.Frame(self.content_frame, bg='white')
        title_frame.pack(fill=tk.X, padx=20, pady=10)
        
        ttk.Label(title_frame, text="⚙️ AYARLAR", style='Title.TLabel').pack(side=tk.LEFT)
        
        # Ana çerçeve
        main_frame = tk.Frame(self.content_frame, bg='white')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Veritabanı işlemleri
        db_frame = tk.LabelFrame(main_frame, text="🗄️ Veritabanı İşlemleri", 
                                font=('Arial', 12, 'bold'), bg='white', padx=20, pady=20)
        db_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Button(db_frame, text="📤 Veritabanını Yedekle", command=self.backup_database,
                 bg='#4CAF50', fg='white', font=('Arial', 12, 'bold'), padx=20, pady=10).pack(side=tk.LEFT, padx=10)
        
        tk.Button(db_frame, text="🧹 Veritabanını Temizle", command=self.clear_database,
                 bg='#f44336', fg='white', font=('Arial', 12, 'bold'), padx=20, pady=10).pack(side=tk.LEFT, padx=10)
        
        # Uygulama bilgileri
        info_frame = tk.LabelFrame(main_frame, text="ℹ️ Uygulama Bilgileri", 
                                  font=('Arial', 12, 'bold'), bg='white', padx=20, pady=20)
        info_frame.pack(fill=tk.X)
        
        info_text = """
        🏪 Market Yönetim Sistemi v1.0 BETA
        
        📝 Özellikler:
        • Ürün yönetimi (ekleme, düzenleme, silme)
        • Satış işlemleri ve sepet yönetimi
        • Stok takibi ve hareket kayıtları
        • Detaylı raporlama sistemi
        • Düşük stok uyarıları
        
        
        👨‍💻 Geliştirici: salim_style
        📅 Sürüm Tarihi: 2025
        📞 İletişim: https://discord.com/invite/Xbk6GYyxX8
        """
        
        tk.Label(info_frame, text=info_text, font=('Arial', 10), bg='white', 
                justify=tk.LEFT, anchor='nw').pack(fill=tk.BOTH, expand=True)
    
    def backup_database(self):
        try:
            import shutil
            from tkinter import filedialog
            
            # Dosya kaydetme dialogu
            backup_path = filedialog.asksaveasfilename(
                title="Veritabanı Yedeği Kaydet",
                defaultextension=".db",
                filetypes=[("SQLite Database", "*.db"), ("All Files", "*.*")]
            )
            
            if backup_path:
                shutil.copy2(self.db.db_name, backup_path)
                messagebox.showinfo("Başarılı", f"Veritabanı başarıyla yedeklendi:\n{backup_path}")
        
        except Exception as e:
            messagebox.showerror("Hata", f"Yedekleme sırasında hata oluştu:\n{str(e)}")
    
    def clear_database(self):
        result = messagebox.askyesnocancel(
            "Uyarı", 
            "Bu işlem tüm verileri silecek!\n\n"
            "• Evet: Tüm verileri sil\n"
            "• Hayır: Sadece satış ve stok hareketlerini sil\n"
            "• İptal: İşlemi iptal et"
        )
        
        if result is None:  # İptal
            return
        
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            if result:  # Evet - Tüm verileri sil
                cursor.execute("DELETE FROM stock_movements")
                cursor.execute("DELETE FROM sales")
                cursor.execute("DELETE FROM products")
                message = "Tüm veriler temizlendi!"
            else:  # Hayır - Sadece satış ve hareketleri sil
                cursor.execute("DELETE FROM stock_movements")
                cursor.execute("DELETE FROM sales")
                cursor.execute("UPDATE products SET stock = 0")
                message = "Satış ve stok hareketleri temizlendi!"
            
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Başarılı", message)
            
            # Sayfaları yenile
            if hasattr(self, 'products_tree'):
                self.refresh_products()
            if hasattr(self, 'stock_tree'):
                self.refresh_stock_data()
        
        except Exception as e:
            messagebox.showerror("Hata", f"Temizleme sırasında hata oluştu:\n{str(e)}")

def main():
    root = tk.Tk()
    app = MarketApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()