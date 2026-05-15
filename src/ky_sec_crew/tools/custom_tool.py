import subprocess
import sys
from crewai.tools import BaseTool
import requests
import pyautogui
import time
import os

class NmapTaramaAraci(BaseTool):
    name: str = "terminal_araci"
    description: str = "Sisteme nmap, gobuster gibi terminal komutları gönderir."
    
    def _run(self, command: str) -> str:
        # Renk kodları (ANSI Escape Codes)
        C_CYAN = '\033[96m'
        C_GREEN = '\033[92m'
        C_RESET = '\033[0m'
        
        print(f"\n{C_CYAN}============================================================{C_RESET}")
        print(f"{C_CYAN}[SİSTEM TAVSİYESİ]: Ajan şu komutu ateşlemek istiyor:{C_RESET}")
        # İŞTE BURASI: Komut yemyeşil yazacak!
        print(f"{C_GREEN}Komut: {command}{C_RESET}") 
        print(f"{C_CYAN}============================================================{C_RESET}")
        
        onay = input("Onaylıyor musun? (Y/N): ")
        
        if onay.lower() == 'y':
            print(f"\n[SİSTEM]: Çalıştırılıyor... (Çıktı canlı aktarılıyor)\n")
            
            # Popen ile canlı akış (live streaming)
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            
            full_output = ""
            # Çıktıyı satır satır okuyup ekrana basıyoruz
            for line in process.stdout:
                sys.stdout.write(line)
                sys.stdout.flush()
                full_output += line
                
            process.wait() # İşlem bitene kadar bekle
            
            return f"Komut çalıştı. Çıktı:\n{full_output}\n\nBu çıktıya göre YALNIZCA TEK BİR CÜMLE ile sıradaki hamleyi Terminal Araci'na gönder."
        else:
            return "Kullanıcı bu komutu reddetti. Neden reddetmiş olabileceğini düşün ve farklı bir araç/komut öner."

class OzelAramaAraci(BaseTool):
    name: str = "Web Zafiyet Arama Aracı"
    description: str = "DuckDuckGo üzerinden bulunan servislerin CVE ve zafiyet (exploit) araştırmasını yapar."
    
    def _run(self, query: str) -> str:
        # Langchain arama aracını burada çağırıyoruz
        from langchain_community.tools import DuckDuckGoSearchRun
        search = DuckDuckGoSearchRun()
        print(f"\n[*] Ajan sessizce internette araştırıyor: {query} ...")
        return search.run(query)
    
class DerinWebAnalizAraci(BaseTool):
    name: str = "derin_web_analiz_araci" 
    description: str = "Hedef web dizininin HTML kaynak kodunu analiz eder ve aktif ekranın görsel kaydını (screenshot) alarak kanıt oluşturur."
    
    def _run(self, url: str) -> str:
        # Kurumsal Terminal Renkleri
        C_CYAN = '\033[96m'
        C_GREEN = '\033[92m'
        C_RESET = '\033[0m'

        print(f"\n{C_CYAN}============================================================{C_RESET}")
        print(f"{C_CYAN}[SİSTEM TAVSİYESİ]: Ajan {url} adresinde potansiyel bilgi/zafiyet sezdi.{C_RESET}")
        print(f"{C_GREEN}Tavsiye: Gelişmiş Web Analizi (Görsel Kayıt + Kaynak Kod İncelemesi){C_RESET}")
        print(f"{C_CYAN}============================================================{C_RESET}")
        
        onay = input("Analizi başlatmak için terminale 'analiz' veya 'Y' yazın: ")
        
        if onay.lower() == 'analiz' or onay.lower() == 'y':
            print("\n[*] Lütfen tarayıcıda ilgili sekmeyi aktif edin. Görsel kayıt 3 saniye içinde alınacaktır.")
            time.sleep(1)
            print("3...")
            time.sleep(1)
            print("2...")
            time.sleep(1)
            print("1...")
            print("[*] Görsel kanıt kaydediliyor...\n")
            
            # 1. Aşama: Görsel Kanıt
            try:
                screenshot = pyautogui.screenshot()
                screenshot.save("kanit_ekran.png")
                foto_durum = "Ekran görseli 'kanit_ekran.png' olarak başarıyla oluşturuldu."
                print(f"[+] {foto_durum}")
            except Exception as e:
                foto_durum = f"Görsel kayıt alınamadı: {e}"
                print(f"[-] {foto_durum}")

            # 2. Aşama: Kaynak Kod İncelemesi
            print("[*] Kaynak kod (HTML) analizi arka planda başlatılıyor...")
            try:
                response = requests.get(url, timeout=5)
                html_content = response.text
                snippet = html_content[:2500] 
                
                print("[+] Kaynak kod başarıyla çekildi. Ajan analize başlıyor...\n")
                
                return f"Operasyon sonucu: {foto_durum}\n\nİşte hedefin HTML kaynak kodunun bir kısmı:\n{snippet}\n\nGÖREV: Bu HTML kodu içinde gizli bir yorum satırı (), 'password', 'admin', 'version' gibi kritik veya unutulmuş bir bilgi var mı? Varsa YALNIZCA TEK BİR CÜMLE ile kullanıcıya özetle."
                
            except Exception as e:
                return f"Kaynak koda ulaşılamadı: {e}"
        else:
            return "Kullanıcı analiz operasyonunu reddetti. Farklı bir vektör öner."