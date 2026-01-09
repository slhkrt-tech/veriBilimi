"""
Film Öneri Sistemi - GUI Versiyonu
Tkinter ile basit ve kullanıcı dostu arayüz
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

import threading
import traceback

class FilmOneriGUI:
    """Film Öneri Sistemi GUI Sınıfı"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.setup_window()
        self.create_widgets()
        
        # Film sistemi değişkenleri
        self.df = None
        self.df_encoded = None
        self.feature_matrix = None
        self.cosine_sim = None
        self.le_dict = {}
        self.regression_model = None
        self.scaler = None
        
        # Sistem başlat
        self.load_system()
    
    def setup_window(self):
        """Pencere ayarları"""
        self.root.title("🎬 Film Öneri Sistemi v2.0")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # İkon ve tema
        try:
            self.root.configure(bg='#f0f0f0')
        except:
            pass
        
        # Pencereyi ortala
        self.center_window()
    
    def center_window(self):
        """Pencereyi ekranın ortasında aç"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def create_widgets(self):
        """GUI bileşenlerini oluştur"""
        
        # Ana başlık
        title_frame = ttk.Frame(self.root)
        title_frame.pack(pady=10, padx=20, fill='x')
        
        title_label = ttk.Label(
            title_frame, 
            text="🎬 Film Öneri Sistemi",
            font=('Arial', 20, 'bold')
        )
        title_label.pack()
        
        subtitle_label = ttk.Label(
            title_frame,
            text="AI Destekli Film Önerileri ve Rating Tahmini",
            font=('Arial', 10, 'italic')
        )
        subtitle_label.pack()
        
        # Ana notebook (sekmeler)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(pady=10, padx=20, fill='both', expand=True)
        
        # Sekmeler oluştur
        self.create_recommendation_tab()
        self.create_prediction_tab()
        self.create_search_tab()
        self.create_stats_tab()
        
        # Alt durum çubuğu
        self.status_frame = ttk.Frame(self.root)
        self.status_frame.pack(side='bottom', fill='x', pady=5, padx=20)
        
        self.status_label = ttk.Label(
            self.status_frame,
            text="🔄 Sistem yükleniyor...",
            font=('Arial', 9)
        )
        self.status_label.pack(side='left')
        
        # Sistem bilgisi
        info_label = ttk.Label(
            self.status_frame,
            text="4000 Film | AI Öneri | v2.0",
            font=('Arial', 9)
        )
        info_label.pack(side='right')
    
    def create_recommendation_tab(self):
        """Film Önerisi sekmesi"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="🎯 Film Önerisi")
        
        # Üst kısım - Giriş
        input_frame = ttk.LabelFrame(tab, text="Film Arama", padding=10)
        input_frame.pack(pady=10, padx=10, fill='x')
        
        ttk.Label(input_frame, text="🎬 Film Adı:").grid(row=0, column=0, sticky='w', pady=5)
        
        self.movie_entry = ttk.Entry(input_frame, font=('Arial', 12), width=40)
        self.movie_entry.grid(row=0, column=1, pady=5, padx=10, sticky='ew')
        self.movie_entry.bind('<Return>', lambda e: self.get_recommendations())
        
        self.recommend_btn = ttk.Button(
            input_frame,
            text="🔍 Öneri Al",
            command=self.get_recommendations
        )
        self.recommend_btn.grid(row=0, column=2, pady=5, padx=5)
        
        input_frame.columnconfigure(1, weight=1)
        
        # Alt kısım - Sonuçlar
        result_frame = ttk.LabelFrame(tab, text="Önerilen Filmler", padding=10)
        result_frame.pack(pady=10, padx=10, fill='both', expand=True)
        
        # Sonuç tablosu
        columns = ('Film', 'Rating', 'Tür', 'Ülke', 'Benzerlik')
        self.recommendation_tree = ttk.Treeview(result_frame, columns=columns, show='headings', height=10)
        
        # Sütun başlıkları
        for col in columns:
            self.recommendation_tree.heading(col, text=col)
            
        # Sütun genişlikleri
        self.recommendation_tree.column('Film', width=200)
        self.recommendation_tree.column('Rating', width=80)
        self.recommendation_tree.column('Tür', width=120)
        self.recommendation_tree.column('Ülke', width=100)
        self.recommendation_tree.column('Benzerlik', width=80)
        
        # Scrollbar
        scrollbar1 = ttk.Scrollbar(result_frame, orient='vertical', command=self.recommendation_tree.yview)
        self.recommendation_tree.configure(yscrollcommand=scrollbar1.set)
        
        self.recommendation_tree.pack(side='left', fill='both', expand=True)
        scrollbar1.pack(side='right', fill='y')
    
    def create_prediction_tab(self):
        """Rating Tahmini sekmesi"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="📈 Rating Tahmini")
        
        # Sol kısım - Giriş
        input_frame = ttk.LabelFrame(tab, text="Film Özellikleri", padding=10)
        input_frame.pack(side='left', pady=10, padx=10, fill='both', expand=True)
        
        # Özellik giriş alanları
        self.feature_vars = {}
        features = [
            ("🎭 Tür (0-23)", "genre"),
            ("🌍 Ülke (0-22)", "country"),
            ("🎥 Yönetmen (0-48)", "director"),
            ("📅 Yıl", "year"),
            ("⏱️ Süre (dk)", "duration"),
            ("😄 Mizah (1-10)", "humor"),
            ("💥 Aksiyon (1-10)", "action"),
            ("💕 Romantizm (1-10)", "romance"),
            ("😰 Gerilim (1-10)", "tension")
        ]
        
        for i, (label, key) in enumerate(features):
            ttk.Label(input_frame, text=label).grid(row=i, column=0, sticky='w', pady=5)
            
            var = tk.StringVar()
            entry = ttk.Entry(input_frame, textvariable=var, width=15)
            entry.grid(row=i, column=1, pady=5, padx=10, sticky='ew')
            
            self.feature_vars[key] = var
            
            # Varsayılan değerler
            if key == "year":
                var.set("2023")
            elif key == "duration":
                var.set("120")
            elif key in ["genre", "country", "director"]:
                var.set("0")
            else:
                var.set("5")
        
        input_frame.columnconfigure(1, weight=1)
        
        # Tahmin butonu
        predict_btn = ttk.Button(
            input_frame,
            text="🎯 Rating Tahmin Et",
            command=self.predict_rating
        )
        predict_btn.grid(row=len(features), column=0, columnspan=2, pady=20)
        
        # Sağ kısım - Sonuç
        result_frame = ttk.LabelFrame(tab, text="Tahmin Sonucu", padding=10)
        result_frame.pack(side='right', pady=10, padx=10, fill='both', expand=True)
        
        self.prediction_result = ttk.Label(
            result_frame,
            text="Tahmin için özellikleri girin ve butona tıklayın",
            font=('Arial', 12),
            justify='center'
        )
        self.prediction_result.pack(expand=True)
    
    def create_search_tab(self):
        """Film Arama sekmesi"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="🔍 Film Ara")
        
        # Arama kısmı
        search_frame = ttk.LabelFrame(tab, text="Film Arama", padding=10)
        search_frame.pack(pady=10, padx=10, fill='x')
        
        ttk.Label(search_frame, text="🔍 Arama:").grid(row=0, column=0, sticky='w', pady=5)
        
        self.search_entry = ttk.Entry(search_frame, font=('Arial', 12), width=50)
        self.search_entry.grid(row=0, column=1, pady=5, padx=10, sticky='ew')
        self.search_entry.bind('<Return>', lambda e: self.search_movies())
        
        search_btn = ttk.Button(
            search_frame,
            text="🔍 Ara",
            command=self.search_movies
        )
        search_btn.grid(row=0, column=2, pady=5, padx=5)
        
        search_frame.columnconfigure(1, weight=1)
        
        # Sonuçlar
        result_frame = ttk.LabelFrame(tab, text="Arama Sonuçları", padding=10)
        result_frame.pack(pady=10, padx=10, fill='both', expand=True)
        
        # Sonuç tablosu
        columns = ('Film', 'Rating', 'Tür', 'Yıl', 'Ülke', 'Süre')
        self.search_tree = ttk.Treeview(result_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            self.search_tree.heading(col, text=col)
            
        # Sütun genişlikleri
        self.search_tree.column('Film', width=200)
        self.search_tree.column('Rating', width=80)
        self.search_tree.column('Tür', width=120)
        self.search_tree.column('Yıl', width=80)
        self.search_tree.column('Ülke', width=100)
        self.search_tree.column('Süre', width=80)
        
        # Scrollbar
        scrollbar2 = ttk.Scrollbar(result_frame, orient='vertical', command=self.search_tree.yview)
        self.search_tree.configure(yscrollcommand=scrollbar2.set)
        
        self.search_tree.pack(side='left', fill='both', expand=True)
        scrollbar2.pack(side='right', fill='y')
    
    def create_stats_tab(self):
        """İstatistikler sekmesi"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="📊 İstatistikler")
        
        # İstatistik metni
        self.stats_text = scrolledtext.ScrolledText(
            tab,
            font=('Courier New', 10),
            wrap=tk.WORD,
            height=25
        )
        self.stats_text.pack(pady=10, padx=10, fill='both', expand=True)
        
        # Güncelle butonu
        refresh_btn = ttk.Button(
            tab,
            text="🔄 İstatistikleri Güncelle",
            command=self.update_stats
        )
        refresh_btn.pack(pady=5)
    
    def create_sample_dataset(self):
        """4000 filmlik sample dataset oluşturur"""
        self.update_status("📊 Film veri seti oluşturuluyor...")
        
        # Base filmler ve Türkçe filmler (önceki koddan)
        base_movies = [
            "Avatar", "Titanic", "Star Wars", "The Godfather", "Pulp Fiction",
            "The Dark Knight", "Fight Club", "Forrest Gump", "Inception", "Matrix",
            "Goodfellas", "Seven", "Silence of the Lambs", "Saving Private Ryan", "Gladiator",
            "Terminator", "Aliens", "Jaws", "E.T.", "Jurassic Park",
            "Back to the Future", "Raiders of the Lost Ark", "Rocky", "Casablanca", "Citizen Kane"
        ]
        
        turkish_movies = [
            "Eşkıya", "Vizontele", "Hababam Sınıfı", "Neşeli Günler", "Süt Kardeşler",
            "Tosun Paşa", "Kibar Feyzo", "Şabanoğlu Şaban", "Banker Bilo", "Gülen Gözler",
            "Recep İvedik", "GORA", "Arog", "Yahşi Batı", "Organize İşler",
            "Kurtlar Vadisi", "Düğün Dernek", "Müslüm", "Ayla", "Babam ve Oğlum"
        ]
        
        variations = [
            "New", "The", "Return of", "Rise of", "Dawn of", "War of", "Age of",
            "Final", "Ultimate", "Super", "Mega", "Epic", "Dark", "Black", "Red",
            "Blue", "Green", "Golden", "Silver", "Crystal", "Diamond", "Platinum"
        ]
        
        genres = [
            "Aksiyon", "Komedi", "Drama", "Korku", "Bilim Kurgu", "Romantik",
            "Gerilim", "Animasyon", "Belgesel", "Fantastik", "Macera", "Suç",
            "Müzikal", "Savaş", "Western", "Tarih", "Biyografi", "Spor",
            "Aile", "Gizem", "Psikolojik", "Zombi", "Vampir", "Süper Kahraman"
        ]
        
        countries = [
            "Amerika", "İngiltere", "Fransa", "Almanya", "İtalya", "İspanya",
            "Japonya", "Güney Kore", "Çin", "Hindistan", "Rusya", "Kanada",
            "Avustralya", "Brezilya", "Meksika", "Arjantin", "İsveç", "Norveç",
            "Danimarka", "Hollanda", "Belçika", "İsviçre", "Türkiye"
        ]
        
        directors = [
            "Christopher Nolan", "Steven Spielberg", "Martin Scorsese", "Quentin Tarantino",
            "Alfred Hitchcock", "Stanley Kubrick", "Francis Ford Coppola", "Ridley Scott",
            "James Cameron", "George Lucas", "Tim Burton", "David Fincher",
            "Yılmaz Erdoğan", "Cem Yılmaz", "Nuri Bilge Ceylan", "Fatih Akın"
        ]
        
        # Film verileri oluştur
        films = []
        all_movies = base_movies + turkish_movies
        
        for i in range(4000):
            if i < len(all_movies):
                name = all_movies[i]
            else:
                base = np.random.choice(all_movies)
                variation = np.random.choice(variations)
                number = np.random.randint(1, 100)
                name = f"{variation} {base} {number}"
            
            film = {
                'movie_title': name,
                'genre': np.random.choice(genres),
                'year': np.random.randint(1950, 2024),
                'avg_vote': round(np.random.normal(6.5, 1.5), 1),
                'country': np.random.choice(countries),
                'duration': np.random.randint(80, 180),
                'directors': np.random.choice(directors),
                'mizah': np.random.randint(1, 10),
                'aksiyon': np.random.randint(1, 10),
                'romantizm': np.random.randint(1, 10),
                'gerilim': np.random.randint(1, 10),
                'drama': np.random.randint(1, 10),
                'ritim': np.random.randint(1, 10),
                'gorsel': np.random.randint(1, 10),
                'muzik': np.random.randint(1, 10),
                'yaraticilik': np.random.randint(1, 10)
            }
            
            # Avg_vote sınırları
            if film['avg_vote'] < 1:
                film['avg_vote'] = 1.0
            elif film['avg_vote'] > 10:
                film['avg_vote'] = 10.0
                
            films.append(film)
        
        return pd.DataFrame(films)
    
    def load_system(self):
        """Sistem yükleme işlemini arka planda yap"""
        def load_in_background():
            try:
                self.update_status("🔄 Sistem başlatılıyor...")
                
                # Veri yükle
                self.df = self.create_sample_dataset()
                self.update_status("📊 Veri ön işleme...")
                
                # Veri ön işleme
                self.preprocess_data()
                self.update_status("🤖 Öneri sistemi hazırlanıyor...")
                
                # Öneri sistemi
                self.prepare_recommendation_system()
                self.update_status("📈 Regresyon modeli hazırlanıyor...")
                
                # Regresyon modeli
                self.prepare_regression_model()
                
                self.update_status("✅ Sistem hazır! Film önerisi alabilirsiniz.")
                
                # Başlangıç istatistikleri
                self.root.after(1000, self.update_stats)
                
            except Exception as e:
                error_msg = f"❌ Sistem yükleme hatası: {str(e)}"
                self.update_status(error_msg)
                messagebox.showerror("Hata", f"Sistem başlatılamadı:\n{str(e)}")
        
        # Arka plan thread'i başlat
        thread = threading.Thread(target=load_in_background, daemon=True)
        thread.start()
    
    def preprocess_data(self):
        """Veri ön işleme"""
        self.df_encoded = self.df.copy()
        
        # Kategorik sütunlar
        categorical_columns = ['genre', 'country', 'directors']
        
        # LabelEncoder
        for col in categorical_columns:
            le = LabelEncoder()
            self.df_encoded[col] = self.df_encoded[col].fillna('Unknown')
            self.df_encoded[col + '_encoded'] = le.fit_transform(self.df_encoded[col])
            self.le_dict[col] = le
        
        # Sayısal sütunlar
        numeric_columns = ['mizah', 'aksiyon', 'romantizm', 'gerilim', 'drama', 
                          'ritim', 'gorsel', 'muzik', 'yaraticilik']
        
        for col in numeric_columns:
            self.df_encoded[col] = self.df_encoded[col].fillna(self.df_encoded[col].mean())
        
        # Toplam skor
        self.df_encoded['toplam_skor'] = self.df_encoded[numeric_columns].mean(axis=1)
        
        # Binary sınıflandırma
        threshold = self.df_encoded['toplam_skor'].median()
        self.df_encoded['siniflandirma'] = (self.df_encoded['toplam_skor'] > threshold).astype(int)
    
    def prepare_recommendation_system(self):
        """Öneri sistemi hazırlama"""
        feature_columns = ['genre_encoded', 'country_encoded', 'directors_encoded', 
                          'year', 'duration', 'mizah', 'aksiyon', 'romantizm', 
                          'gerilim', 'drama', 'ritim', 'gorsel', 'muzik', 'yaraticilik']
        
        feature_data = []
        for _, row in self.df_encoded.iterrows():
            features = []
            for col in feature_columns:
                features.append(str(row[col]))
            feature_data.append(' '.join(features))
        
        vectorizer = CountVectorizer()
        self.feature_matrix = vectorizer.fit_transform(feature_data)
        self.cosine_sim = cosine_similarity(self.feature_matrix)
    
    def prepare_regression_model(self):
        """Regresyon modeli hazırlama"""
        features = ['genre_encoded', 'country_encoded', 'directors_encoded', 
                   'year', 'duration', 'mizah', 'aksiyon', 'romantizm', 'gerilim']
        
        X = self.df_encoded[features]
        y = self.df_encoded['avg_vote']
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        self.scaler = StandardScaler()
        X_train_scaled = self.scaler.fit_transform(X_train)
        
        self.regression_model = LinearRegression()
        self.regression_model.fit(X_train_scaled, y_train)
    
    def update_status(self, message):
        """Durum çubuğunu güncelle"""
        self.root.after(0, lambda: self.status_label.config(text=message))
    
    def get_recommendations(self):
        """Film önerisi al"""
        if self.df is None or self.cosine_sim is None:
            messagebox.showwarning("Uyarı", "Sistem henüz hazır değil, lütfen bekleyin.")
            return
        
        movie_name = self.movie_entry.get().strip()
        if not movie_name:
            messagebox.showwarning("Uyarı", "Lütfen bir film adı girin!")
            return
        
        try:
            self.update_status(f"🔍 '{movie_name}' için öneriler aranıyor...")
            
            # Film ara
            movie_name_lower = movie_name.lower()
            matches = self.df[self.df['movie_title'].str.lower().str.contains(movie_name_lower, na=False)]
            
            if len(matches) == 0:
                self.update_status("❌ Film bulunamadı!")
                messagebox.showinfo("Sonuç", f"'{movie_name}' filmi bulunamadı!\nBaşka bir film adı deneyin.")
                return
            
            # İlk eşleşmeyi al
            film_idx = matches.index[0]
            
            # Benzerlik skorları
            sim_scores = list(enumerate(self.cosine_sim[film_idx]))
            sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
            
            # En benzer 5 filmi al (kendisi hariç)
            sim_indices = [i[0] for i in sim_scores[1:6]]
            
            # Tabloyu temizle
            for item in self.recommendation_tree.get_children():
                self.recommendation_tree.delete(item)
            
            # Önerileri tabloya ekle
            for i, idx in enumerate(sim_indices):
                film = self.df.iloc[idx]
                similarity = sim_scores[i+1][1]
                
                self.recommendation_tree.insert('', 'end', values=(
                    film['movie_title'],
                    f"{film['avg_vote']:.1f}",
                    film['genre'],
                    film['country'],
                    f"{similarity:.3f}"
                ))
            
            self.update_status(f"✅ '{movie_name}' için 5 öneri bulundu!")
            
        except Exception as e:
            error_msg = f"Öneri alma hatası: {str(e)}"
            self.update_status(f"❌ {error_msg}")
            messagebox.showerror("Hata", error_msg)
    
    def predict_rating(self):
        """Rating tahmini yap"""
        if self.regression_model is None or self.scaler is None:
            messagebox.showwarning("Uyarı", "Tahmin modeli henüz hazır değil!")
            return
        
        try:
            # Özellikleri al
            features = []
            for key in ['genre', 'country', 'director', 'year', 'duration', 'humor', 'action', 'romance', 'tension']:
                value = self.feature_vars[key].get().strip()
                if not value:
                    messagebox.showwarning("Uyarı", f"Lütfen {key} değerini girin!")
                    return
                features.append(float(value))
            
            self.update_status("📈 Rating tahmin ediliyor...")
            
            # Tahmin
            X_scaled = self.scaler.transform([features])
            prediction = self.regression_model.predict(X_scaled)[0]
            
            # Sonucu göster
            result_text = f"🎯 Tahmin Edilen Rating: {prediction:.2f}/10\n\n"
            
            if prediction >= 8:
                result_text += "🌟 Muhteşem film olacak!"
                color = "green"
            elif prediction >= 7:
                result_text += "⭐ Harika film olacak!"
                color = "blue"
            elif prediction >= 6:
                result_text += "👍 İyi film olacak!"
                color = "orange"
            elif prediction >= 5:
                result_text += "👌 Fena değil!"
                color = "gray"
            else:
                result_text += "👎 Pek iyi olmayabilir..."
                color = "red"
            
            self.prediction_result.config(text=result_text, foreground=color)
            self.update_status("✅ Rating tahmini tamamlandı!")
            
        except ValueError:
            messagebox.showerror("Hata", "Lütfen geçerli sayısal değerler girin!")
        except Exception as e:
            error_msg = f"Tahmin hatası: {str(e)}"
            self.update_status(f"❌ {error_msg}")
            messagebox.showerror("Hata", error_msg)
    
    def search_movies(self):
        """Film arama"""
        if self.df is None:
            messagebox.showwarning("Uyarı", "Sistem henüz hazır değil!")
            return
        
        search_term = self.search_entry.get().strip()
        if not search_term:
            messagebox.showwarning("Uyarı", "Lütfen arama terimi girin!")
            return
        
        try:
            self.update_status(f"🔍 '{search_term}' aranıyor...")
            
            # Arama
            search_lower = search_term.lower()
            results = self.df[
                self.df['movie_title'].str.lower().str.contains(search_lower, na=False) |
                self.df['genre'].str.lower().str.contains(search_lower, na=False) |
                self.df['country'].str.lower().str.contains(search_lower, na=False) |
                self.df['directors'].str.lower().str.contains(search_lower, na=False)
            ]
            
            # Tabloyu temizle
            for item in self.search_tree.get_children():
                self.search_tree.delete(item)
            
            if len(results) == 0:
                self.update_status("❌ Arama sonucu bulunamadı!")
                messagebox.showinfo("Sonuç", f"'{search_term}' için sonuç bulunamadı!")
                return
            
            # Sonuçları tabloya ekle (ilk 50 tanesi)
            for _, film in results.head(50).iterrows():
                self.search_tree.insert('', 'end', values=(
                    film['movie_title'],
                    f"{film['avg_vote']:.1f}",
                    film['genre'],
                    film['year'],
                    film['country'],
                    f"{film['duration']} dk"
                ))
            
            result_count = len(results)
            shown_count = min(result_count, 50)
            
            self.update_status(f"✅ {result_count} sonuç bulundu, {shown_count} tanesi gösteriliyor!")
            
        except Exception as e:
            error_msg = f"Arama hatası: {str(e)}"
            self.update_status(f"❌ {error_msg}")
            messagebox.showerror("Hata", error_msg)
    
    def update_stats(self):
        """İstatistikleri güncelle"""
        if self.df is None:
            return
        
        try:
            self.stats_text.delete(1.0, tk.END)
            
            stats_text = f"""
🎬 FİLM ÖNERİ SİSTEMİ - İSTATİSTİKLER
{'=' * 50}

📊 GENEL BİLGİLER:
{'─' * 30}
📱 Toplam film sayısı         : {len(self.df):,}
🎭 Farklı tür sayısı          : {self.df['genre'].nunique()}
🌍 Farklı ülke sayısı         : {self.df['country'].nunique()}
🎥 Farklı yönetmen sayısı     : {self.df['directors'].nunique()}
📅 Yıl aralığı               : {self.df['year'].min()} - {self.df['year'].max()}

⭐ RATING İSTATİSTİKLERİ:
{'─' * 30}
📊 Ortalama rating           : {self.df['avg_vote'].mean():.2f}
📈 En yüksek rating          : {self.df['avg_vote'].max():.1f}
📉 En düşük rating           : {self.df['avg_vote'].min():.1f}
📏 Rating standart sapması   : {self.df['avg_vote'].std():.2f}

⏱️ SÜRE İSTATİSTİKLERİ:
{'─' * 30}
🕐 Ortalama süre             : {self.df['duration'].mean():.0f} dakika
⏰ En uzun film              : {self.df['duration'].max()} dakika
⏱️ En kısa film              : {self.df['duration'].min()} dakika

🎭 TÜR DAĞILIMI (İlk 10):
{'─' * 30}"""
            
            # Tür dağılımı
            genre_counts = self.df['genre'].value_counts().head(10)
            for genre, count in genre_counts.items():
                percentage = (count / len(self.df)) * 100
                stats_text += f"\n{genre:<20} : {count:>4} (%{percentage:.1f})"
            
            stats_text += f"""

🌍 ÜLKE DAĞILIMI (İlk 10):
{'─' * 30}"""
            
            # Ülke dağılımı
            country_counts = self.df['country'].value_counts().head(10)
            for country, count in country_counts.items():
                percentage = (count / len(self.df)) * 100
                stats_text += f"\n{country:<20} : {count:>4} (%{percentage:.1f})"
            
            if hasattr(self, 'df_encoded') and self.df_encoded is not None:
                stats_text += f"""

🎯 SINIFLANDIRMA:
{'─' * 30}
⬆️ Üst sınıf filmler         : {self.df_encoded['siniflandirma'].sum():,}
⬇️ Alt sınıf filmler         : {(len(self.df_encoded) - self.df_encoded['siniflandirma'].sum()):,}
📊 Eşik değeri              : {self.df_encoded['toplam_skor'].median():.2f}"""
            
            stats_text += f"""

🤖 SİSTEM BİLGİLERİ:
{'─' * 30}"""
            
            if hasattr(self, 'feature_matrix') and self.feature_matrix is not None:
                stats_text += f"\n🔧 Özellik matrisi boyutu    : {self.feature_matrix.shape}"
            
            if hasattr(self, 'cosine_sim') and self.cosine_sim is not None:
                stats_text += f"\n🧮 Benzerlik matrisi boyutu  : {self.cosine_sim.shape}"
            
            stats_text += f"\n✅ Öneri sistemi durumu      : {'Hazır' if self.cosine_sim is not None else 'Yükleniyor'}"
            stats_text += f"\n📈 Regresyon modeli durumu   : {'Hazır' if self.regression_model is not None else 'Yükleniyor'}"
            
            stats_text += f"""

📚 POPÜLER FİLMLER (Rating > 8.0):
{'─' * 30}"""
            
            # Popüler filmler
            popular = self.df[self.df['avg_vote'] > 8.0].nlargest(10, 'avg_vote')
            for _, film in popular.iterrows():
                stats_text += f"\n🎬 {film['movie_title']:<25} ({film['avg_vote']:.1f}) - {film['genre']}"
            
            stats_text += f"""

{'=' * 50}
🕐 Son güncelleme: {pd.Timestamp.now().strftime('%d.%m.%Y %H:%M:%S')}
🎬 Film Öneri Sistemi v2.0 - GUI Edition
"""
            
            self.stats_text.insert(1.0, stats_text)
            
        except Exception as e:
            error_msg = f"İstatistik güncelleme hatası: {str(e)}"
            self.stats_text.delete(1.0, tk.END)
            self.stats_text.insert(1.0, f"❌ {error_msg}")
    
    def run(self):
        """GUI'yi başlat"""
        self.root.mainloop()

def main():
    """Ana fonksiyon"""
    try:
        app = FilmOneriGUI()
        app.run()
    except Exception as e:
        print(f"❌ GUI başlatma hatası: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()