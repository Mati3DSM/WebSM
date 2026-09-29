#!/usr/bin/env python3
"""Builds the six static pages of the Supermarket site."""
import re
import html
import pathlib

OUT = pathlib.Path(__file__).parent
CDN = "assets/"
REEL_MP4 = ("assets/videos/Web-Reel-Sin-Logo-Al-Final-transcode.mp4")

# CAMBIAR antes de publicar: dominio final, sin barra al final.
# Se usa para <link rel="canonical">, Open Graph, robots.txt y sitemap.xml.
DOMAIN = "https://www.wearesupermarket.com"
DEFAULT_OG_IMAGE = CDN + "images/logo.png"  # imagen de respaldo para compartir en redes

IMG = {
    "board":    CDN + "images/logo.png",
    "abstract": CDN + "images/abstract.png",
    "gif_hero": CDN + "images/offer.gif",
    "gif_brand": CDN + "images/label.gif",
    "gif_film": CDN + "images/film.gif",
    "gif_strat": CDN + "images/like.gif",
    "gif_ux":   CDN + "images/mobile.gif",
    "ab1": CDN + "images/hamza-shaikh-uXtvnZl_FWM-unsplash.webp",
    "ab2": CDN + "images/louise-viallesoubranne-5EhN4wbfvBc-unsplash.webp",
    "ab3": CDN + "images/kobu-agency-MBtcLadqc6c-unsplash.webp",
    "ab4": CDN + "images/philipp-mandler-CiNHG2xuVlQ-unsplash.webp",
    "ab5": CDN + "images/annie-spratt-hCb3lIB8L8E-unsplash.webp",
    "of2": CDN + "images/oficina02.jpg",
    "of3": CDN + "images/oficina03.jpg",
    "of1": CDN + "images/oficina01_V2.png",
    "ai":  CDN + "images/SM-About-Us_V2.jpg",
    "contact": CDN + "images/phone_006.webp",
}
TEAM = [
    ("Martín Marinovic", "Founder", CDN + "images/martin.jpeg"),
    ("Andrés Schmisser", "Founder", CDN + "images/andres.jpeg"),
    ("Ignacio Acosta", "Global Business Development", CDN + "images/Nacho_2.jpg"),
    ("Catalina Mulhall", "Creative Director", CDN + "images/catalina.jpeg"),
    ("George Marinovic", "Finance &amp; HR GM", CDN + "images/george.jpeg"),
    ("Hernán Marinovic", "Accounts GM", CDN + "images/hernan.jpeg"),
]

WORKS = [
    ("Swift Picante", "swift-picante"), ("Swift Verano", "swift-verano"),
    ("Ficohsa ¡Gana un carro por mes!", "ficohsa-gana-un-carro-por-mes"),
    ("Barça Games Social Media", "barca-games-social-media"),
    ("Ficohsa Mastercard AA", "ficohsa-tarjeta-mastercard"),
    ("OKY Digital", "oky-digital"), ("Swift Veggies", "swift-veggies"),
    ("Swift Categorías", "swift-categorias"), ("Tienda La Virginia", "tienda-la-virginia"),
    ("Método UCEMA", "metodo-ucema"), ("P!CKERS by McCain", "pickers-by-mccain"),
    ("Aero Assist Handling", "aero-assist-handling"),
    ("Brand Character — Rob", "brand-character-rob"),
    ("Revlon Love is On", "revlon-love-is-on"), ("Revlon Naté", "revlon-nate"),
    ("Barça Games", "barca-games"), ("Revlon Colorburst", "revlon-butter"),
    ("Revlon", "revlon"), ("Coca Cola", "coca-cola"), ("Izzi", "izzi"),
    ("Tigo Rebranding", "tigo-rebranding"), ("Sodastream", "sodastream"),
    ("Nubceo", "nubceo"), ("Tigo Money", "tigo-money"), ("Prester", "prester"),
    ("Facebank", "facebank"), ("UCEMA", "ucema"), ("PEISA", "peisa"),
    ("Vireyes", "vireyes"), ("Lati", "lati"), ("Chocolates Arcor", "chocolates-arcor"),
    ("Serenito", "serenito"), ("Oky", "oky"), ("Felaban", "felaban"),
    ("Stanley", "stanley"), ("Eron", "eron"), ("Glenhaven", "glenhaven"),
    ("Delicia", "delicia"), ("GoGym", "gogym"), ("Arcor Frutas", "arcor-frutas"),
    ("Tigoooool", "tigoooool"), ("Clave", "clave"), ("Miller", "miller"),
    ("Rob Ortiz", "rob-ortiz"), ("Deconté", "deconte"),
    ("Club de la Cerveza", "club-de-la-cerveza"), ("Swift Grasa", "swift-grasa"),
    ("Natural One", "natural-one"), ("Levite Limonada", "levite-limonada"),
    ("Hogareñas", "hogarenas"), ("Mr Pops", "mr-pops"),
    ("Natural Break — Arcor", "natural-break-arcor"), ("Prestix", "prestix"),
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


def header(current, pre=""):
    links = "".join(
        '<a href="{}{}"{}>{}</a>'.format(
            pre, href, ' aria-current="page"' if href == current else "", label)
        for label, href in NAV)
    return f"""<a class="skip" href="#main">Skip to content</a>
<header class="header">
  <div class="header__inner">
    <a class="brand" href="{pre}index.html" aria-label="Supermarket, home">
      <img class="brand__mark" src="assets/images/logo.svg" alt="Supermarket">
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


def page(title, current, body, description="", pre="", path="", image=None):
    full_title = f"{title} — Supermarket"
    desc_text = description or "Supermarket is a global creative agency."
    desc = f'\n  <meta name="description" content="{html.escape(desc_text)}">'
    canonical = f"{DOMAIN}/{path}"
    og_image = f"{DOMAIN}/{image or DEFAULT_OG_IMAGE}"
    social = f"""
  <link rel="canonical" href="{canonical}">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Supermarket">
  <meta property="og:title" content="{html.escape(full_title)}">
  <meta property="og:description" content="{html.escape(desc_text)}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="{og_image}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{html.escape(full_title)}">
  <meta name="twitter:description" content="{html.escape(desc_text)}">
  <meta name="twitter:image" content="{og_image}">"""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{full_title}</title>{desc}{social}
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



PROJECTS = {
    "swift-picante": {
                "client": "Swift",
                "year": "",
                "segment": "",
                "services": "Advertising, Creativity, Design, POP",
                "intro": (
                    "We created a campaign to introduce the new spicy versions of SWIFT spreads, bringing a fresh, fun, and eye-catching spin to the original product. The focus was on communicating innovation through a playful tone, inviting consumers to discover the spice in a relaxed and engaging way. With a vibrant and dynamic aesthetic, we aimed for the campaign to feel modern, attractive, and easily recognizable across any format."),
                "thumb": CDN + "images/Works/Swift/swift-picantes-portada.png",
                "hero": CDN + "images/Works/Swift/swift-picantes-portada.png",
                "media": [
                    ("quote", "Crafting a vibrant, playful campaign with a modern, spicy twist."),
                    ("pair",  [(CDN + "images/Works/Swift/swift-picantes-Artboard1.png"),
                              CDN + "images/Works/Swift/swift-picantes-Artboard2.png"]),
                    ("bleed",  CDN + "images/Works/Swift/swift-GIFUntables.gif"),
                    ("sheet",  CDN + "images/Works/Swift/swift-picantes-Artboard3.png"),
                    ("sheet",  CDN + "images/Works/Swift/swift-picantes-Artboard4.png"),
                    ("sheet",  CDN + "images/Works/Swift/swift-picantes-words.gif"),
                    ("full",  CDN + "images/Works/Swift/swift-picantes-billboard.png"),
                    ("bleed", (CDN + "images/Works/Swift/swift-GIFSabrosos.gif")),
                    ("pair",  [(CDN + "images/Works/Swift/swift-picantes-Artboard8.png"),
                               CDN + "images/Works/Swift/swift-picantes-Artboard9.png"]),
                    ("full",  CDN + "images/Works/Swift/swift-picantes-Artboard10.png"),
                ],
                "credits": [("Creative direction", "Supermarket"),
                            ("Art direction &amp; design", "Supermarket"),
                            ("Content production", "Supermarket")],
            },

    "swift-verano": {
        "client": "Swift",
        "year": "",
        "segment": "",
        "services": "Advertising, Art direction, Design, POP",
        "intro": (
            "We created a summer campaign for Swift that combined the World Cup spirit with pop activations across beaches, points of sale, and dining venues. Through a fresh, summer-inspired visual system, the brand established a strong presence in seaside resorts and key venues, connecting everyday consumption with moments of enjoyment and celebration."),
        "thumb": CDN + "images/Works/Swift/SWIFT_VeranoMundial_2526_CasoSM-hero.jpg",
        "hero": CDN + "images/Works/Swift/SWIFT_VeranoMundial_2526_CasoSM-hero.jpg",
        "media": [
            ("full",  CDN + "images/Works/Swift/SWIFT_VeranoMundial_2526_CasoSM-01.jpg"),
            ("quote", "Vibrant summer campaign and multi-touchpoint activations that merged matchday excitement with seasonal fun."),
            ("full",  CDN + "images/Works/Swift/SWIFT_VeranoMundial_2526_CasoSM-02.jpg"),
            ("full",   CDN + "images/Works/Swift/SWIFT_VeranoMundial_2526_CasoSM-03.jpg"),
            ("full", (CDN + "images/Works/Swift/SWIFT_VeranoMundial_2526_CasoSM-04.jpg")),
            ("full",  CDN + "images/Works/Swift/SWIFT_VeranoMundial_2526_CasoSM-05.jpg"),
            ("full",  CDN + "images/Works/Swift/SWIFT_VeranoMundial_2526_CasoSM-06.jpg"),
            ("full",  CDN + "images/Works/Swift/SWIFT_VeranoMundial_2526_CasoSM-07.jpg"),
            ("full", CDN + "images/Works/Swift/SWIFT_VeranoMundial_2526_CasoSM-08.jpg"),
            ("full", CDN + "images/Works/Swift/SWIFT_VeranoMundial_2526_CasoSM-09.jpg"),
        ],
        "credits": [("Creative direction", "Supermarket"),
                    ("Art direction &amp; design", "Supermarket"),
                    ("Content production", "Supermarket")],
    },

 "ficohsa-gana-un-carro-por-mes": {
        "client": "Ficohsa",
        "year": "",
        "segment": "",
        "services": "Identity, Strategy, Art direction",
        "intro": (
            "We developed the visual identity and branding system for a promotional campaign by Ficohsa, centered around a car giveaway. The campaign featured the raffle of six cars, one per month, and was open to all customers who deposited a qualifying amount of money with the bank. The identity was designed to be dynamic, trustworthy, and engaging, supporting the campaign across multiple touchpoints and reinforcing the bank’s brand presence throughout the promotion."),
        "thumb": CDN + "images/Works/Ficohsa/ficohsa-carro-hero.jpg",
        "hero": CDN + "images/Works/Ficohsa/ficohsa-carro-hero.jpg",
        "media": [
            ("quote", "Promotional campaign identity to drive customer engagement across every touchpoint."),
            ("pair",  [(CDN + "images/Works/Ficohsa/ficohsa-carro-Artboard1.jpg"),
                      CDN + "images/Works/Ficohsa/ficohsa-carro-Artboard3.jpg"]),
            ("full",  CDN + "images/Works/Ficohsa/ficohsa-carro-Artboard2.jpg"),
            ("full",  CDN + "images/Works/Ficohsa/ficohsa-carro-Artboard4.jpg"),
            ("full",   CDN + "images/Works/Ficohsa/ficohsa-carro-Artboard5.jpg"),
            ("full", CDN + "images/Works/Ficohsa/ficohsa-carro-autoFINAL.gif"),
            ("full", (CDN + "images/Works/Ficohsa/ficohsa-carro-Artboard6.jpg")),
            ("full",  CDN + "images/Works/Ficohsa/ficohsa-carro-Artboard8.jpg"),
            ("full",  CDN + "images/Works/Ficohsa/ficohsa-carro-Artboard9.jpg"),
            ("full",  CDN + "images/Works/Ficohsa/ficohsa-carro-Artboard10.jpg"),
        ],
        "credits": [("Creative direction", "Supermarket"),
                    ("Art direction &amp; design", "Supermarket"),
                    ("Content production", "Supermarket")],
    },

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
            "thumb": CDN + "images/Works/Barca-Games/barca-games-social-hero.jpg",
            "hero": CDN + "images/Works/Barca-Games/barca-games-social-hero.jpg",
            "media": [
                ("full",  CDN + "images/Works/Barca-Games/CasoBG-Redes-artboard1.jpg"),
                ("quote", "One app, three seasons, three graphic identities."),
                ("pair",  [(CDN + "images/Works/Barca-Games/PORTADA-CHRISTMAS.gif"),
                           CDN + "images/Works/Barca-Games/CasoBG-Redes-05.jpg"]),
                ("full",  CDN + "images/Works/Barca-Games/CasoBG-Redes-04.jpg"),
                ("full",   CDN + "images/Works/Barca-Games/CasoBG-Redes-Artboard3.jpg"),
                ("bleed", (CDN + "images/Works/Barca-Games/PORTADA-KINGS.gif")),
                ("sheet",  CDN + "images/Works/Barca-Games/CasoBG-Redes-06.jpg"),
                ("sheet",  CDN + "images/Works/Barca-Games/POSTEOS.gif"),
                ("sheet",  CDN + "images/Works/Barca-Games/CasoBG-Redes-08.jpg"),
                ("full", (CDN + "images/Works/Barca-Games/PORTADA-CARNAVAL.gif")),
                ("pair",  [CDN + "images/Works/Barca-Games/CasoBG-Redes-11.jpg",
                           CDN + "images/Works/Barca-Games/SALTO.gif"]),
            ],
            "credits": [("Creative direction", "Supermarket"),
                        ("Art direction &amp; design", "Supermarket"),
                        ("Content production", "Supermarket")],
        },

         "ficohsa-tarjeta-mastercard": {
                    "client": "Ficohsa",
                    "year": "",
                    "segment": "",
                    "services": "Social media strategy, art direction, design, content production",
                    "intro": (
                        "We developed the creative concept and full rollout for the launch campaign of the new Ficohsa Mastercard American Airlines AAdvantage® card. A concept inspired by the universal dream of travel, connecting everyday purchases with the excitement of planning the next journey. Built around the central idea 'Your new boarding pass', we created a visual and narrative system that links card usage with access to exclusive travel benefits: miles accumulation, upgrades, lounge access, and more. The campaign came to life through multiple touchpoints: point-of-sale materials, key urban placements, digital assets, and in-branch signage. An integrated experience designed to remind users that every purchase brings them one step closer to their next destination. "),
                    "thumb": CDN + "images/Works/Ficohsa/FICOHSA-card-hero.jpg",
                    "hero": CDN + "images/Works/Ficohsa/FICOHSA-card-hero.jpg",
                    "media": [
                        ("quote", "Ficohsa Mastercard AAdvantage® Launch / 360° Campaign for Frequent Travelers"),
                        ("full",  CDN + "images/Works/Ficohsa/FICOHSA-card-CasoSM-01.jpg"),
                        ("full",  CDN + "images/Works/Ficohsa/FICOHSA-card-CasoSM-02.jpg"),
                        ("full",   CDN + "images/Works/Ficohsa/FICOHSA-card-CasoSM-03.jpg"),
                        ("full", (CDN + "images/Works/Ficohsa/FICOHSA-card-CasoSM-04.jpg")),
                        ("full",  CDN + "images/Works/Ficohsa/FICOHSA-card-CasoSM-05.jpg"),
                        ("full",  CDN + "images/Works/Ficohsa/FICOHSA-card-CasoSM-06.jpg"),
                        ("full",  CDN + "images/Works/Ficohsa/FICOHSA-card-CasoSM-07.jpg"),
                        ("full", (CDN + "images/Works/Ficohsa/FICOHSA-card-CasoSM-08.jpg")),
                       
                    ],
                    "credits": [("Creative direction", "Supermarket"),
                                ("Art direction &amp; design", "Supermarket"),
                                ("Content production", "Supermarket")],
                },

                 "oky-digital": {
                                    "client": "OKY",
                                    "year": "",
                                    "segment": "",
                                    "services": "Identity, Strategy, Design, UX/UI",
                                    "intro": (
                                        "Design and development of the digital experience for Oky, a platform offering personalized financial services for migrant communities, and its B2B counterpart, Oky Business. The challenge was to create a cohesive visual identity for both audiences, integrating clarity, trust, and scalability across the experience. We worked on information architecture, navigation, and brand tone to reflect Oky’s values of inclusion and accessible technology. The user-facing site focuses on a clean, modern, and friendly interface, while Oky Business strengthens institutional messaging and highlights benefits for corporate partners. "),
                                    "thumb": CDN + "images/Works/Oky/oky-digital-hero.jpg",
                                    "hero": CDN + "images/Works/Oky/oky-digital-hero.jpg",
                                    "media": [
                                        ("quote", "Designing a seamless, high-trust digital experience for Oky"),
                                        ("video",  CDN + "videos/OKY/oky-digital-01.mp4"),
                                        ("full",  CDN + "images/Works/Oky/oky-digital-02.jpg"),
                                        ("full",   CDN + "images/Works/Oky/oky-digital-03.gif"),
                                        ("full", (CDN + "images/Works/Oky/oky-digital-04.jpg")),
                                        ("full",  CDN + "images/Works/Oky/oky-digital-05.gif"),
                                        ("bleed",  CDN + "images/Works/Oky/oky-digital-06.jpg"),
                                        ("full",  CDN + "images/Works/Oky/oky-digital-07.jpg"),
                                        ("full", (CDN + "images/Works/Oky/oky-digital-08.gif")),
                                        ("full",  CDN + "images/Works/Oky/oky-digital-09.gif"),
                                        ("full",  CDN + "images/Works/Oky/oky-digital-10.jpg"),
                                        ("full", (CDN + "images/Works/Oky/oky-digital-11.jpg")),
                                    ],
                                    "credits": [("Creative direction", "Supermarket"),
                                                ("Art direction &amp; design", "Supermarket"),
                                                ("Content production", "Supermarket")],
                                },

                  "swift-veggies": {
                                    "client": "Swift",
                                    "year": "",
                                    "segment": "Branding",
                                    "services": "Branding, Communication, POP",
                                    "intro": (
                                        "We supported the launch of Swift Veggies, Swift’s new line of frozen plant-based products — including veggie nuggets and patties — by developing its visual identity from the ground up. We created the graphic universe, branding, and full communication strategy to position this new category within the Swift portfolio. We also designed and produced materials for retail spaces and sales commercials, ensuring a strong, consistent, and appealing presence across all consumer touchpoints."),
                                    "thumb": CDN + "images/Works/Swift/SWIFT-Veggie-hero.jpg",
                                    "hero": CDN + "images/Works/Swift/SWIFT-Veggie-hero.jpg",
                                    "media": [
                                        ("quote", "Building the brand universe and communication strategy to launch Swift Veggies."),
                                        ("full",  CDN + "images/Works/Swift/SWIFT-Veggie-CasoSM-01.jpg"),
                                        ("full",  CDN + "images/Works/Swift/SWIFT-Veggie-logo.gif"),
                                        ("sheet",   CDN + "images/Works/Swift/SWIFT-Veggie-CasoSM-02.jpg"),
                                        ("sheet", (CDN + "images/Works/Swift/SWIFT-Veggie-CasoSM-03.jpg")),
                                        ("full",  CDN + "images/Works/Swift/SWIFT-Veggie-BusinessCard.gif"),
                                        ("full",  CDN + "images/Works/Swift/SWIFT-Veggie-CasoSM-04.jpg"),
                                        ("full",  CDN + "images/Works/Swift/SWIFT-Veggie-CasoSM-05.jpg"),
                                        ("sheet",  CDN + "images/Works/Swift/SWIFT-Veggie-CasoSM-06.jpg"),
                                        ("sheet", (CDN + "images/Works/Swift/SWIFT-Veggie-logo.gif")),
                                  
                                    ],
                                    "credits": [("Creative direction", "Supermarket"),
                                                ("Art direction &amp; design", "Supermarket"),
                                                ("Content production", "Supermarket")],
                                },

                  "swift-categorias": {
                                    "client": "Swift",
                                    "year": "2024",
                                    "segment": "Branding",
                                    "services": "Branding, Communication, Creativity",
                                    "intro": (
                                        "We designed the visual identity and communication strategy for SWIFT’s new product categorization as part of its brand relaunch. The objective: reorganize the portfolio and boost the visibility of each product family across points of sale and communication channels. From naming to photography production, we developed a simple, cohesive, and memorable visual system tailored to simplify consumer decision-making and reinforce brand positioning. A comprehensive proposal combining strategy, design, and creativity to power this new chapter for SWIFT."),
                                    "thumb": CDN + "images/Works/Swift/swift-categorias-hero.jpg",
                                    "hero": CDN + "images/Works/Swift/swift-categorias-hero.jpg",
                                    "media": [
                                        ("quote", "Product portfolio relaunch from naming to shelf."),
                                        ("full",  CDN + "images/Works/Swift/swift-categorias-CasoSM-01.jpg"),
                                        ("full",  CDN + "images/Works/Swift/swift-categorias-grupo-foto2.gif"),
                                        ("full",   CDN + "images/Works/Swift/swift-categorias-CasoSM-02.jpg"),
                                        ("full",  CDN + "images/Works/Swift/swift-categorias-CasoSM_Portada.gif"),
                                        ("full", (CDN + "images/Works/Swift/swift-categorias-CasoSM-03.jpg")),
                                        ("full",  CDN + "images/Works/Swift/swift-categorias-grupo-foto1.gif"),
                                        ("full",  CDN + "images/Works/Swift/swift-categorias-CasoSM-04.jpg"),
                                        ("full",  CDN + "images/Works/Swift/swift-categorias-CasoSM-05.jpg"),
                                        ("full",  CDN + "images/Works/Swift/swift-categorias-CasoSM-06.jpg"),
                                        ("full",  CDN + "images/Works/Swift/swift-categorias-CasoSM-07.jpg"),
                                        ("full", (CDN + "images/Works/Swift/swift-categorias-CasoSM-09.jpg")),
                                        ("full",  CDN + "images/Works/Swift/swift-categorias-CasoSM-10.jpg"),
                                  
                                    ],
                                    "credits": [("Creative direction", "Supermarket"),
                                                ("Art direction &amp; design", "Supermarket"),
                                                ("Content production", "Supermarket")],
                                },    
                                
                  "tienda-la-virginia": {
                                    "client": "La Virginia",
                                    "year": "",
                                    "segment": "",
                                    "services": "Strategy, Identity, UX/UI",
                                    "intro": (
                                        "A full redesign of La Virginia’s e-commerce site, focused on improving navigation, visual clarity, and the overall shopping experience. The project involved restructuring the site’s information architecture and developing a visual design system aligned with the brand’s warm and traditional identity. With a user-centered approach, we optimized the journey from product exploration to checkout. UX principles were applied to streamline navigation, build user trust, and improve conversion. The result is a functional and visually appealing online store, ready to scale and strengthen the brand’s digital presence while enhancing user engagement."),
                                    "thumb": CDN + "images/Works/La_Virginia/LV-tienda-hero.gif",
                                    "hero": CDN + "images/Works/La_Virginia/LV-tienda-hero.gif",
                                    "media": [
                                        ("quote", "User-centered UX and a refined design system."),
                                        ("full",  CDN + "images/Works/La_Virginia/LV-tienda-gif1.gif"),
                                        ("full",  CDN + "images/Works/La_Virginia/LV-tienda-img1.jpg"),
                                        ("sheet",   CDN + "images/Works/La_Virginia/LV-tienda-gif2.gif"),
                                        ("sheet",  CDN + "images/Works/La_Virginia/LV-tienda-gif3.gif"),
                                        ("sheet", (CDN + "images/Works/La_Virginia/LV-tienda-img2.jpg")),
                                  
                                    ],
                                    "credits": [("Creative direction", "Supermarket"),
                                                ("Art direction &amp; design", "Supermarket"),
                                                ("Content production", "Supermarket")],
                                },         
                                
                  "metodo-ucema": {
                                    "client": "UCEMA",
                                    "year": "2025",
                                    "segment": "",
                                    "services": "Branding, Creativity, Visual Communication",
                                    "intro": (
                                        "We developed the visual identity and communication campaign for a special program at UCEMA University. Designed to support first-year students in mastering applied mathematics—a crucial foundation for their academic path across various degree programs—the project spanned branding, creative development, and communication assets. Our goal was to convey approachability, clarity, and the essential value of a strong academic foundation right from the start."),
                                    "thumb": CDN + "images/Works/UCEMA/UCEMA-Metodo_01.jpg",
                                    "hero": CDN + "images/Works/UCEMA/UCEMA-Metodo_01.jpg",
                                    "media": [
                                        ("quote", "Shaping the visual identity and communication for UCEMA."),
                                        ("full",  CDN + "images/Works/UCEMA/UCEMA-Metodo_02.gif"),
                                        ("full",  CDN + "images/Works/UCEMA/UCEMA-Metodo_03.jpg"),
                                        ("full",   CDN + "images/Works/UCEMA/UCEMA-Metodo_04.jpg"),
                                        ("full",  CDN + "images/Works/UCEMA/UCEMA-Metodo_05.jpg"),
                                        ("full", (CDN + "images/Works/UCEMA/UCEMA-Metodo_06.jpg")),
                                        ("full",  CDN + "images/Works/UCEMA/UCEMA-Metodo_07.gif"),
                                  
                                    ],
                                    "credits": [("Creative direction", "Supermarket"),
                                                ("Art direction &amp; design", "Supermarket"),
                                                ("Content production", "Supermarket")],
                                },                                                                                        

                  "pickers-by-mccain": {
                                    "client": "McCain",
                                    "year": "",
                                    "segment": "",
                                    "services": "Creativity, Content production, Advertising",
                                    "intro": (
                                        "Bold bites deserve bold branding. For McCain’s playful, flavor-packed food segment P!CKERS, we cooked up a full spread of in-store and commercial materials for vendors and gastronomic shops. From sizzling catalogues and crave-worthy brochures to flyers, sell sheets, napkins, tablemats, and tabletents—we made sure every touchpoint served the vibe just right."),
                                    "thumb": CDN + "images/Works/McCain/mccain-pickers-hero.jpg",
                                    "hero": CDN + "images/Works/McCain/mccain-pickers-hero.jpg",
                                    "media": [
                                        ("quote", ""),
                                        ("full",  CDN + "images/Works/McCain/mccain-pickers-01.gif"),
                                        ("full",  CDN + "images/Works/McCain/mccain-pickers-02.jpg"),
                                        ("full",   CDN + "images/Works/McCain/mccain-pickers-03.jpg"),
                                        ("full",  CDN + "images/Works/McCain/mccain-pickers-04.jpg"),
                                        ("full", (CDN + "images/Works/McCain/mccain-pickers-05.gif")),
                                        ("full",  CDN + "images/Works/McCain/mccain-pickers-06.jpg"),
                                        ("pair",  [(CDN + "images/Works/McCain/mccain-pickers-07.gif"),
                                                    CDN + "images/Works/McCain/mccain-pickers-08.gif"]),
                                        ("pair",  [(CDN + "images/Works/McCain/mccain-pickers-09.gif"),
                                                  CDN + "images/Works/McCain/mccain-pickers-10.gif"]),
                                  
                                    ],
                                    "credits": [("Creative direction", "Supermarket"),
                                                ("Art direction &amp; design", "Supermarket"),
                                                ("Content production", "Supermarket")],
                                },     

                  "aero-assist-handling": {
                                    "client": "Aero Assist",
                                    "year": "",
                                    "segment": "",
                                    "services": "Identity, Logos, Art direction, Strategy",
                                    "intro": (
                                        "We took off with Aero Assist Handling to build a bold, modern brand ready to move at airport speed. From logo lift-off to smooth landings across stationery, brand guidelines, ads, and a sleek web presence—we designed every touchpoint to feel sharp, functional, and confidently global. This is airport handling, reimagined with altitude."),
                                    "thumb": CDN + "images/Works/Aeroassist/AA-handling-hero.jpg",
                                    "hero": CDN + "images/Works/Aeroassist/AA-handling-hero.jpg",
                                    "media": [
                                        ("quote", "A sharp global identity built to move at airport speed."),
                                        ("full",  CDN + "images/Works/Aeroassist/AA-handling-01.jpg"),
                                        ("full",  CDN + "images/Works/Aeroassist/AA-handling-02.jpg"),
                                        ("full",   CDN + "images/Works/Aeroassist/AA-handling-03.jpg"),
                                        ("full",  CDN + "images/Works/Aeroassist/AA-handling-04.jpg"),
                                  
                                    ],
                                    "credits": [("Creative direction", "Supermarket"),
                                                ("Art direction &amp; design", "Supermarket"),
                                                ("Content production", "Supermarket")],
                                }, 

                  "brand-character-rob": {
                                    "client": "Barça Games",
                                    "year": "",
                                    "segment": "",
                                    "services": "Branding, Strategy, Motion graphics",
                                    "intro": (
                                        ""),
                                    "thumb": CDN + "images/Works/Barca-Games/bg-rob-hero.webp",
                                    "hero": CDN + "images/Works/Barca-Games/bg-rob-hero.webp",
                                    "media": [
                                        ("quote", ""),
                                        ("full",  CDN + "images/Works/Barca-Games/bg-rob-01.png"),
                                        ("full",  CDN + "images/Works/Barca-Games/bg-rob-02.png"),
                                        ("full",   CDN + "images/Works/Barca-Games/bg-rob-03.png"),
                                        ("full",  CDN + "images/Works/Barca-Games/bg-rob-04.png"),
                                        ("pair",  [(CDN + "images/Works/Barca-Games/bg-rob-08.png"),
                                                   CDN + "images/Works/Barca-Games/bg-rob-09.png"]),
                                        ("pair",  [(CDN + "images/Works/Barca-Games/bg-rob-10.png"),
                                                 CDN + "images/Works/Barca-Games/bg-rob-11.png"]),
                                        ("vimeo_full",  ("https://vimeo.com/1077970839?fl=pl&fe=cm", "9:16")),
                                  
                                    ],
                                    "credits": [("Creative direction", "Supermarket"),
                                                ("Art direction &amp; design", "Supermarket"),
                                                ("Content production", "Supermarket")],
                                }, 

                  "revlon-love-is-on": {
                                    "client": "Revlon",
                                    "year": "",
                                    "segment": "",
                                    "services": "",
                                    "intro": (
                                        ""),
                                    "thumb": CDN + "images/Works/Revlon/revlon-love-hero.jpg",
                                    "hero": CDN + "images/Works/Revlon/revlon-love-hero.jpg",
                                    "media": [
                                        ("quote", ""),
                                        ("full",  CDN + "images/Works/Revlon/revlon-love-01.jpg"),
                                        ("pair",  [(CDN + "images/Works/Revlon/revlon-love-02.jpg"),
                                                  CDN + "images/Works/Revlon/revlon-love-03.jpg"]),
                                        ("full",  CDN + "images/Works/Revlon/revlon-love-04.jpg"),
                                        ("full",   CDN + "images/Works/Revlon/revlon-love-05.jpg"),
                                        ("full",  CDN + "images/Works/Revlon/revlon-love-06.jpg"),
                                        ("pair",  [(CDN + "images/Works/Revlon/revlon-love-07.jpg"),
                                                   CDN + "images/Works/Revlon/revlon-love-08.jpg"]),
                                        ("pair",  [(CDN + "images/Works/Revlon/revlon-love-09.jpg"),
                                                  CDN + "images/Works/Revlon/revlon-love-10.jpg"]),
                                        ("pair",  [(CDN + "images/Works/Revlon/revlon-love-11.jpg"),
                                                  CDN + "images/Works/Revlon/revlon-love-12.jpg"]),
                                        ("full", (CDN + "images/Works/Revlon/revlon-love-13.jpg")),
                                        ("full",  CDN + "images/Works/Revlon/revlon-love-14.jpg"),
                                        
                                  
                                    ],
                                    "credits": [("Creative direction", "Supermarket"),
                                                ("Art direction &amp; design", "Supermarket"),
                                                ("Content production", "Supermarket")],
                                },

                  "revlon-nate": {
                                    "client": "Revlon",
                                    "year": "",
                                    "segment": "",
                                    "services": "",
                                    "intro": (
                                        ""),
                                    "thumb": CDN + "images/Works/Revlon/revlon-nate-hero.jpg",
                                    "hero": CDN + "images/Works/Revlon/revlon-nate-hero.jpg",
                                    "media": [
                                        ("quote", ""),
                                        ("full",  CDN + "images/Works/Revlon/revlon-nate-01.jpg"),
                                        ("pair",  [(CDN + "images/Works/Revlon/revlon-nate-02.jpg"),
                                                  CDN + "images/Works/Revlon/revlon-nate-03.jpg"]),
                                        ("full",  CDN + "images/Works/Revlon/revlon-nate-04.jpg"),
                                        ("pair",  [(CDN + "images/Works/Revlon/revlon-nate-05.jpg"),
                                                   CDN + "images/Works/Revlon/revlon-nate-06.jpg"]),     
                                        ("full",  CDN + "images/Works/Revlon/revlon-nate-07.jpg"),
                                        
                                  
                                    ],
                                    "credits": [("Creative direction", "Supermarket"),
                                                ("Art direction &amp; design", "Supermarket"),
                                                ("Content production", "Supermarket")],
                                },                                

                 "barca-games": {
                                    "client": "Barça Games",
                                    "year": "",
                                    "segment": "",
                                    "services": "Branding, Strategy, Social media strategy, Motion graphics",
                                    "intro": (
                                        ""),
                                    "thumb": CDN + "images/Works/Barca-Games/barca-games-hero.png",
                                    "hero": CDN + "images/Works/Barca-Games/barca-games-hero.png",
                                    "media": [
                                        ("quote", ""),
                                        ("full",  CDN + "images/Works/Barca-Games/barca-games-01.jpg"),
                                        ("full",  CDN + "images/Works/Barca-Games/barca-games-02.jpg"),
                                        ("pair",  [(CDN + "images/Works/Barca-Games/barca-games-03.jpg"),
                                                  CDN + "images/Works/Barca-Games/barca-games-04.jpg"]),
                                        ("full",  CDN + "images/Works/Barca-Games/barca-games-05.jpg"),
                                        ("pair",  [(CDN + "images/Works/Barca-Games/barca-games-06.jpg"),
                                                   CDN + "images/Works/Barca-Games/barca-games-07.jpg"]),     
                                        ("full",  CDN + "images/Works/Barca-Games/barca-games-08.jpg"),
                                        ("full",  CDN + "images/Works/Barca-Games/barca-games-09.jpg"),
                                        ("full",  CDN + "images/Works/Barca-Games/barca-games-10.jpg"),
                                        ("pair",  [(CDN + "images/Works/Barca-Games/barca-games-11.jpg"),
                                                   CDN + "images/Works/Barca-Games/barca-games-12.jpg"]),
                                        ("full",  CDN + "images/Works/Barca-Games/barca-games-13.jpg"),                     
                                  
                                    ],
                                    "credits": [("Creative direction", "Supermarket"),
                                                ("Art direction &amp; design", "Supermarket"),
                                                ("Content production", "Supermarket")],
                                },                                

                  "revlon-butter": {
                                    "client": "Revlon",
                                    "year": "",
                                    "segment": "",
                                    "services": "",
                                    "intro": (
                                        ""),
                                    "thumb": CDN + "images/Works/Revlon/revlon-colorburst-hero.jpg",
                                    "hero": CDN + "images/Works/Revlon/revlon-colorburst-hero.jpg",
                                    "media": [
                                        ("quote", ""),
                                        ("full",  CDN + "images/Works/Revlon/revlon-colorburst-01.jpg"),
                                        ("pair",  [(CDN + "images/Works/Revlon/revlon-colorburst-02.jpg"),
                                                   CDN + "images/Works/Revlon/revlon-colorburst-03.jpg"]),
                                        ("pair",  [(CDN + "images/Works/Revlon/revlon-colorburst-04.jpg"),
                                                   CDN + "images/Works/Revlon/revlon-colorburst-05.jpg"]),     
                                        ("pair",  [(CDN + "images/Works/Revlon/revlon-colorburst-06.jpg"),
                                                   CDN + "images/Works/Revlon/revlon-colorburst-07.jpg"]),
                                        ("pair",  [(CDN + "images/Works/Revlon/revlon-colorburst-08.jpg"),
                                                   CDN + "images/Works/Revlon/revlon-colorburst-09.jpg"]),
                                        ("full",  CDN + "images/Works/Revlon/revlon-colorburst-10.jpg"),                     
                                  
                                    ],
                                    "credits": [("Creative direction", "Supermarket"),
                                                ("Art direction &amp; design", "Supermarket"),
                                                ("Content production", "Supermarket")],
                                },      

                  "revlon": {
                                    "client": "Revlon",
                                    "year": "",
                                    "segment": "",
                                    "services": "",
                                    "intro": (
                                        ""),
                                    "thumb": CDN + "images/Works/Revlon/revlon-campaigns-hero.jpg",
                                    "hero": CDN + "images/Works/Revlon/revlon-campaigns-hero.jpg",
                                    "media": [
                                        ("quote", ""),
                                        ("full",  CDN + "images/Works/Revlon/revlon-campaigns-01.jpg"),
                                        ("pair",  [(CDN + "images/Works/Revlon/revlon-campaigns-02.jpg"),
                                                   CDN + "images/Works/Revlon/revlon-campaigns-03.jpg"]),
                                         ("full",  CDN + "images/Works/Revlon/revlon-campaigns-04.jpg"),
                                        ("pair",  [(CDN + "images/Works/Revlon/revlon-campaigns-05.jpg"),
                                                   CDN + "images/Works/Revlon/revlon-campaigns-06.jpg"]),     
                                        ("pair",  [(CDN + "images/Works/Revlon/revlon-campaigns-07.jpg"),
                                                   CDN + "images/Works/Revlon/revlon-campaigns-08.jpg"]),
                                        ("pair",  [(CDN + "images/Works/Revlon/revlon-campaigns-09.jpg"),
                                                   CDN + "images/Works/Revlon/revlon-campaigns-10.jpg"]),
                                        ("full",  CDN + "images/Works/Revlon/revlon-campaigns-11.jpg"),     
                                        ("pair",  [(CDN + "images/Works/Revlon/revlon-campaigns-12.jpg"),
                                                  CDN + "images/Works/Revlon/revlon-campaigns-13.jpg"]),
                                        ("full",  CDN + "images/Works/Revlon/revlon-campaigns-14.jpg"),                      
                                  
                                    ],
                                    "credits": [("Creative direction", "Supermarket"),
                                                ("Art direction &amp; design", "Supermarket"),
                                                ("Content production", "Supermarket")],
                                },        

                  "coca-cola": {
                                    "client": "Coca Cola",
                                    "year": "",
                                    "segment": "",
                                    "services": "",
                                    "intro": (
                                        ""),
                                    "thumb": CDN + "images/Works/Cocacola/coca-cola-hero.jpg",
                                    "hero": CDN + "images/Works/Cocacola/coca-cola-hero.jpg",
                                    "media": [
                                        ("quote", ""),
                                        ("embed", "-XQAwHtUfhY"),
                                        ("embed", "J8A5fD8K4Ns"),                
                                  
                                    ],
                                    "credits": [("Creative direction", "Supermarket"),
                                                ("Art direction &amp; design", "Supermarket"),
                                                ("Content production", "Supermarket")],
                                },                     

                  "izzi": {
                                    "client": "Izzi",
                                    "year": "",
                                    "segment": "",
                                    "services": "",
                                    "intro": (
                                        ""),
                                    "thumb": CDN + "images/Works/Izzi/izzi-hero.png",
                                    "hero": CDN + "images/Works/Izzi/izzi-hero.png",
                                    "media": [
                                        ("quote", ""),
                                        ("full",  CDN + "images/Works/Izzi/izzi-01.jpeg"),
                                        ("pair",  [(CDN + "images/Works/Izzi/izzi-02.jpeg"),
                                                   CDN + "images/Works/Izzi/izzi-03.jpeg"]),
                                        ("pair",  [(CDN + "images/Works/Izzi/izzi-04.jpeg"),
                                                   CDN + "images/Works/Izzi/izzi-05.jpeg"]),
                                        ("pair",  [(CDN + "images/Works/Izzi/izzi-06.jpeg"),
                                                   CDN + "images/Works/Izzi/izzi-07.jpeg"]),
                                        ("full",  CDN + "images/Works/Izzi/izzi-08.jpeg"),                       
                                  
                                    ],
                                    "credits": [("Creative direction", "Supermarket"),
                                                ("Art direction &amp; design", "Supermarket"),
                                                ("Content production", "Supermarket")],
                                },        

                  "tigo-rebranding": {
                                    "client": "Tigo",
                                    "year": "",
                                    "segment": "",
                                    "services": "",
                                    "intro": (
                                        ""),
                                    "thumb": CDN + "images/Works/Tigo/tigo-rebrand-hero.jpg",
                                    "hero": CDN + "images/Works/Tigo/tigo-rebrand-hero.jpg",
                                    "media": [
                                        ("quote", ""),
                                        ("full",  CDN + "images/Works/Tigo/tigo-rebrand-01.jpg"),
                                        ("pair",  [(CDN + "images/Works/Tigo/tigo-rebrand-02.jpg"),
                                                   CDN + "images/Works/Tigo/tigo-rebrand-03.jpg"]),
                                        ("pair",  [(CDN + "images/Works/Tigo/tigo-rebrand-04.jpg"),
                                                   CDN + "images/Works/Tigo/tigo-rebrand-05.jpg"]),
                                        ("pair",  [(CDN + "images/Works/Tigo/tigo-rebrand-06.jpg"),
                                                   CDN + "images/Works/Tigo/tigo-rebrand-07.jpg"]),          
                                        ("full",  CDN + "images/Works/Tigo/tigo-rebrand-08.jpg"),
                                        ("pair",  [(CDN + "images/Works/Tigo/tigo-rebrand-09.jpg"),
                                                 CDN + "images/Works/Tigo/tigo-rebrand-10.jpg"]),
                                        ("pair",  [(CDN + "images/Works/Tigo/tigo-rebrand-11.jpg"),
                                                  CDN + "images/Works/Tigo/tigo-rebrand-12.jpg"]),
                                        ("pair",  [(CDN + "images/Works/Tigo/tigo-rebrand-13.jpg"),
                                                  CDN + "images/Works/Tigo/tigo-rebrand-14.jpg"]),
                                        ("pair",  [(CDN + "images/Works/Tigo/tigo-rebrand-15.jpg"),
                                                CDN + "images/Works/Tigo/tigo-rebrand-16.jpg"]),
                                        ("full",  CDN + "images/Works/Tigo/tigo-rebrand-17.jpg"),    
                                        ("pair",  [(CDN + "images/Works/Tigo/tigo-rebrand-18.jpg"),
                                                  CDN + "images/Works/Tigo/tigo-rebrand-19.jpg"]),
                                        ("pair",  [(CDN + "images/Works/Tigo/tigo-rebrand-20.jpg"),
                                                  CDN + "images/Works/Tigo/tigo-rebrand-21.jpg"]),
                                       ("pair",  [(CDN + "images/Works/Tigo/tigo-rebrand-22.jpg"),
                                                 CDN + "images/Works/Tigo/tigo-rebrand-23.jpg"]),
                                        ("pair",  [(CDN + "images/Works/Tigo/tigo-rebrand-24.jpg"),
                                                  CDN + "images/Works/Tigo/tigo-rebrand-25.jpg"]),                 
                                  
                                    ],
                                    "credits": [("Creative direction", "Supermarket"),
                                                ("Art direction &amp; design", "Supermarket"),
                                                ("Content production", "Supermarket")],
                                },                                       

                    "sodastream": {
                                    "client": "Sodastream",
                                    "year": "",
                                    "segment": "",
                                    "services": "",
                                    "intro": (
                                        ""),
                                    "thumb": CDN + "images/Works/Sodastream/sodastream-hero.jpg",
                                    "hero": CDN + "images/Works/Sodastream/sodastream-hero.jpg",
                                    "media": [
                                        ("quote", ""),
                                        ("full",  CDN + "images/Works/Sodastream/sodastream-01.png"),
                                        ("pair",  [(CDN + "images/Works/Sodastream/sodastream-02.png"),
                                                   CDN + "images/Works/Sodastream/sodastream-03.jpg"]),
                                        ("pair",  [(CDN + "images/Works/Sodastream/sodastream-04.jpg"),
                                                   CDN + "images/Works/Sodastream/sodastream-05.jpg"]),
                                        ("pair",  [(CDN + "images/Works/Sodastream/sodastream-06.jpg"),
                                                   CDN + "images/Works/Sodastream/sodastream-07.jpg"]),          
                                        ("pair",  [(CDN + "images/Works/Sodastream/sodastream-08.jpg"),
                                                 CDN + "images/Works/Sodastream/sodastream-09.png"]),
                                                                         
                                    ],
                                    "credits": [("Creative direction", "Supermarket"),
                                                ("Art direction &amp; design", "Supermarket"),
                                                ("Content production", "Supermarket")],
                                },                              

                    "nubceo": {
                                    "client": "Nubceo",
                                    "year": "2019",
                                    "segment": "",
                                    "services": "Branding, Identity, Design",
                                    "intro": (
                                        "Brand creation, complete identity design, branding, and application across all brand elements and communications."),
                                    "thumb": CDN + "images/Works/Nubceo/nubceo-hero.jpeg",
                                    "hero": CDN + "images/Works/Nubceo/nubceo-hero.jpeg",
                                    "media": [
                                        ("quote", ""),
                                        ("full",  CDN + "images/Works/Nubceo/nubceo-01.jpeg"),
                                        ("full",  CDN + "images/Works/Nubceo/nubceo-02.jpeg"),
                                        ("full",  CDN + "images/Works/Nubceo/nubceo-03.jpeg"),
                                        ("full",  CDN + "images/Works/Nubceo/nubceo-04.jpeg"),
                                        ("full",  CDN + "images/Works/Nubceo/nubceo-05.jpeg"),
                                        ("full",  CDN + "images/Works/Nubceo/nubceo-06.jpeg"),
                                        ("full",  CDN + "images/Works/Nubceo/nubceo-07.jpeg"),
                                        ("full",  CDN + "images/Works/Nubceo/nubceo-08.jpeg"),
                                        ("bleed",  CDN + "images/Works/Nubceo/nubceo-09.jpeg"),
                                        ("full",  CDN + "images/Works/Nubceo/nubceo-10.jpeg"),
                                        ("pair",  [(CDN + "images/Works/Nubceo/nubceo-11.jpeg"),
                                                   CDN + "images/Works/Nubceo/nubceo-12.jpeg"]),
                                        ("full",  CDN + "images/Works/Nubceo/nubceo-13.jpeg"),
                                        ("pair",  [(CDN + "images/Works/Nubceo/nubceo-14.jpeg"),
                                                   CDN + "images/Works/Nubceo/nubceo-15.jpeg"]),
                                        ("full",  CDN + "images/Works/Nubceo/nubceo-16.jpeg"),
                                                                         
                                    ],
                                    "credits": [("Creative direction", "Supermarket"),
                                                ("Art direction &amp; design", "Supermarket"),
                                                ("Content production", "Supermarket")],
                                },     

                    "tigo-money": {
                                    "client": "Tigo",
                                    "year": "2022",
                                    "segment": "",
                                    "services": "Advertising, Strategy, Filming, Production, Media",
                                    "intro": (
                                        "Among the wide range of services and products offered by Tigo, Tigo Money has stood out as a highly valued option for users in the Digital Wallet market. To successfully enter such a competitive industry, the launch of Tigo Money needed to live up to expectations. Therefore, we devised and executed a comprehensive cross-platform campaign for Tigo Money. We take care of the entire production process, from filming and photo shoots to post-production, special effects and motion graphics. Once production was completed, we deployed the campaign in digital and mass media, adopting a 360 approach that ensured wide coverage and an effective connection with the target audience in all relevant channels."),
                                    "thumb": CDN + "images/Works/Tigo/tigo-money-hero.jpeg",
                                    "hero": CDN + "images/Works/Tigo/tigo-money-hero.jpeg",
                                    "media": [
                                        ("quote", "Tigo Money 360° Launch Campaign / full-scale production and a 360° cross-platform campaign for maximum market impact."),
                                        ("video",  CDN + "videos/tigo-money-01.mp4"),
                                        ("full",  CDN + "images/Works/Tigo/tigo-money-02.png"),
                                        ("full",  CDN + "images/Works/Tigo/tigo-money-03.jpeg"),
                                        ("full",  CDN + "images/Works/Tigo/tigo-money-04.jpg"),
                                        ("full",  CDN + "images/Works/Tigo/tigo-money-05.png"),
                                        ("full",  CDN + "images/Works/Tigo/tigo-money-06.jpg"),
                                        ("full",  CDN + "images/Works/Tigo/tigo-money-07.png"),
                                        ("full",  CDN + "images/Works/Tigo/tigo-money-08.png"),
                                        ("full",  CDN + "images/Works/Tigo/tigo-money-09.jpg"),
                                        ("full",  CDN + "images/Works/Tigo/tigo-money-10.png"),
                                        ("full",  CDN + "images/Works/Tigo/tigo-money-11.jpg"),
                                        ("full",  CDN + "images/Works/Tigo/tigo-money-12.png"),
                                        ("full",  CDN + "images/Works/Tigo/tigo-money-13.jpg"),
                                        ("full",  CDN + "images/Works/Tigo/tigo-money-14.jpg"),
                                        ("full",  CDN + "images/Works/Tigo/tigo-money-15.jpg"),
                                        ("full",  CDN + "images/Works/Tigo/tigo-money-16.jpg"),
                                        ("full",  CDN + "images/Works/Tigo/tigo-money-17.jpg"),
                                        ("full",  CDN + "images/Works/Tigo/tigo-money-18.jpeg"),
                                        ("full",  CDN + "images/Works/Tigo/tigo-money-19.png"),
                                        ("full",  CDN + "images/Works/Tigo/tigo-money-20.jpg"),
                                        ("full",  CDN + "images/Works/Tigo/tigo-money-21.jpg"),
                                     
                                    ],
                                    "credits": [("Creative direction", "Supermarket"),
                                                ("Art direction &amp; design", "Supermarket"),
                                                ("Content production", "Supermarket")],
                                },                                     

                    "prester": {
                                    "client": "Prester",
                                    "year": "2019",
                                    "segment": "",
                                    "services": "Branding, Identity, UX/UI",
                                    "intro": (
                                        "We love to be aligned with our customers and with Prester we are united by two fundamental virtues: we are both fast and safe.\n" 
                                        "\n"
                                        "These are some of our projects. In a world where Fintechs are experiencing rapid growth, it is essential to maintain a strong identity and a secure presence to meet customer demands. In this regard, Prester stands out with its new branding and communications, which reflect our commitment to speed, safety and reliability. We worked on the development of this identity under the firm understanding that customer trust is paramount and must be conveyed clearly and unreservedly. Every element of our branding and communications has been conceived with these values and missions in mind, ensuring that every interaction with Prester inspires security and peace of mind in our customers."),
                                    "thumb": CDN + "images/Works/Prester/prester-hero.jpg",
                                    "hero": CDN + "images/Works/Prester/prester-hero.jpg",
                                    "media": [
                                        ("quote", "Complete Identity Creation, Institutional Launch Branding and Prester App Branding."),
                                        ("full",  CDN + "images/Works/Prester/prester-01.jpg"),
                                        ("full",  CDN + "images/Works/Prester/prester-02.jpg"),
                                        ("sheet",  CDN + "images/Works/Prester/prester-03.jpg"),
                                        ("sheet",  CDN + "images/Works/Prester/prester-04.jpg"),
                                        ("sheet",  CDN + "images/Works/Prester/prester-05.jpg"),
                                        ("full",  CDN + "images/Works/Prester/prester-06.jpg"),
                                        ("full",  CDN + "images/Works/Prester/prester-07.jpg"),
                                        ("full",  CDN + "images/Works/Prester/prester-08.jpg"),
                                        ("full",  CDN + "images/Works/Prester/prester-09.jpg"),
                                     
                                    ],
                                    "credits": [("Creative direction", "Supermarket"),
                                                ("Art direction &amp; design", "Supermarket"),
                                                ("Content production", "Supermarket")],
                                },                               

                      "facebank": {
                                    "client": "Facebank",
                                    "year": "2022",
                                    "segment": "",
                                    "services": "Institutional rebranding, Social media campaign",
                                    "intro": (
                                        "FACEBANK has emerged as one of the most reliable options for the Latin community in the growing market of digital wallets in dollars. We embarked on a rebranding project aimed at creating a new visual identity that not only reflected the essence of the brand but also laid the groundwork for future comprehensive campaigns. We accompanied FACEBANK in this corporate image renewal with the goal of launching a pioneering regional campaign targeted at entrepreneurs and independent workers. These individuals, with a pressing need to receive payment for their services in the United States and other parts of the world, represented the central focus of our launch strategy. Simultaneously, we developed a visual identity system for social media, which would complement and reinforce these campaigns. Additionally, we implemented email marketing tactics, sponsored relevant events, and executed specific campaigns in various countries in Latin America. In summary, our work with FACEBANK not only involved creating a new corporate image but also entailed the design and implementation of comprehensive marketing strategies aimed at positioning the brand as the preferred choice for the Latin community in the digital world of finance."),
                                    "thumb": CDN + "images/Works/Facebank/facebank-hero.jpeg",
                                    "hero": CDN + "images/Works/Facebank/facebank-hero.jpeg",
                                    "media": [
                                        ("quote", ""),
                                        ("full",  CDN + "images/Works/Facebank/facebank-01.jpeg"),
                                        ("full",  CDN + "images/Works/Facebank/facebank-02.jpeg"),
                                        ("full",  CDN + "images/Works/Facebank/facebank-03.jpeg"),
                                        ("full",  CDN + "images/Works/Facebank/facebank-04.jpg"),
                                        ("full",  CDN + "images/Works/Facebank/facebank-05.jpeg"),
                                        ("full",  CDN + "images/Works/Facebank/facebank-06.jpeg"),
                                        ("full",  CDN + "images/Works/Facebank/facebank-07.jpeg"),
                                        ("full",  CDN + "images/Works/Facebank/facebank-08.jpg"),
                                     
                                    ],
                                    "credits": [("Creative direction", "Supermarket"),
                                                ("Art direction &amp; design", "Supermarket"),
                                                ("Content production", "Supermarket")],
                                },                               

                      "ucema": {
                                    "client": "UCEMA",
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
                                    "thumb": CDN + "images/Works/UCEMA/ucema-brand-hero.jpg",
                                    "hero": CDN + "images/Works/UCEMA/ucema-brand-hero.jpg",
                                    "media": [
                                        ("quote", "One app, three seasons, three graphic identities."),
                                        ("full",  CDN + "images/Works/UCEMA/ucema-brand-01.jpeg"),
                                        ("full",  CDN + "images/Works/UCEMA/ucema-brand-02.jpeg"),
                                        ("full",  CDN + "images/Works/UCEMA/ucema-brand-03.jpeg"),
                                        ("full",  CDN + "images/Works/UCEMA/ucema-brand-04.jpeg"),
                                        ("full",  CDN + "images/Works/UCEMA/ucema-brand-05.jpeg"),
                                        ("full",  CDN + "images/Works/UCEMA/ucema-brand-06.jpeg"),
                                        ("full",  CDN + "images/Works/UCEMA/ucema-brand-07.jpeg"),
                                        ("full",  CDN + "images/Works/UCEMA/ucema-brand-08.jpeg"),
                                        ("full",  CDN + "images/Works/UCEMA/ucema-brand-09.jpeg"),
                                        ("full",  CDN + "images/Works/UCEMA/ucema-brand-10.jpeg"),
                                        ("full",  CDN + "images/Works/UCEMA/ucema-brand-11.jpeg"),
                                        ("full",  CDN + "images/Works/UCEMA/ucema-brand-12.jpeg"),
                                        ("full",  CDN + "images/Works/UCEMA/ucema-brand-13.jpeg"),
                                        ("full",  CDN + "images/Works/UCEMA/ucema-brand-14.jpeg"),
                                        ("full",  CDN + "images/Works/UCEMA/ucema-brand-15.jpeg"),
                                        ("full",  CDN + "images/Works/UCEMA/ucema-brand-16.jpeg"),
                                        ("full",  CDN + "images/Works/UCEMA/ucema-brand-18.jpeg"),
                                        ("full",  CDN + "images/Works/UCEMA/ucema-brand-19.jpeg"),
                                        ("full",  CDN + "images/Works/UCEMA/ucema-brand-20.jpeg"),
                                        ("full",  CDN + "images/Works/UCEMA/ucema-brand-21.jpeg"),
                                        ("full",  CDN + "images/Works/UCEMA/ucema-brand-22.jpeg"),
                                        ("full",  CDN + "images/Works/UCEMA/ucema-brand-23.jpeg"),                                     
                                     
                                    ],
                                    "credits": [("Creative direction", "Supermarket"),
                                                ("Art direction &amp; design", "Supermarket"),
                                                ("Content production", "Supermarket")],
                                },                          

                      "peisa": {
                                    "client": "Peisa",
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
                                    "thumb": CDN + "images/Works/Peisa/peisa-hero.jpeg",
                                    "hero": CDN + "images/Works/Peisa/peisa-hero.jpeg",
                                    "media": [
                                        ("quote", "One app, three seasons, three graphic identities."),
                                        ("full",  CDN + "images/Works/Peisa/peisa-01.jpg"),
                                        ("full",  CDN + "images/Works/Peisa/peisa-02.jpeg"),
                                        ("full",  CDN + "images/Works/Peisa/peisa-03.jpg"),
                                        ("full",  CDN + "images/Works/Peisa/peisa-04.jpg"),
                                        ("full",  CDN + "images/Works/Peisa/peisa-05.jpeg"),
                                        ("full",  CDN + "images/Works/Peisa/peisa-06.jpg"),
                                        ("full",  CDN + "images/Works/Peisa/peisa-07.jpeg"),
                                        ("full",  CDN + "images/Works/Peisa/peisa-08.jpeg"),                       
                                     
                                    ],
                                    "credits": [("Creative direction", "Supermarket"),
                                                ("Art direction &amp; design", "Supermarket"),
                                                ("Content production", "Supermarket")],
                                },                          

                      "vireyes": {
                                    "client": "Vireyes",
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
                                    "thumb": CDN + "images/Works/Vireyes/vireyes-hero.jpeg",
                                    "hero": CDN + "images/Works/Vireyes/vireyes-hero.jpeg",
                                    "media": [
                                        ("quote", "One app, three seasons, three graphic identities."),
                                        ("full",  CDN + "images/Works/Vireyes/vireyes-01.jpg"),
                                        ("full",  CDN + "images/Works/Vireyes/vireyes-02.jpg"),
                                        ("full",  CDN + "images/Works/Vireyes/vireyes-03.jpg"),
                                        ("full",  CDN + "images/Works/Vireyes/vireyes-04.jpg"),
                                        ("full",  CDN + "images/Works/Vireyes/vireyes-05.jpg"),
                                        ("full",  CDN + "images/Works/Vireyes/vireyes-06.jpg"),
                                        ("full",  CDN + "images/Works/Vireyes/vireyes-07.jpg"),
                                        ("full",  CDN + "images/Works/Vireyes/vireyes-08.jpg"), 
                                        ("full",  CDN + "images/Works/Vireyes/vireyes-09.jpg"),                                                                 
                                     
                                    ],
                                    "credits": [("Creative direction", "Supermarket"),
                                                ("Art direction &amp; design", "Supermarket"),
                                                ("Content production", "Supermarket")],
                                },                          

                      "lati": {
                                    "client": "Lati",
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
                                    "thumb": CDN + "images/Works/Lati/lati-hero.jpg",
                                    "hero": CDN + "images/Works/Lati/lati-hero.jpg",
                                    "media": [
                                        ("quote", "One app, three seasons, three graphic identities."),
                                        ("full",  CDN + "images/Works/Lati/lati-01.jpg"),
                                        ("full",  CDN + "images/Works/Lati/lati-02.jpg"),
                                        ("full",  CDN + "images/Works/Lati/lati-03.jpg"),
                                        ("full",  CDN + "images/Works/Lati/lati-04.jpg"),
                                        ("full",  CDN + "images/Works/Lati/lati-05.jpg"),
                                        ("full",  CDN + "images/Works/Lati/lati-06.jpg"),
                                        ("full",  CDN + "images/Works/Lati/lati-07.jpg"),
                                        ("full",  CDN + "images/Works/Lati/lati-08.jpg"), 
                                        ("full",  CDN + "images/Works/Lati/lati-09.jpg"),                                                                 
                                     
                                    ],
                                    "credits": [("Creative direction", "Supermarket"),
                                                ("Art direction &amp; design", "Supermarket"),
                                                ("Content production", "Supermarket")],
                                },                          

                      "chocolates-arcor": {
                                    "client": "Arcor",
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
                                    "thumb": CDN + "images/Works/Arcor/chocolates-arcor-hero.jpeg",
                                    "hero": CDN + "images/Works/Arcor/chocolates-arcor-hero.jpeg",
                                    "media": [
                                        ("quote", "One app, three seasons, three graphic identities."),
                                        ("full",  CDN + "images/Works/Arcor/chocolates-arcor-01.jpg"),
                                        ("full",  CDN + "images/Works/Arcor/chocolates-arcor-02.jpg"),
                                        ("sheet",  CDN + "images/Works/Arcor/chocolates-arcor-03.jpeg"),
                                        ("sheet",  CDN + "images/Works/Arcor/chocolates-arcor-04.jpeg"),
                                        ("full",  CDN + "images/Works/Arcor/chocolates-arcor-05.jpg"),
                                        ("full",  CDN + "images/Works/Arcor/chocolates-arcor-06.jpg"),
                                        ("full",  CDN + "images/Works/Arcor/chocolates-arcor-07.jpg"),
                                        ("pair",  [(CDN + "images/Works/Arcor/chocolates-arcor-08.jpg"),
                                                   CDN + "images/Works/Arcor/chocolates-arcor-09.jpg"]),                                      
                                        ("sheet",  CDN + "images/Works/Arcor/chocolates-arcor-10.jpeg"), 
                                        ("sheet",  CDN + "images/Works/Arcor/chocolates-arcor-11.jpeg"),                                                                 
                                     
                                    ],
                                    "credits": [("Creative direction", "Supermarket"),
                                                ("Art direction &amp; design", "Supermarket"),
                                                ("Content production", "Supermarket")],
                                },                          

                      "serenito": {
                                    "client": "Serenito",
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
                                    "thumb": CDN + "images/Works/Serenito/serenito-hero.jpg",
                                    "hero": CDN + "images/Works/Serenito/serenito-hero.jpg",
                                    "media": [
                                        ("quote", "One app, three seasons, three graphic identities."),
                                        ("full",  CDN + "images/Works/Serenito/serenito-01.jpg"),
                                        ("full",  CDN + "images/Works/Serenito/serenito-02.jpg"),
                                        ("full",  CDN + "images/Works/Serenito/serenito-03.jpg"),
                                        ("full",  CDN + "images/Works/Serenito/serenito-04.jpg"),
                                        ("full",  CDN + "images/Works/Serenito/serenito-05.jpg"),   
                                        ("pair",  [(CDN + "images/Works/Serenito/serenito-06.jpg"),
                                                   CDN + "images/Works/Serenito/serenito-07.jpg"]),                                                                                                                                                  
                                     
                                    ],
                                    "credits": [("Creative direction", "Supermarket"),
                                                ("Art direction &amp; design", "Supermarket"),
                                                ("Content production", "Supermarket")],
                                },      

                      "oky": {
                                    "client": "Oky",
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
                                    "thumb": CDN + "images/Works/Oky/oky-hero.jpg",
                                    "hero": CDN + "images/Works/Oky/oky-hero.jpg",
                                    "media": [
                                        ("quote", "One app, three seasons, three graphic identities."),
                                        ("full",  CDN + "images/Works/Oky/oky-01.jpg"),
                                        ("full",  CDN + "images/Works/Oky/oky-02.jpg"),
                                        
                                        ("full",  CDN + "images/Works/Oky/oky-03.jpg"),
                                        ("full",  CDN + "images/Works/Oky/oky-04.jpg"), 
                                        ("full",  CDN + "images/Works/Oky/oky-05.jpg"),
                                        ("full",  CDN + "images/Works/Oky/oky-06.jpg"),
                                        ("bleed",  CDN + "images/Works/Oky/oky-07.jpg"),
                                     
                                    ],
                                    "credits": [("Creative direction", "Supermarket"),
                                                ("Art direction &amp; design", "Supermarket"),
                                                ("Content production", "Supermarket")],
                                },      

                      "felaban": {
                                    "client": "Felaban",
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
                                    "thumb": CDN + "images/Works/Felaban/felaban-hero.jpg",
                                    "hero": CDN + "images/Works/Felaban/felaban-hero.jpg",
                                    "media": [
                                        ("quote", "One app, three seasons, three graphic identities."),
                                        ("full",  CDN + "images/Works/Felaban/felaban-01.jpg"),
                                        ("full",  CDN + "images/Works/Felaban/felaban-02.jpg"),
                                        ("full",  CDN + "images/Works/Felaban/felaban-03.jpg"),
                                        ("pair",  [(CDN + "images/Works/Felaban/felaban-04.jpg"),
                                                   CDN + "images/Works/Felaban/felaban-05.jpg"]),                                         
                                     
                                    ],
                                    "credits": [("Creative direction", "Supermarket"),
                                                ("Art direction &amp; design", "Supermarket"),
                                                ("Content production", "Supermarket")],                                         
                                },      

                      "stanley": {
                                    "client": "Stanley",
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
                                    "thumb": CDN + "images/Works/Stanley/stanley-hero.jpg",
                                    "hero": CDN + "images/Works/Stanley/stanley-hero.jpg",
                                    "media": [
                                        ("quote", "One app, three seasons, three graphic identities."),
                                        ("full",  CDN + "images/Works/Stanley/stanley-01.jpg"),
                                        ("full",  CDN + "images/Works/Stanley/stanley-02.jpg"),
                                        ("full",  CDN + "images/Works/Stanley/stanley-03.jpg"),
                                        ("pair",  [(CDN + "images/Works/Stanley/stanley-04.jpg"),
                                                   CDN + "images/Works/Stanley/stanley-05.jpg"]),  
                                        ("full",  CDN + "images/Works/Stanley/stanley-06.jpg"),
                                        ("full",  CDN + "images/Works/Stanley/stanley-07.jpg"),
                                        ("full",  CDN + "images/Works/Stanley/stanley-08.jpg"), 
                                        ("full",  CDN + "images/Works/Stanley/stanley-09.jpg"),                                                                                             
                                     
                                    ],
                                    "credits": [("Creative direction", "Supermarket"),
                                                ("Art direction &amp; design", "Supermarket"),
                                                ("Content production", "Supermarket")],                                           
                                },      

                      "eron": {
                                    "client": "Eron",
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
                                    "thumb": CDN + "images/Works/Eron/eron-hero.jpg",
                                    "hero": CDN + "images/Works/Eron/eron-hero.jpg",
                                    "media": [
                                        ("quote", "One app, three seasons, three graphic identities."),
                                        ("full",  CDN + "images/Works/Eron/eron-01.jpg"),
                                        ("full",  CDN + "images/Works/Eron/eron-02.jpg"),
                                        ("full",  CDN + "images/Works/Eron/eron-03.jpg"),
                                        ("full",  CDN + "images/Works/Eron/eron-04.jpg"),
                                        ("pair",  [(CDN + "images/Works/Eron/eron-05.jpg"),
                                                   CDN + "images/Works/Eron/eron-06.jpg"]),  
                                        ("full",  CDN + "images/Works/Eron/eron-07.jpg"),
                                        ("full",  CDN + "images/Works/Eron/eron-08.jpg"),                                                                                          
                                     
                                    ],
                                    "credits": [("Creative direction", "Supermarket"),
                                                ("Art direction &amp; design", "Supermarket"),
                                                ("Content production", "Supermarket")],                                          
                                },      

                      "glenhaven": {
                                    "client": "Glenhaven",
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
                                    "thumb": CDN + "images/Works/Glenhaven/glenhaven-hero.jpeg",
                                    "hero": CDN + "images/Works/Glenhaven/glenhaven-hero.jpeg",
                                    "media": [
                                        ("quote", "One app, three seasons, three graphic identities."),
                                        ("full",  CDN + "images/Works/Glenhaven/glenhaven-01.jpeg"),
                                        ("full",  CDN + "images/Works/Glenhaven/glenhaven-02.jpeg"),
                                        ("full",  CDN + "images/Works/Glenhaven/glenhaven-03.jpeg"),
                                        ("full",  CDN + "images/Works/Glenhaven/glenhaven-04.jpeg"),
                                        ("full",  CDN + "images/Works/Glenhaven/glenhaven-05.jpeg"),                                                                                      
                                     
                                    ],
                                    "credits": [("Creative direction", "Supermarket"),
                                                ("Art direction &amp; design", "Supermarket"),
                                                ("Content production", "Supermarket")],                                          
                                },      

                      "delicia": {
                                    "client": "Delicia",
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
                                    "thumb": CDN + "images/Works/Delicia/delicia-hero.jpeg",
                                    "hero": CDN + "images/Works/Delicia/delicia-hero.jpeg",
                                    "media": [
                                        ("quote", "One app, three seasons, three graphic identities."),
                                        ("full",  CDN + "images/Works/Delicia/delicia-01.jpeg"),
                                        ("full",  CDN + "images/Works/Delicia/delicia-02.jpeg"),
                                        ("full",  CDN + "images/Works/Delicia/delicia-03.jpeg"),
                                        ("full",  CDN + "images/Works/Delicia/delicia-04.jpeg"),  
                                        ("full",  CDN + "images/Works/Delicia/delicia-05.jpeg"),
                                        ("full",  CDN + "images/Works/Delicia/delicia-06.jpeg"),  
                                        ("full",  CDN + "images/Works/Delicia/delicia-07.jpeg"),
                                        ("full",  CDN + "images/Works/Delicia/delicia-08.jpeg"),                                          
                                        ("pair",  [(CDN + "images/Works/Delicia/delicia-09.jpeg"),
                                                   CDN + "images/Works/Delicia/delicia-10.jpeg"]), 
                                        ("pair",  [(CDN + "images/Works/Delicia/delicia-11.jpeg"),
                                                     CDN + "images/Works/Delicia/delicia-12.jpeg"]),                                                                                                                                                                                 
                                     
                                    ],
                                    "credits": [("Creative direction", "Supermarket"),
                                                ("Art direction &amp; design", "Supermarket"),
                                                ("Content production", "Supermarket")],                                         
                                },      

    # --- proyectos incorporados desde la rama de Mati ---
    "alicante": {
        "client": "La Virginia",
        "year": "2021",
        "segment": "",
        "services": "Social media strategy, art direction, design, content production",
        "intro": (
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
            " quis nostrud exercitation ullamco laboris nisi ut aliqui "
            "strategy to design and production of Instagram posts, Stories, and Reels, helping "
            "build an engaging and playful presence for the app across platforms. We developed "
            "tailored campaigns for key moments in the calendar — including Christmas, King's Day, "
            "and Carnival — each with its own graphic identity and tone, driving visibility, "
            "downloads, and fan engagement through festive, high-impact content."),
        "thumb": CDN + "images/Works/Alicante/AlicanteBanner.jpeg", # <- nueva línea
        "hero": CDN + "images/Works/Alicante/AlicanteBanner.jpeg",
        "media": [
            ("full",  CDN + "images/Works/Alicante/AlicanteBanner.jpeg"),
            ("quote", "One app, three seasons, three graphic identities."),
            ("full",  CDN + "images/Works/Alicante/AlicanteMockupSopaLista.jpeg"),
            ("pair",  [(CDN + "images/Works/Alicante/AlicanteMockupSopaListaSupermercado.jpeg"),
                       CDN + "images/Works/Alicante/AlicanteMockupSopaListaSupermercado2.jpeg"]),
            ("bleed", (CDN + "images/Works/Alicante/AlicanteSopaListaArte.jpeg")),
            ("full",  CDN + "images/Works/Alicante/AlicanteMockupSopaListaSupermercado.jpeg"),
            ("bleed", (CDN + "images/Works/Alicante/AlicanteMockupCartel.jpeg")),
        ],
        "credits": [("Creative direction", "Supermarket"),
                    ("Art direction &amp; design", "Supermarket"),
                    ("Content production", "Supermarket")],
    },
    "vital-polvo": {
            "client": "Vital",
            "year": "2017",
            "segment": "",
            "services": "Social media strategy, art direction, design, content production",
            "intro": (
                "Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
                " quis nostrud exercitation ullamco laboris nisi ut aliqui "
                "strategy to design and production of Instagram posts, Stories, and Reels, helping "
                "build an engaging and playful presence for the app across platforms. We developed "
                "tailored campaigns for key moments in the calendar — including Christmas, King's Day, "
                "and Carnival — each with its own graphic identity and tone, driving visibility, "
                "downloads, and fan engagement through festive, high-impact content."),
            "thumb": CDN + "images/Works/Vital-Polvo/VitalPolvoBanner.jpeg", # <- nueva línea
            "hero": CDN + "images/Works/Vital-Polvo/VitalPolvoBanner.jpeg",
            "media": [
                ("full",  CDN + "images/Works/Vital-Polvo/VitalPolvoTV.jpeg"),
                ("quote", "One app, three seasons, three graphic identities."),
                ("full",  CDN + "images/Works/Vital-Polvo/VitalPolvoCartelEsquina.jpeg"),
                ("pair",  [(CDN + "images/Works/Vital-Polvo/VitalPolvoMamadera.jpeg"),
                           CDN + "images/Works/Vital-Polvo/VitalPolvoBolsoMamá.jpeg"]),
                ("bleed", (CDN + "images/Works/Vital-Polvo/VitalPolvoMockupSupermercado.jpeg")),
                ("full",  CDN + "images/Works/Vital-Polvo/VitalPolvoMockupCochecito.jpeg"),
          
            ],
            "credits": [("Creative direction", "Supermarket"),
                        ("Art direction &amp; design", "Supermarket"),
                        ("Content production", "Supermarket")],
        },
    "cutex-pro": {
                                "client": "Cutex Pro",
                                "year": "2017",
                                "segment": "",
                                "services": "Social media strategy, art direction, design, content production",
                                "intro": (
                                    "Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
                                    " quis nostrud exercitation ullamco laboris nisi ut aliqui "
                                    "strategy to design and production of Instagram posts, Stories, and Reels, helping "
                                    "build an engaging and playful presence for the app across platforms. We developed "
                                    "tailored campaigns for key moments in the calendar — including Christmas, King's Day, "
                                    "and Carnival — each with its own graphic identity and tone, driving visibility, "
                                    "downloads, and fan engagement through festive, high-impact content."),
                                "thumb": CDN + "images/Works/Cutex-Pro/CutexProBanner.jpeg", # <- nueva línea
                                "hero": CDN + "images/Works/Cutex-Pro/CutexProBanner.jpeg",
                                "media": [
                                    ("full",  CDN + "images/Works/Cutex-Pro/CutexProGrid.jpeg"),
                                    ("quote", "One app, three seasons, three graphic identities."),
                                    ("bleed",  CDN + "images/Works/Cutex-Pro/CutexProCartel.jpeg"),
                                    ("pair",  [(CDN + "images/Works/Cutex-Pro/CutexProA4.jpeg"),
                                               CDN + "images/Works/Cutex-Pro/CutexProRevista2.jpeg"]),
                                    ("full",  CDN + "images/Works/Cutex-Pro/CutexProStand.jpeg"),
                                    ("full", (CDN + "images/Works/Cutex-Pro/CutexProMockupsVarios.jpeg")),
                                    ("bleed",  CDN + "images/Works/Cutex-Pro/CutexProRevista.jpeg"),
                                    ("full", (CDN + "images/Works/Cutex-Pro/CutexProMockupsVarios2.jpeg")),
                                    ("full", (CDN + "images/Works/Cutex-Pro/CutexProCatalogo.jpeg")),
                                    ("pair",  [(CDN + "images/Works/Cutex-Pro/CutexProCartelSalientes.jpeg"),
                                                CDN + "images/Works/Cutex-Pro/CutexProRevista3.jpeg"]),
                                    ("full",  CDN + "images/Works/Cutex-Pro/CutexProExibidores.jpeg"),
                                    ("bleed", (CDN + "images/Works/Cutex-Pro/CutexProCarteles.jpeg")),
                                    ("full",  CDN + "images/Works/Cutex-Pro/CutexProTablet.jpeg"),
                              
                                ],
                                "credits": [("Creative direction", "Supermarket"),
                                            ("Art direction &amp; design", "Supermarket"),
                                            ("Content production", "Supermarket")],
                            },         
    "wing": {
                                    "client": "Wing",
                                    "year": "2017",
                                    "segment": "",
                                    "services": "Social media strategy, art direction, design, content production",
                                    "intro": (
                                        "Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
                                        " quis nostrud exercitation ullamco laboris nisi ut aliqui "
                                        "strategy to design and production of Instagram posts, Stories, and Reels, helping "
                                        "build an engaging and playful presence for the app across platforms. We developed "
                                        "tailored campaigns for key moments in the calendar — including Christmas, King's Day, "
                                        "and Carnival — each with its own graphic identity and tone, driving visibility, "
                                        "downloads, and fan engagement through festive, high-impact content."),
                                    "thumb": CDN + "images/Works/Wing/WingBanner.jpeg", # <- nueva línea
                                    "hero": CDN + "images/Works/Wing/WingVentana.jpeg",
                                    "media": [
                                        ("full",  CDN + "images/Works/Wing/WingBanner.jpeg"),
                                        ("quote", "One app, three seasons, three graphic identities."),
                                        ("full",  CDN + "images/Works/Wing/WingLogo.jpeg"),
                                        ("bleed",  CDN + "images/Works/Wing/WingMockupVertical.jpeg"),
                                        ("bleed",  CDN + "images/Works/Wing/WingGrid.jpeg"),
                                        ("pair",  [(CDN + "images/Works/Wing/WingMockupCartel.jpeg"),
                                                   CDN + "images/Works/Wing/WingMockupCamion.jpeg"]),
                                        ("full",  CDN + "images/Works/Wing/WingArtesVarios.jpeg"),
                                        ("full", (CDN + "images/Works/Wing/WingOficina.jpeg")),
                                        ("full", (CDN + "images/Works/Wing/WingMockupPhone.jpeg")),
                                        ("bleed", (CDN + "images/Works/Wing/WingKVFoto2.jpg")),
                                        ("full", (CDN + "images/Works/Wing/WingMockupPhone.jpeg")),
                                        ("full", (CDN + "images/Works/Wing/WingComputer.jpeg")),
                                        ("pair",  [(CDN + "images/Works/Wing/WingKVFoto.jpg"),
                                                    CDN + "images/Works/Wing/WingMockupPhone2.jpeg"]),
                                        ("sheet",  CDN + "images/Works/Wing/WingIconography.jpeg"),
                                        ("sheet",  CDN + "images/Works/Wing/WingEmbajador.jpeg"),
                                        ("sheet",  CDN + "images/Works/Wing/WingEmbajador2.jpeg"),
                                  
                                    ],
                                    "credits": [("Creative direction", "Supermarket"),
                                                ("Art direction &amp; design", "Supermarket"),
                                                ("Content production", "Supermarket")],
                                },      
    "cutex": {
                                    "client": "Cutex",
                                    "year": "2017",
                                    "segment": "",
                                    "services": "Social media strategy, art direction, design, content production",
                                    "intro": (
                                        "Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
                                        " quis nostrud exercitation ullamco laboris nisi ut aliqui "
                                        "strategy to design and production of Instagram posts, Stories, and Reels, helping "
                                        "build an engaging and playful presence for the app across platforms. We developed "
                                        "tailored campaigns for key moments in the calendar — including Christmas, King's Day, "
                                        "and Carnival — each with its own graphic identity and tone, driving visibility, "
                                        "downloads, and fan engagement through festive, high-impact content."),
                                    "thumb": CDN + "images/Works/Cutex/CutexBanner.jpeg", # <- nueva línea
                                    "hero": CDN + "images/Works/Cutex/CutexBanner.jpeg",
                                    "media": [
                                        ("full",  CDN + "images/Works/Cutex/CutexPortadaCartel.jpeg"),
                                        ("quote", "One app, three seasons, three graphic identities."),
                                        ("full",  CDN + "images/Works/Cutex/CutexBotellas.jpeg"),
                                        ("full",  CDN + "images/Works/Cutex/CutexEsmaltes.jpeg"),
                                        ("full",  CDN + "images/Works/Cutex/CutexPapel.jpeg"),
                                        ("pair",  [(CDN + "images/Works/Cutex/CutexCartelesVerticales.jpeg"),
                                                   CDN + "images/Works/Cutex/CutexMockupPuesto.jpeg"]),
                                        ("full",  CDN + "images/Works/Cutex/CutexMockupsRevista.jpeg"),
                                        ("pair",  [(CDN + "images/Works/Cutex/CutexBannersVerticales.jpeg"),
                                                   CDN + "images/Works/Cutex/CutexExibidores.jpeg"]),
                                        ("full", (CDN + "images/Works/Cutex/CutexExibidores2.jpeg")),
                                        ("bleed",  CDN + "images/Works/Cutex/CutexBannerCalle.jpeg"),
                                        ("pair",  [(CDN + "images/Works/Cutex/CutexMockupDiario2.jpeg"),
                                                    CDN + "images/Works/Cutex/CutexGrid.jpeg"]),
                                        ("full",  CDN + "images/Works/Cutex/CutexPapel2.jpeg"),
                                        ("full",  CDN + "images/Works/Cutex/CutexStickers.jpeg"),
                                        ("bleed", (CDN + "images/Works/Cutex/CutexGrid2.jpeg")),
                                        ("full",  CDN + "images/Works/Cutex/CutexBotellas2.jpeg"),
                                        ("full",  CDN + "images/Works/Cutex/CutexMockupsShopping.jpeg"),
                                        ("full",  CDN + "images/Works/Cutex/CutexMockupDiario.jpeg"),
                                        ("pair",  [(CDN + "images/Works/Cutex/CutexMockupCartelCalle.jpeg"),
                                                    CDN + "images/Works/Cutex/CutexMockupCartelesGondolas.jpeg"]),
                                    ],
                                    "credits": [("Creative direction", "Supermarket"),
                                                ("Art direction &amp; design", "Supermarket"),
                                                ("Content production", "Supermarket")],
                                },
    "arcor-patria": {
                                    "client": "Arcor",
                                    "year": "2017",
                                    "segment": "",
                                    "services": "Social media strategy, art direction, design, content production",
                                    "intro": (
                                        "Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
                                        " quis nostrud exercitation ullamco laboris nisi ut aliqui "
                                        "strategy to design and production of Instagram posts, Stories, and Reels, helping "
                                        "build an engaging and playful presence for the app across platforms. We developed "
                                        "tailored campaigns for key moments in the calendar — including Christmas, King's Day, "
                                        "and Carnival — each with its own graphic identity and tone, driving visibility, "
                                        "downloads, and fan engagement through festive, high-impact content."),
                                    "thumb": CDN + "images/Works/Arcor-Patria/ArcorPatriaBanner.jpeg", # <- nueva línea
                                    "hero": CDN + "images/Works/Arcor-Patria/ArcorPatriaBanner.jpeg",
                                    "media": [
                                        ("sheet",  CDN + "images/Works/Arcor-Patria/ArcorPatriaSheet1.jpeg"),
                                        ("sheet",  CDN + "images/Works/Arcor-Patria/ArcorPatriaSheet2.jpeg"),
                                        ("sheet",  CDN + "images/Works/Arcor-Patria/ArcorPatriaSheet3.jpeg"),
                                        ("sheet",  CDN + "images/Works/Arcor-Patria/ArcorPatriaSheet4.jpeg"),
                                    ],
                                    "credits": [("Creative direction", "Supermarket"),
                                                ("Art direction &amp; design", "Supermarket"),
                                                ("Content production", "Supermarket")],
                                },
    "quilmes-pumas": {
                                        "client": "Quilmes",
                                        "year": "2017",
                                        "segment": "",
                                        "services": "Social media strategy, art direction, design, content production",
                                        "intro": (
                                            "Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
                                            " quis nostrud exercitation ullamco laboris nisi ut aliqui "
                                            "strategy to design and production of Instagram posts, Stories, and Reels, helping "
                                            "build an engaging and playful presence for the app across platforms. We developed "
                                            "tailored campaigns for key moments in the calendar — including Christmas, King's Day, "
                                            "and Carnival — each with its own graphic identity and tone, driving visibility, "
                                            "downloads, and fan engagement through festive, high-impact content."),
                                        "thumb": CDN + "images/Works/Quilmes-Pumas/QuilmesPumasCartelBanner.png", # <- nueva línea
                                        "hero": CDN + "images/Works/Quilmes-Pumas/QuilmesPumasCartelBanner.png",
                                        "media": [
                                            ("full",  CDN + "images/Works/Quilmes-Pumas/QuilmesPumasKV.png"),
                                            ("full",  CDN + "images/Works/Quilmes-Pumas/QuilmesPumasMockupCartelBondi.png"),
                                            ("full",  CDN + "images/Works/Quilmes-Pumas/QuilmesPumasKV2.png"),
                                            ("full",  CDN + "images/Works/Quilmes-Pumas/QuilmesPumasMockupCancha.png"),
                                        ],
                                        "credits": [("Creative direction", "Supermarket"),
                                                    ("Art direction &amp; design", "Supermarket"),
                                                    ("Content production", "Supermarket")],
                                    },
    "prestix": {
                                        "client": "Prestix",
                                        "year": "2017",
                                        "segment": "",
                                        "services": "Social media strategy, art direction, design, content production",
                                        "intro": (
                                            "Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
                                            " quis nostrud exercitation ullamco laboris nisi ut aliqui "
                                            "strategy to design and production of Instagram posts, Stories, and Reels, helping "
                                            "build an engaging and playful presence for the app across platforms. We developed "
                                            "tailored campaigns for key moments in the calendar — including Christmas, King's Day, "
                                            "and Carnival — each with its own graphic identity and tone, driving visibility, "
                                            "downloads, and fan engagement through festive, high-impact content."),
                                        "thumb": CDN + "images/Works/Prestix/PrestixBanner.jpeg", # <- nueva línea
                                        "hero": CDN + "images/Works/Prestix/PrestixBanner.jpeg",
                                        "media": [
                                            ("full",  CDN + "images/Works/Prestix/PrestixLogo.png"),
                                            ("quote", "One app, three seasons, three graphic identities."),
                                            ("full",  CDN + "images/Works/Prestix/PrestixLogoColor.png"),
                                            ("bleed",  CDN + "images/Works/Prestix/PrestixIconography.jpeg"),
                                            ("pair",  [(CDN + "images/Works/Prestix/PrestixIconography2.jpeg"),
                                                       CDN + "images/Works/Prestix/PrestixKV.png"]),
                                            ("full",  CDN + "images/Works/Prestix/PrestixMockupCartelVertical.jpeg"),
                                            ("full", (CDN + "images/Works/Prestix/PrestixBannerCartel.jpeg")),
                                            ("full", (CDN + "images/Works/Prestix/PrestixMockupPhone.jpeg")),
                                            ("bleed", (CDN + "images/Works/Wing/WingKVFoto2.jpg")),
                                            ("full", (CDN + "images/Works/Wing/WingMockupPhone.jpeg")),
                                            ("full", (CDN + "images/Works/Wing/WingComputer.jpeg")),
                                            ("pair",  [(CDN + "images/Works/Wing/WingKVFoto.jpg"),
                                                        CDN + "images/Works/Wing/WingMockupPhone2.jpeg"]),
                                            ("sheet",  CDN + "images/Works/Wing/WingIconography.jpeg"),
                                            ("sheet",  CDN + "images/Works/Wing/WingEmbajador.jpeg"),
                                            ("sheet",  CDN + "images/Works/Wing/WingEmbajador2.jpeg"),
                                      
                                        ],
                                        "credits": [("Creative direction", "Supermarket"),
                                                    ("Art direction &amp; design", "Supermarket"),
                                                    ("Content production", "Supermarket")],
                                    },
    "natural-break-arcor": {
                "client": "Arcor",
                "year": "2017",
                "segment": "",
                "services": "Social media strategy, art direction, design, content production",
                "intro": (
                    "Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
                    " quis nostrud exercitation ullamco laboris nisi ut aliqui "
                    "strategy to design and production of Instagram posts, Stories, and Reels, helping "
                    "build an engaging and playful presence for the app across platforms. We developed "
                    "tailored campaigns for key moments in the calendar — including Christmas, King's Day, "
                    "and Carnival — each with its own graphic identity and tone, driving visibility, "
                    "downloads, and fan engagement through festive, high-impact content."),
                "thumb": CDN + "images/Works/ArcorNaturalBreak/ArcorNaturalBreakBanner.png", # <- nueva línea
                "hero": CDN + "images/Works/ArcorNaturalBreak/ArcorNaturalBreakBanner.png",
                "media": [
                    ("full",  CDN + "images/Works/ArcorNaturalBreak/ArcorNaturalBreakKV.png"),
                    ("quote", "One app, three seasons, three graphic identities."),
                    ("full",  CDN + "images/Works/ArcorNaturalBreak/ArcorNaturalBreakKV2.png"),
                    ("pair",  [(CDN + "images/Works/ArcorNaturalBreak/ArcorNaturalBreakKV3.png"),
                               CDN + "images/Works/ArcorNaturalBreak/ArcorNaturalBreakKV4.png"]),
                    ("bleed", (CDN + "images/Works/ArcorNaturalBreak/ArcorNaturalBreakMockupCartelCalle.png")),
                    ("full",  CDN + "images/Works/ArcorNaturalBreak/ArcorNaturalBreakMockupSachetSupermercado.png"),
                    ("full",  CDN + "images/Works/ArcorNaturalBreak/ArcorNaturalBreakGif.gif"),
                    ("bleed", (CDN + "images/Works/ArcorNaturalBreak/ArcorNaturalBreakKV5.png")),
              
                ],
                "credits": [("Creative direction", "Supermarket"),
                            ("Art direction &amp; design", "Supermarket"),
                            ("Content production", "Supermarket")],
            },
    "mr-pops": {
                    "client": "Arcor",
                    "year": "2017",
                    "segment": "",
                    "services": "Social media strategy, art direction, design, content production",
                    "intro": (
                        "Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
                        " quis nostrud exercitation ullamco laboris nisi ut aliqui "
                        "strategy to design and production of Instagram posts, Stories, and Reels, helping "
                        "build an engaging and playful presence for the app across platforms. We developed "
                        "tailored campaigns for key moments in the calendar — including Christmas, King's Day, "
                        "and Carnival — each with its own graphic identity and tone, driving visibility, "
                        "downloads, and fan engagement through festive, high-impact content."),
                    "thumb": CDN + "images/Works/Mr-Pops/MrPopsBanner.jpeg", # <- nueva línea
                    "hero": CDN + "images/Works/Mr-Pops/MrPopsBanner.jpeg",
                    "media": [
                        ("full",  CDN + "images/Works/Mr-Pops/MrPopsKV.jpeg"),
                        ("quote", "One app, three seasons, three graphic identities."),
                        ("full",  CDN + "images/Works/Mr-Pops/MrPopsKV2.jpeg"),
                        ("pair",  [(CDN + "images/Works/Mr-Pops/MrPopsKV3.jpeg"),
                                   CDN + "images/Works/Mr-Pops/MrPopsKV4.jpeg"]),
                        ("bleed", (CDN + "images/Works/Mr-Pops/MrPopsMockupSupermercadoCartel.jpeg")),
                        ("full",  CDN + "images/Works/Mr-Pops/MrPopsKV5.jpeg"),
                        ("full",  CDN + "images/Works/Mr-Pops/MrPopsMockupSupermercadoCaja.jpeg"),
                        ("bleed", (CDN + "images/Works/Mr-Pops/MrPopsMockupSupermercadoVentana.jpeg")),
                  
                    ],
                    "credits": [("Creative direction", "Supermarket"),
                                ("Art direction &amp; design", "Supermarket"),
                                ("Content production", "Supermarket")],
                },  
    "hogarenas": {
                "client": "Arcor",
                "year": "2017",
                "segment": "",
                "services": "Social media strategy, art direction, design, content production",
                "intro": (
                    "Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
                    " quis nostrud exercitation ullamco laboris nisi ut aliqui "
                    "strategy to design and production of Instagram posts, Stories, and Reels, helping "
                    "build an engaging and playful presence for the app across platforms. We developed "
                    "tailored campaigns for key moments in the calendar — including Christmas, King's Day, "
                    "and Carnival — each with its own graphic identity and tone, driving visibility, "
                    "downloads, and fan engagement through festive, high-impact content."),
                "thumb": CDN + "images/Works/Hogarenas/HogarenasBanner.jpeg", # <- nueva línea
                "hero": CDN + "images/Works/Hogarenas/HogarenasBanner.jpeg",
                "media": [
                    ("full",  CDN + "images/Works/Hogarenas/HogarenasLogo.jpeg"),
                    ("quote", "One app, three seasons, three graphic identities."),
                    ("full",  CDN + "images/Works/Hogarenas/HogarenasColectivo.jpeg"),
                    ("pair",  [(CDN + "images/Works/Hogarenas/HogarenasColectivoParada.jpeg"),
                               CDN + "images/Works/Hogarenas/HogarenasKV.jpeg"]),
                    ("bleed", (CDN + "images/Works/Hogarenas/HogarenasCarteleria.jpeg")),
                    ("full",  CDN + "images/Works/Hogarenas/HogarenasBannerKV2.jpeg"),
              
                ],
                "credits": [("Creative direction", "Supermarket"),
                            ("Art direction &amp; design", "Supermarket"),
                            ("Content production", "Supermarket")],
            },
    "levite-limonada": {
                "client": "Villa del Sur",
                "year": "2017",
                "segment": "",
                "services": "Social media strategy, art direction, design, content production",
                "intro": (
                    "Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
                    " quis nostrud exercitation ullamco laboris nisi ut aliqui "
                    "strategy to design and production of Instagram posts, Stories, and Reels, helping "
                    "build an engaging and playful presence for the app across platforms. We developed "
                    "tailored campaigns for key moments in the calendar — including Christmas, King's Day, "
                    "and Carnival — each with its own graphic identity and tone, driving visibility, "
                    "downloads, and fan engagement through festive, high-impact content."),
                "thumb": CDN + "images/Works/Levite-Limonada/LeviteLimonadaBanner.jpeg", # <- nueva línea
                "hero": CDN + "images/Works/Levite-Limonada/LeviteLimonadaBanner.jpeg",
                "media": [
                    ("full",  CDN + "images/Works/Levite-Limonada/LeviteLimonadaKV.png"),
                    ("quote", "One app, three seasons, three graphic identities."),
                    ("full",  CDN + "images/Works/Levite-Limonada/LeviteLimonadaMockupCartel.jpeg"),
                    ("pair",  [(CDN + "images/Works/Levite-Limonada/LeviteLimonadaMockupCartelPlaya.jpeg"),
                               CDN + "images/Works/Levite-Limonada/LeviteLimonadaMockupCartelPlaya2.jpeg"]),
                    ("bleed", (CDN + "images/Works/Levite-Limonada/LeviteLimonadaYoga.jpeg")),
                    ("full",  CDN + "images/Works/Levite-Limonada/LeviteLimonadaMockupCartel2.jpeg"),
                    ("full",  CDN + "images/Works/Levite-Limonada/LeviteLimonadaMockupCartel3.jpeg"),
                    ("bleed", (CDN + "images/Works/Levite-Limonada/LeviteLimonadaKV2.jpeg")),
              
                ],
                "credits": [("Creative direction", "Supermarket"),
                            ("Art direction &amp; design", "Supermarket"),
                            ("Content production", "Supermarket")],
            },
    "natural-one": {
                        "client": "Natural One",
                        "year": "2017",
                        "segment": "",
                        "services": "Social media strategy, art direction, design, content production",
                        "intro": (
                            "Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
                            " quis nostrud exercitation ullamco laboris nisi ut aliqui "
                            "strategy to design and production of Instagram posts, Stories, and Reels, helping "
                            "build an engaging and playful presence for the app across platforms. We developed "
                            "tailored campaigns for key moments in the calendar — including Christmas, King's Day, "
                            "and Carnival — each with its own graphic identity and tone, driving visibility, "
                            "downloads, and fan engagement through festive, high-impact content."),
                        "thumb": CDN + "images/Works/Natural-One/NaturalOneBanner.png", # <- nueva línea
                        "hero": CDN + "images/Works/Natural-One/NaturalOneBanner.png",
                        "media": [
                            ("full",  CDN + "images/Works/Natural-One/NaturalOneTote.png"),
                            ("quote", "One app, three seasons, three graphic identities."),
                            ("full",  CDN + "images/Works/Natural-One/NaturalOneKV.png"),
                            ("pair",  [(CDN + "images/Works/Natural-One/NaturalOneCarrusel.png"),
                                       CDN + "images/Works/Natural-One/NaturalOneMockupCartel.png"]),
                            ("bleed", (CDN + "images/Works/Natural-One/NaturalOneKV2.png")),
                            ("full",  CDN + "images/Works/Natural-One/NaturalOneLogo.png"),

                        ],
                        "credits": [("Creative direction", "Supermarket"),
                                    ("Art direction &amp; design", "Supermarket"),
                                    ("Content production", "Supermarket")],
                    },  
    "swift-grasa": {
                    "client": "Arcor",
                    "year": "2017",
                    "segment": "",
                    "services": "Social media strategy, art direction, design, content production",
                    "intro": (
                        "Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
                        " quis nostrud exercitation ullamco laboris nisi ut aliqui "
                        "strategy to design and production of Instagram posts, Stories, and Reels, helping "
                        "build an engaging and playful presence for the app across platforms. We developed "
                        "tailored campaigns for key moments in the calendar — including Christmas, King's Day, "
                        "and Carnival — each with its own graphic identity and tone, driving visibility, "
                        "downloads, and fan engagement through festive, high-impact content."),
                    "thumb": CDN + "images/Works/Swift-Grasa/SwiftGrasaBanner.jpeg", # <- nueva línea
                    "hero": CDN + "images/Works/Swift-Grasa/SwiftGrasaBanner.jpeg",
                    "media": [
                        ("full",  CDN + "images/Works/Swift-Grasa/SwiftGrasaMockup.jpeg"),
                        ("quote", "One app, three seasons, three graphic identities."),
                        ("full",  CDN + "images/Works/Swift-Grasa/SwiftGrasaMockupSupermercado.jpeg"),
                        ("pair",  [(CDN + "images/Works/Swift-Grasa/SwiftGrasaMockupDelantal.jpeg"),
                                   CDN + "images/Works/Swift-Grasa/SwiftGrasaMockupFacturas.jpeg"]),
                        ("bleed", (CDN + "images/Works/Swift-Grasa/SwiftGrasaBanner.jpeg")),                  
                    ],
                    "credits": [("Creative direction", "Supermarket"),
                                ("Art direction &amp; design", "Supermarket"),
                                ("Content production", "Supermarket")],
                },
    "club-de-la-cerveza": {
                                        "client": "Club de la Cerveza",
                                        "year": "2017",
                                        "segment": "",
                                        "services": "Social media strategy, art direction, design, content production",
                                        "intro": (
                                            "Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
                                            " quis nostrud exercitation ullamco laboris nisi ut aliqui "
                                            "strategy to design and production of Instagram posts, Stories, and Reels, helping "
                                            "build an engaging and playful presence for the app across platforms. We developed "
                                            "tailored campaigns for key moments in the calendar — including Christmas, King's Day, "
                                            "and Carnival — each with its own graphic identity and tone, driving visibility, "
                                            "downloads, and fan engagement through festive, high-impact content."),
                                        "thumb": CDN + "images/Works/ClubDeLaCerveza/ClubDeLaCervezaBanner.jpeg", # <- nueva línea
                                        "hero": CDN + "images/Works/ClubDeLaCerveza/ClubDeLaCervezaBanner.jpeg",
                                        "media": [
                                            ("sheet",  CDN + "images/Works/ClubDeLaCerveza/ClubDeLaCervezaSheet1.jpeg"),
                                            ("sheet",  CDN + "images/Works/ClubDeLaCerveza/ClubDeLaCervezaSheet2.jpeg"),
                                            ("sheet",  CDN + "images/Works/ClubDeLaCerveza/ClubDeLaCervezaSheet3.jpeg"),
                                            ("sheet",  CDN + "images/Works/ClubDeLaCerveza/ClubDeLaCervezaSheet4.jpeg"),
                                            ("sheet",  CDN + "images/Works/ClubDeLaCerveza/ClubDeLaCervezaSheet5.jpeg"),
                                            ("sheet",  CDN + "images/Works/ClubDeLaCerveza/ClubDeLaCervezaSheet6.jpeg"),
                                        ],
                                        "credits": [("Creative direction", "Supermarket"),
                                                    ("Art direction &amp; design", "Supermarket"),
                                                    ("Content production", "Supermarket")],
                                    },
    "deconte": {
                                    "client": "Deconté",
                                    "year": "2017",
                                    "segment": "",
                                    "services": "Social media strategy, art direction, design, content production",
                                    "intro": (
                                        "Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
                                        " quis nostrud exercitation ullamco laboris nisi ut aliqui "
                                        "strategy to design and production of Instagram posts, Stories, and Reels, helping "
                                        "build an engaging and playful presence for the app across platforms. We developed "
                                        "tailored campaigns for key moments in the calendar — including Christmas, King's Day, "
                                        "and Carnival — each with its own graphic identity and tone, driving visibility, "
                                        "downloads, and fan engagement through festive, high-impact content."),
                                    "thumb": CDN + "images/Works/Deconte/DeconteBanner.jpeg", # <- nueva línea
                                    "hero": CDN + "images/Works/Deconte/DeconteBanner.jpeg",
                                    "media": [
                                        ("full",  CDN + "images/Works/Deconte/DeconteCard.jpeg"),
                                        ("quote", "One app, three seasons, three graphic identities."),
                                        ("bleed",  CDN + "images/Works/Deconte/DeconteFloreros.jpeg"),
                                        ("pair",  [(CDN + "images/Works/Deconte/DeconteLetrero.jpeg"),
                                                   CDN + "images/Works/Deconte/DeconteTarjeton.jpeg"]),
                                        ("full",  CDN + "images/Works/Deconte/DecontePackaging.jpeg"),
                                        ("full", (CDN + "images/Works/Deconte/DeconteTazas.jpeg")),
                                        ("bleed",  CDN + "images/Works/Deconte/DeconteDifusor.jpeg"),
                                        ("bleed", (CDN + "images/Works/Deconte/DeconteLogos.jpeg")),
                                        ("full", (CDN + "images/Works/Deconte/DeconteLaptop.jpeg")),
                                        ("full", (CDN + "images/Works/Deconte/DeconteLogo.jpeg")),
                                        ("full",  CDN + "images/Works/Deconte/DeconteExibidores.jpeg"),
                                        ("full",  CDN + "images/Works/Deconte/DeconteTablet.jpeg"),
                                  
                                    ],
                                    "credits": [("Creative direction", "Supermarket"),
                                                ("Art direction &amp; design", "Supermarket"),
                                                ("Content production", "Supermarket")],
                                },
    "rob-ortiz": {
            "client": "Rob Ortiz",
            "year": "2021",
            "segment": "",
            "services": "Social media strategy, art direction, design, content production",
            "intro": (
                "Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
                " quis nostrud exercitation ullamco laboris nisi ut aliqui "
                "strategy to design and production of Instagram posts, Stories, and Reels, helping "
                "build an engaging and playful presence for the app across platforms. We developed "
                "tailored campaigns for key moments in the calendar — including Christmas, King's Day, "
                "and Carnival — each with its own graphic identity and tone, driving visibility, "
                "downloads, and fan engagement through festive, high-impact content."),
            "thumb": CDN + "images/Works/RobOrtiz/RobOrtizBanner.jpeg", # <- nueva línea
            "hero": CDN + "images/Works/RobOrtiz/RobOrtizBanner.jpeg",
            "media": [
                ("full",  CDN + "images/Works/RobOrtiz/RobOrtizComputer.jpeg"),
                ("quote", "One app, three seasons, three graphic identities."),
                ("full",  CDN + "images/Works/RobOrtiz/RobOrtizEstudio.jpeg"),
                ("pair",  [(CDN + "images/Works/RobOrtiz/RobOrtizPhone.jpeg"),
                           CDN + "images/Works/RobOrtiz/RobOrtizGrid.jpeg"]),
                ("bleed", (CDN + "images/Works/RobOrtiz/RobOrtizMockupVarios.jpeg")),
                ("full",  CDN + "images/Works/RobOrtiz/RobOrtizNotebook.jpeg"),
                ("bleed", (CDN + "images/Works/RobOrtiz/RobOrtizVelas.jpeg")),
            ],
            "credits": [("Creative direction", "Supermarket"),
                        ("Art direction &amp; design", "Supermarket"),
                        ("Content production", "Supermarket")],
        },
    "miller": {
                "client": "Miller",
                "year": "2021",
                "segment": "",
                "services": "Social media strategy, art direction, design, content production",
                "intro": (
                    "Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
                    " quis nostrud exercitation ullamco laboris nisi ut aliqui "
                    "strategy to design and production of Instagram posts, Stories, and Reels, helping "
                    "build an engaging and playful presence for the app across platforms. We developed "
                    "tailored campaigns for key moments in the calendar — including Christmas, King's Day, "
                    "and Carnival — each with its own graphic identity and tone, driving visibility, "
                    "downloads, and fan engagement through festive, high-impact content."),
                "thumb": CDN + "images/Works/Miller/MillerBanner.jpeg", # <- nueva línea
                "hero": CDN + "images/Works/Miller/MillerBanner.jpeg",
                "media": [
                    ("full",  CDN + "images/Works/Miller/MillerKV.jpeg"),
                    ("quote", "One app, three seasons, three graphic identities."),
                    ("full",  CDN + "images/Works/Miller/MillerMockupCartelColectivo.jpeg"),
                    ("full",  CDN + "images/Works/Miller/MillerMockupCartel.jpeg"),
                    ("bleed", (CDN + "images/Works/Miller/MillerExhibidor.jpeg")),
                    ("full",  CDN + "images/Works/Miller/MillerMockupCartelSubte.jpeg"),
                ],
                "credits": [("Creative direction", "Supermarket"),
                            ("Art direction &amp; design", "Supermarket"),
                            ("Content production", "Supermarket")],
            },  
    "clave": {
                                    "client": "Clave",
                                    "year": "2017",
                                    "segment": "",
                                    "services": "Social media strategy, art direction, design, content production",
                                    "intro": (
                                        "Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
                                        " quis nostrud exercitation ullamco laboris nisi ut aliqui "
                                        "strategy to design and production of Instagram posts, Stories, and Reels, helping "
                                        "build an engaging and playful presence for the app across platforms. We developed "
                                        "tailored campaigns for key moments in the calendar — including Christmas, King's Day, "
                                        "and Carnival — each with its own graphic identity and tone, driving visibility, "
                                        "downloads, and fan engagement through festive, high-impact content."),
                                    "thumb": CDN + "images/Works/Clave/ClaveBanner.jpeg", # <- nueva línea
                                    "hero": CDN + "images/Works/Clave/ClaveBanner.jpeg",
                                    "media": [
                                        ("full",  CDN + "images/Works/Clave/ClaveKV.jpeg"),
                                        ("quote", "One app, three seasons, three graphic identities."),
                                        ("bleed",  CDN + "images/Works/Clave/ClavePhone.jpeg"),
                                        ("pair",  [(CDN + "images/Works/Clave/ClaveMockupCartel.jpeg"),
                                                   CDN + "images/Works/Clave/ClaveSocialM.jpeg"]),
                                        ("full",  CDN + "images/Works/Clave/ClavePhoneSocialM.jpeg"),
                                        ("full", (CDN + "images/Works/Clave/ClaveLaptopSocialM.jpeg")),
                                        ("bleed",  CDN + "images/Works/Clave/ClaveBleed.jpeg"),
                                        ("full", (CDN + "images/Works/Clave/ClaveMockupCartel2.jpeg")),
                                        ("full", (CDN + "images/Works/Clave/ClaveMockupVerticales.jpeg")),
                                        ("full",  CDN + "images/Works/Clave/ClaveMockupColectivo.jpeg"),
                                  
                                    ],
                                    "credits": [("Creative direction", "Supermarket"),
                                                ("Art direction &amp; design", "Supermarket"),
                                                ("Content production", "Supermarket")],
                                },
    "tigoooool": {
                                        "client": "Tigo",
                                        "year": "2017",
                                        "segment": "",
                                        "services": "Social media strategy, art direction, design, content production",
                                        "intro": (
                                            "Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
                                            " quis nostrud exercitation ullamco laboris nisi ut aliqui "
                                            "strategy to design and production of Instagram posts, Stories, and Reels, helping "
                                            "build an engaging and playful presence for the app across platforms. We developed "
                                            "tailored campaigns for key moments in the calendar — including Christmas, King's Day, "
                                            "and Carnival — each with its own graphic identity and tone, driving visibility, "
                                            "downloads, and fan engagement through festive, high-impact content."),
                                        "thumb": CDN + "images/Works/tigoooool/TigooooolMockupEstadio.jpeg", # <- nueva línea
                                        "hero": CDN + "images/Works/tigoooool/TigooooolMockupEstadio.jpeg",
                                        "media": [
                                            ("full",  CDN + "images/Works/tigoooool/TigooooolMockupCartelSubte.jpeg"),
                                            ("quote", "One app, three seasons, three graphic identities."),
                                            ("full",  CDN + "images/Works/tigoooool/TigooooolGrid.jpeg"),
                                            ("pair",  [(CDN + "images/Works/tigoooool/TigooooolMockupVerticales.jpeg"),
                                                       CDN + "images/Works/tigoooool/TigooooolGrid2.jpeg"]),
                                            ("bleed",  CDN + "images/Works/tigoooool/TigooooolGrid3.jpeg"),
                                            ("full",  CDN + "images/Works/tigoooool/TigooooolMockupEscaleras.jpeg"),
                                            ("full", (CDN + "images/Works/tigoooool/TigooooolMockupVarios.jpeg")),
                                            ("bleed", (CDN + "images/Works/tigoooool/TigooooolMockupVarios2.jpeg")),
                                            ("full", (CDN + "images/Works/tigoooool/TigooooolMockupCarteles.jpeg")),
                                            ("full",  CDN + "images/Works/tigoooool/TigooooolGridVerticales.jpeg"),
                                            ("full",  CDN + "images/Works/tigoooool/TigooooolGrid4.jpeg"),
                                      
                                        ],
                                        "credits": [("Creative direction", "Supermarket"),
                                                    ("Art direction &amp; design", "Supermarket"),
                                                    ("Content production", "Supermarket")],
                                    },
    "gogym": {
                                            "client": "Go Gym",
                                            "year": "2017",
                                            "segment": "",
                                            "services": "Social media strategy, art direction, design, content production",
                                            "intro": (
                                                "Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
                                                " quis nostrud exercitation ullamco laboris nisi ut aliqui "
                                                "strategy to design and production of Instagram posts, Stories, and Reels, helping "
                                                "build an engaging and playful presence for the app across platforms. We developed "
                                                "tailored campaigns for key moments in the calendar — including Christmas, King's Day, "
                                                "and Carnival — each with its own graphic identity and tone, driving visibility, "
                                                "downloads, and fan engagement through festive, high-impact content."),
                                            "thumb": CDN + "images/Works/GoGym/GoGymBanner.jpeg", # <- nueva línea
                                            "hero": CDN + "images/Works/GoGym/GoGymBanner.jpeg",
                                            "media": [
                                                ("full",  CDN + "images/Works/GoGym/GoGymKV.jpeg"),
                                                ("quote", "One app, three seasons, three graphic identities."),
                                                ("full",  CDN + "images/Works/GoGym/GoGymKV2.jpeg"),
                                                ("pair",  [(CDN + "images/Works/GoGym/GoGymKV3.jpeg"),
                                                           CDN + "images/Works/GoGym/GoGymKV4.jpeg"]),
                                                ("bleed",  CDN + "images/Works/GoGym/GoGymVarios.jpeg"),
                                                ("full",  CDN + "images/Works/GoGym/GoGymMockupVertical.jpeg"),
                                                ("full", (CDN + "images/Works/GoGym/GoGymKV5.jpeg")),
                                            ],
                                            "credits": [("Creative direction", "Supermarket"),
                                                        ("Art direction &amp; design", "Supermarket"),
                                                        ("Content production", "Supermarket")],
                                        },
    "arcor-frutas": {
                                                "client": "Go Gym",
                                                "year": "2017",
                                                "segment": "",
                                                "services": "Social media strategy, art direction, design, content production",
                                                "intro": (
                                                    "Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
                                                    " quis nostrud exercitation ullamco laboris nisi ut aliqui "
                                                    "strategy to design and production of Instagram posts, Stories, and Reels, helping "
                                                    "build an engaging and playful presence for the app across platforms. We developed "
                                                    "tailored campaigns for key moments in the calendar — including Christmas, King's Day, "
                                                    "and Carnival — each with its own graphic identity and tone, driving visibility, "
                                                    "downloads, and fan engagement through festive, high-impact content."),
                                                "thumb": CDN + "images/Works/Arcor-Frutas/ArcorFrutasBanner.png", # <- nueva línea
                                                "hero": CDN + "images/Works/Arcor-Frutas/ArcorFrutasBanner.png",
                                                "media": [
                                                    ("full",  CDN + "images/Works/Arcor-Frutas/ArcorFrutasKV.png"),
                                                    ("quote", "One app, three seasons, three graphic identities."),
                                                    ("bleed",  CDN + "images/Works/Arcor-Frutas/ArcorFrutasManzanaDurazno.png"),
                                                    ("pair",  [(CDN + "images/Works/Arcor-Frutas/ArcorFrutasMockupCompotas.png"),
                                                               CDN + "images/Works/Arcor-Frutas/ArcorFrutasMockupBebe.jpeg"]),
                                                    
                                                    ("full",  CDN + "images/Works/Arcor-Frutas/ArcorFrutasCompotaMix.jpeg"),
                                                    ("full", (CDN + "images/Works/Arcor-Frutas/ArcorFrutasKVDurazno.png")),
                                                    ("full", (CDN + "images/Works/Arcor-Frutas/ArcorFrutasGlobos.png")),
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
    thumb = PROJECTS.get(slug, {}).get("thumb") or POOL[i % len(POOL)]
    cards.append(f"""      <a class="card{wide}" href="{WORK_BASE}{slug}.html">
        <div class="card__figure"><img src="{thumb}" alt="{html.escape(name)}" loading="lazy"></div>
        <h3 class="card__name">{name}</h3>
        <p class="meta">View project</p>
      </a>""")

home_body = f"""<section class="hero">
  <video class="hero__media" src="{REEL_MP4}" autoplay muted loop playsinline preload="metadata"
         poster="{IMG['board']}"></video>
  <div class="hero__overlay">
  <div class="hero__overlay-inner">
    <h1 class="hero__line">We are Supermarket. A global force of creativity.</h1>
    <p class="hero__side">Effective, no excuses.<br>Independent since 2009</p>
  </div>
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
        <div class="tile__figure"><img src="{thumb}" alt="{html.escape(name)}" loading="lazy"></div>
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
    (OUT / filename).write_text(page(title, current, body, desc, path=filename), encoding="utf-8")
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
#    ("sheet",  url)              como "full", pero sin separación arriba/abajo:
#                                  encadená varios "sheet" seguidos para que se
#                                  lean como una sola imagen continua
#    ("video",  url)              mp4 propio, autoplay muteado en loop
#    ("embed",  youtube_id)       reproductor de YouTube
#    ("vimeo",  url_o_id)         reproductor de Vimeo
#    ("vimeo",  (url_o_id, "9:16"))  Vimeo con otra proporción (vertical, 1:1, 4:5)
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


def _paragraphs(text):
    """Splits an intro on blank lines and wraps each part in its own <p>.
    A blank line in the source string ("\n\n") marks a new paragraph;
    single line breaks inside a paragraph are treated as normal spaces."""
    parts = [" ".join(part.split()) for part in text.split("\n\n")]
    return "".join(f"<p>{part}</p>" for part in parts if part)


def _path(url, pre=""):
    """Prefixes local asset paths so they resolve from work/<slug>.html."""
    if url.startswith(("http://", "https://", "//", "/", "data:", "#")):
        return url
    return pre + url

def _vimeo_src(payload, background=False):
    """Accepts a Vimeo URL or an id ("123456789", "123456789/abc123def4")
    and returns the player URL, keeping the privacy hash of unlisted videos."""
    m = re.search(r"(\d{6,})(?:/([0-9a-f]+)|\?h=([0-9a-f]+))?", payload)
    if not m:
        raise ValueError(f"Vimeo: no encuentro el ID en {payload!r}")
    vid, h = m.group(1), m.group(2) or m.group(3)
    return (f"https://player.vimeo.com/video/{vid}?" + (f"h={h}&" if h else "") + "dnt=1"
            + ("&background=1" if background else ""))


def _frame_style(ratio, center=False):
    """Inline style for a player frame with a custom ratio such as "9:16".
    Vertical frames are capped at ~85% of the screen height so they fit."""
    try:
        w, h = (float(n) for n in str(ratio).replace("/", ":").split(":"))
    except ValueError:
        raise ValueError(f'Proporción no válida: {ratio!r} (usa por ejemplo "9:16")')
    w, h = f"{w:g}", f"{h:g}"
    style = f"aspect-ratio:{w}/{h}"
    if float(h) > float(w):
        style += f";width:min(100%,calc(85vh*{w}/{h}))"
        if center:
            style += ";margin-inline:auto"
    return f' style="{style}"'

def _fig(item, cls="shot", pre=""):
    url, cap = _split(item)
    url = _path(url, pre)
    figcap = f'<figcaption class="shot__cap">{cap}</figcaption>' if cap else ""
    return (f'<figure class="{cls}"><img src="{url}" alt="" loading="lazy">'
            f'{figcap}</figure>')


def module_html(kind, payload, pre=""):
    if kind == "bleed":
        return f'  {_fig(payload, "shot shot--bleed", pre)}'
    if kind == "full":
        return f'  <div class="wrap">{_fig(payload, pre=pre)}</div>'
    if kind == "sheet":
        return f'  <div class="wrap wrap--sheet">{_fig(payload, "shot shot--sheet", pre)}</div>'
    if kind in ("pair", "trio"):
        cells = "".join(_fig(i, pre=pre) for i in payload)
        return f'  <div class="wrap"><div class="shots shots--{kind}">{cells}</div></div>'
    if kind == "video":
        return (f'  <div class="wrap"><video class="shot shot--video" src="{_path(payload, pre)}" '
                f'autoplay muted loop playsinline preload="metadata"></video></div>')
    if kind == "embed":
        return (f'  <div class="wrap"><div class="reel__frame">'
                f'<iframe src="https://www.youtube.com/embed/{payload}?rel=0" title="Project video" '
                f'allow="encrypted-media; picture-in-picture" allowfullscreen loading="lazy">'
                f'</iframe></div></div>')
    if kind == "vimeo":
        url, ratio = payload if isinstance(payload, (tuple, list)) else (payload, None)
        style = _frame_style(ratio) if ratio else ""
        return (f'  <div class="wrap"><div class="reel__frame"{style}>'
                f'<iframe src="{_vimeo_src(url)}" title="Project video" '
                f'allow="autoplay; fullscreen; picture-in-picture" allowfullscreen loading="lazy">'
                f'</iframe></div></div>')
    if kind == "vimeo_full":
        url, ratio = payload if isinstance(payload, (tuple, list)) else (payload, None)
        style = _frame_style(ratio, center=True) if ratio else ""
        return (f'  <div class="reel__frame"{style}>'
                f'<iframe src="{_vimeo_src(url, background=True)}" title="Project video" '
                f'allow="autoplay; fullscreen; picture-in-picture" loading="lazy">'
                f'</iframe></div>')
    if kind == "quote":
        return f'  <div class="wrap"><p class="work__quote">{payload}</p></div>'
    return ""


def project_page(i):
    pre = "../"                      # las fichas viven en work/
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

    intro = (f'<div class="work__intro">{_paragraphs(d["intro"])}</div>'
             if d.get("intro") else
             '<!-- Intro pending: add "intro" in PROJECTS -->')

    hero = _path(d.get("hero") or POOL[i % len(POOL)], pre)
    hero_client = d.get("client") or client_for(name)
    hero_alt = html.escape(f"{name} — {hero_client}" if hero_client else name)

    if d.get("media"):
        media = "\n".join(module_html(k, v, pre) for k, v in d["media"])
    else:
        media = ("  <!-- Placeholder gallery: add \"media\" in PROJECTS. Módulos:\n"
                 "       bleed · full · pair · trio · sheet · video · embed · vimeo · quote -->\n"
                 + "\n".join(module_html(k, v, pre) for k, v in [
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

  <figure class="work__hero"><img src="{hero}" alt="{hero_alt}" fetchpriority="high"></figure>

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
                d.get("intro", "")[:150] or f"{name} — a Supermarket project.", pre=pre,
                path=f"work/{slug}.html", image=d.get("hero"))


workdir = OUT / "work"
workdir.mkdir(exist_ok=True)
for i in range(len(WORKS)):
    (workdir / (WORKS[i][1] + ".html")).write_text(project_page(i), encoding="utf-8")
print("wrote", len(WORKS), "project pages")

# ------------------------------------------------------------- SEO: sitemap + robots
all_paths = [filename for filename, *_ in PAGES] + [f"work/{slug}.html" for _, slug in WORKS]

urls = "\n".join(
    f"  <url><loc>{DOMAIN}/{p}</loc></url>" for p in all_paths
)
sitemap = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{urls}
</urlset>
"""
(OUT / "sitemap.xml").write_text(sitemap, encoding="utf-8")
print("wrote sitemap.xml —", len(all_paths), "urls")

robots = f"""User-agent: *
Allow: /

Sitemap: {DOMAIN}/sitemap.xml
"""
(OUT / "robots.txt").write_text(robots, encoding="utf-8")
print("wrote robots.txt")
