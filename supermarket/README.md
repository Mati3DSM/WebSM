# Supermarket — rediseño 2026

Seis páginas estáticas (HTML + CSS + JS sin dependencias) más 60 fichas de proyecto.
Mismas secciones y el mismo contenido del sitio actual; cambia el sistema visual.

```
index.html      Home        reel de portada + statement + last works
services.html   Services    intro + 4 bloques de servicio
works.html      Works       índice completo de 60 proyectos con preview al hover
about.html      About       mosaico, cifras, manifiesto, IA, categorías, marquee, equipo
reel.html       Reels       dos embeds de YouTube
contact.html    Contact     formulario + foto
work/<slug>.html            ficha de proyecto (60 páginas, una plantilla)
sitemap.xml     robots.txt  generados automáticamente por el build
assets/styles.css
assets/main.js
build.py        genera todo lo anterior (editá acá y volvé a correr el build)
```

## Cómo generar el sitio

Todo el contenido vive en `build.py`. Los archivos de arriba son su **salida**: no se
editan a mano, porque el próximo build los pisa.

```
python3 build.py
```

Regenera las 6 páginas, las 60 fichas, `sitemap.xml` y `robots.txt`. Repetir cada vez
que se edite `build.py`; los cambios en `styles.css` o `main.js` no lo necesitan.

## Estado actual (para quien se sume ahora)

La estructura de las 60 fichas está completa: todos los proyectos en `PROJECTS`
tienen `thumb`, `hero`, `media` y `credits` cargados. Lo que falta es contenido:

- **Textos de intro.** Es lo más urgente. Hoy, de las 60 fichas: 37 tienen el texto
  de Barça Games copiado (mencionan "FC Barcelona" o "Barça Games" aunque el
  proyecto sea otro), 22 tienen relleno `Lorem ipsum`, y solo `swift-picante` tiene
  texto propio. Ese campo es también la meta description de la página, así que
  mientras no se reemplace, la mayoría de las fichas comparten texto entre sí — mal
  para SEO además de para el contenido. Repartir esos 59 slugs es la tarea principal
  pendiente.
- **Formulario de contacto.** `main.js` valida y muestra los estados de éxito y
  error, pero el `action` está vacío. Conectarlo a Formspree o a un endpoint propio.
- **Fuente.** Se carga desde Google Fonts. Para producción conviene self-hostear
  el `.woff2` variable de Archivo.
- **Video de portada.** Autoplay muteado, sin variante liviana para mobile. Vale
  la pena servir una versión de ~1500px de ancho con `<source media>`.
- **`DOMAIN`, al principio de `build.py`.** Se usa para `canonical`, Open Graph,
  `sitemap.xml` y `robots.txt`. Ya apunta a `wearesupermarket.com`; conviene
  revisarlo una vez más antes de publicar.

## Sistema

**Color.** Papel gris frío `#EFEFED`, tinta negra pura, línea `#C7C7C1`, negro para
las bandas oscuras y un único rojo de señalética `#E0122B` usado con cuentagotas
(punto del logotipo, página activa, hover del botón, una franja del marquee).
Todo vive en `:root` de `styles.css`: cambiando `--accent` cambia el sitio entero.

**Tipografía.** Una sola familia, Archivo variable, explotando el eje de ancho:
los titulares van en `wdth 108–118` y peso 600; el texto en ancho normal y peso 400.
Un solo tipo en muchos anchos da unidad sin decorar.

**Composición.** Todo alineado a la izquierda, bandera derecha. Grilla asimétrica:
titular grande a la izquierda, dato o bajada a la derecha. Nada centrado.

**Movimiento.** Un solo momento: la entrada del titular sobre el reel en Home.
El resto responde al usuario (hover, apertura del menú). `prefers-reduced-motion`
está respetado en todo el sitio.

## La ficha de proyecto

Una sola plantilla, `work/<slug>.html`, generada para los 60 proyectos a partir de
su entrada en el diccionario `PROJECTS`. Cargar un proyecto nuevo es agregar ahí una
clave con el mismo slug que tiene en `WORKS`.

Campos de cada proyecto:

| Campo      | Dónde aparece                                                            |
|------------|---------------------------------------------------------------------------|
| (nombre)   | Titular grande; sale de la tupla en `WORKS`                               |
| `client`   | Rail de datos, a la derecha del titular                                   |
| `year`     | Rail de datos                                                             |
| `segment`  | Rail de datos                                                             |
| `services` | Rail de datos                                                             |
| `intro`    | Bloque de texto único, debajo del hero (y meta description de la página)  |
| `hero`     | Imagen a sangre completa, 16:9                                            |
| `thumb`    | Miniatura 4:3 en Works (grilla y preview del índice)                      |
| `media`    | Galería: secuencia de módulos                                             |
| `credits`  | Bloque de créditos al final                                               |

Los campos vacíos no imprimen su etiqueta: si `year` o `segment` están vacíos, esa
fila del rail directamente no se dibuja.

### Vocabulario de módulos

La galería no es una lista plana de imágenes: es una secuencia de módulos. Cargar un
proyecto es elegir el ritmo. En `build.py`, dentro de `PROJECTS[slug]["media"]`:

| Módulo        | Qué hace                                                                | Cuándo usarlo |
|---------------|---------------------------------------------------------------------------|---------------|
| `bleed`       | pieza a sangre, de borde a borde de pantalla                              | el remate de cada capítulo del caso |
| `full`        | pieza al ancho de la grilla                                                | la pieza principal de una tanda |
| `pair`        | dos piezas en fila                                                        | variantes, antes/después, dos formatos |
| `trio`        | tres piezas en fila                                                       | familias de posts, sistema de packaging |
| `sheet`       | pieza suelta, sin recorte, en su propio contenedor                        | piezas sueltas que no encajan en los anteriores |
| `video`       | mp4 propio, autoplay muteado en loop                                      | loops cortos, motion |
| `embed`       | reproductor de YouTube                                                    | el film completo, con audio |
| `vimeo`       | reproductor de Vimeo (URL o ID)                                           | el film completo, si lo alojan en Vimeo |
| `vimeo_full`  | Vimeo a sangre, sin controles, autoplay, loop y mudo (plan de pago)       | loops de motion o piezas de portada |
| `quote`       | una frase grande, sin imagen                                              | la idea del caso, una sola vez |

Tanto `vimeo` como `vimeo_full` aceptan una proporción distinta a 16:9 pasando una
tupla en vez de la URL: `("vimeo_full", (url, "9:16"))`, para videos verticales.

Cualquier módulo de imagen acepta pie de foto pasando una tupla en lugar de la URL:
`("bleed", (url, "King's Day"))`. El pie va debajo, en gris chico.

La regla de ritmo: nunca dos `bleed` seguidos, y el `quote` una sola vez por caso,
temprano, antes de que el scroll se vuelva galería. Si un caso necesita dos frases,
probablemente sean dos casos.

Las piezas de la galería **no se recortan**: cada imagen conserva su proporción
original y el gris solo se ve mientras carga. Es la decisión más importante de la
ficha — una agencia no debería cropear su propio trabajo para que entre en una grilla.

Al final va el bloque **Credits**, con el mismo rail de hairlines del encabezado.
No se dibuja si el proyecto no tiene `credits`.

## SEO

Cada página lleva `<link rel="canonical">`, Open Graph y Twitter Card, armados en
la función `page()` a partir de `DOMAIN`, del título y de la `intro` del proyecto
(o de la descripción fija de cada página principal). Las fichas usan su `hero` como
imagen para compartir; las páginas principales usan `DEFAULT_OG_IMAGE`.

`sitemap.xml` y `robots.txt` se generan solos al final del build, a partir de
`PAGES` y `WORKS`, así que nunca quedan desincronizados de las páginas reales.

## Works: dos vistas

La página tiene un switch **Grid / Index** arriba a la derecha. Grid es la vista por
defecto: thumbnail 4:3, nombre debajo, tres columnas. Index es la lista tipográfica
con preview flotante al hover. En mobile el preview se desactiva.

Los thumbnails salen del campo `thumb` de cada proyecto en `PROJECTS`; mientras un
proyecto no lo tenga, usa el `POOL` de imágenes de respaldo (hoy los 60 ya lo
tienen cargado).

## Decisiones de diseño que conviene conocer

- **Works como índice, no como grilla pura.** La vista Index existe porque 60
  proyectos en miniaturas obligan a 60 imágenes parejas; como lista tipográfica con
  preview al hover, el peso lo lleva el nombre del cliente. Grid queda como vista
  por defecto ahora que las imágenes están cargadas.
- **Mayúsculas a caja alta y baja.** Los títulos y nombres de proyecto van en caja
  alta y baja ("Effective, no excuses.", no "EFFECTIVE, NO EXCUSES."). Es solo
  tratamiento tipográfico.
- **Un solo acento.** El rojo aparece en cinco lugares en todo el sitio (punto del
  logotipo, página activa, hover del botón, una franja del marquee). Si se pone en
  más lugares, deja de leerse como señal.
