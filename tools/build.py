#!/usr/bin/env python3
"""Statik sayfaları üretir ve indirilecek görsel listesini (tools/images.txt) yazar.

Kullanım (proje kökünden):  python3 tools/build.py
"""
import html
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ORIGIN = "https://www.dukkanoglu.com/wp-content/uploads"
YEAR_RANGE = "2015–2026"

# ---------------------------------------------------------------- görseller
def names_dsc(nums):
    return nums

GALLERIES = {
    "okul": ("2015/11", [
        "DSC_3510", "DSC_4353", "DSC_4366", "DSC_4377", "DSC_4381", "DSC_4412", "DSC_4420",
        "DSC_4449", "DSC_4466", "DSC_4485-", "DSC_4491", "DSC_4516", "DSC_4632", "DSC_4661",
    ], "jpg"),
    "araclar-dsc": ("2015/11", [
        "DSC_3510", "DSC_4353", "DSC_4366", "DSC_4377", "DSC_4381", "DSC_4412", "DSC_4420",
        "DSC_4449", "DSC_4466", "DSC_4485-", "DSC_4491", "DSC_4516", "DSC_4632", "DSC_4661",
    ], "jpg"),
    "araclar-ek": ("2015/11", [f"dukkanogluek{i}" for i in range(1, 69) if i != 38], "jpeg"),
    "kahvalti": ("2020/01", [
        "DSC_7902", "DSC_7905", "DSC_7915", "DSC_7918", "DSC_7920", "DSC_7921", "DSC_7926",
        "DSC_7934", "DSC_7937", "DSC_7945", "DSC_7946", "DSC_7952", "DSC_7964", "DSC_7977",
        "DSC_7988", "DSC_7992", "DSC_8004", "DSC_8013", "DSC_8017", "DSC_8023", "DSC_8028",
        "DSC_8038", "DSC_8043", "DSC_8048", "DSC_8055", "DSC_8064", "DSC_8070", "DSC_8079",
        "DSC_8090", "DSC_8103", "DSC_8140", "DSC_8145R",
    ], "jpg"),
    "teknoloji": ("2015/12", [
        "DSC_4517", "DSC_4518", "DSC_4522", "DSC_4537", "DSC_4539", "DSC_4540", "DSC_4544",
        "DSC_4554", "DSC_4558", "DSC_4560", "DSC_4561", "DSC_4575", "DSC_4578", "DSC_4585-",
        "DSC_4601-", "DSC_4607-", "DSC_4611", "DSC_4632-", "DSC_4651-", "DSC_4668", "DSC_4670",
    ], "jpg"),
    "yonelt": ("2015/12", [
        "DSC_4362", "DSC_4390", "DSC_4399", "DSC_4429", "DSC_4438", "DSC_4439", "DSC_4474",
        "DSC_4479-", "DSC_4484-", "DSC_4493", "DSC_4494", "DSC_4497",
    ], "jpg"),
}

# Araç hijyen/ilaçlama görselleri: sitede yalnızca bu boyutlar yayınlanıyor
CORONA = [
    ("2020/03", "corona1-1024x768.jpeg"), ("2020/03", "corona6-1024x768.jpeg"),
    ("2020/03", "corona7-1024x768.jpeg"), ("2020/03", "corona4-768x1024.jpeg"),
    ("2020/03", "corona5-1024x768.jpeg"), ("2020/03", "corona3-768x1024.jpeg"),
    ("2020/03", "corona8-1024x768.jpeg"),
]

SLIDES = [
    ("2020/01", "slide_a.jpg"), ("2020/01", "slide_b.jpg"), ("2015/11", "slide03.jpg"),
    ("2015/11", "yonelt_slide01.jpg"), ("2015/11", "tek_slide02.jpg"),
]

manifest = []  # (url, yerel yol)


def reg(folder, subdir, filename):
    url = f"{ORIGIN}/{folder}/{filename}"
    local = f"assets/img/{subdir}/{filename}"
    if (url, local) not in manifest:
        manifest.append((url, local))
    return local


def gallery_items(key):
    folder, names, ext = GALLERIES[key]
    return [reg(folder, key.split("-")[0], f"{n}.{ext}") for n in names]


LOGO = reg("2015/08", "ortak", "logo.png")
LOGO2X = reg("2015/08", "ortak", "logo@2x.png")

# ---------------------------------------------------------------- şablon
NAV = [
    ("index.html", "Anasayfa"),
    ("okul-servisi.html", "Okul Servisi"),
    ("ozel-turlar.html", "Özel Turlar"),
    ("personel-tasimaciligi.html", "Personel Taşımacılığı"),
    ("araclarimiz.html", "Araçlarımız"),
    ("foto-galeri.html", "Foto Galeri"),
    ("hakkimizda.html", "Hakkımızda"),
    ("iletisim.html", "İletişim"),
]

PHONE_MAIN = ("0 252 214 73 77", "+902522147377")


def esc(s):
    return html.escape(s, quote=True)


def layout(filename, title, description, body, crumb=None, hero=None, parent=None):
    nav = "\n".join(
        '          <li><a href="{h}"{c}>{t}</a></li>'.format(
            h=h, t=t, c=' aria-current="page"' if (h == filename or h == parent) else ""
        )
        for h, t in NAV
    )
    page_title = (
        "Dükkanoğlu Taşımacılık – Muğla Okul Servisi, Personel Servisi"
        if filename == "index.html"
        else f"{title} – Dükkanoğlu Taşımacılık"
    )
    head_block = ""
    if filename != "index.html":
        crumbs = '<a href="index.html">Anasayfa</a>'
        if parent:
            ptitle = dict(NAV)[parent]
            crumbs += f' / <a href="{parent}">{esc(ptitle)}</a>'
        crumbs += f" / {esc(title)}"
        head_block = f"""
    <div class="page-title">
      <div class="container">
        <h1>{esc(title)}</h1>
        <div class="breadcrumb">{crumbs}</div>
      </div>
    </div>"""
    return f"""<!DOCTYPE html>
<html lang="tr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(page_title)}</title>
  <meta name="description" content="{esc(description)}">
  <link rel="icon" href="{LOGO}">
  <link rel="stylesheet" href="assets/css/style.css">
</head>
<body>
  <div class="topbar">
    <div class="container">Tel: <a href="tel:{PHONE_MAIN[1]}">&nbsp;{PHONE_MAIN[0]}</a></div>
  </div>

  <header class="site-header">
    <div class="container">
      <a class="logo" href="index.html" aria-label="Dükkanoğlu Taşımacılık – Anasayfa">
        <img src="{LOGO}" srcset="{LOGO} 1x, {LOGO2X} 2x" alt="Dükkanoğlu Taşımacılık">
      </a>
      <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="menu">☰ Menü</button>
      <nav class="nav" id="menu" aria-label="Ana menü">
        <ul>
{nav}
        </ul>
      </nav>
    </div>
  </header>
{hero or ""}{head_block}
  <main>
{body}
  </main>

  <footer class="site-footer">
    <div class="container">
      <span>© {YEAR_RANGE} Dükkanoğlu Ltd. Şti.</span>
      <span>Menteşe / MUĞLA</span>
    </div>
  </footer>

  <script src="assets/js/main.js"></script>
</body>
</html>
"""


def gallery_html(items, alt):
    out = ['    <div class="gallery">']
    for i, src in enumerate(items, 1):
        out.append(
            f'      <a href="{src}" data-lightbox><img src="{src}" alt="{esc(alt)} {i}" loading="lazy"></a>'
        )
    out.append("    </div>")
    return "\n".join(out)


pages = {}

# ---- Anasayfa
slides = [reg(f, "slider", n) for f, n in SLIDES]
hero = """
  <div class="hero" aria-label="Öne çıkan görseller">
    <div class="slides">
""" + "\n".join(
    f'      <div class="slide"><img src="{s}" alt="Dükkanoğlu Taşımacılık"{"" if i == 0 else " loading=\"lazy\""}></div>'
    for i, s in enumerate(slides)
) + """
    </div>
    <div class="slider-dots"></div>
  </div>
"""
hijyen = [reg(f, "hijyen", n) for f, n in CORONA]
hijyen_gallery = gallery_html(hijyen, "Araç temizlik ve ilaçlama çalışması")

pages["index.html"] = layout(
    "index.html",
    "Anasayfa",
    "Dükkanoğlu Taşımacılık: Muğla okul servisi, personel taşımacılığı ve özel tur hizmetleri.",
    f"""    <section>
      <div class="container">
        <h2>Güvenle, zamanında, konforla</h2>
        <p class="lead">2009'dan beri Muğla'da öğrenci ve personel taşımacılığı yapıyoruz.</p>
        <div class="cards" style="margin-top:1.8rem">
          <a class="card" href="okul-servisi.html"><h3>Okul Servisi</h3><p>Geleceğimizin teminatı çocuklarımızın, eğitim hayatları boyunca güvenle yolculuk etmeleri en büyük önceliğimiz.</p></a>
          <a class="card" href="personel-tasimaciligi.html"><h3>Personel Taşımacılığı</h3><p>Çalışanlarınızın zamanında ve güvenle olmaları gereken yere ulaşmasını, güven ve konforla sağlıyoruz.</p></a>
          <a class="card" href="ozel-turlar.html"><h3>Gezi Turları</h3><p>Türkiye'nin en önemli turizm noktalarına, uzman kadromuzla seyahat etmenin keyfini çıkarın.</p></a>
          <a class="card" href="ozel-turlar.html"><h3>Özel Tur</h3><p>Her türlü faaliyetinizde isteğinize uygun aracı en kısa sürede hizmetinize sunarak, ülkenin her köşesine konforlu ulaşım imkânı.</p></a>
        </div>
      </div>
    </section>

    <section class="section-soft">
      <div class="container notice">
        <div>
          <h2>Servislerimizde hijyen önlemleri</h2>
          <p>Yolcularımızın sağlığı bizim için en az güvenlikleri kadar önemli. Servis hizmetlerinde kullanılan tüm araçlarımız düzenli olarak temizlenir, dezenfekte edilir ve gerektiğinde ilaçlanır. Böylece çocuklarımızın ve çalışanlarımızın daha sağlıklı bir ortamda, güvenle yolculuk etmesini sağlıyoruz.</p>
          <p>Araç içi hijyen ve temizlik kontrollerini sezon boyunca aksatmadan sürdürüyoruz.</p>
        </div>
        <div>
{hijyen_gallery}
        </div>
      </div>
    </section>

    <section>
      <div class="container" style="text-align:center">
        <h2>Dükkanoğlu Taşımacılık</h2>
        <p class="lead" style="margin-inline:auto">Detaylı bilgi için bizimle iletişime geçin.</p>
        <p style="margin-top:1.2rem"><a class="btn" href="iletisim.html">Bize ulaşın</a></p>
      </div>
    </section>""",
    hero=hero,
)

# ---- Okul Servisi
okul = gallery_items("okul")
pages["okul-servisi.html"] = layout(
    "okul-servisi.html",
    "Okul Servisi",
    "Dükkanoğlu Taşımacılık okul servisi hizmet verdiği okullar ve servis kayıtları.",
    f"""    <section>
      <div class="container">
        <p class="lead"><strong>Okul servis kayıtlarımız başlamıştır.</strong></p>
        <ul class="check-list">
          <li>Muğla Gazi Anadolu Lisesi</li>
          <li><a href="teknoloji-ve-kultur-koleji.html">Teknoloji ve Kültür Koleji</a></li>
          <li><a href="yonelt-koleji.html">Yönelt Koleji</a></li>
          <li>Yatağan Anadolu Lisesi</li>
          <li>Yatağan Gazi Anadolu Lisesi</li>
          <li>Yatağan Sağlık Meslek Lisesi</li>
          <li>Bayır Lisesi</li>
          <li>Ula Hüseyin Ercan Ermaş Mermer Anadolu Lisesi</li>
        </ul>
      </div>
    </section>
    <section class="section-soft">
      <div class="container">
{gallery_html(okul, "Okul servisi aracı")}
      </div>
    </section>""",
)

# ---- Özel Turlar
pages["ozel-turlar.html"] = layout(
    "ozel-turlar.html",
    "Özel Turlar",
    "Özel günler ve şehir dışı geziler için araç temini.",
    """    <section>
      <div class="container prose">
        <p class="lead">Özel günlerde araç temin edilir.</p>
        <p class="lead">Gezilerde şehir dışına araç temin edilir.</p>
        <p style="margin-top:1.5rem"><a class="btn" href="iletisim.html">Bilgi ve rezervasyon</a></p>
      </div>
    </section>""",
)

# ---- Personel Taşımacılığı
pages["personel-tasimaciligi.html"] = layout(
    "personel-tasimaciligi.html",
    "Personel Taşımacılığı",
    "Şirketler, fabrikalar ve kurumlar için hızlı, güvenli personel taşımacılığı.",
    """    <section>
      <div class="container prose">
        <p class="lead">Hızlı, güvenli ve sorunsuz personel taşımacılığı için hizmetinizdeyiz.</p>
        <p style="margin-top:1.5rem"><a class="btn" href="iletisim.html">Teklif alın</a></p>
      </div>
    </section>""",
)

# ---- Araçlarımız
araclar = gallery_items("araclar-dsc") + gallery_items("araclar-ek")
pages["araclarimiz.html"] = layout(
    "araclarimiz.html",
    "Araçlarımız",
    "Dükkanoğlu Taşımacılık araç filosu.",
    f"""    <section>
      <div class="container">
{gallery_html(araclar, "Araç")}
      </div>
    </section>""",
)

# ---- Foto Galeri (Birlik ve Beraberlik Kahvaltımız)
kahvalti = gallery_items("kahvalti")
pages["foto-galeri.html"] = layout(
    "foto-galeri.html",
    "Foto Galeri",
    "Birlik ve Beraberlik Kahvaltımızdan fotoğraflar.",
    f"""    <section>
      <div class="container">
        <h2>Birlik ve Beraberlik Kahvaltımız</h2>
{gallery_html(kahvalti, "Birlik ve Beraberlik Kahvaltısı")}
      </div>
    </section>""",
)

# ---- Hakkımızda
pages["hakkimizda.html"] = layout(
    "hakkimizda.html",
    "Hakkımızda",
    "Dükkanoğlu Turizm'in hikâyesi: 1989'dan bugüne Muğla'da.",
    """    <section>
      <div class="container prose">
        <p>1989 yılında Orgeneral Mustafa Muğlalı İşhanı'nda açtığımız küçük bir tuhafiye dükkânında başladı iş hayatımız; aynı zamanda Datça, Marmaris gibi ilçelerimizde uzun yıllar pazarcılık yaptık. Sayın Muğla halkına hizmet vermeye devam ediyoruz.</p>
        <p>23.06.2009 tarihinden itibaren öğrenci ve personel taşımacılığı yapmaktayız. Güvenilir, tecrübeli ve son model araçlarımızla hizmet vermekteyiz. Geniş araç filosu, deneyimli şoförler, güler yüzlü ve güvenilir hostesler ile geleceğimiz olan çocuklarımız başta olmak üzere güvenli ve konforlu bir ulaşım sağlayan Dükkanoğlu Turizm, bugüne dek birçok özel ve devlet okuluna çözüm ortağı olmuştur.</p>
        <p>Emin ellerde güvenli taşımacılık yapmak için tüm çabamızla çalışmaktayız. Dükkanoğlu Turizm tüm enerjisini mutlu öğrencileri için bir araya getirdi.</p>
        <p>Ayrıca şirketlere, holdinglere, fabrikalara, özel ve kamu kuruluşlarına personel taşımacılığı konusunda da hizmet vermektedir. Müşteri memnuniyetini ve güler yüzlü hizmeti en temel ilke olarak kabul ederek kendi alanında en iyisi olmak için her geçen gün yenilenen teknolojiyi ve güvenlik unsurlarını göz önünde tutarak yoluna devam etmektedir.</p>
        <p>Servis turizm 365 gün ve 24 saat kesintisiz hizmet sürekliliği ve üst model minibüs ve binek araçlara sahiptir. Sizlerin yol arkadaşı olarak sürdürdüğümüz bu keyif dolu ticari faaliyetlerimizde desteklerinizden dolayı teşekkür eder, iyi yolculuklar dileriz.</p>
        <p>Dükkanoğlu Turizm olarak tek hedefimiz sizin mutluluğunuz ve bizim hizmetimizdir.</p>
      </div>
    </section>""",
)

# ---- İletişim
pages["iletisim.html"] = layout(
    "iletisim.html",
    "İletişim",
    "Dükkanoğlu Taşımacılık adres ve telefon bilgileri.",
    f"""    <section>
      <div class="container">
        <p class="lead">Dükkanoğlu Turizm Tekstil Taşımacılık İnşaat San. ve Tic. Ltd. Şti.</p>
        <div class="contact-grid" style="margin-top:1.5rem">
          <div class="card">
            <h3>Adres</h3>
            <p>Menteşe / MUĞLA</p>
          </div>
          <div class="card">
            <h3>Telefon</h3>
            <p>Tel: <a href="tel:+902522147377">0 252 214 73 77</a></p>
            <p>Faks: 0 252 214 73 77</p>
            <p>Cep: <a href="tel:+905324601283">0 532 460 12 83</a> – <a href="tel:+905304977377">0 530 497 73 77</a></p>
          </div>
        </div>
      </div>
    </section>""",
)

# ---- Kolej sayfaları
for fname, title, key in [
    ("teknoloji-ve-kultur-koleji.html", "Teknoloji ve Kültür Koleji", "teknoloji"),
    ("yonelt-koleji.html", "Yönelt Koleji", "yonelt"),
]:
    items = gallery_items(key)
    pages[fname] = layout(
        fname, title, f"{title} servis araçları.",
        f"""    <section>
      <div class="container">
{gallery_html(items, title)}
      </div>
    </section>""",
        parent="okul-servisi.html",
    )

# ---- 404
pages["404.html"] = layout(
    "404.html", "Sayfa bulunamadı", "Aradığınız sayfa bulunamadı.",
    """    <section>
      <div class="container prose">
        <p class="lead">Aradığınız sayfa bulunamadı.</p>
        <p><a class="btn" href="index.html">Anasayfaya dön</a></p>
      </div>
    </section>""",
)

# ---------------------------------------------------------------- yazma
for name, content in pages.items():
    (ROOT / name).write_text(content, encoding="utf-8")

(ROOT / "tools" / "images.txt").write_text(
    "\n".join(f"{u}\t{l}" for u, l in manifest) + "\n", encoding="utf-8"
)
print(f"{len(pages)} sayfa, {len(manifest)} görsel kaydı yazıldı.")
