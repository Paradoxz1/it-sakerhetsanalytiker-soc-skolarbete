Välkommen till verkligheten!

Grattis! Ni har precis fått ert första riktiga uppdrag som junior systemadministratörer. Ett litet företag (vi kallar dem “Kaos AB”) har precis insett att de inte kan fortsätta hantera sina servrar genom att ropa “Hej Teknisk Support!” varje gång något går fel.

Er uppgift? Rädda dem från kaoset!

Ni ska sätta upp ett Linux-system som faktiskt är säkert (ja, root-inloggning är förbjudet - vi är inte barbarer), skapa smarta skript som gör jobbet medan ni dricker kaffe, och se till att backuper faktiskt existerar innan hårddisken kraschar klockan 03:00 en söndagsnatt.


Uppgift 1:

Installera en Linux-distribution (Ubuntu Server, Debian eller liknande) i en virtuell miljö via Hyper-V. Du kan använda WSL för Linux-VM, och om SSH inte är igång eller installerat, starta eller vid behov installera open-ssh via apt-get install.

Konfigurera grundläggande säkerhet:
  Konfigurera en brandvägg (ufw eller iptables)
  Inaktivera root-inloggning via SSH (för säkerhets skull och för att imponera på framtida arbetsgivare)
  Konfigurera SSH med nyckelbaserad autentisering (ingen kommer ihåg lösenord ändå)

Installera nödvändiga paket för projektet

Uppgift 2:
Skapa följande struktur:

* 3 grupper: developers, admins, users
* 5 användare fördelade på grupperna
* Konfigurera sudo-rättigheter för admins-gruppen (makt åt folket… men bara vissa folk)
* Skapa en delad mapp för varje grupp med korrekta rättigheter (chmod 777 är INTE lösningen här, trust us)

Uppgift 3:
Skapa minst tre funktionella Bash-skript:

Skript 1: Backup-skript (backup.sh)
‘Det enda som står mellan er och en panikattack kl 03:00’

* Ta backup av en vald mapp
* Komprimera backupen med datum i filnamnet
* Radera backuper äldre än 7 dagar (disk space växer inte på träd)
* Logga varje backup-operation till en loggfil (för när chefen frågar “har ni backup?”)

Skript 2: Användarhanteringsskript (user_manager.sh)
‘Ett GUI… fast i terminalen. Vi lever i framtiden!’

Meny med alternativ för att:
  * Skapa ny användare
  * Ta bort användare (med stor försiktighet)
  * Lista alla användare i systemet
  * Lägga till användare i grupp
* Felhantering och användarvänliga meddelanden (programmet ska inte bara säga “Error” och försvinna)
  
Antingen: Användarinmatning och “menyval” från en enkel numrerad meny (read-kommandot) eller hjälpfunktion ./user-handler.sh -help som förklarar vilka parametrar jag kan skicka till skriptet och avläsning av inargument med “$1”, “$2” etc.

Skript 3: Systemrapport och logganalys (system_report.sh)
‘CSI: Linux Edition - Vem försökte logga in 47 gånger från Ryssland?’

Detta skript ska generera en säkerhets- och aktivitetsrapport genom att analysera systemloggar. Skriptet måste använda kommandona grep, tail, awk/sed och pipes för att:

* Visa de senaste 10 misslyckade inloggningsförsöken (spoiler: det är alltid någon som glömt sitt lösenord)
* Lista de 5 senast skapade användarna på systemet
* Visa vilka användare som använt sudo de senaste 24 timmarna (power corrupts!)
* Räkna antal SSH-anslutningar per IP-adress de senaste 100 loggraderna
* Visa aktuellt diskutrymme och markera om det är över 80% fullt (varning: log-filer och katt-videos tar plats)
* Spara rapporten till en fil med datum i filnamnet

Uppgift 4:

Konfigurera SSH för säker fjärråtkomst
Demonstrera anslutning från en annan dator/VM - dvs. det går utmärkt att emulera SSH-inloggning från annan dator genom att logga in från din host (Windows) till ditt Linux VM.
Implementera minst två säkerhetsåtgärder (t.ex. fail2ban, ändra SSH-port, använd SSH-nycklar)

Uppgift 5:
Skapa en README-fil som innehåller:

* Översikt över systemet (skriv så att er framtida själv förstår om 6 månader)
* Installationsinstruktioner (steg för steg, ingen ska behöva gissa)
* Beskrivning av alla skript med exempel på output
* Säkerhetskonfigurationer som gjorts
* Reflektion: Vilka utmaningar stötte ni på? Vad skulle ni gjort annorlunda? (Var ärliga - vi vet att något gick fel)
