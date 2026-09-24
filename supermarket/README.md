# Supermarket — rediseño 2026

Seis páginas estáticas (HTML + CSS + JS sin dependencias). Mismas secciones y el mismo
contenido del sitio actual; cambia el sistema visual.

```
index.html      Home        reel de portada + statement + last works
services.html   Services    intro + 4 bloques de servicio
works.html      Works       índice completo de 60 proyectos con preview al hover
about.html      About       mosaico, cifras, manifiesto, IA, categorías, marquee, equipo
reel.html       Reels       dos embeds de YouTube
contact.html    Contact     formulario + foto
work/<slug>.html            ficha de proyecto (60 páginas, una plantilla)
assets/styles.css
assets/main.js
build.py        genera los seis HTML (editá acá y volvé a correr `python3 build.py`)
```

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

## Decisiones que conviene revisar

- **Works como índice, no como grilla.** 60 proyectos en miniaturas obligan a
  60 imágenes parejas; como lista tipográfica con preview al hover, el peso lo
  lleva el nombre del cliente y la página carga instantáneo. En mobile el preview
  se desactiva.
- **Mayúsculas a caja alta y baja.** "EFFECTIVE, NO EXCUSES." pasó a
  "Effective, no excuses."; los nombres de proyecto también. Es solo tratamiento
  tipográfico, el texto es el mismo.
- **Un solo acento.** El rojo aparece en cinco lugares en todo el sitio. Si lo
  ponés en más, deja de leerse como señal.

## Works: dos vistas

La página tiene un switch **Grid / Index** arriba a la derecha. Grid es la vista por
defecto: thumbnail 4:3, nombre debajo, tres columnas. Index es la lista tipográfica
con preview flotante al hover.

Los thumbnails salen del campo `thumb` de cada proyecto en `PROJECTS`; mientras no
esté cargado usan el pool de placeholders, que es por qué hoy se repiten. Es el único
dato que falta para que la página quede terminada.

## La ficha de proyecto

Una sola plantilla, `work/<slug>.html`, generada para los 60 proyectos.
**Barça Games Social Media está cargado con su contenido real**: sirve de referencia
de cómo se ve la plantilla llena. Los otros 59 tienen la misma estructura esperando
los campos del CMS.

### Vocabulario de módulos

La galería no es una lista plana de imágenes: es una secuencia de módulos. Cargar un
proyecto es elegir el ritmo. En `build.py`, dentro de `PROJECTS[slug]["media"]`:

| Módulo   | Qué hace                                        | Cuándo usarlo |
|----------|-------------------------------------------------|---------------|
| `bleed`  | pieza a sangre, de borde a borde de pantalla     | el remate de cada capítulo del caso |
| `full`   | pieza al ancho de la grilla                      | la pieza principal de una tanda |
| `pair`   | dos piezas en fila                               | variantes, antes/después, dos formatos |
| `trio`   | tres piezas en fila                              | familias de posts, sistema de packaging |
| `video`  | mp4 propio, autoplay muteado en loop             | loops cortos, motion |
| `embed`  | reproductor de YouTube                           | el film completo, con audio |
| `quote`  | una frase grande, sin imagen                     | la idea del caso, una sola vez |

Cualquier módulo de imagen acepta pie de foto pasando una tupla en lugar de la URL:
`("bleed", (url, "King's Day"))`. El pie va debajo, en gris chico.

La regla de ritmo que usé en Barça: nunca dos `bleed` seguidos, y el `quote` una sola
vez por caso, temprano, antes de que el scroll se vuelva galería. Si un caso necesita
dos frases, probablemente sean dos casos.

Al final va el bloque **Credits**, con el mismo rail de hairlines del encabezado.

Mapeo con tu colección de Webflow:

| Campo CMS   | Dónde aparece                                       |
|-------------|-----------------------------------------------------|
| Name        | Titular grande                                       |
| Client      | Rail de datos, a la derecha del titular              |
| Year        | Rail de datos                                        |
| Segment     | Rail de datos                                        |
| Services    | Rail de datos                                        |
| Description | Bloque de texto único, debajo del hero               |
| Hero        | Imagen a sangre completa, 16:9                       |
| Gallery     | Stream de piezas: alterna ancho completo y pares     |

Cuatro cosas que estaban rotas en las fichas actuales y acá quedaron resueltas:

1. **La descripción aparecía dos veces** — arriba y otra vez dentro del bloque
   "Services". Ahora va una sola vez.
2. **Campos vacíos que igual imprimían su etiqueta** (Year, Segment sin valor).
   La plantilla no dibuja la fila si el campo está vacío.
3. **"Next Project" apuntaba a `#`.** Ahora hay anterior y siguiente reales,
   calculados sobre el orden del índice, y el último vuelve al primero.
4. **"No items found."** del listado de relacionados. Reemplazado por esa
   navegación anterior/siguiente, que hace el mismo trabajo sin depender de que
   cargues un campo de relación por proyecto.

Las piezas de la galería **no se recortan**: cada imagen conserva su proporción
original y el gris solo se ve mientras carga. Es la decisión más importante de la
ficha — una agencia no debería cropear su propio trabajo para que entre en una grilla.

## Para poner en producción

1. **Imágenes de trabajos.** Los thumbnails de Home y los previews del índice usan
   imágenes tuyas ya existentes como placeholder. En `build.py`, la lista `POOL`
   y las tuplas de `WORKS` son el único lugar a tocar; en el HTML, cada fila del
   índice lleva su `data-img`.
2. **Links de proyecto.** Van a `work/<slug>.html` con los slugs reales de tu
   Webflow, así que la migración es directa. Para volver a apuntar al sitio vivo,
   cambiá `WORK_BASE` por `LIVE_BASE` en `build.py`.
   El contenido de cada ficha se carga en el diccionario `PROJECTS`.
3. **Formulario.** `main.js` valida y muestra los estados de éxito y error; el
   `action` está vacío. Apuntalo a Formspree, a tu endpoint o al form de Webflow.
4. **Fuente.** Se carga desde Google Fonts. Para producción conviene
   self-hostear el .woff2 variable de Archivo.
5. **Video de portada.** Autoplay muteado con `poster`. Pesa: vale la pena servir
   una versión de ~1500px de ancho para mobile con `<source media>`.
