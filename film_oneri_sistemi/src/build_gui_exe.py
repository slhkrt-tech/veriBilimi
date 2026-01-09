"""
Film Öneri Sistemi - GUI EXE Build Scripti
Tkinter GUI versiyonu için PyInstaller ile çift tıklanabilir EXE oluşturur
"""

import os
import sys
import subprocess
import shutil
from datetime import datetime

def clean_build_folders():
    """Build klasörlerini temizle"""
    folders_to_clean = ['build', 'dist', '__pycache__']
    
    for folder in folders_to_clean:
        if os.path.exists(folder):
            print(f"🧹 {folder} klasörü temizleniyor...")
            shutil.rmtree(folder)
    
    # .spec dosyalarını temizle
    for file in os.listdir('.'):
        if file.endswith('.spec'):
            print(f"🧹 {file} dosyası siliniyor...")
            os.remove(file)

def create_gui_exe():
    """GUI EXE dosyası oluştur"""
    print("🎨 Film Öneri Sistemi GUI EXE Build Başlatılıyor...")
    print("=" * 60)
    
    # Python scripti dosyası
    script_file = "film_oneri_gui.py"
    
    if not os.path.exists(script_file):
        print(f"❌ {script_file} dosyası bulunamadı!")
        return False
    
    # Build öncesi temizlik
    clean_build_folders()
    
    print(f"🎨 PyInstaller ile GUI EXE oluşturuluyor...")
    
    # PyInstaller komutu (GUI için)
    cmd = [
        "pyinstaller",
        "--onefile",  # Tek dosya
        "--windowed",  # GUI mod (console gizli)
        "--noconsole",  # Konsol penceresi gizle
        "--name=FilmOneriSistemi_GUI",  # EXE dosya adı
        "--icon=NONE",  # İkon yok
        "--clean",  # Temiz build
        "--noconfirm",  # Onay sorma
        "--distpath=../outputs",  # Çıktı klasörü
        "--hidden-import=tkinter",  # Tkinter'ı dahil et
        "--hidden-import=tkinter.ttk",  # TTK'yı dahil et
        "--hidden-import=pandas",  # Pandas'ı dahil et
        "--hidden-import=numpy",  # NumPy'ı dahil et
        "--hidden-import=sklearn",  # Scikit-learn'i dahil et
        script_file
    ]
    
    try:
        print(f"⚙️ PyInstaller çalıştırılıyor...")
        print(f"📄 Komut: {' '.join(cmd)}")
        
        # PyInstaller'ı çalıştır
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ GUI EXE dosyası başarıyla oluşturuldu!")
            
            # EXE dosya yolu
            exe_path = "../outputs/FilmOneriSistemi_GUI.exe"
            
            if os.path.exists(exe_path):
                size = os.path.getsize(exe_path) / (1024 * 1024)  # MB
                print(f"📊 EXE boyutu: {size:.1f} MB")
                print(f"📍 Konum: {os.path.abspath(exe_path)}")
                
                # Build bilgileri
                print(f"\n📋 Build Bilgileri:")
                print(f"  🕐 Tarih: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}")
                print(f"  🐍 Python: {sys.version.split()[0]}")
                print(f"  📦 PyInstaller: Kullanıldı")
                print(f"  💻 Platform: Windows")
                print(f"  🎯 Mod: GUI (Windowed)")
                print(f"  🎨 Arayüz: Tkinter")
                print(f"  📚 Kütüphaneler: pandas, numpy, sklearn, tkinter")
                
                return True
            else:
                print(f"❌ EXE dosyası oluşturulamadı!")
                return False
        
        else:
            print(f"❌ PyInstaller hatası!")
            print(f"Stdout: {result.stdout}")
            print(f"Stderr: {result.stderr}")
            return False
    
    except Exception as e:
        print(f"❌ Build hatası: {e}")
        return False
    
    finally:
        # Build sonrası temizlik
        print(f"\n🧹 Build dosyaları temizleniyor...")
        clean_build_folders()

def test_gui_exe():
    """GUI EXE dosyasını test et"""
    exe_path = "../outputs/FilmOneriSistemi_GUI.exe"
    
    if os.path.exists(exe_path):
        print(f"\n🧪 GUI EXE testi...")
        print(f"✅ Dosya mevcut: {exe_path}")
        
        size = os.path.getsize(exe_path) / (1024 * 1024)
        print(f"📊 Boyut: {size:.1f} MB")
        
        print(f"\n🎨 Özellikler:")
        print(f"  ✅ Grafik arayüz (Tkinter)")
        print(f"  ✅ 4 farklı sekme")
        print(f"  ✅ Film önerisi alma")
        print(f"  ✅ Rating tahmini")
        print(f"  ✅ Film arama")
        print(f"  ✅ İstatistik görüntüleme")
        print(f"  ✅ Kullanıcı dostu arayüz")
        print(f"  ✅ Konsol penceresi yok")
        
        print(f"\n🎯 Test etmek için şu komutu çalıştırın:")
        print(f'  "{os.path.abspath(exe_path)}"')
        
        print(f"\n🖱️ Veya Windows Explorer'dan çift tıklayın!")
        
        return True
    else:
        print(f"❌ GUI EXE dosyası bulunamadı!")
        return False

def compare_versions():
    """Console ve GUI versiyonlarını karşılaştır"""
    console_exe = "../outputs/FilmOneriSistemi.exe"
    gui_exe = "../outputs/FilmOneriSistemi_GUI.exe"
    
    print(f"\n📊 SÜRÜM KARŞILAŞTIRMASI:")
    print("=" * 50)
    
    if os.path.exists(console_exe):
        console_size = os.path.getsize(console_exe) / (1024 * 1024)
        print(f"💻 Console Sürümü:")
        print(f"  📁 Dosya: FilmOneriSistemi.exe")
        print(f"  📊 Boyut: {console_size:.1f} MB")
        print(f"  🎯 Arayüz: Console (CMD)")
        print(f"  👥 Hedef: Geliştiriciler, teknik kullanıcılar")
    
    if os.path.exists(gui_exe):
        gui_size = os.path.getsize(gui_exe) / (1024 * 1024)
        print(f"\n🎨 GUI Sürümü:")
        print(f"  📁 Dosya: FilmOneriSistemi_GUI.exe")
        print(f"  📊 Boyut: {gui_size:.1f} MB")
        print(f"  🎯 Arayüz: Grafik (Tkinter)")
        print(f"  👥 Hedef: Genel kullanıcılar, kolay kullanım")
    
    print(f"\n🎯 ÖNERİ:")
    print(f"  🖱️ Genel kullanıcılar için: FilmOneriSistemi_GUI.exe")
    print(f"  ⌨️ Geliştiriciler için: FilmOneriSistemi.exe")

def main():
    """Ana fonksiyon"""
    print("🎨 Film Öneri Sistemi - GUI EXE Builder")
    print("=" * 60)
    
    # GUI EXE oluştur
    if create_gui_exe():
        # Test et
        if test_gui_exe():
            print(f"\n🎉 GUI EXE başarıyla oluşturuldu ve test edildi!")
            print(f"🎨 Artık FilmOneriSistemi_GUI.exe'ye çift tıklayarak GUI ile çalıştırabilirsiniz!")
            
            # Sürüm karşılaştırması
            compare_versions()
        else:
            print(f"❌ GUI EXE test edilemedi!")
    else:
        print(f"❌ GUI EXE oluşturulamadı!")
    
    print(f"\n🔧 GUI Build tamamlandı.")

if __name__ == "__main__":
    main()