import random
from decimal import Decimal, ROUND_HALF_UP
import customtkinter
from customtkinter import set_appearance_mode, set_default_color_theme
import ipaddress

set_appearance_mode("light")
set_default_color_theme("blue")


class Mathetrainer(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title('Fachinformatiker Mathetrainer Pro')
        self.geometry('1024x900')

        self.tr_window = None
        self.note_window = None
        self.hilfe_window = None
        #Hilfe Lexikon
        self.hilfe_texte = {
            "binär": (
                "--- DEZIMAL -> BINÄR (Modulo-Methode) ---\n\n"
                "1. Teile die Zahl durch 2.\n"
                "2. Den Rest (0 oder 1) schreibst du von RECHTS nach LINKS auf.\n\n"
                "Beispiel 13:\n"
                "13 : 2 = 6 Rest 1  ---> [Bit ganz rechts]          (1)\n"
                " 6 : 2 = 3 Rest 0  ---> [Nächstes Bit links daneben] (01)\n"
                " 3 : 2 = 1 Rest 1  ---> [Und noch eins links]      (101)\n"
                " 1 : 2 = 0 Rest 1  ---> [Letztes Bit ganz links]  (1101)\n\n"
                "MERKE: Der ERSTE Rest ist immer die Einer-Stelle (ganz rechts).\n"
                "------------------------------------------\n\n"
                "--- BINÄR -> DEZIMAL (Stellenwert-Methode) ---\n\n"
                "Schreibe die Zweierpotenzen über die Binärzahl:\n"
                "Wert:  128 | 64 | 32 | 16 | 8 | 4 | 2 | 1\n"
                "Bit:    0  |  0 |  0 |  0 | 1 | 1 | 0 | 1\n\n"
                "Rechnung: Überall wo eine '1' steht, addierst du den Wert:\n"
                "8 + 4 + 1 = 13"
            ),
            "hexadezimal": (
                "--- DAS HEXADEZIMAL-SYSTEM (Basis 16) ---\n\n"
                "Hex nutzt 16 Symbole: 0, 1, 2, 3, 4, 5, 6, 7, 8, 9 und\n"
                "A=10, B=11, C=12, D=13, E=14, F=15\n\n"
                "------------------------------------------\n"
                "1. HEX -> DEZIMAL (Stellenwert-Methode)\n"
                "Jede Stelle hat den Wert 16^x (1, 16, 256, 4096...).\n\n"
                "Beispiel '3F4':\n"
                "  4 * 1    =      4\n"
                "  F * 16   =    240 (denn F=15, also 15*16)\n"
                "  3 * 256  =    768\n"
                "  SUMME    =   1012\n\n"
                "------------------------------------------\n"
                "2. DEZIMAL -> HEX (Modulo-Methode)\n"
                "Teile durch 16 und notiere den Rest.\n\n"
                "Beispiel 1012:\n"
                "  1012 : 16 = 63 Rest 4  -> [4]\n"
                "    63 : 16 =  3 Rest 15 -> [F]\n"
                "     3 : 16 =  0 Rest 3  -> [3]\n"
                "Ergebnis (von unten nach oben): 3F4\n\n"
                "------------------------------------------\n"
                "3. HEX <-> BINÄR (Die 8-4-2-1 Methode)\n"
                "Jedes Hex-Zeichen entspricht GENAU 4 Bit (ein Nibble).\n\n"
                "Hex '3F4' zu Binär:\n"
                "  3 -> 0011\n"
                "  F -> 1111\n"
                "  4 -> 0100\n"
                "Ergebnis: 0011 1111 0100\n\n"
                "Binär zu Hex: Gruppiere immer 4 Bits von RECHTS beginnend\n"
                "und wandle jede Gruppe einzeln in ein Hex-Zeichen um."
            ),

            "speichergrößen": (
                "--- SPEICHERGRÖSSEN & UMRECHNUNG ---\n\n"
                "Es gibt zwei Arten von Präfixen:\n"
                "1. BINÄR (IEC): KiB, MiB, GiB, TiB (Faktor 1024)\n"
                "2. DEZIMAL (SI): KB, MB, GB, TB (Faktor 1000)\n\n"
                "REIHENFOLGE: Byte -> Kilo -> Mega -> Giga -> Tera\n\n"
                "------------------------------------------\n"
                "1. RECHNEN INNERHALB EINES SYSTEMS\n"
                "• In kleinere Einheit (z.B. GiB -> MiB): Multiplizieren (*)\n"
                "• In größere Einheit (z.B. MiB -> GiB): Dividieren (/)\n\n"
                "Beispiel: 4 GiB in MiB\n"
                "Rechnung: 4 * 1024 = 4096 MiB\n\n"
                "------------------------------------------\n"
                "2. WECHSEL (BINÄR <-> DEZIMAL)\n"
                "Wenn du von GiB nach GB umrechnen musst, führt der Weg immer über die kleinste gemeinsame Einheit (Byte).\n\n"
                "Beispiel: 1 TiB in TB umrechnen\n"
                "1. Schritt (zu Byte): 1 * 1024 * 1024 * 1024 * 1024\n"
                "2. Schritt (zu TB): Ergebnis / 1000 / 1000 / 1000 / 1000\n\n"
                "KURZFORM für den Wechsel:\n"
                "• Binär zu Dezimal: Wert * (1024 / 1000)^Ebene\n"
                "• Dezimal zu Binär: Wert * (1000 / 1024)^Ebene\n"
                "(Ebene: Kilo=1, Mega=2, Giga=3, Tera=4)\n\n"
                "------------------------------------------\n"
                "WICHTIG:\n"
                "• 1 Byte = 8 Bit\n"
                "• IHK-Tipp: 'Festplattenkapazität' wird oft dezimal (1000) angegeben, 'Arbeitsspeicher' binär (1024)."

            ),

            "downloadgeschwindigkeit": (
                "--- DOWNLOADZEIT BERECHNEN ---\n\n"
                "Der wichtigste Schritt ist das Angleichen der Einheiten (Bit vs. Byte).\n\n"
                "--- SCHRITT-FÜR-SCHRITT-ANLEITUNG ---\n\n"
                "1. DATEI IN MBIT UMRECHNEN:\n"
                "   Dateigrößen werden in Byte (GB) angegeben, Leitungen in Bit (Mbit/s).\n"
                "   Rechnung: GB * 1024 (zu MB) * 8 (zu Mbit).\n"
                "   Beispiel: 10 GB = 10 * 1024 * 8 = 81.920 Mbit.\n\n"
                "2. ZEIT IN SEKUNDEN BERECHNEN:\n"
                "   Formel: Zeit (s) = Datenmenge (Mbit) / Leitung (Mbit/s).\n"
                "   Beispiel: 81.920 Mbit / 100 Mbit/s = 819,2 Sekunden.\n\n"
                "3. IN MINUTEN ODER STUNDEN UMRECHNEN:\n"
                "   • Sekunden -> Minuten: Durch 60 teilen.\n"
                "   • Minuten -> Stunden: Nochmal durch 60 teilen.\n"
                "   Beispiel: 819,2s / 60 = 13,65 Minuten.\n\n"
                "------------------------------------------\n"
                "MERKE:\n"
                "• Faktor 8: Um von Byte zu Bit zu kommen.\n"
                "• Faktor 1024: Um von Giga zu Mega zu kommen.\n"
                "• Faktor 60: Für die Zeitumrechnung."

            ),

            "elektrotechnik (u, i, r, p)": (
                "--- GRUNDLAGEN DER ELEKTROTECHNIK ---\n\n"
                "Es gibt zwei Hauptformeln, die du beherrschen musst:\n"
                "1. Das Ohmsche Gesetz: U = R * I  (Spannung = Widerstand * Strom)\n"
                "2. Die elektrische Leistung: P = U * I (Leistung = Spannung * Strom)\n\n"
                "EINHEITEN:\n"
                "• U: Spannung in Volt (V)\n"
                "• I: Stromstärke in Ampere (A)  <-- ACHTUNG: 1000 mA = 1 A!\n"
                "• R: Widerstand in Ohm (Ω)\n"
                "• P: Leistung in Watt (W)\n\n"
                "------------------------------------------\n"
                "SPEZIALFALL: VORWIDERSTAND BERECHNEN\n"
                "Wenn ein Bauteil (z.B. eine LED) weniger Spannung verträgt als die Quelle liefert,\n"
                "muss der Rest am Widerstand 'verbraten' werden.\n\n"
                "SCHRITT-FÜR-SCHRITT :\n"
                "Quelle: 24V | Bauteil: 3,3V | Strom: 130 mA\n\n"
                "1. SPANNUNG AM WIDERSTAND (Ur) BERECHNEN:\n"
                "   Ur = U_quelle - U_bauteil\n"
                "   Ur = 24V - 3,3V = 20,7V\n\n"
                "2. EINHEIT UMRECHNEN:\n"
                "   130 mA / 1000 = 0,13 A\n\n"
                "3. WIDERSTAND (R) BERECHNEN:\n"
                "   Formel: R = Ur / I\n"
                "   Rechnung: 20,7V / 0,13 A = 159,23 Ohm\n\n"
                "------------------------------------------\n"
                "TIPP FÜR DIE PRÜFUNG:\n"
                "Merk dir das 'URI'-Dreieck. Was du suchst, hältst du zu:\n"
                "• U oben, R und I unten nebeneinander."
            ),

            "subnetting": (
                "--- SUBNETTING SCHRITT-FÜR-SCHRITT ---\n\n"
                "Beispiel"
                ": 192.168.62.0 /23\n\n"
                "1. DIE MASKE (Subnetzmaske):\n"
                "Die Zahl nach dem '/' (CIDR) gibt an, wie viele Bits '1' sind.\n"
                "• /23 bedeutet: 8 + 8 + 7 Bits sind gesetzt.\n"
                "• Oktett 1-3: 255 . 255 . 254 (da das 8. Bit im 3. Oktett 0 ist).\n"
                "• Ergebnis: 255.255.254.0\n\n"
                "------------------------------------------\n"
                "2. DIE SPRUNGWEITE:\n"
                "Suche das 'interessante Oktett' (da, wo die Maske nicht 255 oder 0 ist).\n"
                "Rechnung: 256 - Maskenwert des Oktetts.\n"
                "• Hier (3. Oktett): 256 - 254 = 2.\n"
                "• Sprungweite ist 2. Alle Netze starten in 2er Schritten im 3. Oktett.\n\n"
                "------------------------------------------\n"
                "3. NETZ-ID & BROADCAST:\n"
                "• Netz-ID: Die Startadresse des Blocks.\n"
                "  Suche das Vielfache der Sprungweite (2), das knapp an der .62 liegt.\n"
                "  Da 62 durch 2 teilbar ist: 192.168.62.0.\n\n"
                "• Broadcast: Die Adresse VOR dem nächsten Netz.\n"
                "  Nächstes Netz wäre 62 + 2 = 64.0.\n"
                "  Eins davor ist: 192.168.63.255.\n\n"
                "------------------------------------------\n"
                "4. HOSTS (Nutzbare Adressen):\n"
                "Formel: 2^(Verbleibende Host-Bits) - 2\n"
                "• /23 lässt 32 - 23 = 9 Bits für Hosts.\n"
                "• 2^9 = 512.\n"
                "• Nutzbar: 512 - 2 = 510 Hosts.\n\n"
                "TIPP: Merk dir die Potenzen! 2^7=128, 2^8=256, 2^9=512, 2^10=1024."
            ),

            "handelskalkulation": (
                "--- DIE HANDELSKALKULATION ---\n\n"
                "Dieses Schema ist das Herzstück der kaufmännischen Steuerung.\n"
                "Man unterscheidet zwischen EINKAUFS- und VERKAUFSKALKULATION.\n\n"
                "------------------------------------------\n"
                "1. DAS GRUNDSCHEMA (Einkauf bis Selbstkosten)\n"
                "   Listeneinkaufspreis (LEP)\n"
                " - Lieferrabatt (% von LEP)\n"
                " = Zieleinkaufspreis (ZEP)\n"
                " - Lieferskonto (% von ZEP)\n"
                " = Bareinkaufspreis (BEP)\n"
                " + Bezugskosten (Porto, Fracht - absolut)\n"
                " = Bezugspreis (Einstandspreis)\n"
                " + Handlungskosten (% vom Bezugspreis)\n"
                " = SELBSTKOSTEN (Deine absolute Schmerzgrenze)\n\n"
                "------------------------------------------\n"
                "2. DAS VERKAUFSSCHEMA (Profit & Steuer)\n"
                "   Selbstkosten\n"
                " + Gewinnzuschlag (% von Selbstkosten)\n"
                " = Barverkaufspreis\n\n"
                "--- ACHTUNG: Die IHK-Falle im Verkauf ---\n"
                "Skonto, Provision und Rabatt im Verkauf werden IM HUNDERT berechnet!\n"
                "Rechnung: Betrag / (100 - Prozentsatz) * 100\n\n"
                " + Kundenskonto & Vertreterprovision\n"
                " = Zielverkaufspreis\n"
                " + Kundenrabatt\n"
                " = Nettoverkaufspreis (NVP)\n"
                " + Umsatzsteuer (19% von NVP)\n"
                " = BRUTTOVERKAUFSPREIS\n\n"
                "------------------------------------------\n"
                "WICHTIGE TIPPS:\n"
                "• Vorwärtskalkulation: Von oben nach unten rechnen.\n"
                "• Rückwärtskalkulation: Von unten nach oben (Vorzeichen umkehren!).\n"
                "• Bezugskosten werden addiert, Rabatte und Skonti abgezogen."
            ),

            "raid": (
                "--- RAID-SYSTEME (Redundant Array of Independent Disks) ---\n\n"
                "RAID dient dazu, mehrere physische Festplatten zu einem logischen\n"
                "Laufwerk zusammenzufassen, um Speed oder Sicherheit zu erhöhen.\n\n"
                "------------------------------------------\n"
                "1. RAID 0 (Striping - 'Daten-Streifen')\n"
                "• Fokus: Maximale Geschwindigkeit.\n"
                "• Kapazität: n * Kapazität der kleinsten Platte (Alle werden genutzt).\n"
                "• Ausfallsicherheit: NULL. Fällt eine Platte aus, sind ALLE Daten weg.\n"
                "• Beispiel (Dein Screen): 5 x 4 TB = 20 TB Nutzkapazität.\n\n"
                "------------------------------------------\n"
                "2. RAID 1 (Mirroring - 'Spiegelung')\n"
                "• Fokus: Maximale Sicherheit.\n"
                "• Kapazität: 1 * Kapazität der kleinsten Platte (Daten werden dupliziert).\n"
                "• Ausfallsicherheit: n-1 Platten dürfen ausfallen.\n\n"
                "------------------------------------------\n"
                "3. RAID 5 (Parität)\n"
                "• Fokus: Guter Kompromiss aus Speed und Sicherheit.\n"
                "• Kapazität: (n - 1) * Kapazität der kleinsten Platte.\n"
                "• Ausfallsicherheit: Genau 1 beliebige Platte darf ausfallen.\n"
                "• Mindestanzahl: 3 Festplatten.\n\n"
                "------------------------------------------\n"
                "4. RAID 10 (1+0 - 'Spiegelung von Stripes')\n"
                "• Fokus: High-End Performance + Sicherheit.\n"
                "• Kapazität: (n / 2) * Kapazität der kleinsten Platte.\n"
                "• Ausfallsicherheit: Mindestens 1 Platte (pro Mirror-Set).\n"
                "• Mindestanzahl: 4 Festplatten.\n\n"
                "------------------------------------------\n"
                "TIPP FÜR DEN TRAINER:\n"
                "Bei der Ausfallsicherheit im Trainer ist meist gefragt, WIE VIELE\n"
                "Platten maximal gleichzeitig kaputt gehen dürfen, ohne Datenverlust."
            ),

            "speicherbedarf": (
                "--- SPEICHERBEDARF (Bilder & Videos) ---\n\n"
                "Das Grundprinzip ist immer: Multipliziere alle Faktoren,\n"
                "um zuerst das Ergebnis in BIT zu erhalten.\n\n"
                "------------------------------------------\n"
                "1. BILDDATEI (Unkomprimiert)\n"
                "Formel: Breite * Höhe * Farbtiefe (in Bit)\n\n"
                "Beispiel:\n"
                "• Auflösung: 3840 x 768 Pixel\n"
                "• Farbtiefe: 16 Bit\n"
                "1. Rechnung (in Bit): 3840 * 768 * 16 = 47.185.920 Bit\n"
                "2. Zu Byte: 47.185.920 / 8 = 5.898.240 Byte\n"
                "3. Zu KB: 5.898.240 / 1024 = 5.760 KB\n"
                "4. Zu MB: 5.760 / 1024 = 5,625 MB\n\n"
                "------------------------------------------\n"
                "2. VIDEODATEI (Unkomprimiert)\n"
                "Formel: Bildgröße * Bilder pro Sekunde (FPS) * Zeit (s)\n\n"
                "Schritt-für-Schritt:\n"
                "1. Größe eines Einzelbildes berechnen (siehe oben).\n"
                "2. Mal FPS (z.B. 30 oder 60 Bilder/s).\n"
                "3. Mal Dauer des Videos in SEKUNDEN.\n"
                "4. Ergebnis durch 8 (Byte) und dann durch 1024 (KB, MB, GB) teilen.\n\n"
                "------------------------------------------\n"
                "WICHTIGE KONSTANTEN:\n"
                "• Farbtiefe: 8 Bit = 1 Byte pro Pixel, 24 Bit = 3 Byte pro Pixel.\n"
                "• Zeit: Rechne immer in Sekunden (1 Min = 60s).\n"
                "• Umrechnung: Nutze 1024 für KB/MB/GB (Binärpräfixe)."
            ),

            "verfügbarkeit": (
                "--- VERFÜGBARKEIT & SLA-BERECHNUNG ---\n\n"
                "Die Verfügbarkeit gibt an, wie lange ein System im Verhältnis zur\n"
                "geplanten Zeit betriebsbereit sein muss.\n\n"
                "------------------------------------------\n"
                "1. MAX. AUSFALLZEIT BERECHNEN\n"
                "Gesucht: Wie viele Minuten darf das System offline sein?\n\n"
                "Schritt-für-Schritt :\n"
                "• Zeitraum: 1 Quartal (90 Tage)\n"
                "• SLA-Level: 99,95%\n\n"
                "1. Gesamtzeit in Minuten berechnen:\n"
                "   90 Tage * 24 Std * 60 Min = 129.600 Minuten.\n\n"
                "2. Ausfall-Prozentsatz ermitteln:\n"
                "   100% - 99,95% = 0,05% zulässiger Ausfall.\n\n"
                "3. Ausfallzeit in Minuten berechnen:\n"
                "   129.600 Min * (0,05 / 100) = 64,8 Minuten.\n\n"
                "------------------------------------------\n"
                "2. VERFÜGBARKEIT IN PROZENT BERECHNEN\n"
                "Gesucht: Welches SLA-Level wurde erreicht?\n\n"
                "Formel: (Gesamtzeit - Ausfallzeit) / Gesamtzeit * 100\n\n"
                "Beispiel:\n"
                "• Gesamtzeit: 10.000 Min\n"
                "• Ausfall: 50 Min\n"
                "Rechnung: (10.000 - 50) / 10.000 * 100 = 99,5%.\n\n"
                "------------------------------------------\n"
                "WICHTIGE ZEITWERTE (Basis):\n"
                "• 1 Tag: 1.440 Minuten\n"
                "• 1 Monat (30 Tage): 43.200 Minuten\n"
                "• 1 Jahr (365 Tage): 525.600 Minuten"
            ),

            "netzplan": (
                "--- NETZPLAN-TECHNIK (Kritischer Pfad) ---\n\n"
                "Ein Netzplan hilft dabei, die Gesamtdauer eines Projekts und\n"
                "Zeitreserven (Puffer) der einzelnen Aufgaben zu berechnen.\n\n"
                "------------------------------------------\n"
                "1. VORWÄRTSRECHNUNG (Obere Zeile: FAZ & FEZ)\n"
                "Ziel: Frühestes Projektende ermitteln.\n\n"
                "• Start (Knoten A): FAZ = 0. FEZ = FAZ + Dauer.\n"
                "• Nachfolger: Der FEZ eines Knotens wird zum FAZ des nächsten.\n"
                "• WICHTIG (Zusammenfluss): Haben Knoten zwei Vorgänger (wie F im Bild),\n"
                "  nimm den GRÖSSEREN FEZ als neuen FAZ.\n\n"
                "------------------------------------------\n"
                "2. RÜCKWÄRTSRECHNUNG (Untere Zeile: SAZ & SEZ)\n"
                "Ziel: Spätesten Startzeitpunkt ohne Projektverzögerung finden.\n\n"
                "• Start am Ende: Übernehme den FEZ des letzten Knotens als SEZ.\n"
                "• Rechnung: SAZ = SEZ - Dauer.\n"
                "• WICHTIG (Verzweigung): Geht ein Pfeil zu zwei Vorgängern zurück,\n"
                "  nimm den KLEINEREN SAZ als neuen SEZ.\n\n"
                "------------------------------------------\n"
                "3. PUFFERZEITEN & KRITISCHER PFAD\n"
                "• Gesamtpuffer (GP): SAZ - FAZ (oder SEZ - FEZ).\n"
                "  Gibt an, um wie viel sich ein Vorgang maximal verzögern darf.\n"
                "• Freier Puffer (FP): FAZ(Nachfolger) - FEZ(aktuell).\n"
                "• KRITISCHER PFAD: Die Kette aller Knoten, bei denen der\n"
                "  Gesamtpuffer GENAU 0 ist. (Im Trainer: Gold markieren!)\n\n"
                "TIPP: Wenn du dich vorwärts verrechnest, stimmt hinten nichts mehr.\n"
                "Prüfe am Ende, ob FAZ und SAZ beim ersten Knoten wieder bei 0 landen!"
            ),

            "gantt-diagramm (zeitplan)": (
                "--- GANTT-DIAGRAMM (Zeitstrahl-Analyse) ---\n\n"
                "Ein Gantt-Diagramm visualisiert Projektaufgaben auf einer Zeitachse.\n"
                "Es zeigt, wann Aufgaben starten, wie lange sie dauern und\n"
                "welche Abhängigkeiten bestehen.\n\n"
                "------------------------------------------\n"
                "1. MODUS: ABLESEN (Dein aktueller Screen)\n"
                "Ziel: Wandle die Balken in numerische Werte um.\n\n"
                "• FAZ (Frühester Anfang): Wo beginnt der Balken?\n"
                "  Beispiel Analyse (A): Startet bei der Linie '0'. -> FAZ = 0.\n\n"
                "• FEZ (Frühester Ende): Wo hört der Balken auf?\n"
                "  Beispiel Analyse (A): Endet bei der Linie '5'. -> FEZ = 5.\n\n"
                "• DAUER: Die Länge des Balkens (FEZ - FAZ).\n"
                "  Beispiel Analyse (A): 5 - 0 = 5 Tage Dauer.\n\n"
                "------------------------------------------\n"
                "2. MODUS: BERECHNEN (Planung)\n"
                "Ziel: Erstelle den Zeitplan basierend auf Vorgängern.\n\n"
                "• Logik: Ein Balken kann erst starten, wenn der Vorgänger fertig ist.\n"
                "• Zusammenfluss (z.B. Vorgang D): Wenn D von B UND C abhängt,\n"
                "  darf D erst beim HÖHEREN FEZ von beiden starten.\n\n"
                "------------------------------------------\n"
                "WICHTIGE SYMBOLE & BEGRIFFE:\n"
                "• Meilenstein: Ein Ereignis ohne Dauer (oft als Raute dargestellt).\n"
                "• Kritischer Pfad: Die Kette von Balken ohne zeitliche Lücken.\n"
                "• Puffer: Sichtbar durch Lücken zwischen dem Ende eines Balkens\n"
                "  und dem Start des nächsten abhängigen Vorgangs."
            )
        }



        # Logik-Variablen
        self.aktuelle_zahl = 0
        self.korrektes_ergebnis = 0
        self.fehler_count = 0  # Counter für Fehlversuche
        self.sol_net = ""
        self.sol_bc = ""
        self.sol_mask = ""

        self.mode_switch = customtkinter.CTkSwitch(self, text="Dunkelmodus", command=self.change_appearance_mode)
        self.mode_switch.place(relx=0.82, rely=0.05)

        self.label = customtkinter.CTkLabel(self, text="Fachinformatiker Mathetrainer", font=("Arial", 24, "bold"))
        self.label.pack(pady=20)

        # Frames
        self.main_menu_frame = customtkinter.CTkFrame(self)
        self.binär_frame = customtkinter.CTkFrame(self)
        self.hex_frame = customtkinter.CTkFrame(self)
        self.speicher_frame = customtkinter.CTkFrame(self)
        self.storage_frame = customtkinter.CTkFrame(self)
        self.download_frame = customtkinter.CTkFrame(self)
        self.elektro_frame = customtkinter.CTkFrame(self)
        self.subnet_frame = customtkinter.CTkFrame(self)
        self.kalk_frame = customtkinter.CTkFrame(self)
        self.raid_frame = customtkinter.CTkFrame(self)
        self.availability_frame = customtkinter.CTkFrame(self)
        self.netzplan_frame = customtkinter.CTkFrame(self)
        self.gantt_frame = customtkinter.CTkFrame(self)

        self.alle_frames = [self.main_menu_frame, self.binär_frame, self.hex_frame,self.speicher_frame, self.download_frame, self.elektro_frame, self.subnet_frame, self.kalk_frame, self.raid_frame,self.storage_frame,self.availability_frame,self.netzplan_frame,self.gantt_frame]

        # UI Setups
        self.setup_main_menu()
        self.setup_binär_screen()
        self.setup_hex_screen()
        self.setup_speicher_screen()
        self.setup_download_screen()
        self.setup_elektro_screen()
        self.setup_subnet_screen()
        self.setup_kalkulation_screen()
        self.setup_raid_screen()
        self.setup_storage_screen()
        self.setup_availability_screen()
        self.setup_netzplan_screen()
        self.setup_gantt_screen()




        # "Zurück" und "Skip" Buttons für alle Trainer-Screens
        for seite in self.alle_frames[1:]:
            nav_frame = customtkinter.CTkFrame(seite, fg_color="transparent")
            nav_frame.pack(side="bottom", pady=20)

            # Rechner Button
            customtkinter.CTkButton(nav_frame, text="Rechner 🖩", command=self.toggle_taschenrechner,width=100, fg_color="#333333").pack(side="left", padx=5)

            #Hilfe Button
            customtkinter.CTkButton(nav_frame, text="Erklärung 💡", command=self.toggle_hilfe,width=100, fg_color="#1f6aa5").pack(side="left", padx=5)

            # Notizblock Button
            customtkinter.CTkButton(nav_frame, text="Rechenweg 📝", command=self.toggle_notizblock,width=100, fg_color="#333333").pack(side="left", padx=5)

            # Restliche Buttons
            customtkinter.CTkButton(nav_frame, text="Überspringen ↻", command=self.skip_aufgabe,width=130, fg_color="#A9711C").pack(side="left", padx=5)
            customtkinter.CTkButton(nav_frame, text="Menü", command=self.zurück_zum_menü,width=100, fg_color="#555555").pack(side="left", padx=5)

        self.zurück_zum_menü()

    # --- HILFSFUNKTIONEN ---
    def skip_aufgabe(self):
        """Ermittelt, welcher Frame gerade offen ist und würfelt neu."""
        if self.binär_frame.winfo_viewable():
            self.neue_binär_aufgabe()
        elif self.hex_frame.winfo_viewable():
            self.neue_hex_aufgabe()
        elif self.speicher_frame.winfo_viewable():
            self.neue_speicher_aufgabe()
        elif self.download_frame.winfo_viewable():
            self.neue_download_aufgabe()
        elif self.elektro_frame.winfo_viewable():
            self.neue_elektro_aufgabe()
        elif self.subnet_frame.winfo_viewable():
            self.neue_subnet_aufgabe()
        elif self.kalk_frame.winfo_viewable():
            self.neue_kalk_aufgabe()
        elif self.raid_frame.winfo_viewable():
            self.neue_raid_aufgabe()
        elif self.storage_frame.winfo_viewable():
            self.neue_storage_aufgabe()
        elif self.availability_frame.winfo_viewable():
            self.neue_availability_aufgabe()
        elif self.netzplan_frame.winfo_viewable():
            self.neue_netzplan_aufgabe()
        elif self.gantt_frame.winfo_viewable():
            self.neue_gantt_aufgabe()


    def reset_fehler(self):
        self.fehler_count = 0

    def alle_frames_verstecken(self):
        for frame in self.alle_frames:
            frame.pack_forget()

    def zurück_zum_menü(self):
        self.alle_frames_verstecken()
        self.main_menu_frame.pack(fill="both", expand=True, padx=20, pady=20)
        self.label.configure(text="Fachinformatiker Mathetrainer")

    def change_appearance_mode(self):
        mode = "dark" if self.mode_switch.get() == 1 else "light"
        customtkinter.set_appearance_mode(mode)

    def setup_main_menu(self):
        # Container für die Buttons im Hauptmenü
        self.button_container = customtkinter.CTkFrame(self.main_menu_frame, fg_color="transparent")
        self.button_container.pack(expand=True)

        # Titel im Hauptmenü
        customtkinter.CTkLabel(self.button_container,text="Wähle ein Trainingsmodul",font=("Arial", 22, "bold")).pack(pady=(0, 20))

        # Einheitliche Konfiguration für alle Buttons
        btn_width = 300
        btn_height = 45
        standard_color = "#2c3e50"
        hover_color = "#34495e"


        # Liste der Module für eine saubere Erstellung
        module = [
            ("Binär", self.show_binär_trainer),
            ("Hexadezimal", self.show_hex_trainer),
            ("Speichergrößen", self.show_speicher_trainer),
            ("Downloadgeschwindigkeit", self.show_download_trainer),
            ("Elektrotechnik (U, I, R, P)", self.show_elektro_trainer),
            ("Subnetting", self.show_subnet_trainer),
            ("Handelskalkulation", self.show_kalk_trainer),
            ("RAID", self.show_raid_trainer),  # <-- HIER HINZUFÜGEN
            ("Speicherbedarf", self.show_storage_trainer),
            ("Verfügbarkeit", self.show_availability_trainer),
            ("Netzplan", self.show_netzplan_trainer),
            ("Gantt-Diagramm", self.show_gantt_trainer),
        ]


        for text, befehl in module:
            customtkinter.CTkButton(self.button_container,text=text,command=befehl,width=btn_width,height=btn_height,fg_color=standard_color,hover_color=hover_color,font=("Arial", 14)).pack(pady=8)

    # --- NAVIGATIONS-FUNKTIONEN ---


    def show_binär_trainer(self):
        self.verstecke_alle_frames()
        self.binär_frame.pack(fill="both", expand=True)
        self.neue_binär_aufgabe()

    def show_hex_trainer(self):
        self.verstecke_alle_frames()
        self.hex_frame.pack(fill="both", expand=True)
        self.neue_hex_aufgabe()
        self.after(100, lambda: self.hex_entry.focus())

    def show_speicher_trainer(self):
        self.verstecke_alle_frames()
        self.speicher_frame.pack(fill="both", expand=True)
        self.neue_speicher_aufgabe()


    def show_download_trainer(self):
        self.verstecke_alle_frames()
        self.download_frame.pack(fill="both", expand=True)
        self.neue_download_aufgabe()
        self.after(100, lambda: self.dl_entry.focus())

    def show_storage_trainer(self):
        self.verstecke_alle_frames()
        self.storage_frame.pack(fill="both", expand=True)
        self.neue_storage_aufgabe()
        self.after(100, lambda: self.st_entry.focus())


    def show_elektro_trainer(self):
        self.verstecke_alle_frames()
        self.elektro_frame.pack(fill="both", expand=True)
        self.neue_elektro_aufgabe()

    def show_subnet_trainer(self):
        self.verstecke_alle_frames()
        self.subnet_frame.pack(fill="both", expand=True, padx=20, pady=20)
        self.label.configure(text="Subnetting-Trainer")
        self.neue_subnet_aufgabe()


    def show_kalk_trainer(self):
        self.verstecke_alle_frames()
        self.kalk_frame.pack(fill="both", expand=True)
        self.neue_kalk_aufgabe()

    def show_raid_trainer(self):
        self.verstecke_alle_frames()
        self.raid_frame.pack(fill="both", expand=True)
        self.neue_raid_aufgabe()

    def show_availability_trainer(self):
        self.verstecke_alle_frames()
        self.availability_frame.pack(fill="both", expand=True)
        self.neue_availability_aufgabe()
        self.after(100, lambda: self.av_entry.focus())

    def show_netzplan_trainer(self):
        self.alle_frames_verstecken()
        self.netzplan_frame.pack(fill="both", expand=True)
        self.neue_netzplan_aufgabe()

    def show_gantt_trainer(self):
        self.alle_frames_verstecken()
        self.gantt_frame.pack(fill="both", expand=True)
        self.label.configure(text="Gantt-Diagramm Training")
        self.neue_gantt_aufgabe()



    def verstecke_alle_frames(self):
        for frame in self.alle_frames:
            frame.pack_forget()

    def toggle_taschenrechner(self):
        if self.tr_window is None or not self.tr_window.winfo_exists():
            self.tr_window = customtkinter.CTkToplevel(self)
            self.tr_window.title("Tachenrechner")
            self.tr_window.geometry("350x500")
            self.tr_window.attributes("-topmost", True)
            self.tr_window.resizable(False, False)

            # Display
            self.display = customtkinter.CTkEntry(self.tr_window, font=("Arial", 28), justify="right", state="readonly")
            self.display.grid(row=0, column=0, columnspan=4, padx=10, pady=20, sticky="nsew")

            buttons = [
                'C', '(', ')', '/',
                '7', '8', '9', '*',
                '4', '5', '6', '-',
                '1', '2', '3', '+',
                '0', '.', '√', '=',
                '^'
            ]

            r, c = 1, 0
            for button in buttons:
                b_color = "#1f6aa5" if button == "=" else ("#A82424" if button == "C" else None)
                cmd = lambda x=button: self.rechner_klick(x)
                btn = customtkinter.CTkButton(self.tr_window, text=button, width=70, height=50,command=cmd, font=("Arial", 18), fg_color=b_color)
                btn.grid(row=r, column=c, padx=5, pady=5)
                c += 1
                if c > 3:
                    c = 0
                    r += 1

            self.tr_window.bind("<Key>", self.rechner_key_event)
            self.tr_window.focus_force()
        else:
            self.tr_window.focus()
            self.tr_window.attributes("-topmost", True)

    def toggle_hilfe(self):
        """Öffnet das Hilfe-Fenster passend zum aktuellen Trainer."""
        if self.hilfe_window is not None and self.hilfe_window.winfo_exists():
            self.hilfe_window.focus()
            return


        selected_key = None

        frame_mapping = {
            "binär_frame": "binär",
            "hex_frame": "hexadezimal",
            "speicher_frame": "speichergrößen",
            "download_frame": "downloadgeschwindigkeit",
            "elektro_frame": "elektrotechnik (u, i, r, p)",
            "subnet_frame": "subnetting",
            "kalk_frame": "handelskalkulation",
            "raid_frame": "raid",
            "storage_frame": "speicherbedarf",
            "availability_frame": "verfügbarkeit",
            "netzplan_frame": "netzplan",
            "gantt_frame": "gantt-diagramm (zeitplan)"
        }

        for attr_name, key in frame_mapping.items():
            if hasattr(self, attr_name):
                frame_obj = getattr(self, attr_name)
                if frame_obj is not None and frame_obj.winfo_viewable():
                    selected_key = key
                    break

        inhalt = self.hilfe_texte.get(selected_key, "Keine Hilfe für diesen Bereich verfügbar.")

        # 2. Fenster erstellen
        self.hilfe_window = customtkinter.CTkToplevel(self)
        self.hilfe_window.title("Lern-Hilfe")
        self.hilfe_window.geometry("500x450")
        self.hilfe_window.attributes("-topmost", True)

        hilfe_box = customtkinter.CTkTextbox(self.hilfe_window, font=("Consolas", 12), wrap="word")
        hilfe_box.pack(fill="both", expand=True, padx=20, pady=20)

        hilfe_box.insert("1.0", inhalt)
        hilfe_box.configure(state="disabled")

    def rechner_klick(self, taste):
        self.display.configure(state="normal")
        aktuell = self.display.get()

        if taste == "C":
            self.display.delete(0, "end")
        elif taste == "=":
            try:
                ausdruck = aktuell.replace('√', '**(0.5)').replace('^', '**')
                ergebnis = eval(ausdruck, {"__builtins__": None}, {})
                self.display.delete(0, "end")
                self.display.insert(0, str(round(ergebnis, 4)))
            except:
                self.display.delete(0, "end")
                self.display.insert(0, "Fehler")
        else:
            self.display.insert("end", taste)

        self.display.configure(state="readonly")

    def rechner_key_event(self, event):
        if event.char.isdigit() or event.char in "+-*/().^":
            self.rechner_klick(event.char)
        elif event.keysym == "Return":
            self.rechner_klick("=")
        elif event.keysym == "BackSpace":
            self.display.configure(state="normal")
            current_text = self.display.get()
            if current_text:
                self.display.delete(len(current_text) - 1, "end")
            self.display.configure(state="readonly")
        elif event.keysym == "Escape":
            self.rechner_klick("C")

        return "break"

    def toggle_notizblock(self):
        if self.note_window is None or not self.note_window.winfo_exists():
            self.note_window = customtkinter.CTkToplevel(self)
            self.note_window.title("Rechenweg / Notizen")
            self.note_window.geometry("400x400")
            self.note_window.attributes("-topmost", True)

            # Textfeld für Notizen
            self.notiz_text = customtkinter.CTkTextbox(self.note_window, font=("Consolas", 14))
            self.notiz_text.pack(fill="both", expand=True, padx=10, pady=10)

            # Button zum schnellen Löschen
            customtkinter.CTkButton(self.note_window, text="Alles löschen",command=lambda: self.notiz_text.delete("1.0", "end"),fg_color="#A82424").pack(pady=5)

            self.note_window.focus_force()
        else:
            self.note_window.focus()
            self.note_window.attributes("-topmost", True)



    # --- BINÄR ---

    def setup_binär_screen(self):
        self.bin_modus_switch = customtkinter.CTkSegmentedButton(self.binär_frame,values=["Dez -> Bin", "Bin -> Dez"],command=self.neue_binär_aufgabe)
        self.bin_modus_switch.set("Dez -> Bin")
        self.bin_modus_switch.pack(pady=10)

        self.bin_aufgaben_label = customtkinter.CTkLabel(self.binär_frame,text="",font=("Arial", 20))
        self.bin_aufgaben_label.pack(pady=20)

        self.bin_entry = customtkinter.CTkEntry(self.binär_frame, width=250)
        self.bin_entry.pack(pady=10)
        self.bin_entry.bind("<Return>", self.binär_prüfen)

        self.bin_feedback_label = customtkinter.CTkLabel(self.binär_frame, text="")
        self.bin_feedback_label.pack(pady=10)


        self.bin_btn_frame = customtkinter.CTkFrame(self.binär_frame, fg_color="transparent")
        self.bin_btn_frame.pack(pady=10)

        self.bin_prüfen_button = customtkinter.CTkButton(self.bin_btn_frame,text="Prüfen",command=self.binär_prüfen)
        self.bin_prüfen_button.pack(side="left", padx=5)

        self.bin_next_button = customtkinter.CTkButton(self.bin_btn_frame,text="Nächste Aufgabe",command=self.neue_binär_aufgabe,fg_color="green")

        self.neue_binär_aufgabe()
        self.after(200, lambda: self.bin_entry.focus())

    def neue_binär_aufgabe(self, _=None):
        self.reset_fehler()
        self.aktuelle_zahl = random.randint(1, 255)
        self.bin_entry.delete(0, "end")
        self.bin_feedback_label.configure(text="")
        self.bin_next_button.pack_forget()
        modus = self.bin_modus_switch.get()
        self.bin_aufgaben_label.configure(text=f"Dezimal: {self.aktuelle_zahl}" if modus == "Dez -> Bin" else f"Binär: {bin(self.aktuelle_zahl)[2:]}")

        if hasattr(self, 'bin_entry'):
            self.bin_entry.delete(0, "end")
            self.bin_entry.focus()

    def binär_prüfen(self, _=None):
        try:
            eingabe = self.bin_entry.get().strip()
            if not eingabe: raise ValueError

            korrekt = bin(self.aktuelle_zahl)[2:] if self.bin_modus_switch.get() == "Dez -> Bin" else str(self.aktuelle_zahl)

            if eingabe == korrekt:
                self.bin_feedback_label.configure(text="Richtig!", text_color="green")
                self.bin_next_button.pack(side="left", padx=5)  # Erscheint neben Prüfen
            else:
                self.fehler_count += 1
                if self.fehler_count < 3:
                    self.bin_feedback_label.configure(text="Falsch! Versuch es nochmal.", text_color="red")
                else:
                    self.bin_feedback_label.configure(text=f"Falsch! Lösung: {korrekt}", text_color="red")
                    self.bin_next_button.pack(side="left", padx=5)
        except ValueError:
            self.bin_feedback_label.configure(text="Bitte etwas eingeben!", text_color="orange")

    # --- HEX ---

    def setup_hex_screen(self):
        self.hex_modus_switch = customtkinter.CTkSegmentedButton(self.hex_frame,values=["Hex -> Dez", "Dez -> Hex", "Hex -> Bin", "Bin -> Hex"],command=self.neue_hex_aufgabe)
        self.hex_modus_switch.set("Hex -> Dez")
        self.hex_modus_switch.pack(pady=10)

        self.hex_aufgaben_label = customtkinter.CTkLabel(self.hex_frame,text="",font=("Arial", 20))
        self.hex_aufgaben_label.pack(pady=20)

        self.hex_entry = customtkinter.CTkEntry(self.hex_frame, width=250)
        self.hex_entry.pack(pady=10)
        self.hex_entry.bind("<Return>", self.hex_prüfen)

        self.hex_feedback_label = customtkinter.CTkLabel(self.hex_frame, text="")
        self.hex_feedback_label.pack(pady=10)

        self.hex_btn_frame = customtkinter.CTkFrame(self.hex_frame, fg_color="transparent")
        self.hex_btn_frame.pack(pady=10)

        self.hex_prüfen_button = customtkinter.CTkButton(self.hex_btn_frame,text="Prüfen",command=self.hex_prüfen)
        self.hex_prüfen_button.pack(side="left", padx=5)

        self.hex_next_button = customtkinter.CTkButton(self.hex_btn_frame,text="Nächste Aufgabe",command=self.neue_hex_aufgabe,fg_color="green")

        self.neue_hex_aufgabe()
        self.after(200, lambda: self.hex_entry.focus())

    def neue_hex_aufgabe(self, _=None):
        self.reset_fehler()
        self.aktuelle_zahl = random.randint(1, 1024)
        self.hex_entry.delete(0, "end")
        self.hex_feedback_label.configure(text="")
        self.hex_next_button.pack_forget()
        modus = self.hex_modus_switch.get()
        txt = {"Hex -> Dez": f"Hex: {hex(self.aktuelle_zahl)[2:].upper()}",
               "Dez -> Hex": f"Dezimal: {self.aktuelle_zahl}",
               "Hex -> Bin": f"Hex: {hex(self.aktuelle_zahl)[2:].upper()}",
               "Bin -> Hex": f"Binär: {bin(self.aktuelle_zahl)[2:]}"}[modus]
        self.hex_aufgaben_label.configure(text=txt)

    def hex_prüfen(self, _=None):
        try:
            eingabe = self.hex_entry.get().strip().lower()
            if not eingabe: raise ValueError

            sol = {"Hex -> Dez": str(self.aktuelle_zahl),
                   "Dez -> Hex": hex(self.aktuelle_zahl)[2:],
                   "Hex -> Bin": bin(self.aktuelle_zahl)[2:],
                   "Bin -> Hex": hex(self.aktuelle_zahl)[2:]}[self.hex_modus_switch.get()]

            if eingabe == sol:
                self.hex_feedback_label.configure(text="Korrekt!", text_color="green")
                self.hex_next_button.pack(side="left", padx=5)
            else:
                self.fehler_count += 1
                if self.fehler_count < 3:
                    self.hex_feedback_label.configure(text="Falsch! Versuch es nochmal.", text_color="red")
                else:
                    self.hex_feedback_label.configure(text=f"Falsch! Lösung: {sol.upper()}", text_color="red")
                    self.hex_next_button.pack(side="left", padx=5)
        except (ValueError, KeyError):
            self.hex_feedback_label.configure(text="Bitte gültige Eingabe machen!", text_color="orange")


    # --- SPEICHER ---

    def setup_speicher_screen(self):
        self.speicher_typ_switch = customtkinter.CTkSegmentedButton(self.speicher_frame,values=["Binär (1024)", "Dezimal (1000)","Wechsel"],command=self.neue_speicher_aufgabe)
        self.speicher_typ_switch.set("Binär (1024)")
        self.speicher_typ_switch.pack(pady=10)
        self.speicher_aufgaben_label = customtkinter.CTkLabel(self.speicher_frame, text="", font=("Arial", 18))
        self.speicher_aufgaben_label.pack(pady=20)

        self.speicher_entry = customtkinter.CTkEntry(self.speicher_frame, width=250)
        self.speicher_entry.pack(pady=10)
        self.speicher_entry.bind("<Return>", self.speicher_prüfen)

        self.speicher_feedback_label = customtkinter.CTkLabel(self.speicher_frame, text="")
        self.speicher_feedback_label.pack(pady=10)

        self.speicher_btn_frame = customtkinter.CTkFrame(self.speicher_frame, fg_color="transparent")
        self.speicher_btn_frame.pack(pady=10)

        self.speicher_prüfen_button = customtkinter.CTkButton(self.speicher_btn_frame, text="Prüfen",command=self.speicher_prüfen)
        self.speicher_prüfen_button.pack(side="left", padx=5)

        self.speicher_next_button = customtkinter.CTkButton(self.speicher_btn_frame, text="Nächste Aufgabe",command=self.neue_speicher_aufgabe, fg_color="green")

    def neue_speicher_aufgabe(self, modus_auswahl=None):
        from decimal import Decimal
        import random

        self.reset_fehler()


        self.speicher_entry.delete(0, "end")
        self.speicher_feedback_label.configure(text="")
        self.speicher_next_button.pack_forget()


        if modus_auswahl is None or isinstance(modus_auswahl, (int, float)):
            modus_auswahl = self.speicher_typ_switch.get()

        einheiten_bin = ["Byte", "KiB", "MiB", "GiB", "TiB"]
        einheiten_dez = ["Byte", "KB", "MB", "GB", "TB"]


        idx_von = random.randint(0, 4)
        idx_zu = random.randint(0, 4)
        while idx_von == idx_zu:
            idx_zu = random.randint(0, 4)


        if "Binär" in modus_auswahl:
            basis = 1024
            einh_v, einh_z = einheiten_bin, einheiten_bin
        elif "Dezimal" in modus_auswahl:
            basis = 1000
            einh_v, einh_z = einheiten_dez, einheiten_dez
        else:
            basis = 1024

        if idx_von < idx_zu:
            stufen_diff = idx_zu - idx_von
            min_wert = max(1, int(basis ** stufen_diff / 100))
            max_wert = max(min_wert + 100, int(basis ** stufen_diff * 10))
            self.aktuelle_zahl = Decimal(str(random.randint(min_wert, max_wert)))
        else:
            typische_werte = [0.5, 1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024]
            self.aktuelle_zahl = Decimal(str(random.choice(typische_werte)))

        if self.aktuelle_zahl <= 0:
            self.aktuelle_zahl = Decimal("1")

        b = Decimal(str(basis))
        if "Binär" in modus_auswahl or "Dezimal" in modus_auswahl:
            self.korrektes_ergebnis = self.aktuelle_zahl * (b ** (idx_von - idx_zu))
        else:
            if random.choice([True, False]):
                einh_v, einh_z = einheiten_bin, einheiten_dez
                bytes_wert = self.aktuelle_zahl * (Decimal("1024") ** idx_von)
                self.korrektes_ergebnis = bytes_wert / (Decimal("1000") ** idx_zu)
            else:
                einh_v, einh_z = einheiten_dez, einheiten_bin
                bytes_wert = self.aktuelle_zahl * (Decimal("1000") ** idx_von)
                self.korrektes_ergebnis = bytes_wert / (Decimal("1024") ** idx_zu)

        self.aktuelle_stellen = 4 if self.korrektes_ergebnis < 1 else 2
        anzeige_zahl = format(self.aktuelle_zahl, 'f').rstrip('0').rstrip('.')

        self.speicher_aufgaben_label.configure(text=f"Wandle {anzeige_zahl} {einh_v[idx_von]} in {einh_z[idx_zu]} um:\n"f"(Auf {self.aktuelle_stellen} Stellen runden)")

        self.speicher_entry.focus()

    def speicher_prüfen(self, _=None):
        try:
            raw_input = self.speicher_entry.get().replace(",", ".").strip()
            if not raw_input: raise ValueError

            u = Decimal(raw_input)
            q = Decimal("1." + "0" * self.aktuelle_stellen)
            sol_q = self.korrektes_ergebnis.quantize(q, ROUND_HALF_UP)

            if u.quantize(q, ROUND_HALF_UP) == sol_q:
                self.speicher_feedback_label.configure(text="Richtig!", text_color="green")
                self.speicher_next_button.pack(side="left", padx=5)
            else:
                self.fehler_count += 1
                if self.fehler_count < 3:
                    self.speicher_feedback_label.configure(text="Falsch! Versuch es nochmal.", text_color="red")
                else:
                    self.speicher_feedback_label.configure(text=f"Falsch! Lösung: {sol_q}", text_color="red")
                    self.speicher_next_button.pack(side="left", padx=5)
        except ValueError:
            self.speicher_feedback_label.configure(text="Bitte eine Zahl eingeben!", text_color="orange")


    def setup_storage_screen(self):
        if hasattr(self, 'st_label'): return

        self.st_label = customtkinter.CTkLabel(self.storage_frame, text="Speicherbedarf berechnen",
                                               font=("Arial", 22, "bold"))
        self.st_label.pack(pady=20)

        self.st_aufgaben_label = customtkinter.CTkLabel(self.storage_frame, text="", font=("Arial", 18))
        self.st_aufgaben_label.pack(pady=20)

        self.st_entry = customtkinter.CTkEntry(self.storage_frame, width=300)
        self.st_entry.pack(pady=10)
        self.st_entry.bind("<Return>", lambda e: self.storage_prüfen())

        self.st_feedback = customtkinter.CTkLabel(self.storage_frame, text="")
        self.st_feedback.pack(pady=10)

        # Button Container für nebeneinander liegende Buttons
        self.st_btn_frame = customtkinter.CTkFrame(self.storage_frame, fg_color="transparent")
        self.st_btn_frame.pack(pady=10)

        self.st_pruefen_btn = customtkinter.CTkButton(self.st_btn_frame, text="Prüfen", command=self.storage_prüfen)
        self.st_pruefen_btn.pack(side="left", padx=5)

        self.st_next = customtkinter.CTkButton(self.st_btn_frame,text="Nächste Aufgabe",command=self.neue_storage_aufgabe,fg_color="green")

    def neue_storage_aufgabe(self):
        self.fehler_count = 0
        self.st_next.pack_forget()
        self.st_feedback.configure(text="", fg_color="transparent")
        self.st_entry.delete(0, "end")

        aufgabentyp = random.choice(["Bild", "Video"])

        if aufgabentyp == "Bild":
            # Werte für ein Bild würfeln
            breite = random.choice([1024, 1920, 3840])
            höhe = random.choice([768, 1080, 2160])
            bit = random.choice([8, 16, 24, 32])  # Farbtiefe

            # Formel: (Pixel * Bit) / 8 / 1024 / 1024 = MB
            self.korrektes_ergebnis = round((breite * höhe * bit) / 8 / 1024 / 1024, 2)

            self.st_aufgaben_label.configure(text=f"Typ: Bilddatei\nAuflösung: {breite} x {höhe} Pixel\nFarbtiefe: {bit} Bit\n\nBerechne die Dateigröße in MB (unkomprimiert)!")
            self.st_entry.configure(placeholder_text="Ergebnis in MB...")

        else:
            # Werte für ein Video würfeln
            minuten = random.randint(5, 90)
            bitrate = random.randint(5, 50)  # Mbit/s

            # Formel: (Sekunden * Mbit) / 8 / 1024 = GB
            self.korrektes_ergebnis = round((minuten * 60 * bitrate) / 8 / 1024, 2)

            self.st_aufgaben_label.configure(text=f"Typ: Videodatei\nDauer: {minuten} Minuten\nBitrate: {bitrate} Mbit/s\n\nBerechne den Speicherbedarf in GB!")
            self.st_entry.configure(placeholder_text="Ergebnis in GB...")

        self.after(100, self.st_entry.focus)

    def storage_prüfen(self):
        try:
            val = float(self.st_entry.get().replace(',', '.'))
            # Wir prüfen, ob im Aufgabentext "MB" oder "GB" steht
            einheit = "MB" if "MB" in self.st_aufgaben_label.cget("text") else "GB"

            if abs(val - self.korrektes_ergebnis) < 0.1:
                self.st_feedback.configure(text="Richtig! Sauber berechnet.", text_color="green",fg_color="transparent")
                self.st_next.pack(side="left", padx=5)
                self.fehler_count = 0
            else:
                self.fehler_count += 1
                if self.fehler_count >= 3:
                    self.st_feedback.configure(text=f"Falsch! Lösung: {self.korrektes_ergebnis} {einheit}",text_color="red", fg_color="transparent")
                    self.st_next.pack(side="left", padx=5)
                else:
                    self.st_feedback.configure(text="Falsch! Versuchs nochmal.", text_color="red",fg_color="transparent")
        except ValueError:
            self.st_feedback.configure(text="Bitte eine Zahl eingeben!", text_color="orange", fg_color="transparent")

    def show_storage_trainer(self):
        self.verstecke_alle_frames()
        self.storage_frame.pack(fill="both", expand=True)
        self.setup_storage_screen()  # Falls noch nicht initialisiert
        self.neue_storage_aufgabe()

    # --- DOWNLOAD ---

    def setup_download_screen(self):
        self.dl_label = customtkinter.CTkLabel(self.download_frame, text="", font=("Arial", 18))
        self.dl_label.pack(pady=20)

        self.dl_entry = customtkinter.CTkEntry(self.download_frame, width=250, placeholder_text="Sekunden...")
        self.dl_entry.pack(pady=10)
        self.dl_entry.bind("<Return>", self.download_prüfen)

        self.dl_feedback = customtkinter.CTkLabel(self.download_frame, text="")
        self.dl_feedback.pack(pady=10)

        self.dl_btn_frame = customtkinter.CTkFrame(self.download_frame, fg_color="transparent")
        self.dl_btn_frame.pack(pady=10)

        self.dl_prüfen_button = customtkinter.CTkButton(self.dl_btn_frame, text="Prüfen", command=self.download_prüfen)
        self.dl_prüfen_button.pack(side="left", padx=5)

        self.dl_next = customtkinter.CTkButton(self.dl_btn_frame,text="Nächste Aufgabe",command=self.neue_download_aufgabe,fg_color="green")


        self.neue_download_aufgabe()
        self.after(200, lambda: self.dl_entry.focus())

    def neue_download_aufgabe(self):
        self.reset_fehler()
        gb = random.randint(5, 500)
        mbit = random.choice([16, 50, 100, 250, 500, 1000])

        sekunden_gesamt = (gb * 1024 * 8) / mbit
        self.aktuelle_einheit = "Sekunden"
        self.korrektes_ergebnis = sekunden_gesamt

        if sekunden_gesamt > 3600:
            self.aktuelle_einheit = "Stunden"
            self.korrektes_ergebnis = sekunden_gesamt / 3600
        elif sekunden_gesamt > 120:
            self.aktuelle_einheit = "Minuten"
            self.korrektes_ergebnis = sekunden_gesamt / 60

        self.dl_label.configure(text=f"Datei: {gb} GB\nLeitung: {mbit} Mbit/s\n\n"
                 f"Berechne die Dauer in {self.aktuelle_einheit}:\n"
                 f"(Auf 2 Stellen runden)")

        self.dl_entry.delete(0, "end")
        self.dl_entry.configure(placeholder_text=f"{self.aktuelle_einheit}...")
        self.dl_feedback.configure(text="")
        self.dl_next.pack_forget()

    def download_prüfen(self, _=None):
        try:
            raw_input = self.dl_entry.get().replace(",", ".").strip()
            if not raw_input: raise ValueError

            u = float(raw_input)
            if abs(u - self.korrektes_ergebnis) < 2:
                self.dl_feedback.configure(text="Korrekt!", text_color="green")
                self.dl_next.pack(side="left", padx=5)
            else:
                self.fehler_count += 1
                if self.fehler_count < 3:
                    self.dl_feedback.configure(text="Falsch! Versuch es nochmal.", text_color="red")
                else:
                    self.dl_feedback.configure(text=f"Falsch! Lösung: ca. {int(self.korrektes_ergebnis)}s",text_color="red")
                    self.dl_next.pack(side="left", padx=5)
        except ValueError:
            self.dl_feedback.configure(text="Bitte eine Zahl eingeben!", text_color="orange")

    # --- ELEKTRO ---

    def setup_elektro_screen(self):
        self.komponenten = {
            "Kleinspannung": [
                {"name": "Steuer-Relais", "u": 5, "i": 0.07},
                {"name": "Lüfter", "u": 12, "i": 0.15},
                {"name": "Signal-LED", "u": 2.1, "i": 0.02},
                {"name": "Sensor", "u": 3.3, "i": 0.01}
            ],
            "Leistung": [
                {"name": "Heizlüfter", "p": 2000, "u": 230},
                {"name": "Motor", "p": 4500, "u": 400},
                {"name": "Ladestation", "p": 11000, "u": 400},
                {"name": "Wasserkocher", "p": 1200, "u": 230}
            ]
        }

        self.fehler_count = 0
        self.korrektes_ergebnis = 0

        self.el_modus_switch = customtkinter.CTkSegmentedButton(self.elektro_frame,values=["R = U / I", "I = P / U", "U = R * I", "P = U * I"],command=self.neue_elektro_aufgabe)
        self.el_modus_switch.set("R = U / I")
        self.el_modus_switch.pack(pady=10)

        self.el_label = customtkinter.CTkLabel(self.elektro_frame, text="", font=("Arial", 14), justify="left",wraplength=450)
        self.el_label.pack(pady=20)

        self.entry_container = customtkinter.CTkFrame(self.elektro_frame, fg_color="transparent")
        self.entry_container.pack(pady=10)

        self.el_entry = customtkinter.CTkEntry(self.entry_container, width=150, placeholder_text="Ergebnis...")
        self.el_entry.pack(side="left", padx=5)
        self.el_entry.bind("<Return>", self.elektro_prüfen)  # Enter-Taste binden

        self.el_unit_label = customtkinter.CTkLabel(self.entry_container, text="", font=("Arial", 14, "bold"))
        self.el_unit_label.pack(side="left", padx=5)

        self.el_feedback = customtkinter.CTkLabel(self.elektro_frame, text="")
        self.el_feedback.pack(pady=10)

        self.el_btn_frame = customtkinter.CTkFrame(self.elektro_frame, fg_color="transparent")
        self.el_btn_frame.pack(pady=10)

        self.el_prüfen_button = customtkinter.CTkButton(self.el_btn_frame, text="Auftrag prüfen",command=self.elektro_prüfen)
        self.el_prüfen_button.pack(side="left", padx=5)

        self.el_next = customtkinter.CTkButton(self.el_btn_frame, text="Nächster Auftrag",command=self.neue_elektro_aufgabe, fg_color="green")

    def neue_elektro_aufgabe(self, _=None):
        self.el_entry.delete(0, "end")
        self.el_feedback.configure(text="")
        self.el_next.pack_forget()
        self.fehler_count = 0
        self.el_entry.bind("<Return>", self.elektro_prüfen)

        modus = self.el_modus_switch.get()
        auftrag = ""

        if modus == "R = U / I":
            u_bauteil = random.choice([1.8, 2.2, 3.3, 5.0, 12.0])
            u_quelle = random.choice([9, 12, 18, 24, 36])
            if u_quelle <= u_bauteil: u_quelle = 24

            i_ma = random.randint(10, 150)
            i_amp = i_ma / 1000

            self.korrektes_ergebnis = round((u_quelle - u_bauteil) / i_amp, 1)
            self.el_unit_label.configure(text="Ohm (Ω)")
            auftrag = f"AUFTRAG: Ein Bauteil ({u_bauteil}V) soll an eine {u_quelle}V Quelle.\nBerechne den Vorwiderstand (R) für einen Strom von genau {i_ma} mA."

        elif modus == "I = P / U":
            u = random.choice([230, 400])
            p = random.randint(5, 35) * 100

            self.korrektes_ergebnis = round(p / u, 2)
            self.el_unit_label.configure(text="Ampere (A)")
            auftrag = f"AUFTRAG: Ein Gerät mit einer Nennleistung von {p}W wird an {u}V betrieben.\nWelche Stromstärke (I) fließt im Betrieb?"

        elif modus == "U = R * I":
            u_quelle = random.choice([12, 24, 230])
            r_leitung = round(random.uniform(0.2, 4.5), 2)
            i = round(random.uniform(0.5, 12.0), 1)

            self.korrektes_ergebnis = round(u_quelle - (r_leitung * i), 2)
            self.el_unit_label.configure(text="Volt (V)")
            auftrag = f"AUFTRAG: Eine Leitung mit R={r_leitung}Ω versorgt eine Last ({i}A).\nDie Quelle liefert {u_quelle}V. Welche Spannung (U) liegt am Verbraucher noch an?"

        elif modus == "P = U * I":
            if random.choice([True, False]):
                u = round(random.uniform(11.5, 14.4), 1)  # KFZ Bereich
                i = random.randint(2, 40)
                txt = "KFZ-Bordsystem (Batterie)"
            else:
                u = round(random.uniform(30.0, 45.0), 1)  # PV-Modul Bereich
                i = round(random.uniform(4.0, 10.0), 1)
                txt = "Photovoltaik-Modul"

            self.korrektes_ergebnis = round(u * i, 1)
            self.el_unit_label.configure(text="Watt (W)")
            auftrag = f"AUFTRAG: Messung an einem {txt}.\nGemessene Werte: {u}V und {i}A. Wie hoch ist die aktuelle Leistung (P)?"

        self.el_label.configure(text=auftrag)
        self.el_entry.focus()

    def elektro_prüfen(self, _=None):
        try:
            raw_input = self.el_entry.get().replace(",", ".").strip()
            if not raw_input: return

            eingabe = float(raw_input)
            diff = abs(eingabe - self.korrektes_ergebnis)
            toleranz = max(0.1, self.korrektes_ergebnis * 0.03)

            if diff <= toleranz:
                self.el_feedback.configure(text="✅ Korrekt!", text_color="green")
                self.el_next.pack(side="left", padx=5)
                self.el_entry.unbind("<Return>")
            else:
                self.fehler_count += 1
                if self.fehler_count < 3:
                    verbleibend = 3 - self.fehler_count
                    self.el_feedback.configure(text=f"❌ Falsch! Noch {verbleibend} Versuche.", text_color="red")
                else:
                    self.el_feedback.configure(text=f"❌ Lösung: {self.korrektes_ergebnis} {self.el_unit_label.cget('text')}", text_color="red")
                    self.el_next.pack(side="left", padx=5)
                    self.el_entry.unbind("<Return>")

        except ValueError:
            self.el_feedback.configure(text="⚠️ Bitte nur Zahlen eingeben!", text_color="orange")

    # --- SUBNETTING ---

    def setup_subnet_screen(self):
        self.sn_label = customtkinter.CTkLabel(self.subnet_frame, text="Subnetting-Trainer",font=("Arial", 24, "bold"))
        self.sn_label.pack(pady=(20, 10))

        self.sn_modus_switch = customtkinter.CTkSegmentedButton(self.subnet_frame,values=["Standard", "Planung", "Analyse", "Segmentierung"],command=lambda m: self.neue_subnet_aufgabe())
        self.sn_modus_switch.set("Standard")
        self.sn_modus_switch.pack(pady=10)

        self.sn_instruktion = customtkinter.CTkLabel(self.subnet_frame, text="Lade Aufgabe...", font=("Arial", 14),wraplength=550, justify="center")
        self.sn_instruktion.pack(pady=(0, 20))

        self.sn_scroll_container = customtkinter.CTkScrollableFrame(self.subnet_frame, width=600, height=380, fg_color="transparent")
        self.sn_scroll_container.pack(pady=10, fill="both", expand=True)
        self.sn_entries = {}
        self.sn_feedback = customtkinter.CTkLabel(self.subnet_frame, text="")
        self.sn_feedback.pack(pady=10)
        self.sn_btn_container = customtkinter.CTkFrame(self.subnet_frame, fg_color="transparent")
        self.sn_btn_container.pack(pady=10)
        self.sn_pruefen_btn = customtkinter.CTkButton(self.sn_btn_container, text="Prüfen", command=self.subnet_prüfen)
        self.sn_pruefen_btn.pack(side="left", padx=5)
        self.sn_next = customtkinter.CTkButton(self.sn_btn_container, text="Nächste Aufgabe",command=self.neue_subnet_aufgabe, fg_color="green")
        self.neue_subnet_aufgabe()

    def neue_subnet_aufgabe(self):
        self.fehler_count = 0
        self.sn_next.pack_forget()
        self.sn_feedback.configure(text="", fg_color="transparent")
        self.sn_pruefen_btn.configure(state="normal")

        for child in self.sn_scroll_container.winfo_children():
            child.destroy()
        self.sn_entries = {}

        wahl = self.sn_modus_switch.get()
        cidr = random.randint(20, 30)
        o1, o2 = 192, 168

        if cidr < 24:
            block_size_o3 = 2 ** (24 - cidr)
            o3 = (random.randint(0, 255) // block_size_o3) * block_size_o3
            sprung_sol = str(block_size_o3)
        else:
            o3 = random.randint(0, 255)
            sprung_sol = str(2 ** (32 - cidr))

        base_ip = f"{o1}.{o2}.{o3}.0"
        total_ips = 2 ** (32 - cidr)
        bc_ip = self.get_broadcast(base_ip, cidr)

        if wahl == "Segmentierung":
            anzahl = random.randint(2, 8)

            if anzahl <= 1:
                s_cidr = 24
            elif anzahl <= 2:
                s_cidr = 25
            elif anzahl <= 4:
                s_cidr = 26
            else:
                s_cidr = 27

            block = 2 ** (32 - s_cidr)
            self.aktuelle_sn_aufgabe = {"sol": {}}
            self.sn_instruktion.configure(text=f"Teile {o1}.{o2}.{o3}.0/24 in {anzahl} Subnetze (/{s_cidr}) auf.")

            for i in range(anzahl):
                row = customtkinter.CTkFrame(self.sn_scroll_container, fg_color="transparent")
                row.pack(fill="x", pady=2)
                customtkinter.CTkLabel(row, text=f"Netz {i + 1}:", width=60).pack(side="left")

                en = customtkinter.CTkEntry(row, placeholder_text="Netz-ID", width=180)
                en.pack(side="left", padx=5)
                eb = customtkinter.CTkEntry(row, placeholder_text="Broadcast", width=180)
                eb.pack(side="left", padx=5)

                self.sn_entries[f"n{i}"] = en
                self.sn_entries[f"b{i}"] = eb
                self.aktuelle_sn_aufgabe["sol"][f"n{i}"] = f"{o1}.{o2}.{o3}.{i * block}"
                self.aktuelle_sn_aufgabe["sol"][f"b{i}"] = f"{o1}.{o2}.{o3}.{(i * block) + block - 1}"

        else:
            field_configs = []
            if wahl == "Standard":
                field_configs = [("anzahl", "Anzahl Subnetze"), ("sprung", "Sprungweite"), ("net", "Netz-ID"),
                                 ("bc", "Broadcast"), ("mask", "Maske"), ("hosts", "Hosts")]
                self.aktuelle_sn_aufgabe = {
                    "sol": {"anzahl": str(2 ** (cidr - 24)) if cidr >= 24 else "1", "sprung": sprung_sol,
                            "net": base_ip, "bc": bc_ip, "mask": self.cidr_to_netmask(cidr),
                            "hosts": str(total_ips - 2)}}
                self.sn_instruktion.configure(text=f"Berechne alle Werte für: {base_ip} /{cidr}")

            elif wahl == "Planung":
                req, sz_text = self.get_realistisches_szenario()
                c = 32 - (req + 2).bit_length()
                if (2 ** (32 - c) - 2) < req: c -= 1
                field_configs = [("sprung", "Sprungweite"), ("mask", "Maske"), ("hosts", "Hosts")]
                s_val = 2 ** (32 - c) if c >= 24 else 2 ** (24 - c)
                self.aktuelle_sn_aufgabe = {
                    "sol": {"sprung": str(s_val), "mask": self.cidr_to_netmask(c), "hosts": str(2 ** (32 - c) - 2)}}
                self.sn_instruktion.configure(text=sz_text)

            elif wahl == "Analyse":
                r = random.random()
                curr_ip = base_ip if r < 0.15 else bc_ip if r < 0.3 else f"{o1}.{o2}.{o3}.{random.randint(1, 250)}"
                field_configs = [("sprung", "Sprungweite"), ("net", "Netz-ID"), ("bc", "Broadcast")]
                self.aktuelle_sn_aufgabe = {"sol": {"sprung": sprung_sol, "net": base_ip, "bc": bc_ip}}
                self.sn_instruktion.configure(text=f"Analysiere die IP: {curr_ip} /{cidr}\nBestimme die Blockgrenzen.")

            for key, placeholder in field_configs:
                entry = customtkinter.CTkEntry(self.sn_scroll_container, width=300, placeholder_text=placeholder)
                entry.pack(pady=5)
                self.sn_entries[key] = entry
                entry.bind("<Return>", lambda e, k=key: self.sn_focus_next(k))

        self.after(150, self.set_initial_focus)

    def sn_focus_next(self, current_key):
        keys = list(self.sn_entries.keys())
        if current_key in keys:
            idx = keys.index(current_key)
            if idx + 1 < len(keys):
                self.sn_entries[keys[idx + 1]].focus()
                return
        self.subnet_prüfen()

    def subnet_prüfen(self, _=None):
        if not hasattr(self, 'aktuelle_sn_aufgabe'): return
        sol = self.aktuelle_sn_aufgabe["sol"]

        for k in sol:
            if not self.sn_entries[k].get().strip():
                self.sn_feedback.configure(text="Bitte alle Felder ausfüllen!", text_color="orange")
                return

        richtig = True
        for k, v in sol.items():
            if self.sn_entries[k].get().strip().lower() != v.lower():
                richtig = False
                self.sn_entries[k].configure(border_color="red")
            else:
                self.sn_entries[k].configure(border_color="green")

        if richtig:
            self.sn_feedback.configure(text="Korrekt! Alles richtig.", text_color="green")
            self.sn_next.pack(side="left", padx=5)
            self.sn_pruefen_btn.configure(state="disabled")
        else:
            self.fehler_count += 1
            if self.fehler_count >= 2:
                msg = "Lösung:\n" + "\n".join([f"{k.upper()}: {v}" for k, v in sol.items()])
                self.sn_feedback.configure(text=msg, text_color="red")
                self.sn_next.pack(side="left", padx=5)
            else:
                self.sn_feedback.configure(text="Einige Werte sind falsch.", text_color="red")

    def get_broadcast(self, ip, cidr):
        try:
            net = ipaddress.IPv4Network(f"{ip}/{cidr}", strict=False)
            return str(net.broadcast_address)
        except:
            return "Fehler"

    def cidr_to_netmask(self, cidr):
        mask = (0xffffffff >> (32 - cidr)) << (32 - cidr)
        return f"{(mask >> 24) & 0xff}.{(mask >> 16) & 0xff}.{(mask >> 8) & 0xff}.{mask & 0xff}"

    def get_realistisches_szenario(self):
        szenarien = [
            (random.randint(2, 5), "Transfernetz"), (random.randint(10, 25), "Abteilung"),
            (random.randint(50, 150), "Gäste-WLAN"), (random.randint(200, 500), "Server-Segment")
        ]
        h, desc = random.choice(szenarien)
        geplant = int(h * 1.3)
        return geplant, f"Szenario: {desc}. Bedarf: {h} Hosts. Plane mit 30% Puffer ({geplant} Hosts)."

    def set_initial_focus(self):
        if self.sn_entries:
            list(self.sn_entries.values())[0].focus()

    # --- Handelskalkulation ---
    def setup_kalkulation_screen(self):

        self.kalk_modus_switch = customtkinter.CTkSegmentedButton(self.kalk_frame,values=["Vorwärtskalkulation", "Rückwärtskalkulation"],command=self.neue_kalk_aufgabe)
        self.kalk_modus_switch.set("Vorwärtskalkulation")
        self.kalk_modus_switch.pack(pady=10)

        self.tabelle_container = customtkinter.CTkFrame(self.kalk_frame, fg_color="transparent")
        self.tabelle_container.pack(pady=10, padx=20, fill="both", expand=True)

        self.kalk_feedback = customtkinter.CTkLabel(self.kalk_frame, text="")
        self.kalk_feedback.pack(pady=5)

        self.kalk_button_frame = customtkinter.CTkFrame(self.kalk_frame, fg_color="transparent")
        self.kalk_button_frame.pack(pady=10)

        customtkinter.CTkButton(self.kalk_button_frame, text="Prüfen", command=self.kalk_prüfen).pack(side="left",padx=5)
        self.kalk_next = customtkinter.CTkButton(self.kalk_button_frame,text="Nächste Aufgabe",command=self.neue_kalk_aufgabe,fg_color="green")

        self.neue_kalk_aufgabe()

        self.after(200, self.fokus_auf_erstes_kalk_feld)


    def reset_fehler(self):
        self.fehler_count = 0

    def fokus_auf_erstes_kalk_feld(self):
        if hasattr(self, 'kalk_entries') and self.kalk_entries:
            self.kalk_entries[0].focus()

    def neue_kalk_aufgabe(self, _=None):
        self.reset_fehler()
        self.kalk_next.pack_forget()
        self.kalk_feedback.configure(text="")

        for widget in self.tabelle_container.winfo_children():
            widget.destroy()

        modus = self.kalk_modus_switch.get()

        p_rabatt_e = Decimal(str(random.randint(1, 20)))
        p_skonto_e = Decimal(str(random.choice([2, 3])))
        p_hk = Decimal(str(random.randint(10, 25)))
        p_gewinn = Decimal(str(random.randint(5, 25)))
        p_skonto_v = Decimal(str(random.choice([2, 3])))
        p_prov = Decimal(str(random.randint(1, 5)))
        p_rabatt_v = Decimal(str(random.randint(5, 20)))
        random_bezugskosten = Decimal(str(random.randint(2, 15))).quantize(Decimal("0.01"))

        self.kalk_daten = [
            {"label": "Listeneinkaufspreis", "proz": None},
            {"label": "- Lieferrabatt", "proz": p_rabatt_e},
            {"label": "= Zieleinkaufspreis", "proz": None},
            {"label": "- Lieferskonto", "proz": p_skonto_e},
            {"label": "= Bareinkaufspreis", "proz": None},
            {"label": "+ Bezugskosten", "fix_betrag": random_bezugskosten},
            {"label": "= Bezugspreis", "proz": None},
            {"label": "+ Handlungskosten", "proz": p_hk},
            {"label": "= Selbstkosten", "proz": None},
            {"label": "+ Gewinnzuschlag", "proz": p_gewinn},
            {"label": "= Barverkaufspreis", "proz": None},
            {"label": "+ Kundenskonto", "proz": p_skonto_v},
            {"label": "+ Vertreterprovision", "proz": p_prov},
            {"label": "= Zielverkaufspreis", "proz": None},
            {"label": "+ Kundenrabatt", "proz": p_rabatt_v},
            {"label": "= Nettoverkaufspreis", "proz": None},
            {"label": "+ Umsatzsteuer", "proz": 19},
            {"label": "= Bruttoverkaufspreis", "proz": None}
        ]

        if modus == "Vorwärtskalkulation":
            start_wert = Decimal(str(random.randint(100, 800))).quantize(Decimal("0.01"))
            self.berechne_kalkulation(start_wert, vorwaerts=True)
        else:
            start_wert = Decimal(str(random.randint(300, 2000))).quantize(Decimal("0.01"))
            self.berechne_kalkulation(start_wert, vorwaerts=False)


        self.kalk_entries = []
        for i, zeile in enumerate(self.kalk_daten):
            lbl_text = zeile["label"]
            if "fix_betrag" in zeile:
                lbl_text += f" ({zeile['fix_betrag']:.2f} €)"

            customtkinter.CTkLabel(self.tabelle_container, text=lbl_text, anchor="w", width=200).grid(row=i, column=0,padx=5, pady=2)

            p_text = f"{zeile['proz']}%" if zeile.get('proz') else ""
            customtkinter.CTkLabel(self.tabelle_container, text=p_text, width=50).grid(row=i, column=1, padx=5, pady=2)

            entry = customtkinter.CTkEntry(self.tabelle_container, width=120)
            entry.grid(row=i, column=2, padx=5, pady=2)

            entry.bind("<FocusOut>", lambda e, idx=i: self.einzel_prüfung(idx))
            entry.bind("<Return>", lambda e, idx=i: self.einzel_prüfung(idx))

            if (modus == "Vorwärtskalkulation" and i == 0) or (modus == "Rückwärtskalkulation" and i == 17):
                entry.insert(0, f"{zeile['wert']:.2f}")

            if hasattr(self, 'kalk_entries') and self.kalk_entries:
                self.kalk_entries[0].focus()


            self.kalk_entries.append(entry)

    def berechne_kalkulation(self, start, vorwaerts=True):
        d = self.kalk_daten
        hundert = Decimal("100")

        if vorwaerts:
            d[0]["wert"] = start
            d[1]["wert"] = (d[0]["wert"] * d[1]["proz"] / hundert).quantize(Decimal("0.01"), ROUND_HALF_UP)
            d[2]["wert"] = d[0]["wert"] - d[1]["wert"]
            d[3]["wert"] = (d[2]["wert"] * d[3]["proz"] / hundert).quantize(Decimal("0.01"), ROUND_HALF_UP)
            d[4]["wert"] = d[2]["wert"] - d[3]["wert"]

            d[5]["wert"] = d[5]["fix_betrag"]
            d[6]["wert"] = d[4]["wert"] + d[5]["wert"]
            d[7]["wert"] = (d[6]["wert"] * d[7]["proz"] / hundert).quantize(Decimal("0.01"), ROUND_HALF_UP)
            d[8]["wert"] = d[6]["wert"] + d[7]["wert"]

            d[9]["wert"] = (d[8]["wert"] * d[9]["proz"] / hundert).quantize(Decimal("0.01"), ROUND_HALF_UP)
            d[10]["wert"] = d[8]["wert"] + d[9]["wert"]

            f_sk_pr = (hundert - d[11]["proz"] - d[12]["proz"]) / hundert
            d[13]["wert"] = (d[10]["wert"] / f_sk_pr).quantize(Decimal("0.01"), ROUND_HALF_UP)
            d[11]["wert"] = (d[13]["wert"] * d[11]["proz"] / hundert).quantize(Decimal("0.01"), ROUND_HALF_UP)
            d[12]["wert"] = (d[13]["wert"] * d[12]["proz"] / hundert).quantize(Decimal("0.01"), ROUND_HALF_UP)

            f_rab = (hundert - d[14]["proz"]) / hundert
            d[15]["wert"] = (d[13]["wert"] / f_rab).quantize(Decimal("0.01"), ROUND_HALF_UP)
            d[14]["wert"] = d[15]["wert"] - d[13]["wert"]

            d[16]["wert"] = (d[15]["wert"] * d[16]["proz"] / hundert).quantize(Decimal("0.01"), ROUND_HALF_UP)
            d[17]["wert"] = d[15]["wert"] + d[16]["wert"]

        else:
            d[17]["wert"] = start
            ust_faktor = (hundert + Decimal(str(d[16]["proz"]))) / hundert
            d[15]["wert"] = (d[17]["wert"] / ust_faktor).quantize(Decimal("0.01"), ROUND_HALF_UP)
            d[16]["wert"] = d[17]["wert"] - d[15]["wert"]

            d[14]["wert"] = (d[15]["wert"] * Decimal(str(d[14]["proz"])) / hundert).quantize(Decimal("0.01"),
                                                                                             ROUND_HALF_UP)
            d[13]["wert"] = d[15]["wert"] - d[14]["wert"]

            d[11]["wert"] = (d[13]["wert"] * Decimal(str(d[11]["proz"])) / hundert).quantize(Decimal("0.01"),
                                                                                             ROUND_HALF_UP)
            d[12]["wert"] = (d[13]["wert"] * Decimal(str(d[12]["proz"])) / hundert).quantize(Decimal("0.01"),
                                                                                             ROUND_HALF_UP)
            d[10]["wert"] = d[13]["wert"] - d[11]["wert"] - d[12]["wert"]

            gewinn_faktor = (hundert + Decimal(str(d[9]["proz"]))) / hundert
            d[8]["wert"] = (d[10]["wert"] / gewinn_faktor).quantize(Decimal("0.01"), ROUND_HALF_UP)
            d[9]["wert"] = d[10]["wert"] - d[8]["wert"]

            hk_faktor = (hundert + Decimal(str(d[7]["proz"]))) / hundert
            d[6]["wert"] = (d[8]["wert"] / hk_faktor).quantize(Decimal("0.01"), ROUND_HALF_UP)
            d[7]["wert"] = d[8]["wert"] - d[6]["wert"]

            d[5]["wert"] = d[5]["fix_betrag"]
            d[4]["wert"] = d[6]["wert"] - d[5]["wert"]

            sk_e_faktor = (hundert - Decimal(str(d[3]["proz"]))) / hundert
            d[2]["wert"] = (d[4]["wert"] / sk_e_faktor).quantize(Decimal("0.01"), ROUND_HALF_UP)
            d[3]["wert"] = d[2]["wert"] - d[4]["wert"]

            rab_e_faktor = (hundert - Decimal(str(d[1]["proz"]))) / hundert
            d[0]["wert"] = (d[2]["wert"] / rab_e_faktor).quantize(Decimal("0.01"), ROUND_HALF_UP)
            d[1]["wert"] = d[0]["wert"] - d[2]["wert"]

    def einzel_prüfung(self, idx):
        entry = self.kalk_entries[idx]
        try:
            val = Decimal(entry.get().replace(",", ".").strip())
            sol = self.kalk_daten[idx]["wert"]
            if abs(val - sol) <= Decimal("0.02"):
                entry.configure(border_color="green")
            else:
                entry.configure(border_color="red")
        except:
            if entry.get() != "":
                entry.configure(border_color="red")

    def kalk_prüfen(self):
        alle_korrekt = True
        for i in range(len(self.kalk_entries)):
            self.einzel_prüfung(i)
            if self.kalk_entries[i].cget("border_color") != "green":
                if self.kalk_entries[i].cget("state") != "disabled":
                    alle_korrekt = False

        if alle_korrekt:
            self.kalk_feedback.configure(text="✔ Alles richtig!", text_color="green")
            self.kalk_next.pack(side="left", padx=5)
        else:
            self.kalk_feedback.configure(text="❌ Korrigiere die roten Felder.", text_color="red")

    # --- Raid ---
    def setup_raid_screen(self):
        self.raid_label = customtkinter.CTkLabel(self.raid_frame, text="", font=("Arial", 18), justify="left")
        self.raid_label.pack(pady=20)

        self.raid_entry_cap = customtkinter.CTkEntry(self.raid_frame, width=250,placeholder_text="Nutzbare Kapazität in TB...")
        self.raid_entry_cap.pack(pady=5)

        self.raid_entry_cap.bind("<Return>", lambda e: self.raid_entry_fault.focus())

        self.raid_entry_fault = customtkinter.CTkEntry(self.raid_frame, width=250,placeholder_text="Wie viele Platten dürfen ausfallen?...")
        self.raid_entry_fault.pack(pady=5)

        self.raid_entry_fault.bind("<Return>", self.raid_prüfen)

        self.raid_feedback = customtkinter.CTkLabel(self.raid_frame, text="")
        self.raid_feedback.pack(pady=10)

        self.raid_btn_container = customtkinter.CTkFrame(self.raid_frame, fg_color="transparent")
        self.raid_btn_container.pack(pady=10)

        self.raid_pruefen_btn = customtkinter.CTkButton(self.raid_btn_container, text="Prüfen",command=self.raid_prüfen)
        self.raid_pruefen_btn.pack(side="left", padx=5)

        self.raid_next = customtkinter.CTkButton(self.raid_btn_container, text="Nächste Aufgabe",command=self.neue_raid_aufgabe, fg_color="green")

    def neue_raid_aufgabe(self):
        self.reset_fehler()
        self.raid_entry_cap.delete(0, "end")
        self.raid_entry_fault.delete(0, "end")
        self.raid_feedback.configure(text="")
        self.raid_next.pack_forget()
        self.raid_entry_cap.focus()

        level = random.choice([0, 1, 5, 6, 10])
        anzahl_platten = 0
        kapazität_pro_platte = random.choice([1, 2, 4, 8, 10, 12, 16])

        if level == 0:
            anzahl_platten = random.randint(2, 6)
            self.sol_cap = anzahl_platten * kapazität_pro_platte
            self.sol_fault = 0
        elif level == 1:
            anzahl_platten = 2
            self.sol_cap = kapazität_pro_platte
            self.sol_fault = 1
        elif level == 5:
            anzahl_platten = random.randint(3, 8)
            self.sol_cap = (anzahl_platten - 1) * kapazität_pro_platte
            self.sol_fault = 1
        elif level == 6:
            anzahl_platten = random.randint(4, 10)
            self.sol_cap = (anzahl_platten - 2) * kapazität_pro_platte
            self.sol_fault = 2
        elif level == 10:
            anzahl_platten = random.choice([4, 6, 8, 10])
            self.sol_cap = (anzahl_platten / 2) * kapazität_pro_platte
            self.sol_fault = 1

        self.raid_label.configure(text=f"RAID-Konfiguration:\n\n"
                                       f"RAID-Level: {level}\n"
                                       f"Anzahl Festplatten: {anzahl_platten}\n"
                                       f"Kapazität pro Platte: {kapazität_pro_platte} TB\n\n"
                                       f"Berechne die nutzbare Kapazität und die Ausfallsicherheit!")

    def raid_prüfen(self, _=None):
        try:
            raw_cap = self.raid_entry_cap.get().replace(",", ".").strip()
            raw_fault = self.raid_entry_fault.get().strip()

            if not raw_cap or not raw_fault:
                raise ValueError

            user_cap = float(raw_cap)
            user_fault = int(raw_fault)

            if abs(user_cap - float(self.sol_cap)) < 0.01 and user_fault == self.sol_fault:
                self.raid_feedback.configure(text="Richtig! RAID-Verbund korrekt berechnet.", text_color="green")
                self.raid_next.pack(side="left", padx=5)  # Hier ist das side="left" wichtig!
            else:
                self.fehler_count += 1
                if self.fehler_count < 3:
                    self.raid_feedback.configure(text="Falsch! Überprüfe Kapazität oder Plattenanzahl.",
                                                 text_color="red")
                else:
                    msg = f"Falsch! Lösung: {self.sol_cap} TB Kapazität, {self.sol_fault} Platte(n) Fehlertoleranz"
                    self.raid_feedback.configure(text=msg, text_color="red")
                    self.raid_next.pack(side="left", padx=5)  # Hier ebenfalls

        except ValueError:
            self.raid_feedback.configure(text="Bitte gültige Zahlen eingeben!", text_color="orange")

    # --- Verfügbarkeit ---
    def setup_availability_screen(self):
        if hasattr(self, 'av_label'): return

        self.av_label = customtkinter.CTkLabel(self.availability_frame, text="Verfügbarkeits-Rechner", font=("Arial", 22, "bold"))
        self.av_label.pack(pady=10)

        self.av_modus_switch = customtkinter.CTkSegmentedButton(self.availability_frame,values=["Ausfallzeit berechnen", "% Verfügbarkeit berechnen"],command=self.neue_availability_aufgabe)
        self.av_modus_switch.set("Ausfallzeit berechnen")
        self.av_modus_switch.pack(pady=10)

        self.av_aufgaben_label = customtkinter.CTkLabel(self.availability_frame, text="", font=("Arial", 18))
        self.av_aufgaben_label.pack(pady=20)

        self.av_entry = customtkinter.CTkEntry(self.availability_frame, width=300)
        self.av_entry.pack(pady=10)
        self.av_entry.bind("<Return>", lambda e: self.availability_prüfen())

        self.av_feedback = customtkinter.CTkLabel(self.availability_frame, text="")
        self.av_feedback.pack(pady=10)

        self.av_btn_frame = customtkinter.CTkFrame(self.availability_frame, fg_color="transparent")
        self.av_btn_frame.pack(pady=10)

        self.av_pruefen_btn = customtkinter.CTkButton(self.av_btn_frame, text="Prüfen", command=self.availability_prüfen)
        self.av_pruefen_btn.pack(side="left", padx=5)

        self.av_next = customtkinter.CTkButton(self.av_btn_frame,text="Nächste Aufgabe",command=self.neue_availability_aufgabe,fg_color="green")


    def neue_availability_aufgabe(self, *args):
        self.fehler_count = 0
        self.av_next.pack_forget()
        self.av_feedback.configure(text="", fg_color="transparent")
        self.av_entry.delete(0, "end")

        modus = self.av_modus_switch.get()

        zeiträume = [
            {"name": "1 Woche (7 Tage)", "minuten": 7 * 24 * 60},
            {"name": "1 Quartal (90 Tage)", "minuten": 90 * 24 * 60},
            {"name": "2 Quartale (180 Tage)", "minuten": 180 * 24 * 60},
            {"name": "3 Quartale (270 Tage)", "minuten": 270 * 24 * 60},
            {"name": "1 Jahr (365 Tage)", "minuten": 365 * 24 * 60}
        ]
        auswahl = random.choice(zeiträume)
        minuten_gesamt = auswahl["minuten"]
        zeit_text = auswahl["name"]

        if modus == "Ausfallzeit berechnen":
            prozent = random.choice([99.0, 99.5, 99.9, 99.95, 99.99])
            self.korrektes_ergebnis = round((100 - prozent) / 100 * minuten_gesamt, 2)

            self.av_aufgaben_label.configure(text=f"SLA-Level: {prozent}%\nBezugszeitraum: {zeit_text}\n\nMax. zulässige Ausfallzeit in Minuten?")
            self.av_entry.configure(placeholder_text="Minuten...")
        else:
            ausfall = random.randint(30, 600)
            if "Quartal" in zeit_text: ausfall *= 2
            if "Jahr" in zeit_text: ausfall *= 4

            self.korrektes_ergebnis = round((1 - (ausfall / minuten_gesamt)) * 100, 3)
            self.av_aufgaben_label.configure(text=f"Protokoll-Check:\nIm Zeitraum '{zeit_text}' gab es\ninsgesamt {ausfall} Minuten Downtime.\n\nVerfügbarkeit in %?")
            self.av_entry.configure(placeholder_text="z.B. 99.123")

        self.after(100, self.av_entry.focus)

    def availability_prüfen(self):
        try:
            val = float(self.av_entry.get().replace(',', '.'))
            if abs(val - self.korrektes_ergebnis) < 0.05:
                self.av_feedback.configure(text="Richtig!", text_color="green", fg_color="transparent")
                self.av_next.pack(side="left", padx=5)
                self.fehler_count = 0
            else:
                self.fehler_count += 1
                if self.fehler_count >= 3:
                    einheit = "%" if "%" in self.av_modus_switch.get() else "Min."
                    self.av_feedback.configure(text=f"Falsch! Lösung: {self.korrektes_ergebnis} {einheit}", text_color="red", fg_color="transparent")
                    self.av_next.pack(side="left", padx=5)
                else:
                    self.av_feedback.configure(text="Falsch! Versuch es noch einmal.", text_color="red", fg_color="transparent")
        except ValueError:
            self.av_feedback.configure(text="Bitte eine Zahl eingeben!", text_color="orange", fg_color="transparent")

    def setup_netzplan_screen(self):
        self.np_main_container = customtkinter.CTkFrame(self.netzplan_frame, fg_color="transparent")
        self.np_main_container.pack(fill="both", expand=True)

        self.np_info_label = customtkinter.CTkLabel(self.np_main_container, text="Netzplan",font=("Arial", 20, "bold"))
        self.np_info_label.pack(pady=10)

        self.np_canvas = customtkinter.CTkCanvas(self.np_main_container, height=450, bg="#f5f5f5", highlightthickness=0)
        self.np_canvas.pack(fill="x", padx=20, pady=10)

        self.np_feedback = customtkinter.CTkLabel(self.np_main_container,text="Klicke auf den roten Rahmen/Header der Knoten, um den Kritischen Pfad zu markieren (Gold).",wraplength=600)
        self.np_feedback.pack(pady=5)

        self.np_btn_frame = customtkinter.CTkFrame(self.np_main_container, fg_color="transparent")
        self.np_btn_frame.pack(pady=10)

        customtkinter.CTkButton(self.np_btn_frame, text="Prüfen", command=self.prüfe_netzplan, fg_color="#1f6aa5").pack(side="left", padx=10)


    # --- Netzplan ---
    def create_netzplan_node(self, master, nr, name, dauer):
        container = customtkinter.CTkFrame(master, border_width=2, border_color="#c0392b", fg_color="white",corner_radius=0)

        header = customtkinter.CTkFrame(container, fg_color="#c0392b", corner_radius=0, height=30)
        header.pack(fill="x")

        l1 = customtkinter.CTkLabel(header, text=f"{nr}", text_color="white", font=("Arial", 12, "bold"), width=30)
        l1.pack(side="left")
        l2 = customtkinter.CTkLabel(header, text=f"{name}", text_color="white", font=("Arial", 12, "bold"))
        l2.pack(side="left", expand=True)
        l3 = customtkinter.CTkLabel(header, text=f"{dauer}", text_color="white", font=("Arial", 12, "bold"), width=30)
        l3.pack(side="right")

        grid = customtkinter.CTkFrame(container, fg_color="transparent")
        grid.pack(padx=2, pady=2)

        fields = {}
        config = [
            ("faz", 0, 0, "FAZ"), ("gp", 0, 1, "GP"), ("fez", 0, 2, "FEZ"),
            ("saz", 1, 0, "SAZ"), ("fp", 1, 1, "FP"), ("sez", 1, 2, "SEZ")
        ]

        for key, r, c, hint in config:
            e = customtkinter.CTkEntry(grid,width=50,height=30,placeholder_text=hint,fg_color="white",text_color="black",border_width=1,border_color="#bbbbbb",font=("Arial", 13, "bold"),justify="center")
            e.grid(row=r, column=c, padx=1, pady=1)
            fields[key] = e


        for widget in [container, header, l1, l2, l3, grid]:
            widget.bind("<Button-1>", lambda e, n=container: self.toggle_critical_path(n))

        container.fields = fields
        return container

    def neue_netzplan_aufgabe(self):
        self.np_canvas.delete("all")
        self.np_knoten_widgets = []
        self.np_loesungen = []
        self.np_canvas.configure(bg="#f5f5f5")

        namen = ["Planung", "Verkauf", "Recherche", "Akquise", "Redaktion", "Layout"]
        buchstaben = ["A", "B", "C", "D", "E", "F"]

        d = [random.randint(3, 10) for _ in range(6)]

        faz = [0] * 6
        fez = [0] * 6
        faz[0] = 0
        fez[0] = d[0]

        faz[1] = faz[2] = fez[0]
        fez[1], fez[2] = faz[1] + d[1], faz[2] + d[2]
        faz[3], fez[3] = fez[1], fez[1] + d[3]
        faz[4], fez[4] = fez[2], fez[2] + d[4]
        faz[5] = max(fez[3], fez[4])
        fez[5] = faz[5] + d[5]

        deadline = fez[5] + random.randint(0, 4)
        saz, sez = [0] * 6, [0] * 6

        sez[5] = deadline
        saz[5] = sez[5] - d[5]
        sez[3] = sez[4] = saz[5]
        saz[3], saz[4] = sez[3] - d[3], sez[4] - d[4]
        sez[1], saz[1] = saz[3], saz[3] - d[1]
        sez[2], saz[2] = saz[4], saz[4] - d[2]
        sez[0] = min(saz[1], saz[2])
        saz[0] = sez[0] - d[0]

        gp = [saz[i] - faz[i] for i in range(6)]
        fp = [0] * 6
        fp[0] = min(faz[1], faz[2]) - fez[0]
        fp[1], fp[2] = faz[3] - fez[1], faz[4] - fez[2]
        fp[3], fp[4] = faz[5] - fez[3], faz[5] - fez[4]

        coords = [(30, 150), (250, 50), (250, 250), (500, 50), (500, 250), (750, 150)]
        verbindungen = [(0, 1), (0, 2), (1, 3), (2, 4), (3, 5), (4, 5)]

        for v1, v2 in verbindungen:
            x1, y1 = coords[v1][0] + 165, coords[v1][1] + 55
            x2, y2 = coords[v2][0], coords[v2][1] + 55
            self.np_canvas.create_line(x1, y1, x2, y2, fill="#c0392b", width=2, arrow="last")

        for i in range(6):
            node = self.create_netzplan_node(self.np_canvas, buchstaben[i], namen[i], d[i])
            node.is_critical_selected = False
            self.np_canvas.create_window(coords[i], window=node, anchor="nw")
            self.np_knoten_widgets.append(node)
            self.np_loesungen.append({"faz": faz[i], "fez": fez[i], "saz": saz[i], "sez": sez[i], "gp": gp[i], "fp": fp[i]})

    def toggle_critical_path(self, node):
        node.is_critical_selected = not node.is_critical_selected
        new_color = "#f1c40f" if node.is_critical_selected else "#c0392b"
        new_width = 5 if node.is_critical_selected else 2
        node.configure(border_color=new_color, border_width=new_width)

    def prüfe_netzplan(self):
        fehler = False
        for i, widget in enumerate(self.np_knoten_widgets):
            sol = self.np_loesungen[i]
            for key, entry in widget.fields.items():
                val = entry.get().replace(",", ".").strip()
                if val == str(sol[key]):
                    entry.configure(fg_color="#2e7d32", text_color="white")
                else:
                    entry.configure(fg_color="#c62828", text_color="white")
                    fehler = True

            if (sol["gp"] == 0) != widget.is_critical_selected:
                fehler = True
                widget.configure(border_color="#c62828")

        if not fehler:
            self.np_feedback.configure(text="✅ Alles richtig! Netzplan und Kritischer Pfad stimmen.", text_color="green")
        else:
            self.np_feedback.configure(text="❌ Fehler in den Werten oder beim Kritischen Pfad.", text_color="red")

        # --- GANTT ---

    def setup_gantt_screen(self):
        self.gantt_content_frame = customtkinter.CTkFrame(self.gantt_frame, fg_color="transparent")
        self.gantt_content_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.gantt_input_side = customtkinter.CTkFrame(self.gantt_content_frame, width=300)
        self.gantt_input_side.pack(side="left", fill="y", padx=(0, 10), pady=10)

        customtkinter.CTkLabel(self.gantt_input_side, text="Zeitplanung", font=("Arial", 18, "bold")).pack(pady=10)
        self.gantt_entry_container = customtkinter.CTkFrame(self.gantt_input_side, fg_color="transparent")
        self.gantt_entry_container.pack(pady=10, padx=10)

        self.gantt_canvas_fullscreen = customtkinter.CTkCanvas(self.gantt_content_frame, bg="white",highlightthickness=0)
        self.gantt_canvas_fullscreen.pack(side="left", fill="both", expand=True, pady=10)

        self.gantt_hint = customtkinter.CTkLabel(self.gantt_input_side, text="", wraplength=250)
        self.gantt_hint.pack(side="bottom", pady=10)

        customtkinter.CTkButton(self.gantt_input_side, text="Prüfen", command=self.prüfe_gantt,fg_color="#1f6aa5").pack(side="bottom", pady=5)

    def neue_gantt_aufgabe(self):
        self.gantt_geloest = False
        self.gantt_modus = random.randint(0, 1)
        self.gantt_canvas_fullscreen.delete("all")

        d = [random.randint(3, 6) for _ in range(5)]
        f0 = 0
        e0 = f0 + d[0]
        f1, f2 = e0, e0
        e1, e2 = f1 + d[1], f2 + d[2]
        f3 = max(e1, e2)
        e3 = f3 + d[3]
        f4 = e3
        e4 = f4 + d[4]

        zeiten = [(f0, e0), (f1, e1), (f2, e2), (f3, e3), (f4, e4)]
        vorg = ["-", "A", "A", "B, C", "D"]
        namen = ["Analyse", "Design", "Konzept", "Umsetzung", "Test"]
        ids = ["A", "B", "C", "D", "E"]

        self.gantt_daten = []
        for i in range(5):
            self.gantt_daten.append({"id": ids[i], "name": namen[i], "dauer": d[i], "vorg": vorg[i],"korrekt_faz": zeiten[i][0], "korrekt_fez": zeiten[i][1]})

        msg = "Modus: BERECHNEN" if self.gantt_modus == 0 else "Modus: ABLESEN"
        self.gantt_hint.configure(text=msg, text_color=("black", "white"))

        if self.gantt_modus == 1: self.gantt_geloest = True

        self.draw_gantt_exercise_ui()
        self.update()
        self.draw_fullscreen_gantt()

    def draw_gantt_exercise_ui(self):
        for widget in self.gantt_entry_container.winfo_children():
            widget.destroy()

        self.gantt_inputs = []
        headers = ["ID", "Vorg.", "Dauer", "FAZ", "FEZ"]
        for c, h in enumerate(headers):
            customtkinter.CTkLabel(self.gantt_entry_container, text=h, font=("Arial", 11, "bold")).grid(row=0, column=c,
                                                                                                        padx=4)

        for i, data in enumerate(self.gantt_daten):
            customtkinter.CTkLabel(self.gantt_entry_container, text=data["id"]).grid(row=i + 1, column=0)
            customtkinter.CTkLabel(self.gantt_entry_container, text=data["vorg"]).grid(row=i + 1, column=1)

            if self.gantt_modus == 0:
                dauer_text = str(data["dauer"])
            else:
                dauer_text = "?"

            customtkinter.CTkLabel(self.gantt_entry_container, text=dauer_text, font=("Arial", 11, "italic")).grid(
                row=i + 1, column=2)

            faz_e = customtkinter.CTkEntry(self.gantt_entry_container, width=40, justify="center")
            faz_e.grid(row=i + 1, column=3, padx=2, pady=2)
            fez_e = customtkinter.CTkEntry(self.gantt_entry_container, width=40, justify="center")
            fez_e.grid(row=i + 1, column=4, padx=2, pady=2)

            self.gantt_inputs.append({"faz": faz_e, "fez": fez_e})

    def prüfe_gantt(self):
        fehler = False
        for i, data in enumerate(self.gantt_daten):
            try:
                val_faz = int(self.gantt_inputs[i]["faz"].get())
                val_fez = int(self.gantt_inputs[i]["fez"].get())

                if val_faz == data["korrekt_faz"] and val_fez == data["korrekt_fez"]:
                    self.gantt_inputs[i]["faz"].configure(fg_color="#2e7d32", text_color="white")
                    self.gantt_inputs[i]["fez"].configure(fg_color="#2e7d32", text_color="white")
                else:
                    self.gantt_inputs[i]["faz"].configure(fg_color="#c62828", text_color="white")
                    self.gantt_inputs[i]["fez"].configure(fg_color="#c62828", text_color="white")
                    fehler = True
            except:
                fehler = True

        if not fehler:
            self.gantt_geloest = True
            self.gantt_hint.configure(text="✅ Korrekt! Diagramm erstellt.", text_color="green")
            self.draw_fullscreen_gantt()
        else:
            self.gantt_hint.configure(text="❌ Fehler in der Berechnung.", text_color="red")

    def draw_fullscreen_gantt(self):
        if not hasattr(self, 'gantt_daten'): return
        self.gantt_canvas_fullscreen.delete("all")

        self.update_idletasks()
        c_width = self.gantt_canvas_fullscreen.winfo_width()
        if c_width < 100: c_width = 700  # Fallback

        x_offset = c_width * 0.2
        y_offset = 80
        row_height = 55

        max_t = max(d["korrekt_fez"] for d in self.gantt_daten) + 1
        scale = (c_width - x_offset - 50) / max_t

        for t in range(int(max_t) + 1):
            x = x_offset + (t * scale)
            self.gantt_canvas_fullscreen.create_line(x, y_offset - 10, x, y_offset + (5 * row_height), fill="#f0f0f0")
            self.gantt_canvas_fullscreen.create_text(x, y_offset - 35, text=str(t), font=("Arial", 10, "bold"))

        for i, data in enumerate(self.gantt_daten):
            y = y_offset + (i * row_height) + 10

            self.gantt_canvas_fullscreen.create_text(x_offset - 20, y + 15,text=f"{data['id']}: {data['name']}",anchor="e", font=("Arial", 11, "bold"))

            if self.gantt_geloest:
                xs = x_offset + (data["korrekt_faz"] * scale)
                xe = x_offset + (data["korrekt_fez"] * scale)
                self.gantt_canvas_fullscreen.create_rectangle(xs, y, xe, y + 30,fill="#3498db", outline="#2471a3")


if __name__ == "__main__":
    app = Mathetrainer()
    app.mainloop()

