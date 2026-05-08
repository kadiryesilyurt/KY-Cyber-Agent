import sys
from dotenv import load_dotenv

# Şifreleri yükle
load_dotenv()

# Ajanları çağır
from ky_sec_crew.crew import KySecCrew

def run():
    # --- SİBER GÜVENLİK NEON RENK PALETİ ---
    C1 = '\033[38;5;46m'  # Neon Yeşil
    C2 = '\033[38;5;226m' # Sarı
    C3 = '\033[38;5;208m' # Turuncu
    C4 = '\033[38;5;196m' # Kırmızı
    C5 = '\033[38;5;51m'  # Cyan / Mavi
    RST = '\033[0m'       # Sıfırla

    # Tam istediğin o şekilli ve renk geçişli (gradient) ASCII Art
    print(f"""
{C1}  _  __ __     __      {C4}  _____  ______   _____ 
{C1} | |/ / \\ \\   / /      {C4} / ____||  ____| / ____|
{C2} | ' /   \\ \\_/ /______{C3}| (___  | |__   | |     
{C2} |  <     \\   /______|{C3}  \\___ \\|  __|  | |     
{C3} | . \\     | |        {C2}  ____) | |____ | |____ 
{C3} |_|\\_\\    |_|        {C2} |_____/|______| \\_____|
    """)
    
    # Ekran görüntüsündeki o kutulu tasarımın aynısı!
    print(f"{C1}    +-+-+-+-+-+-+ {C2}+-+-+-+-+-+-+-+ {C4}+-+-+-+-+-+")
    print(f"{C1}    |K|Y|-|S|E|C| {C2}|O|T|O|N|O|M| | {C4}|A|J|A|N|I|")
    print(f"{C1}    +-+-+-+-+-+-+ {C2}+-+-+-+-+-+-+-+ {C4}+-+-+-+-+-+{RST}\n")
    
    print(f"{C5}[?] Hedef IP Adresini ve (varsa) Özel Talimatlarınızı Girin:{RST}")
    
    try:
        hedef = input(f"{C1}ky-sec > {RST}")
        
        if not hedef.strip():
            print(f"{C4}[!] Hedef girmediniz, operasyon iptal ediliyor.{RST}")
            sys.exit()
            
        inputs = {'user_instruction': hedef}
        
        print(f"\n{C4}[!] Hedef kilitlendi: {hedef}{RST}")
        print(f"{C2}[*] Yönetici Ajan uyanıyor, mürettebat toplanıyor...{RST}\n")
        
        KySecCrew().crew().kickoff(inputs=inputs)
        print(f"\n{C1}[+] Operasyon Tamamlandı! Çıktıyı ve rapor dosyasını kontrol edin.{RST}")
        
    except KeyboardInterrupt:
        print(f"\n\n{C4}[!] (Ctrl+C) Acil Çıkış Protokolü Devrede: Kullanıcı operasyonu durdurdu.{RST}")
        print(f"{C2}[*] Karargah sistemleri güvenle kapatılıyor. İyi avlar!{RST}\n")
        sys.exit(0)

if __name__ == "__main__":
    run()