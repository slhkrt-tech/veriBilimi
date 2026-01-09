"""
Film Öneri Sistemi - Standalone Executable Version
Tüm modüller tek dosyada birleştirilmiş optimize edilmiş versiyon
"""

import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

import os
import sys
import traceback

# Veri setini dahili olarak tanımla (EXE için)
def create_sample_dataset():
    """4000 filmlik sample dataset oluşturur"""
    print("📊 Film veri seti oluşturuluyor...")
    
    # Base filmler
    base_movies = [
        "Avatar", "Titanic", "Star Wars", "The Godfather", "Pulp Fiction",
        "The Dark Knight", "Fight Club", "Forrest Gump", "Inception", "Matrix",
        "Goodfellas", "Seven", "Silence of the Lambs", "Saving Private Ryan", "Gladiator",
        "Terminator", "Aliens", "Jaws", "E.T.", "Jurassic Park",
        "Back to the Future", "Raiders of the Lost Ark", "Rocky", "Casablanca", "Citizen Kane",
        "Vertigo", "Psycho", "Sunset Boulevard", "Apocalypse Now", "Taxi Driver",
        "Raging Bull", "Chinatown", "The Shining", "2001: A Space Odyssey", "Singin' in the Rain",
        "Lawrence of Arabia", "Gone with the Wind", "The Wizard of Oz", "On the Waterfront", "North by Northwest",
        "Rear Window", "Some Like It Hot", "Dr. Strangelove", "The Treasure of the Sierra Madre", "The Third Man",
        "The Maltese Falcon", "Double Indemnity", "Touch of Evil", "The Apartment", "Notorious"
    ]
    
    # Türkçe filmler
    turkish_movies = [
        "Eşkıya", "Vizontele", "Hababam Sınıfı", "Neşeli Günler", "Süt Kardeşler",
        "Tosun Paşa", "Kibar Feyzo", "Şabanoğlu Şaban", "Banker Bilo", "Gülen Gözler",
        "Recep İvedik", "GORA", "Arog", "Yahşi Batı", "Organize İşler",
        "Kurtlar Vadisi", "Düğün Dernek", "Müslüm", "Ayla", "Babam ve Oğlum",
        "Dondurmam Gaymak", "Sen Kimsin", "İftarlık Gazoz", "Selvi Boylum Al Yazmalım", "Yol"
    ]
    
    # Varyasyonlar
    variations = [
        "New", "The", "Return of", "Rise of", "Dawn of", "War of", "Age of",
        "Final", "Ultimate", "Super", "Mega", "Epic", "Dark", "Black", "Red",
        "Blue", "Green", "Golden", "Silver", "Crystal", "Diamond", "Platinum",
        "Special", "Director's Cut", "Extended", "Remastered", "Reloaded",
        "Revolution", "Evolution", "Genesis", "Legacy", "Origins", "Destiny",
        "Forever", "Returns", "Begins", "Ends", "Rises", "Falls", "Quest",
        "Adventure", "Journey", "Mission", "Operation", "Project", "Code",
        "Secret", "Hidden", "Lost", "Found", "Last", "First", "Next"
    ]
    
    # Film türleri
    genres = [
        "Aksiyon", "Komedi", "Drama", "Korku", "Bilim Kurgu", "Romantik",
        "Gerilim", "Animasyon", "Belgesel", "Fantastik", "Macera", "Suç",
        "Müzikal", "Savaş", "Western", "Tarih", "Biyografi", "Spor",
        "Aile", "Gizem", "Psikolojik", "Zombi", "Vampir", "Süper Kahraman"
    ]
    
    # Ülkeler
    countries = [
        "Amerika", "İngiltere", "Fransa", "Almanya", "İtalya", "İspanya",
        "Japonya", "Güney Kore", "Çin", "Hindistan", "Rusya", "Kanada",
        "Avustralya", "Brezilya", "Meksika", "Arjantin", "İsveç", "Norveç",
        "Danimarka", "Hollanda", "Belçika", "İsviçre", "Türkiye"
    ]
    
    # Yönetmenler
    directors = [
        "Christopher Nolan", "Steven Spielberg", "Martin Scorsese", "Quentin Tarantino",
        "Alfred Hitchcock", "Stanley Kubrick", "Francis Ford Coppola", "Ridley Scott",
        "James Cameron", "George Lucas", "Tim Burton", "David Fincher",
        "Coen Brothers", "Woody Allen", "Akira Kurosawa", "Federico Fellini",
        "Ingmar Bergman", "Andrei Tarkovsky", "Jean-Luc Godard", "François Truffaut",
        "Pedro Almodóvar", "Alejandro González Iñárritu", "Denis Villeneuve", "Christopher Nolan",
        "Greta Gerwig", "Jordan Peele", "Ari Aster", "Robert Eggers",
        "Chloé Zhao", "Lulu Wang", "Barry Jenkins", "Moonlight", "Parasite",
        "Bong Joon-ho", "Park Chan-wook", "Wong Kar-wai", "Zhang Yimou",
        "Yılmaz Erdoğan", "Cem Yılmaz", "Nuri Bilge Ceylan", "Fatih Akın",
        "Ferzan Özpetek", "Zeki Demirkubuz", "Semih Kaplanoğlu", "Reha Erdem",
        "Yeşim Ustaoğlu", "Derviş Zaim", "Ömer Faruk Sorak", "Mahsun Kırmızıgül",
        "Müfit Can Saçıntı"
    ]
    
    # Film verileri oluştur
    films = []
    all_movies = base_movies + turkish_movies
    
    for i in range(4000):
        if i < len(all_movies):
            # Orijinal filmler
            name = all_movies[i]
        else:
            # Varyasyonlu filmler
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
    
    df = pd.DataFrame(films)
    print(f"✅ {len(df)} film oluşturuldu")
    return df

class FilmOneriSistemi:
    """Film Öneri Sistemi - Ana Sınıf"""
    
    def __init__(self):
        """Sistem başlatma"""
        self.df = None
        self.df_encoded = None
        self.feature_matrix = None
        self.cosine_sim = None
        self.le_dict = {}
        self.regression_model = None
        self.scaler = None
        
        print("🎬 Film Öneri Sistemi Başlatılıyor...")
        self.yukle_veri()
        self.veri_onisleme()
        self.oneri_sistemi_hazirla()
        self.regresyon_modeli_hazirla()
        print("✅ Sistem hazır!")
    
    def yukle_veri(self):
        """Veri yükleme"""
        print("📊 Veri yükleniyor...")
        self.df = create_sample_dataset()
    
    def veri_onisleme(self):
        """Veri ön işleme"""
        print("🔧 Veri ön işleme yapılıyor...")
        
        self.df_encoded = self.df.copy()
        
        # Kategorik sütunlar
        categorical_columns = ['genre', 'country', 'directors']
        
        # LabelEncoder
        for col in categorical_columns:
            le = LabelEncoder()
            # Null değerleri doldur
            self.df_encoded[col] = self.df_encoded[col].fillna('Unknown')
            self.df_encoded[col + '_encoded'] = le.fit_transform(self.df_encoded[col])
            self.le_dict[col] = le
        
        # Sayısal sütunlar
        numeric_columns = ['mizah', 'aksiyon', 'romantizm', 'gerilim', 'drama', 
                          'ritim', 'gorsel', 'muzik', 'yaraticilik']
        
        # Null değerleri ortalama ile doldur
        for col in numeric_columns:
            self.df_encoded[col] = self.df_encoded[col].fillna(self.df_encoded[col].mean())
        
        # Toplam skor hesapla
        self.df_encoded['toplam_skor'] = self.df_encoded[numeric_columns].mean(axis=1)
        
        # Binary sınıflandırma
        threshold = self.df_encoded['toplam_skor'].median()
        self.df_encoded['siniflandirma'] = (self.df_encoded['toplam_skor'] > threshold).astype(int)
        
        print(f"✅ Veri işlendi - {len(self.df_encoded)} film")
    
    def oneri_sistemi_hazirla(self):
        """Öneri sistemi hazırlama"""
        print("🤖 Öneri sistemi hazırlanıyor...")
        
        # Özellik seçimi
        feature_columns = ['genre_encoded', 'country_encoded', 'directors_encoded', 
                          'year', 'duration', 'mizah', 'aksiyon', 'romantizm', 
                          'gerilim', 'drama', 'ritim', 'gorsel', 'muzik', 'yaraticilik']
        
        # Özellik matrisini oluştur
        feature_data = []
        for _, row in self.df_encoded.iterrows():
            features = []
            for col in feature_columns:
                features.append(str(row[col]))
            feature_data.append(' '.join(features))
        
        # CountVectorizer
        vectorizer = CountVectorizer()
        self.feature_matrix = vectorizer.fit_transform(feature_data)
        
        # Cosine Similarity
        self.cosine_sim = cosine_similarity(self.feature_matrix)
        
        print(f"✅ Öneri sistemi hazır - {self.feature_matrix.shape} feature matrix")
    
    def regresyon_modeli_hazirla(self):
        """Regresyon modeli hazırlama"""
        print("📈 Regresyon modeli hazırlanıyor...")
        
        # Özellikler ve hedef
        features = ['genre_encoded', 'country_encoded', 'directors_encoded', 
                   'year', 'duration', 'mizah', 'aksiyon', 'romantizm', 'gerilim']
        
        X = self.df_encoded[features]
        y = self.df_encoded['avg_vote']
        
        # Veri bölme
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Ölçekleme
        self.scaler = StandardScaler()
        X_train_scaled = self.scaler.fit_transform(X_train)
        
        # Model eğitimi
        self.regression_model = LinearRegression()
        self.regression_model.fit(X_train_scaled, y_train)
        
        print(f"✅ Regresyon modeli hazır - {len(X_train)} eğitim örneği")
    
    def film_ara(self, film_adi):
        """Film arama"""
        film_adi = film_adi.lower()
        matches = self.df[self.df['movie_title'].str.lower().str.contains(film_adi, na=False)]
        return matches
    
    def oneri_al(self, film_adi, adet=5):
        """Film önerisi al"""
        # Film ara
        matches = self.film_ara(film_adi)
        
        if len(matches) == 0:
            return None
        
        # İlk eşleşmeyi al
        film_idx = matches.index[0]
        
        # Benzerlik skorları
        sim_scores = list(enumerate(self.cosine_sim[film_idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        
        # En benzer filmleri al (kendisi hariç)
        sim_indices = [i[0] for i in sim_scores[1:adet+1]]
        
        # Önerilen filmler
        oneriler = self.df.iloc[sim_indices].copy()
        oneriler['benzerlik_skoru'] = [sim_scores[i+1][1] for i in range(len(sim_indices))]
        
        return oneriler
    
    def rating_tahmin(self, ozellikler):
        """Rating tahmini"""
        if self.regression_model is None or self.scaler is None:
            return None
        
        # Özellikleri ölçekle
        X_scaled = self.scaler.transform([ozellikler])
        
        # Tahmin
        tahmin = self.regression_model.predict(X_scaled)
        
        return round(tahmin[0], 2)
    
    def istatistik_goster(self):
        """Sistem istatistikleri"""
        if self.df is None:
            return
        
        print(f"\n📊 Sistem İstatistikleri:")
        print(f"📱 Toplam film sayısı: {len(self.df):,}")
        print(f"🎭 Farklı tür sayısı: {self.df['genre'].nunique()}")
        print(f"🌍 Farklı ülke sayısı: {self.df['country'].nunique()}")
        print(f"🎥 Farklı yönetmen sayısı: {self.df['directors'].nunique()}")
        print(f"⭐ Ortalama rating: {self.df['avg_vote'].mean():.1f}")
        print(f"⏱️ Ortalama süre: {self.df['duration'].mean():.0f} dakika")
        
        if self.df_encoded is not None:
            print(f"🎯 Üst sınıf film sayısı: {self.df_encoded['siniflandirma'].sum():,}")
            print(f"📉 Alt sınıf film sayısı: {(len(self.df_encoded) - self.df_encoded['siniflandirma'].sum()):,}")

def main():
    """Ana uygulama"""
    
    try:
        # Sistem başlat
        sistem = FilmOneriSistemi()
        
        while True:
            print(f"\n" + "="*60)
            print(f"🎬 Film Öneri Sistemi - Ana Menü")
            print(f"="*60)
            print(f"1️⃣  Film Önerisi Al")
            print(f"2️⃣  Rating Tahmini Yap")
            print(f"3️⃣  Film Ara")
            print(f"4️⃣  Sistem İstatistikleri")
            print(f"5️⃣  Popüler Filmler")
            print(f"6️⃣  Çıkış")
            print(f"="*60)
            
            secim = input(f"🎯 Seçiminizi yapın (1-6): ").strip()
            
            if secim == '1':
                print(f"\n🎬 Film Önerisi")
                film_adi = input(f"📝 Film adını girin: ").strip()
                
                if not film_adi:
                    print(f"❌ Lütfen bir film adı girin!")
                    continue
                
                print(f"🔍 '{film_adi}' için benzer filmler aranıyor...")
                
                oneriler = sistem.oneri_al(film_adi)
                
                if oneriler is None:
                    print(f"❌ '{film_adi}' filmi bulunamadı!")
                    print(f"💡 İpucu: Film adının bir kısmını yazmayı deneyin")
                else:
                    print(f"\n✅ '{film_adi}' için 5 benzer film:")
                    print(f"-" * 60)
                    
                    for i, (_, film) in enumerate(oneriler.iterrows(), 1):
                        print(f"{i}. 🎬 {film['movie_title']}")
                        print(f"   📊 Rating: {film['avg_vote']}")
                        print(f"   🎭 Tür: {film['genre']}")
                        print(f"   🌍 Ülke: {film['country']}")
                        print(f"   ⭐ Benzerlik: {film['benzerlik_skoru']:.3f}")
                        print()
            
            elif secim == '2':
                print(f"\n📈 Rating Tahmini")
                print(f"📝 Film özelliklerini girin (1-10 arası):")
                
                try:
                    # Basit özellik girişi
                    print(f"Tür kodunu girin (0-23):")
                    genre_code = int(input(f"🎭 Tür kodu: "))
                    
                    print(f"Ülke kodunu girin (0-22):")
                    country_code = int(input(f"🌍 Ülke kodu: "))
                    
                    print(f"Yönetmen kodunu girin (0-48):")
                    director_code = int(input(f"🎥 Yönetmen kodu: "))
                    
                    year = int(input(f"📅 Yıl: "))
                    duration = int(input(f"⏱️ Süre (dakika): "))
                    mizah = int(input(f"😄 Mizah (1-10): "))
                    aksiyon = int(input(f"💥 Aksiyon (1-10): "))
                    romantizm = int(input(f"💕 Romantizm (1-10): "))
                    gerilim = int(input(f"😰 Gerilim (1-10): "))
                    
                    ozellikler = [genre_code, country_code, director_code, 
                                 year, duration, mizah, aksiyon, romantizm, gerilim]
                    
                    tahmin = sistem.rating_tahmin(ozellikler)
                    
                    if tahmin:
                        print(f"\n✅ Tahmin edilen rating: {tahmin}/10")
                        if tahmin >= 7:
                            print(f"🌟 Harika film olacak!")
                        elif tahmin >= 5:
                            print(f"👍 İyi film olacak!")
                        else:
                            print(f"👎 Ortalama altı film olacak!")
                    else:
                        print(f"❌ Tahmin yapılamadı!")
                        
                except ValueError:
                    print(f"❌ Lütfen geçerli sayılar girin!")
            
            elif secim == '3':
                print(f"\n🔍 Film Arama")
                arama = input(f"📝 Aranacak film adı: ").strip()
                
                if not arama:
                    print(f"❌ Lütfen bir arama terimi girin!")
                    continue
                
                sonuclar = sistem.film_ara(arama)
                
                if len(sonuclar) == 0:
                    print(f"❌ '{arama}' için sonuç bulunamadı!")
                else:
                    print(f"\n✅ '{arama}' için {len(sonuclar)} sonuç:")
                    print(f"-" * 60)
                    
                    for i, (_, film) in enumerate(sonuclar.head(10).iterrows(), 1):
                        print(f"{i}. 🎬 {film['movie_title']}")
                        print(f"   📊 Rating: {film['avg_vote']}")
                        print(f"   🎭 Tür: {film['genre']}")
                        print(f"   📅 Yıl: {film['year']}")
                        print()
            
            elif secim == '4':
                sistem.istatistik_goster()
            
            elif secim == '5':
                print(f"\n🌟 En Popüler Filmler (Yüksek Rating)")
                populer = sistem.df.nlargest(10, 'avg_vote')
                
                print(f"-" * 60)
                for i, (_, film) in enumerate(populer.iterrows(), 1):
                    print(f"{i}. 🎬 {film['movie_title']}")
                    print(f"   ⭐ Rating: {film['avg_vote']}")
                    print(f"   🎭 Tür: {film['genre']}")
                    print(f"   📅 Yıl: {film['year']}")
                    print()
            
            elif secim == '6':
                print(f"\n👋 Film Öneri Sistemi kapatılıyor...")
                print(f"🎬 İyi filmler!")
                break
            
            else:
                print(f"❌ Geçersiz seçim! Lütfen 1-6 arası bir sayı girin.")
            
            input(f"\n⏸️ Devam etmek için Enter'a basın...")
    
    except KeyboardInterrupt:
        print(f"\n\n👋 Program kullanıcı tarafından sonlandırıldı.")
    except Exception as e:
        print(f"\n❌ Hata oluştu: {e}")
        print(f"🔧 Detay: {traceback.format_exc()}")
    
    finally:
        print(f"\n🎬 Teşekkürler!")

if __name__ == "__main__":
    main()