===============================================================
🏪 MARKET YÖNETİM SİSTEMİ v1.0 BETA
===============================================================

📋 İÇİNDEKİLER
---------------
1. Genel Bilgiler
2. Sistem Gereksinimleri
3. Kurulum
4. Kullanım
5. Özellikler
6. Dosya Yapısı
7. Veritabanı
8. Sorun Giderme
9. Geliştirici Bilgileri

===============================================================

1. 📖 GENEL BİLGİLER
--------------------
Market Yönetim Sistemi, küçük ve orta ölçekli marketler için 
geliştirilmiş kapsamlı bir stok ve satış yönetim uygulamasıdır.

✨ Ana Özellikler:
• Ürün yönetimi (ekleme, düzenleme, silme)
• Gerçek zamanlı satış işlemleri
• Otomatik stok takibi
• Detaylı raporlama sistemi
• Düşük stok uyarıları
• Kullanıcı dostu arayüz

===============================================================

2. 🖥️ SİSTEM GEREKSİNİMLERİ
-----------------------------
• İşletim Sistemi: Windows 7 ve üzeri
• Python: 3.7 ve üzeri (otomatik kurulacak)
• RAM: Minimum 2GB
• Disk Alanı: 100MB boş alan
• Ekran Çözünürlüğü: 1024x768 ve üzeri

===============================================================

3. 🚀 KURULUM
-------------
█ KOLAY KURULUM (Önerilen):
1. "run_app_hidden.vbs" dosyasına çift tıklayın
2. Python yüklü değilse otomatik kurulum teklif edilecek
3. "Evet" seçeneğine basın ve bekleyin
4. Kurulum tamamlandıktan sonra uygulama otomatik başlar

█ MANUEL KURULUM:
1. Python'u python.org'dan indirin ve kurun
2. Komut satırında şu komutu çalıştırın:
   cd app
   python app.py

█ DOSYA YAPISI:
Proje klasörünüzde şu dosyalar bulunmalı:
├── run_app_hidden.vbs    (Başlatıcı)
├── ikon.png             (Uygulama ikonu)
└── app/
    ├── app.py           (Ana uygulama)
    ├── database.py      (Veritabanı modülü)
    └── market.db        (Veritabanı - otomatik oluşur)

===============================================================

4. 📚 KULLANIM
--------------
█ İLK BAŞLATMA:
1. Uygulama ilk açıldığında boş bir ürün listesi görürsünüz
2. "➕ Yeni Ürün" butonuna basarak ürün eklemeye başlayın
3. Zorunlu alanlar (*) ile işaretlenmiştir

█ ÜRÜN YÖNETİMİ:
• Yeni Ürün: Ürün adı, fiyat ve stok bilgileri girin
• Düzenle: Listeden ürün seçip "✏️ Düzenle" butonuna basın
• Sil: Ürün seçip "🗑️ Sil" butonuna basın
• Arama: Üst kısımdaki arama kutusunu kullanın

█ SATIŞ İŞLEMLERİ:
1. "💰 Satış" sekmesine gidin
2. Sol panelden ürün arayın veya listeden seçin
3. Miktarı belirleyin ve "🛒 Sepete Ekle" butonuna basın
4. Sepeti kontrol edin ve "💳 SATIŞ TAMAMLA" butonuna basın

█ STOK YÖNETİMİ:
• Stok Ekle: Mevcut ürünlere stok ekleyin
• Stok Çıkar: Fire, kayıp gibi durumlar için
• Düşük Stok: Kritik seviyedeki ürünleri görüntüleyin

█ RAPORLAR:
• Günlük Satış: Belirli bir günün satış raporu
• En Çok Satan: Popüler ürünleri görüntüleyin
• Kategori Raporu: Kategori bazlı analiz
• Gelir Raporu: Son 30 günün gelir trendi

===============================================================

5. ⭐ ÖZELLİKLER
---------------
█ ÜRÜN YÖNETİMİ:
✅ Sınırsız ürün ekleme
✅ Barkod desteği
✅ Kategori sistemi
✅ Ürün açıklamaları
✅ Toplu arama ve filtreleme
✅ Çift tıklama ile hızlı düzenleme

█ SATIŞ SİSTEMİ:
✅ Gerçek zamanlı sepet yönetimi
✅ Otomatik stok düşürme
✅ Çoklu ürün satışı
✅ Anlık toplam hesaplama
✅ Satış geçmişi kayıtları

█ STOK TAKİBİ:
✅ Otomatik stok güncellemesi
✅ Stok hareket kayıtları
✅ Düşük stok uyarıları
✅ Renk kodlu stok seviyeleri
✅ Manuel stok düzeltmeleri

█ RAPORLAMA:
✅ Günlük/aylık satış raporları
✅ En çok satan ürün analizi
✅ Kategori bazlı raporlar
✅ Gelir trend analizi
✅ Stok değer hesaplaması

█ EK ÖZELLİKLER:
✅ Veritabanı yedekleme
✅ Veri temizleme araçları
✅ Kullanıcı dostu arayüz
✅ Hızlı klavye kısayolları
✅ Çoklu pencere desteği

===============================================================

6. 📁 DOSYA YAPISI
------------------
run_app_hidden.vbs     → Ana başlatıcı dosya
ikon.png              → Uygulama ikonu (32x32 PNG)
app/
├── app.py            → Ana uygulama kodu
├── database.py       → Veritabanı yönetimi
└── market.db         → SQLite veritabanı (otomatik oluşur)

█ VERİTABAN TABLOLARI:
• products          → Ürün bilgileri
• sales            → Satış kayıtları  
• stock_movements  → Stok hareketleri

===============================================================

7. 🗄️ VERİTABANI
-----------------
█ YEDEKLEME:
1. Ayarlar sekmesine gidin
2. "📤 Veritabanını Yedekle" butonuna basın
3. Kaydetmek istediğiniz konumu seçin

█ GERİ YÜKLEME:
1. Yedek dosyasını "market.db" olarak yeniden adlandırın
2. app/ klasörüne kopyalayın
3. Uygulamayı yeniden başlatın

█ TEMİZLEME:
• Tüm Veriler: Ürünler dahil her şeyi siler
• Sadece İşlemler: Ürünleri korur, satış ve hareketleri siler

===============================================================

8. 🔧 SORUN GİDERME
-------------------
█ UYGULAMA AÇILMIYOR:
• Python yüklü olduğundan emin olun
• Dosya yollarında Türkçe karakter olmamasına dikkat edin
• Antivirus yazılımını geçici olarak kapatın

█ VERİTABAN HATASI:
• market.db dosyasının yazılabilir olduğundan emin olun
• Uygulamayı yönetici olarak çalıştırın
• Veritabanı yedekten geri yükleyin

█ ÜRÜN EKLENEMİYOR:
• Barkod alanı benzersiz olmalıdır
• Fiyat ve stok sayısal değer olmalıdır
• Zorunlu alanları (*) doldurun

█ SATIŞ YAPILAMIYOR:
• Ürünün stokta olduğundan emin olun
• Sepete eklenen miktarı kontrol edin
• Ürün fiyatının doğru olduğunu kontrol edin

█ RAPOR GÖRÜNMÜYOR:
• Tarih formatının doğru olduğundan emin olun (YYYY-MM-DD)
• Seçilen dönemde veri olduğunu kontrol edin
• Uygulamayı yeniden başlatın

===============================================================

9. 👨‍💻 GELİŞTİRİCİ BİLGİLERİ
------------------------------
Geliştirici: salim_style
Versiyon: 1.0 BETA
Geliştirme Tarihi: 2025
Programlama Dili: Python 3.x
GUI Framework: Tkinter
Veritabanı: SQLite3

█ DESTEK:
Bu uygulama açık kaynak olarak geliştirilmiştir.
Hata bildirimleri ve öneriler için iletişime geçebilirsiniz.

█ LİSANS:
Bu yazılım ücretsiz olarak kullanılabilir.
İzinsiz kendi adına paylaşılması yasaktır.

█ GÜNCELLEMELER:
• v1.1: Barkod okuyucu desteği (planlanan)
• v1.2: Çoklu kullanıcı sistemi (planlanan)
• v1.3: Online yedekleme (planlanan)

===============================================================
🔄 Son Güncelleme: 2025
📞 Destek için: Discord: salim_style veya https://discord.com/invite/Xbk6GYyxX8
===============================================================
