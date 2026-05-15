from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import FileReadTool, FileWriterTool
from .tools.custom_tool import NmapTaramaAraci, OzelAramaAraci, DerinWebAnalizAraci

# 1. MOTORLARI TANIMLIYORUZ (En hızlı Flash Lite Preview)
isci_llm = "gemini/gemini-3.1-flash-lite"
yonetici_llm = "gemini/gemini-3.1-flash-lite"
# Araçlarımızı hazır ediyoruz
arama_motoru = OzelAramaAraci()
dosya_okuyucu = FileReadTool()
dosya_not_yazici = FileWriterTool() # Sadece kritik notları yazacak silahımız


@CrewBase
class KySecCrew():
    """KY-Sec Hızlı & İnteraktif Siber Güvenlik Karargahı"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # --- AJANLARIN OLUŞTURULMASI ---
    @agent
    def recon_specialist(self) -> Agent:
        return Agent(
            config=self.agents_config['recon_specialist'],
            llm=isci_llm,
            tools=[NmapTaramaAraci(), dosya_okuyucu],
            verbose=False # Gereksiz kutuları kapatıyoruz
        )

    @agent
    def vuln_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['vuln_analyst'],
            llm=isci_llm,
            tools=[arama_motoru, dosya_okuyucu,NmapTaramaAraci(), DerinWebAnalizAraci()],
            verbose=False
        )

    @agent
    def note_taker(self) -> Agent:
        """Raporcu yerine sadece kısa notlar alan Not Tutucu"""
        return Agent(
            role="Not Tutucu",
            goal="Operasyon sırasında bulunan kritik bilgileri (şifre, port, URL) en kısa haliyle kaydetmek.",
            backstory="Sen bir rapor yazarı değilsin. Sen bir operasyon günlüğü tutuyorsun. Sadece bulguları yazarsın.",
            llm=isci_llm,
            tools=[dosya_not_yazici],
            verbose=False
        )

    # --- GÖREVLERİN OLUŞTURULMASI ---
    @task
    def recon_task(self) -> Task:
        return Task(
            config=self.tasks_config['recon_task']
        )

    @task
    def vuln_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['vuln_analysis_task']
        )

    @task
    def notes_task(self) -> Task:
        """Uzun rapor yerine kısa TXT notu tutan görev"""
        return Task(
            description="""
                Bulunan tüm bilgileri özetle. ASLA rapor formatında yazma. 
                Sadece şunları içeren kısa bir 'ganimet.txt' oluştur:
                - Hedef IP
                - Açık Portlar
                - Olası Zafiyetler
                - Varsa tahmin edilen şifreler/kullanıcı adları.
            """,
            expected_output="Kritik bilgilerin kaydedildiği ganimet.txt dosyası.",
            agent=self.note_taker(),
            output_file='ganimet.txt' # Rapor değil, ganimet listesi!
        )

    # --- MÜRETTEBATIN VE HİYERARŞİNİN KURULMASI ---
    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.hierarchical,
            manager_llm=yonetici_llm,
            memory=False, # Donanım hatasını önlemek için kapalı kalsın
            verbose=True # Pavyon ışıklarını (gereksiz loglar) kapatıyoruz
        )