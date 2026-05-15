import subprocess
import sys
from crewai.tools import BaseTool

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