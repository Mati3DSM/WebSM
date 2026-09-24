#!/usr/bin/env python3
"""Builds the six static pages of the Supermarket site."""
import html
import pathlib

OUT = pathlib.Path(__file__).parent
CDN = "https://cdn.prod.website-files.com/66730869bdf27a5a83765455/"
REEL_MP4 = ("https://cdn.prod.website-files.com/66730869bdf27a5a83765455%2F"
            "66ccb3fab9b13427bc559e96_Web%20Reel%20Sin%20Logo%20Al%20Final-transcode.mp4")

IMG = {
    "board":    CDN + "66d1d1e183b44a53856747b8_65a7cdaf61dd0965e6c71514_Mesa%20de%20trabajo%2068.png",
    "abstract": CDN + "6673086abdf27a5a83765536_abstract.png",
    "gif_hero": CDN + "689a4f18f77e50061b6e9778_Comp_1_1.gif",
    "gif_brand": CDN + "689378ecf3046648477eaaca_Comp%20(1).gif",
    "gif_film": CDN + "68937c266963a5439fc81f73_Comp%2B2.gif",
    "gif_strat": CDN + "68937d6105777952dee55ca6_Comp%2B4.gif",
    "gif_ux":   CDN + "6894ca1a85f93d0aee4cc932_Comp%2B3.gif",
    "ab1": CDN + "6673086abdf27a5a8376551c_hamza-shaikh-uXtvnZl_FWM-unsplash.webp",
    "ab2": CDN + "6673086abdf27a5a8376551d_louise-viallesoubranne-5EhN4wbfvBc-unsplash.webp",
    "ab3": CDN + "6673086abdf27a5a83765531_kobu-agency-MBtcLadqc6c-unsplash.webp",
    "ab4": CDN + "6673086abdf27a5a83765518_philipp-mandler-CiNHG2xuVlQ-unsplash.webp",
    "ab5": CDN + "6673086abdf27a5a83765519_annie-spratt-hCb3lIB8L8E-unsplash.webp",
    "of2": CDN + "66d1ff9214af8e80f180c4eb_oficina02.jpg",
    "of3": CDN + "66d1fecd8d1a247453342a89_oficina03.jpg",
    "of1": CDN + "66d1fecc7c2e698c39ffccbd_oficina01_V2.png",
    "ai":  CDN + "68408dd3a95e332b1bd3e712_SM%20About%20Us_V2.jpg",
    "contact": CDN + "6673086abdf27a5a83765535_6443e29428b76c2c75ba68c3_635fc1d77b758d09fde119e9_006.webp",
}
TEAM = [
    ("Martín Marinovic", "Founder", CDN + "668881ab93250e3d7655eb7b_martin.jpeg"),
    ("Andrés Schmisser", "Founder", CDN + "668881d590384a51e7e5c0ad_andres.jpeg"),
    ("Ignacio Acosta", "Global Business Development", CDN + "668881e20dff414077429c9f_Nacho_2.jpg"),
    ("Catalina Mulhall", "Creative Director", CDN + "6688830b8879e12b63950642_catalina.jpeg"),
    ("George Marinovic", "Finance &amp; HR GM", CDN + "6688831cf9edc70638174f13_george.jpeg"),
    ("Hernán Marinovic", "Accounts GM", CDN + "668883330f5902791d386ece_hernan.jpeg"),
]

WORKS = [
    ("Swift Picante", "swift-picante"), ("Swift Verano", "swift-verano"),
    ("Ficohsa ¡Gana un carro por mes!", "ficohsa-gana-un-carro-por-mes"),
    ("Barça Games Social Media", "barca-games-social-media"),
    ("Ficohsa Mastercard AA", "ficohsa-tarjeta-mastercard"),
    ("OKY Digital", "oky-digital"), ("Swift Veggies", "swift-veggies"),
    ("Swift Categorías", "swift-categorias"), ("Tienda La Virginia", "tienda-la-virginia"),
    ("Método UCEMA", "metodo-ucema"), ("P!CKERS by McCain", "p-ckers-by-mccain"),
    ("Aero Assist Handling", "aero-assist-handling"),
    ("Brand Character — Rob", "brand-character---rob"),
    ("Revlon Love is On", "revlon-love-is-on"), ("Revlon Naté", "revlon-nate"),
    ("Barça Games", "barca-games"), ("Revlon Colorburst", "revlon-butter"),
    ("Revlon", "revlon"), ("Coca Cola", "coca-cola"), ("Izzi", "izzi"),
    ("Tigo Rebranding", "tigo-rebranding"), ("Sodastream", "sodastream"),
    ("Nubceo", "nubceo"), ("Tigo Money", "beooty-78367"), ("Prester", "prester"),
    ("Facebank", "facebank"), ("UCEMA", "timetracking-2c951"), ("PEISA", "peisa"),
    ("Vireyes", "vireyes"), ("Lati", "lati"), ("Chocolates Arcor", "chocolates-arcor"),
    ("Serenito", "serenito"), ("Oky", "oky"), ("Felaban", "felaban"),
    ("Stanley", "stanley"), ("Eron", "eron"), ("Glenhaven", "glanhaven"),
    ("Delicia", "delicia"), ("GoGym", "gogym"), ("Arcor Frutas", "arcor-frutas"),
    ("Tigoooool", "tigoooool"), ("Clave", "clave"), ("Miller", "miller"),
    ("Rob Ortiz", "rob-ortiz"), ("Deconté", "deconte"),
    ("Club de la Cerveza", "club-de-la-cerveza"), ("Swift Grasa", "swift-grasa"),
    ("Natural One", "natural-one"), ("Levite Limonada", "levite-limonada"),
    ("Hogareñas", "hogarenas"), ("Mr Pops", "mr-pops"),
    ("Natural Break — Arcor", "natural-break--arcor"), ("Prestix", "prestix"),
    ("Quilmes Pumas", "quilmes-pumas"), ("Arcor Patria", "arcor-patria"),
    ("Cutex", "cutex"), ("Wing", "wing"), ("Cutex Pro", "cutex-pro"),
    ("Vital Polvo", "vital-polvo"), ("Alicante", "alicante"),
]

# Placeholder pool for the hover previews — swap for real thumbnails.
POOL = [IMG["board"], IMG["abstract"], IMG["of1"], IMG["of2"], IMG["of3"],
        IMG["ab3"], IMG["ab5"], IMG["ai"]]

NAV = [("Home", "index.html"), ("Services", "services.html"), ("Works", "works.html"),
       ("About", "about.html"), ("Reels", "reel.html"), ("Contact", "contact.html")]

WORK_BASE = "work/"          # local project pages
LIVE_BASE = "https://www.wearesupermarket.com/works/"


def header(current, pre=""):
    links = "".join(
        '<a href="{}{}"{}>{}</a>'.format(
            pre, href, ' aria-current="page"' if href == current else "", label)
        for label, href in NAV)
    return f"""<a class="skip" href="#main">Skip to content</a>
<header class="header">
  <div class="header__inner">
    <a class="brand" href="{pre}index.html" aria-label="Supermarket, home">
      <span class="brand__mark">Supermarket</span>
      <span class="brand__dot" aria-hidden="true"></span>
    </a>
    <button class="nav__toggle" type="button" aria-expanded="false" aria-controls="nav">Menu</button>
    <nav class="nav" id="nav" data-open="false" aria-label="Main">{links}</nav>
  </div>
</header>"""


FOOTER = """<footer class="footer">
  <div class="wrap">
    <a class="footer__cta" href="mailto:hello@wearesupermarket.com">Let's work<br>together</a>
    <div class="footer__grid">
      <div>
        <p class="footer__k">Our locations</p>
        <ul>
          <li class="footer__loc">Buenos Aires, Argentina<a href="mailto:martin@wearesupermarket.com">martin@wearesupermarket.com</a></li>
          <li class="footer__loc">Miami, USA<a href="mailto:nacho@wearesupermarket.com">nacho@wearesupermarket.com</a></li>
          <li class="footer__loc">Madrid, España<a href="mailto:diego@wearesupermarket.com">diego@wearesupermarket.com</a></li>
        </ul>
      </div>
      <div>
        <p class="footer__k">Connect with us</p>
        <ul>
          <li><a href="https://www.instagram.com/wearesupermarket/" rel="noopener">Instagram</a></li>
          <li><a href="https://www.linkedin.com/company/supermarketbrands/" rel="noopener">LinkedIn</a></li>
        </ul>
      </div>
      <div>
        <p class="footer__k">Contact us</p>
        <ul><li><a href="mailto:hello@wearesupermarket.com">hello@wearesupermarket.com</a></li></ul>
      </div>
      <div>
        <p class="footer__k">Start a project</p>
        <a class="btn" href="mailto:hello@wearesupermarket.com" style="margin-top:0;background:#F8F8F7;color:#000;border-color:#F8F8F7">Get in touch</a>
      </div>
    </div>
    <div class="footer__base">
      <p>Rights reserved since 2009 &nbsp; Supermarket Agency™</p>
      <p>Effective, no excuses.</p>
    </div>
  </div>
</footer>"""


def page(title, current, body, description="", pre=""):
    desc = f'\n  <meta name="description" content="{html.escape(description)}">' if description else ""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title} — Supermarket</title>{desc}
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,100..900&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{pre}assets/styles.css">
</head>
<body>
{header(current, pre)}
<main id="main">
{body}
</main>
{FOOTER}
<script src="{pre}assets/main.js"></script>
</body>
</html>
"""


CDN2 = "https://cdn.prod.website-files.com/6673086abdf27a5a837654c3/"

PROJECTS = {
    "barca-games-social-media": {
        "client": "Barça Games",
        "year": "",
        "segment": "",
        "services": "Social media strategy, art direction, design, content production",
        "intro": (
            "We led the social media campaign for Barça Games, a mobile app offering a wide "
            "variety of interactive games for FC Barcelona fans. Our work spanned from creative "
            "strategy to design and production of Instagram posts, Stories, and Reels, helping "
            "build an engaging and playful presence for the app across platforms. We developed "
            "tailored campaigns for key moments in the calendar — including Christmas, King's Day, "
            "and Carnival — each with its own graphic identity and tone, driving visibility, "
            "downloads, and fan engagement through festive, high-impact content."),
        "hero": CDN2 + "6849a3083190def1433ecdbc_IMG%20DAMERO.jpg",
        "media": [
            ("full",  CDN2 + "68499577cfa233b97c3b2d16_CasoBG_Redes_artboard%201.jpg"),
            ("quote", "One app, three seasons, three graphic identities."),
            ("pair",  [(CDN2 + "6849a31a2d57027c3a8b1c1d_PORTADA%2BCHRISTMAS%20(1).gif", "Christmas"),
                       CDN2 + "68499576013472df82753e35_CasoBG_Redes_Artboard%203.jpg"]),
            ("pair",  [CDN2 + "6849957681efda02019d9549_CasoBG_Redes-04.jpg",
                       CDN2 + "68499576b552d4bfdce90495_CasoBG_Redes-05.jpg"]),
            ("bleed", (CDN2 + "6849a338abd145fe33f2bf8d_PORTADA%2BKINGS%20(1).gif", "King's Day")),
            ("pair",  [CDN2 + "684995787d3f19255638a61d_CasoBG_Redes-06.jpg",
                       CDN2 + "6849a3450090ded6eac28e07_POSTEOS%20(1).gif"]),
            ("full",  CDN2 + "68499576f1871ab022e8ebcf_CasoBG_Redes-08.jpg"),
            ("bleed", (CDN2 + "6849a3566ddb2e1ba7f23aa2_PORTADA_CARNAVAL%20(1).gif", "Carnival")),
            ("pair",  [CDN2 + "6849957534494e873acaae6a_CasoBG_Redes-11.jpg",
                       CDN2 + "68499583bd077a2628895460_SALTO.gif"]),
        ],
        "credits": [("Creative direction", "Supermarket"),
                    ("Art direction &amp; design", "Supermarket"),
                    ("Content production", "Supermarket")],
    },
}

# ------------------------------------------------------------------ HOME
featured = WORKS[1], WORKS[0], WORKS[2], WORKS[3], WORKS[4]
cards = []
for i, (name, slug) in enumerate(featured):
    wide = ' card--wide' if i == 0 else ''
    cards.append(f"""      <a class="card{wide}" href="{WORK_BASE}{slug}.html">
        <div class="card__figure"><img src="{POOL[i % len(POOL)]}" alt="" loading="lazy"></div>
        <h3 class="card__name">{name}</h3>
        <p class="meta">View project</p>
      </a>""")

home_body = f"""<section class="hero">
  <video class="hero__media" src="{REEL_MP4}" autoplay muted loop playsinline preload="metadata"
         poster="{IMG['board']}"></video>
  <div class="hero__overlay reveal">
    <h1 class="hero__line">We are Supermarket. A global force of creativity.</h1>
    <p class="hero__side">Effective, no excuses.<br>Independent since 2009</p>
  </div>
</section>

<section class="section wrap">
  <div class="statement">
    <h2 class="display">Where human creativity meets the power of AI</h2>
    <div>
      <p class="lede">An independent agency, a design studio, and a production company, working across
      Buenos Aires, Miami and Madrid.</p>
      <p style="margin-top:22px"><a class="btn btn--ghost" href="services.html">See what we do</a></p>
    </div>
  </div>
</section>

<section class="section--tight wrap">
  <div class="pagehead__row" style="margin-bottom:28px">
    <h2 class="subtitle">Last works</h2>
    <a class="meta" href="works.html" style="color:var(--ink)">All works</a>
  </div>
  <div class="cards">
{chr(10).join(cards)}
  </div>
</section>"""

# ------------------------------------------------------------------ SERVICES
SERVICES = [
    ("Branding and advertising",
     "From billboards to identity toolkits, our team handles every aspect your business needs.",
     ["Brand Identity", "Brand Strategy", "Brand Character", "Art direction",
      "Character Development", "Advertising &amp; Creativity",
      "Packaging", "Point of Purchase Media", "Innovation"], IMG["gif_brand"]),
    ("Films and production",
     "Watch your ideas come to life with a full production and post-production service that launches your story to the next level.",
     ["Filming", "Production &amp; Post-Production", "Motion Graphics", "3D Rendering",
      "Screenwriting", "Animation", "Story Boarding", "Sound Editing"], IMG["gif_film"]),
    ("Strategy and media content",
     "Watch your business take off with a complete plan designed to launch your project to new heights.",
     ["Social Media Strategy Plans", "Ads Campaign Creation", "Media Content Design",
      "Data &amp; Metric Analytics", "Creativity &amp; Innovation in Trends",
      "Social Media Management", "Content Scheduling"], IMG["gif_strat"]),
    ("UX/UI design",
     "Launch your digital product with a UX/UI design that connects, engages, and elevates your user experience.",
     ["Information Architecture", "Wire Framing", "User Flows &amp; Journeys",
      "UI Kits &amp; Design Systems", "Prototyping &amp; Usability Testing", "Web Design",
      "Mobile Apps Design", "UX Research"], IMG["gif_ux"]),
]
blocks = []
for name, copy, items, media in SERVICES:
    lis = "".join(f"<li>{i}</li>" for i in items)
    blocks.append(f"""  <div class="service">
    <div class="service__head"><h2 class="title">{name}</h2></div>
    <div>
      <p class="lede" style="max-width:44ch">{copy}</p>
      <ul class="service__list" style="margin-top:28px">{lis}</ul>
    </div>
    <div class="service__media"><img src="{media}" alt="" loading="lazy"></div>
  </div>""")

services_body = f"""<section class="pagehead wrap">
  <div class="pagehead__row">
    <h1 class="display">All the creative solutions you need</h1>
    <ul class="meta" style="min-width:260px">
      <li>Insightful strategy</li><li>Impactful creative</li><li>Smart production</li>
    </ul>
  </div>
  <p class="prose" style="margin-top:clamp(32px,4vw,56px)">We take care of your project from the very
  first interaction, with a multidisciplinary team dedicated to offering the best solutions to achieve
  the results you're looking for.</p>
</section>

<section class="wrap section--tight" style="padding-top:0">
{chr(10).join(blocks)}
</section>"""

# ------------------------------------------------------------------ WORKS
rows, tiles = [], []
for i, (name, slug) in enumerate(WORKS):
    thumb = PROJECTS.get(slug, {}).get("thumb") or POOL[i % len(POOL)]
    rows.append(f"""      <li><a class="index__row" href="{WORK_BASE}{slug}.html" data-img="{thumb}">
        <span class="index__name">{name}</span><span class="index__cue">View project</span></a></li>""")
    tiles.append(f"""      <li><a class="tile" href="{WORK_BASE}{slug}.html">
        <div class="tile__figure"><img src="{thumb}" alt="" loading="lazy"></div>
        <p class="tile__name">{name}</p></a></li>""")

works_body = f"""<section class="pagehead wrap">
  <div class="pagehead__row">
    <h1 class="display">Super works</h1>
    <div class="views" role="group" aria-label="View">
      <button type="button" class="views__btn" data-view="grid" aria-pressed="true">Grid</button>
      <button type="button" class="views__btn" data-view="index" aria-pressed="false">Index</button>
    </div>
  </div>
</section>

<section class="wrap section--tight" style="padding-top:0">
  <div id="works" data-current="grid">
    <ul class="tiles">
{chr(10).join(tiles)}
    </ul>
    <ul class="index" data-index>
{chr(10).join(rows)}
    </ul>
  </div>
</section>"""

# ------------------------------------------------------------------ ABOUT
mosaic = "".join(f'<li><img src="{IMG[k]}" alt="" loading="lazy"></li>'
                 for k in ["ab1", "ab2", "ab3", "ab4", "of1", "of2", "of3", "ab5"])
team = "".join(f"""<li><img src="{ph}" alt="{n}" loading="lazy">
  <p class="team__name">{n}</p><p class="meta">{r}</p></li>""" for n, r, ph in TEAM)
CATS = ["Creativity", "Advertising", "Identity", "Logos", "Strategy", "Media", "Content",
        "Filming", "Production and post-production", "Motion graphics", "UX", "UI / Apps + Webs",
        "Atomic design", "Social media", "Packaging", "POP", "Innovation", "Data analytics"]
ROLES = ["Graphic designers", "Art designers", "Art directors", "Producers", "Post-production",
         "Animators", "AI specialists", "Creative teams", "Account executives", "Account directors",
         "Community management", "Live production teams", "Audio production teams"]
cats = "".join(f"<li>{c}</li>" for c in CATS)
roles = "".join(f"<li>{r}</li>" for r in ROLES)
marq = "".join("<span>effective</span>" for _ in range(12))
marq2 = "".join("<span>no excuses</span>" for _ in range(12))

about_body = f"""<section class="pagehead wrap">
  <div class="pagehead__row">
    <h1 class="display">Everything is possible.</h1>
    <p class="lede" style="max-width:38ch">An independent agency, a design studio, and a production
    company. We are diverse, collaborative, providing flexibility in customizing each project to suit
    your business needs.</p>
  </div>
</section>

<section class="wrap section--tight" style="padding-top:0">
  <ul class="mosaic">{mosaic}</ul>
</section>

<section class="wrap section--tight">
  <div class="stats">
    <div><p class="stat__n">03</p><p class="stat__k meta">Countries</p></div>
    <div><p class="stat__n">+15</p><p class="stat__k meta">Years</p></div>
    <div><p class="stat__n">+10.000</p><p class="stat__k meta">Projects around the world</p></div>
  </div>
</section>

<section class="wrap section rule">
  <div class="statement">
    <h2 class="title">We think and design at the pace of cultural changes.</h2>
    <div class="prose">
      <p>We are a creative agency fueled by high-quality design and bold ideas. We help brands grow by
      transforming challenges into powerful visual solutions.</p>
      <p>Agile and adaptive, we work closely with each client to craft innovative experiences across
      all media. With speed, flexibility, and a collaborative spirit, we deliver results that move
      businesses forward.</p>
    </div>
  </div>
</section>

<section class="wrap section--tight">
  <div class="service__media" style="aspect-ratio:21/9;margin-bottom:clamp(28px,4vw,48px)">
    <img src="{IMG['ai']}" alt="" loading="lazy"></div>
  <div class="statement">
    <h2 class="title">Supermarket is where AI meets creativity</h2>
    <p class="lede">Smart tools, sharp minds — design, evolved. Where ideas pop and AI powers up.
    This is creativity unleashed.</p>
  </div>
</section>

<section class="wrap section rule">
  <div class="pagehead__row" style="margin-bottom:32px">
    <h2 class="title">Projects across all categories</h2>
    <p class="meta">Super ideas. Super results.</p>
  </div>
  <ul class="tags">{cats}</ul>
</section>

<div class="marquee"><div class="marquee__track">{marq}{marq}</div></div>
<div class="marquee marquee--alt"><div class="marquee__track">{marq2}{marq2}</div></div>

<section class="wrap section">
  <h2 class="subtitle" style="margin-bottom:28px">Main team</h2>
  <ul class="team">{team}</ul>
</section>

<section class="wrap section--tight rule">
  <h2 class="title" style="margin-bottom:24px">+30 multidisciplinary team</h2>
  <ul class="tags">{roles}</ul>
</section>"""

# ------------------------------------------------------------------ REEL
reel_body = f"""<section class="pagehead wrap">
  <div class="pagehead__row">
    <h1 class="display">Our reels</h1>
    <p class="lede">Dive into our world of creativity where 3D motion meets the magic of live-action.
    Each reel is a journey, blending cutting-edge technology with captivating storytelling.
    Click play and let our visuals speak for themselves.</p>
  </div>
</section>

<section class="wrap section--tight" style="padding-top:0">
  <div class="reels">
    <div><div class="reel__frame">
      <iframe src="https://www.youtube.com/embed/g1P3enetJEw?rel=0" title="Supermarket reel 01"
        allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
        allowfullscreen loading="lazy"></iframe></div>
      <p class="meta" style="margin-top:12px">Reel 01</p></div>
    <div><div class="reel__frame">
      <iframe src="https://www.youtube.com/embed/ErSDs_nNWj4?rel=0" title="Supermarket reel 02"
        allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
        allowfullscreen loading="lazy"></iframe></div>
      <p class="meta" style="margin-top:12px">Reel 02</p></div>
  </div>
</section>"""

# ------------------------------------------------------------------ CONTACT
contact_body = f"""<section class="pagehead wrap">
  <h1 class="display">Super results start here</h1>
</section>

<section class="wrap section--tight" style="padding-top:0">
  <div class="statement" style="align-items:start">
    <div>
      <p class="lede" style="margin-bottom:32px">Feel free to write us a message. We reply within one
      working day.</p>
      <form class="form" id="contact-form" action="#" method="post" novalidate>
        <div class="field">
          <label for="name">What's your name?</label>
          <input id="name" name="name" type="text" autocomplete="name" required>
        </div>
        <div class="field">
          <label for="email">What's your email address?</label>
          <input id="email" name="email" type="email" autocomplete="email" required>
        </div>
        <div class="field">
          <label for="message">Your message</label>
          <textarea id="message" name="message" rows="4" required></textarea>
        </div>
        <div>
          <button class="btn" type="submit">Send message</button>
        </div>
        <p class="form__msg form__msg--ok" role="status" tabindex="-1">Thank you. Your message has been sent.</p>
        <p class="form__msg form__msg--err" role="alert" tabindex="-1">Something went wrong. Check your name, a valid email and your message, then send again.</p>
      </form>
    </div>
    <div class="service__media" style="aspect-ratio:4/5"><img src="{IMG['contact']}" alt="" loading="lazy"></div>
  </div>
</section>"""

PAGES = [
    ("index.html", "Home", "index.html", home_body, "We are Supermarket. A global force of creativity."),
    ("services.html", "Services", "services.html", services_body, "All the creative solutions you need."),
    ("works.html", "Works", "works.html", works_body, "Selected work by Supermarket."),
    ("about.html", "About", "about.html", about_body, "Learn more about us."),
    ("reel.html", "Reels", "reel.html", reel_body, "Our reels."),
    ("contact.html", "Contact", "contact.html", contact_body, "Super results start here."),
]

for filename, title, current, body, desc in PAGES:
    (OUT / filename).write_text(page(title, current, body, desc), encoding="utf-8")
    print("wrote", filename)

# =====================================================================
#  PROJECT PAGES  (work/<slug>.html)
#
#  ONE template, driven by data. Loading a project = filling a dict.
#
#  Module vocabulary for "media" — each entry is (type, payload):
#    ("bleed",  url)              pieza a sangre, borde a borde
#    ("full",   url)              pieza a ancho de grilla
#    ("pair",   [url, url])       dos piezas en fila
#    ("trio",   [url, url, url])  tres piezas en fila
#    ("video",  url)              mp4 propio, autoplay muteado en loop
#    ("embed",  youtube_id)       reproductor de YouTube
#    ("quote",  texto)            una frase grande: la idea del caso
#  Cualquier módulo de imagen acepta pie: ("full", (url, "pie de foto"))
# =====================================================================

BRANDS = ["Swift", "Ficohsa", "Revlon", "Arcor", "Tigo", "Barça", "Oky", "OKY",
          "Coca Cola", "Cutex", "UCEMA", "McCain", "Quilmes", "Levite", "Stanley",
          "Sodastream", "Miller", "Natural One", "Facebank", "PEISA", "Nubceo"]


def client_for(name):
    for b in BRANDS:
        if name.lower().startswith(b.lower()):
            return b
    return name


def _split(item):
    """Accepts a url or a (url, caption) tuple."""
    if isinstance(item, tuple):
        return item[0], item[1]
    return item, ""


def _fig(item, cls="shot"):
    url, cap = _split(item)
    figcap = f'<figcaption class="shot__cap">{cap}</figcaption>' if cap else ""
    return (f'<figure class="{cls}"><img src="{url}" alt="" loading="lazy">'
            f'{figcap}</figure>')


def module_html(kind, payload):
    if kind == "bleed":
        return f'  {_fig(payload, "shot shot--bleed")}'
    if kind == "full":
        return f'  <div class="wrap">{_fig(payload)}</div>'
    if kind in ("pair", "trio"):
        cells = "".join(_fig(i) for i in payload)
        return f'  <div class="wrap"><div class="shots shots--{kind}">{cells}</div></div>'
    if kind == "video":
        return (f'  <div class="wrap"><video class="shot shot--video" src="{payload}" '
                f'autoplay muted loop playsinline preload="metadata"></video></div>')
    if kind == "embed":
        return (f'  <div class="wrap"><div class="reel__frame">'
                f'<iframe src="https://www.youtube.com/embed/{payload}?rel=0" title="Project video" '
                f'allow="encrypted-media; picture-in-picture" allowfullscreen loading="lazy">'
                f'</iframe></div></div>')
    if kind == "quote":
        return f'  <div class="wrap"><p class="work__quote">{payload}</p></div>'
    return ""


def project_page(i):
    name, slug = WORKS[i]
    d = PROJECTS.get(slug, {})
    prev_name, prev_slug = WORKS[i - 1]
    next_name, next_slug = WORKS[(i + 1) % len(WORKS)]

    fields = [("Client", d.get("client") or client_for(name)),
              ("Year", d.get("year", "")),
              ("Segment", d.get("segment", "")),
              ("Services", d.get("services", ""))]
    rail = "".join(f'<div class="rail__row"><dt>{k}</dt><dd>{v}</dd></div>'
                   for k, v in fields if v)

    intro = (f'<div class="work__intro"><p>{d["intro"]}</p></div>'
             if d.get("intro") else
             '<!-- Description (CMS rich text) binds here -->')

    hero = d.get("hero") or POOL[i % len(POOL)]

    if d.get("media"):
        media = "\n".join(module_html(k, v) for k, v in d["media"])
    else:
        media = ("  <!-- Gallery (CMS) binds here. Módulos disponibles:\n"
                 "       bleed · full · pair · trio · video · embed · quote -->\n"
                 + "\n".join(module_html(k, v) for k, v in [
                     ("full", POOL[(i + 1) % len(POOL)]),
                     ("pair", [POOL[(i + 2) % len(POOL)], POOL[(i + 3) % len(POOL)]]),
                     ("bleed", POOL[(i + 4) % len(POOL)])]))

    credits = ""
    if d.get("credits"):
        rows = "".join(f'<div class="rail__row"><dt>{k}</dt><dd>{v}</dd></div>'
                       for k, v in d["credits"])
        credits = f'''
  <section class="wrap work__credits">
    <h2 class="meta">Credits</h2>
    <dl class="rail">{rows}</dl>
  </section>'''

    body = f"""<article class="work">
  <header class="wrap work__head">
    <a class="work__back" href="../works.html">All works</a>
    <h1 class="display work__title">{name}</h1>
    <dl class="rail">{rail}</dl>
  </header>

  <figure class="work__hero"><img src="{hero}" alt="" fetchpriority="high"></figure>

  <div class="wrap work__body">
    {intro}
  </div>

  <div class="work__media">
{media}
  </div>
{credits}
  <nav class="wrap pager" aria-label="Projects">
    <a class="pager__side" href="{prev_slug}.html">
      <span class="meta">Previous</span><span class="pager__name">{prev_name}</span></a>
    <a class="pager__side pager__side--next" href="{next_slug}.html">
      <span class="meta">Next project</span><span class="pager__name">{next_name}</span></a>
  </nav>
</article>"""

    return page(name, "works.html", body,
                d.get("intro", "")[:150] or f"{name} — a Supermarket project.", pre="../")


workdir = OUT / "work"
workdir.mkdir(exist_ok=True)
for i in range(len(WORKS)):
    (workdir / (WORKS[i][1] + ".html")).write_text(project_page(i), encoding="utf-8")
print("wrote", len(WORKS), "project pages")
