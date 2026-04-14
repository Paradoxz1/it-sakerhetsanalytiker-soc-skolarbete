Beskrivning
I denna uppgift ska du konfigurera en virtuell nätverksmiljö som är både användarvänlig och säker. Detta innebär att du ska skapa en fungerande nätverksmiljö som är lätt att använda och samtidigt skyddad mot potentiella säkerhetsrisker.

Uppgiften består av två huvudsakliga delar: konfiguration och analys. Du ska konfigurera en virtuell nätverksmiljö med hänsyn till användbarhet och säkerhet, och sedan genomföra en analys för att identifiera säkerhetsrisker och föreslå förbättringar.

Syftet med uppgiften är att du ska få praktisk erfarenhet av att konfigurera och säkra en virtuell nätverksmiljö, samt att du ska utveckla din förmåga att analysera och identifiera säkerhetsrisker.

Slutligen ska du presentera din lösning och lämna in en rapport som beskriver din nätverksmiljö och de säkerhetsåtgärder du har vidtagit.

Rapporten ska innehålla en detaljerad beskrivning av din nätverksmiljö, de säkerhetsrisker du har identifierat och de åtgärder som kan tas, eller tagits, för att åtgärda dessa. Du ska även lämna in din exporterade konfiguration så att denna kan återskapas.

Uppgift 1: Grundläggande uppsättning
Router
  * eth0 kan prata med WAN, eth1 kan prata med LAN
  * Ett subnet på LAN ska vara 192.168.0.0/24
DHCP
  * Lease time ska vara 86400 sekunder (en dag)
  * Range på addresser på minst en router ska vara 192.168.0.20 - 192.168.0.50
DNS
  * Ett par maskiner för att verifiera att allt fungerar
  * Två per router per subnet för att verifiera att de kan kommunicera

Uppgift 2: Säkerhet
Firewall

Uppgift 3:
Implementering av minst en av följande punkter:
  * Logging & Monitoring
    * VyOS Monitoring Docs
    * VyOS Event Handling Docs
  * SSH till router för maintenance VyOS SSH Docs
  * Mer detaljerad Firewall Konfiguration VyOS Firewall Docs
  * Port forwarding, en statisk linux server med någon service VyOs DNAT Docs
  * Port forwarding, SSH med nycklar till ubuntu servrar VyOs DNAT Docs

