#!/usr/bin/env python3
"""DewyHosting adatkezelési tájékoztató és ÁSZF PDF."""

from pathlib import Path

from fpdf import FPDF

FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")
OUT = Path(__file__).parent / "legal" / "adatkezeles.pdf"

ORANGE = (255, 122, 26)
BLACK = (12, 12, 14)
GRAY = (70, 70, 74)


class LegalPDF(FPDF):
    def header(self):
        self.set_fill_color(*ORANGE)
        self.rect(0, 0, 210, 8, "F")
        self.set_y(14)
        self.set_font("DejaVu", "B", 11)
        self.set_text_color(*ORANGE)
        self.cell(0, 6, "DewyHosting  -  Hobbi projekt", new_x="LMARGIN", new_y="NEXT")
        self.set_font("DejaVu", "", 8)
        self.set_text_color(*GRAY)
        self.cell(
            0,
            5,
            "Adatkezelési tájékoztató és Általános Szerződési Feltételek",
            new_x="LMARGIN",
            new_y="NEXT",
        )
        self.ln(2)

    def footer(self):
        self.set_y(-16)
        self.set_draw_color(*ORANGE)
        self.set_line_width(0.4)
        self.line(15, self.get_y(), 195, self.get_y())
        self.ln(2)
        self.set_font("DejaVu", "", 8)
        self.set_text_color(*GRAY)
        self.cell(0, 5, "DewyHosting | Frankfurt (node1) | Rackhost domain | /adatkezeles", new_x="LMARGIN", new_y="NEXT")
        self.cell(0, 5, str(self.page_no()), align="R")

    def h1(self, text):
        self.ln(3)
        self.set_x(self.l_margin)
        self.set_font("DejaVu", "B", 14)
        self.set_text_color(*BLACK)
        self.multi_cell(0, 8, text)
        self.set_draw_color(*ORANGE)
        self.set_line_width(0.6)
        y = self.get_y()
        self.line(15, y, 70, y)
        self.ln(4)

    def h2(self, text):
        self.ln(2)
        self.set_x(self.l_margin)
        self.set_font("DejaVu", "B", 11)
        self.set_text_color(*ORANGE)
        self.multi_cell(0, 7, text)
        self.ln(1)

    def p(self, text):
        self.set_x(self.l_margin)
        self.set_font("DejaVu", "", 10)
        self.set_text_color(*BLACK)
        self.multi_cell(0, 5.5, text)
        self.ln(1.5)

    def bullet(self, text):
        self.set_x(self.l_margin)
        self.set_font("DejaVu", "", 10)
        self.set_text_color(*BLACK)
        self.cell(6, 5.5, "-")
        self.multi_cell(0, 5.5, text)
        self.set_x(self.l_margin)
        self.ln(0.5)


def build():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    pdf = LegalPDF(format="A4", unit="mm")
    pdf.set_auto_page_break(auto=True, margin=22)
    pdf.add_font("DejaVu", "", str(FONT_DIR / "DejaVuSans.ttf"))
    pdf.add_font("DejaVu", "B", str(FONT_DIR / "DejaVuSans-Bold.ttf"))
    pdf.set_margins(15, 28, 15)
    pdf.add_page()

    pdf.set_x(pdf.l_margin)
    pdf.set_font("DejaVu", "B", 20)
    pdf.set_text_color(*BLACK)
    pdf.multi_cell(0, 10, "Adatkezelési tájékoztató és ÁSZF")
    pdf.set_x(pdf.l_margin)
    pdf.set_font("DejaVu", "", 10)
    pdf.set_text_color(*GRAY)
    pdf.multi_cell(0, 6, "Hatályos: 2026. október 11.  |  Verzió: 1.0  |  Elérhető: /adatkezeles")
    pdf.ln(2)
    pdf.p(
        "A DewyHosting hobbi projekt. A weboldal használatáért, a Discord közösségért "
        "és az adatkezelési dokumentumokért nem kérünk pénzt. A megjelenített "
        "szervercsomag-árak kizárólag tájékoztató, hobbi jellegű hozzájárulást jelentenek; "
        "a projekt nem gazdasági társaság, áfás számlát nem állít ki, és nem folytat "
        "üzletszerű kereskedelmi tevékenységet."
    )

    pdf.h1("1. Ki működteti a DewyHostingot?")
    pdf.p(
        "A DewyHosting nem bejegyzett gazdasági társaság, hanem magánszemély által "
        "üzemeltetett hobbi hosting projekt. Kapcsolat: Discord (https://discord.gg/3YTspYyhFQ). "
        "A rendeléseket Discord webhookon keresztül fogadjuk, a kapcsolattartás e-mailben "
        "és Discordon történik."
    )
    pdf.p(
        "A honlap domainneve a Rackhost Zrt. rendszerében van regisztrálva. "
        "A virtuális szerverek (node1) fizikai elhelyezkedése: Németország, Frankfurt."
    )

    pdf.h1("2. A domain-regisztrátor: Rackhost Zrt.")
    pdf.p(
        "A domain név szolgáltatója / regisztrátora – és a domainhez kapcsolódó "
        "tárhely-, DNS- és kapcsolódó szolgáltatások vonatkozásában adatfeldolgozó – "
        "a Rackhost Zrt. Az alábbi adatok a Rackhost nyilvános cég- és kapcsolati "
        "adatai alapján szerepelnek:"
    )
    pdf.bullet("Cégnév: Rackhost Zrt.")
    pdf.bullet("Székhely: 6722 Szeged, Tisza Lajos körút 41.")
    pdf.bullet("Üzemeltetési / levelezési cím: 1132 Budapest, Victor Hugo utca 18-22.")
    pdf.bullet("Cégjegyzékszám: 06-10-000489")
    pdf.bullet("Adószám: 25333572-2-06")
    pdf.bullet("Nyilvántartó cégbíróság: Szegedi Törvényszék Cégbírósága")
    pdf.bullet("Kamarai tagság: Csongrád-Csanádi Kereskedelmi és Iparkamara")
    pdf.bullet("Képviselet: Csapó Gergely Gábor vezérigazgató; Virág Zoltán cégvezető")
    pdf.bullet("Honlap: https://www.rackhost.hu")
    pdf.bullet("E-mail: info@rackhost.hu")
    pdf.bullet("Adatvédelmi szabályzat: https://www.rackhost.hu/privacy-policy")
    pdf.p(
        "A Rackhost Zrt. a domain-regisztráció, DNS, webtárhely és az ezekhez "
        "kapcsolódó technikai naplózás (például IP-cím, kapcsolódás időpontja) "
        "körében saját adatkezelési / adatfeldolgozási szabályai szerint jár el. "
        "Ezekről a Rackhost aktuális adatvédelmi dokumentumai adnak tájékoztatást."
    )

    pdf.h1("3. Infrastruktúra és adattárolás helye")
    pdf.bullet("node1 szerverpark: Németország, Frankfurt am Main.")
    pdf.bullet("Az Európai Unió területén belüli tárhely, a GDPR szerinti megfelelő védelem mellett.")
    pdf.bullet("Domain-regisztráció és a domainhez kapcsolódó magyarországi szolgáltatások: Rackhost Zrt. (Magyarország).")
    pdf.bullet("Rendelési értesítések: Discord (Discord Inc. / Discord Netherlands BV) webhook.")
    pdf.p(
        "A virtuális szerveren a megrendelő által telepített szoftverek, botok és "
        "tartalmak felett a megrendelő rendelkezik. A DewyHosting a vendégadatokat "
        "nem olvassa, kivéve üzemzavar, visszaélés-gyanú vagy jogszabályi kötelezettség esetén."
    )

    pdf.h1("4. Milyen adatokat kezelünk?")
    pdf.h2("4.1. Rendelés")
    pdf.p("A rendelési űrlapon kötelezően megadandó:")
    pdf.bullet("szerver / gépnév (a megrendelő által választott azonosító);")
    pdf.bullet("e-mail cím (kapcsolattartás, visszaigazolás);")
    pdf.bullet("választott csomag (Discord csomag vagy egyedi erőforrás-beállítás);")
    pdf.bullet("opcionális kuponkód (pl. HELLO20);")
    pdf.bullet("a rendelés időpontja és a honlap technikai metaadatai (IP, user-agent) a visszaélések ellen.")
    pdf.p(
        "Jogalap: az érintett hozzájárulása (GDPR 6. cikk (1) a)), valamint a "
        "hobbi szolgáltatás teljesítéséhez fűződő jogos érdek / a kérésre történő "
        "lépések (GDPR 6. cikk (1) b) és f))."
    )
    pdf.p(
        "Cél: a virtuális szerver létrehozása, kapcsolattartás, kupon érvényesítése, "
        "visszaélés megelőzése. Tárolás: a szolgáltatás ideje alatt, majd a törlési "
        "kérést vagy a szolgáltatás megszűnését követően indokolatlan késedelem nélkül, "
        "legfeljebb 12 hónapig a panaszkezeléshez."
    )

    pdf.h2("4.2. Honlap-látogatás")
    pdf.p(
        "A weboldal nem használ marketing sütiket, nem kér pénzt, és nem értékesít "
        "személyes adatot. A kiszolgáló (és a Rackhost, ha a domain / tárhely náluk "
        "van) technikai naplókat rögzíthet (IP-cím, időpont, kért URL) a szolgáltatás "
        "biztonsága érdekében, jellemzően rövid ideig."
    )

    pdf.h2("4.3. Discord")
    pdf.p(
        "A közösségi és ügyfélszolgálati csatorna a Discord. A Discord saját "
        "adatkezelési szabályzata: https://discord.com/privacy. A rendelés adatait "
        "a projekt egy Discord webhookon keresztül a saját szervercsatornájára "
        "továbbítja, hogy a kérést emberi ügyintéző lássa."
    )

    pdf.h1("5. Adatfeldolgozók és címzettek")
    pdf.bullet("Rackhost Zrt. – domain, DNS, a domainhez kapcsolódó tárhely és naplózás.")
    pdf.bullet("Frankfurtban üzemelő node1 infrastruktúra – virtuális szerver erőforrás.")
    pdf.bullet("Discord – rendelési értesítés és 24/7 közösségi segítség.")
    pdf.p("Adatot harmadik félnek marketingre, értékesítésre nem adunk át. Pénzt az adatokért nem kérünk és nem fogadunk el.")

    pdf.h1("6. Érintetti jogok")
    pdf.p(
        "Az Infotv. és a GDPR alapján kérheti: tájékoztatást, hozzáférést, helyesbítést, "
        "törlést, korlátozást, adathordozást, tiltakozást, valamint hozzájárulása visszavonását. "
        "Kérelmét Discordon vagy a rendeléskor megadott e-mailre küldött válaszként jelezheti."
    )
    pdf.p(
        "Panasz: Nemzeti Adatvédelmi és Információszabadság Hatóság (NAIH), "
        "1055 Budapest, Falk Miksa utca 9-11., ugyfelszolgalat@naih.hu, https://www.naih.hu"
    )

    pdf.h1("7. Általános szerződési feltételek (hobbi szolgáltatás)")
    pdf.h2("7.1. A szolgáltatás jellege")
    pdf.p(
        "A DewyHosting virtuális szerver erőforrást (CPU hányad, RAM, tárhely, hálózat) "
        "biztosít hobbi célra. Ez nem távközlési előfizetés, nem nyilvános felhőszolgáltatói "
        "vállalkozás, és nem minősül a Rackhost Zrt. saját tárhelycsomagjának. "
        "A Rackhost a domain regisztrátora, a gép (node1) Németországban, Frankfurtban van."
    )
    pdf.h2("7.2. Csomagok")
    pdf.p("Discord csomag (tájékoztató listaár, kupon nélkül): 390 Ft / hónap.")
    pdf.bullet("CPU: 3%")
    pdf.bullet("RAM: 300 MB")
    pdf.bullet("Tárhely: 1 GB")
    pdf.bullet("Hálózat: 1 Gbps")
    pdf.p(
        "Egyedi csomag: a megrendelő állítja be a CPU, RAM és tárhely értékét; "
        "az ár a honlapon látható képlet szerint, élőben jelenik meg. "
        "A HELLO20 kupon az első rendelésre 20% kedvezményt ad."
    )
    pdf.p(
        "A honlap, a dokumentumok és a Discord belépés ingyenes. Nem kérünk pénzt "
        "az adatkezelésért, a tájékoztatókért vagy a közösségi tagságért. "
        "A feltüntetett csomagárak hobbi jellegűek, számlaadási kötelezettség nélkül."
    )
    pdf.h2("7.3. Megrendelés")
    pdf.p(
        "A rendelés akkor érvényes, ha a megrendelő megadja a szerver nevét és egy "
        "elérhető e-mail címet, elfogadja jelen dokumentumot, és a kérés a Discord "
        "csatornára megérkezik. A teljesítés emberi visszaigazolástól függ, nem automatikus SLA."
    )
    pdf.h2("7.4. Üzemeltetés, felelősség")
    pdf.p(
        "A segítség 24/7 a Discordon elérhető, hobbi kapacitás szerint, gyors válaszra "
        "törekszünk, de jótállást, kötbért, kártérítési plafont nem vállalunk. "
        "A szolgáltatás „ahogy van” (best effort). Tilos a node1 erőforrásait jogellenes "
        "tevékenységre, spamre, támadásra, kiskorúak sérelmére vagy a frankfurti "
        "adatközpont / német és magyar jog megsértésére használni. Ilyen esetben a "
        "szolgáltatás azonnal felfüggeszthető."
    )
    pdf.h2("7.5. Elhelyezkedés és hálózat")
    pdf.p(
        "node1: Németország, Frankfurt. Hálózati sebesség a Discord csomagban 1 Gbps "
        "portsebesség; a tényleges átvitel a terheléstől és az útvonaltól függ."
    )
    pdf.h2("7.6. Módosítás")
    pdf.p(
        "A dokumentumot a honlapon közzétett PDF hatályos változata tartalmazza. "
        "A mindenkori szöveg: a domain /adatkezeles útvonalán (PDF)."
    )

    pdf.h1("8. Kapcsolat")
    pdf.bullet("Discord: https://discord.gg/3YTspYyhFQ")
    pdf.bullet("Jogi dokumentum: /adatkezeles (PDF)")
    pdf.bullet("Domain-regisztrátor: Rackhost Zrt., info@rackhost.hu")
    pdf.p("Frankfurt · node1 · DewyHosting hobbi projekt")

    pdf.output(str(OUT))
    public = Path(__file__).parent / "adatkezeles" / "adatkezeles.pdf"
    public.parent.mkdir(parents=True, exist_ok=True)
    public.write_bytes(OUT.read_bytes())
    print(f"Wrote {OUT}")
    print(f"Wrote {public}")


if __name__ == "__main__":
    build()
