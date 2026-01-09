"""
Film Öneri Sistemi - EXE Build Scripti
PyInstaller ile çift tıklanabilir EXE dosyası oluşturur
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

def create_exe():
    """EXE dosyası oluştur"""
    print("🚀 Film Öneri Sistemi EXE Build Başlatılıyor...")
    print("=" * 60)
    
    # Python scripti dosyası
    script_file = "film_oneri_sistemi.py"
    
    if not os.path.exists(script_file):
        print(f"❌ {script_file} dosyası bulunamadı!")
        return False
    
    # Build öncesi temizlik
    clean_build_folders()
    
    print(f"📦 PyInstaller ile EXE oluşturuluyor...")
    
    # PyInstaller komutu
    cmd = [
        "pyinstaller",
        "--onefile",  # Tek dosya
        "--windowed",  # Konsol penceresi gizle (GUI için)
        "--noconsole",  # Konsol yok
        "--name=FilmOneriSistemi",  # EXE dosya adı
        "--icon=NONE",  # İkon yok
        "--clean",  # Temiz build
        "--noconfirm",  # Onay sorma
        "--distpath=../outputs",  # Çıktı klasörü
        script_file
    ]
    
    # Windows console modunda çalıştır (kullanıcı etkileşimi için)
    console_cmd = [
        "pyinstaller",
        "--onefile",  # Tek dosya
        "--console",  # Konsol aç
        "--name=FilmOneriSistemi",  # EXE dosya adı
        "--icon=NONE",  # İkon yok
        "--clean",  # Temiz build
        "--noconfirm",  # Onay sorma
        "--distpath=../outputs",  # Çıktı klasörü
        script_file
    ]
    
    try:
        print(f"⚙️ PyInstaller çalıştırılıyor...")
        print(f"📄 Komut: {' '.join(console_cmd)}")
        
        # PyInstaller'ı çalıştır
        result = subprocess.run(console_cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ EXE dosyası başarıyla oluşturuldu!")
            
            # EXE dosya yolu
            exe_path = "../outputs/FilmOneriSistemi.exe"
            
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
                print(f"  🎯 Mod: Console (Kullanıcı etkileşimi)")
                
                return True
            else:
                print(f"❌ EXE dosyası oluşturulamadı!")
                return False
        
        else:
            print(f"❌ PyInstaller hatası!")
            print(f"Hata: {result.stderr}")
            return False
    
    except Exception as e:
        print(f"❌ Build hatası: {e}")
        return False
    
    finally:
        # Build sonrası temizlik
        print(f"\n🧹 Build dosyaları temizleniyor...")
        clean_build_folders()

def test_exe():
    """EXE dosyasını test et"""
    exe_path = "../outputs/FilmOneriSistemi.exe"
    
    if os.path.exists(exe_path):
        print(f"\n🧪 EXE testi...")
        print(f"✅ Dosya mevcut: {exe_path}")
        
        size = os.path.getsize(exe_path) / (1024 * 1024)
        print(f"📊 Boyut: {size:.1f} MB")
        
        print(f"\n🎯 Test etmek için şu komutu çalıştırın:")
        print(f'  "{os.path.abspath(exe_path)}"')
        
        return True
    else:
        print(f"❌ EXE dosyası bulunamadı!")
        return False

def main():
    """Ana fonksiyon"""
    print("🎬 Film Öneri Sistemi - EXE Builder")
    print("=" * 60)
    
    # EXE oluştur
    if create_exe():
        # Test et
        if test_exe():
            print(f"\n🎉 EXE başarıyla oluşturuldu ve test edildi!")
            print(f"🎬 Artık FilmOneriSistemi.exe'ye çift tıklayarak çalıştırabilirsiniz!")
        else:
            print(f"❌ EXE test edilemedi!")
    else:
        print(f"❌ EXE oluşturulamadı!")
    
    print(f"\n🔧 Build tamamlandı.")

if __name__ == "__main__":
    main()