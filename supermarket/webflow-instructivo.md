# Subir el rediseño a Webflow

Guía de implementación. El código estático que armamos es la especificación:
define tokens, clases, estructura y comportamiento. Webflow es donde eso se
vuelve un sitio editable por el equipo.

---

## Antes de tocar nada: elegí la ruta

**Ruta A — Reconstruir en el Designer.** Recomendada. Usás el código como
espec y rearmás las páginas con elementos nativos. Conservás CMS, Editor,
hosting, formularios y SEO de Webflow. Es la única ruta en la que tu equipo
puede seguir cargando proyectos sin tocar código. Es lo que detalla esta guía.

**Ruta B — Hosting externo.** Subís la carpeta tal cual a Netlify, Vercel o
Cloudflare Pages y apuntás el dominio ahí. Toma diez minutos y el sitio queda
idéntico al preview. El costo es real: te quedás sin CMS y sin Editor, y cada
proyecto nuevo se carga editando `build.py`. Solo tiene sentido si el sitio lo
mantenés vos.

**Ruta C — Pegar todo en Code Embeds.** No. Rompe el CMS, no es editable, no
es responsive desde el Designer y choca contra los límites de caracteres.

---

## 0. Backup

Duplicá el proyecto actual y trabajá sobre la copia. Todo lo que sigue se hace
en el duplicado; producción no se toca hasta el final.

---

## 1. Variables (design tokens)

En el Designer, panel **Variables**. Creá tres colecciones y cargá los valores
del `:root` de `styles.css`. Estas son las que hay que crear:

**Color**

| Variable   | Valor     | Uso |
|------------|-----------|-----|
| Paper      | `#EFEFED` | fondo general |
| Paper pure | `#F8F8F7` | fondo del marquee, texto sobre negro |
| Ink        | `#000000` | tipografía |
| Ink soft   | `#6D6D6A` | metadatos, pies de foto |
| Line       | `#C7C7C1` | hairlines y placeholder de imagen |
| Dark       | `#000000` | hero y footer |
| Accent     | `#E0122B` | punto del logo, página activa, hover |

**Typography** — familia, y los tamaños del type scale (display, xl, lg, md,
body, sm). Ojo: mis tamaños usan `clamp()`, que Webflow no expone en el panel.
Ver el punto 3.

**Layout** — Pad (64px), Gutter (24px), Max width (1560px), Header height (68px).

---

## 2. La tipografía

Archivo es variable y el diseño usa **el eje de ancho** (`wdth`), no solo el
peso: los titulares van en 108–118 de ancho. Ese eje es la mitad de la
personalidad del sitio.

El conector de Google Fonts de Webflow normalmente expone pesos, no anchos. Dos
caminos:

1. **Subir la fuente variable.** Site settings → Fonts → Custom fonts, subí el
   `.woff2` variable de Archivo. Después, en Site settings → Custom code →
   Head, agregá las clases de ancho:

   ```html
   <style>
     .display, .footer-cta { font-variation-settings: "wdth" 114, "wght" 600; }
     .title  { font-variation-settings: "wdth" 108, "wght" 600; }
     .tile-name, .index-name { font-variation-settings: "wdth" 106, "wght" 500; }
   </style>
   ```

2. **Plan B sin código:** usar *Archivo Expanded* como familia separada para
   titulares y *Archivo* para texto. Se pierde la transición fina de ancho en el
   hover del índice, pero el resto se sostiene.

---

## 3. Los tamaños fluidos

El type scale usa `clamp(mín, vw, máx)` para que el titular respire en mobile
sin achicarse de golpe. En Webflow tenés dos opciones:

- **Nativa:** definir el tamaño por breakpoint (Desktop / Tablet / Mobile
  landscape / Mobile portrait). Es más trabajo y los saltos se notan.
- **Con código:** pegar los `clamp()` en Site settings → Head, dentro de un
  `<style>`, usando las clases que vayas creando. Es una sola vez y queda
  idéntico al preview.

Recomiendo la segunda. Copiá el bloque `:root` completo de `styles.css` y
después las reglas de `.display`, `.title`, `.subtitle`, `.lede` y `.meta`.

---

## 4. Componentes globales

Convertí en **Components** (antes Symbols):

- **Navbar** — logotipo con el punto rojo, seis links, botón Menu en mobile.
  El estado de página activa lo maneja Webflow solo con "Current" en el link.
- **Footer** — "Let's work together", las tres oficinas con sus mails,
  Instagram, LinkedIn, hello@, la línea de derechos.

Se arman una vez y se insertan en las siete plantillas.

---

## 5. La colección CMS "Works"

Ya existe. Revisá que tenga estos campos, con estos tipos:

| Campo        | Tipo             | Dónde aparece |
|--------------|------------------|---------------|
| Name         | Plain text       | titular de la ficha, nombre en grilla e índice |
| Slug         | Slug             | URL — **no lo cambies**, ver punto 10 |
| Thumbnail    | Image            | grilla de Works y preview del índice |
| Hero         | Image            | imagen a sangre de la ficha |
| Client       | Plain text       | rail de datos |
| Year         | Plain text       | rail de datos |
| Segment      | Plain text       | rail de datos |
| Services     | Plain text       | rail de datos |
| Description  | Rich text        | bloque de texto de la ficha |
| Quote        | Plain text       | módulo de frase grande (opcional) |
| Featured     | Switch           | filtra los cinco de Home |
| Order        | Number           | orden del índice |

**Thumbnail es el campo que hoy falta.** Sin eso, ni la grilla ni el índice
tienen imagen. Es lo primero que hay que cargar.

---

## 6. La galería de cada proyecto

Acá está la decisión de arquitectura. El diseño usa siete módulos con distinto
ancho (`bleed`, `full`, `pair`, `trio`, `video`, `embed`, `quote`) y un campo
multi-imagen de Webflow no puede expresar ese ritmo: te da todas las piezas
iguales.

**Opción simple.** Campo *Multi-image* + Collection List con un ritmo fijo
(por ejemplo: primera a ancho completo, después pares). Se carga rápido, todos
los casos se ven igual.

**Opción correcta.** Una segunda colección, **Project modules**, con:

- `Reference` → Works (a qué proyecto pertenece)
- `Type` → Option: bleed / full / pair / trio / video / embed / quote
- `Image 1`, `Image 2`, `Image 3` → Image
- `Caption` → Plain text
- `Order` → Number

En la plantilla de proyecto ponés un **Collection List de Project modules
filtrado por "Reference = Current Works"**, ordenado por Order, y le das
condiciones de visibilidad por `Type`: un bloque distinto para cada módulo, y
solo se muestra el que corresponde. Con eso cada caso arma su propio ritmo
desde el Editor, sin tocar el Designer.

Es más setup inicial y es lo que hace que las 60 fichas no se vean iguales.

---

## 7. La página Works, con sus dos vistas

Dos Collection Lists sobre la misma colección, una arriba de la otra:

- **Grid** — 3 columnas, ítem = imagen 4:3 + nombre debajo.
- **Index** — filas con hairline, ítem = nombre grande + "View project".

El switch lo maneja este código. Va en Page settings → Before `</body>`, y los
botones necesitan el atributo `data-view` con valor `grid` o `index`, y el
contenedor de las dos listas el id `works`:

```html
<script>
  var box = document.getElementById('works');
  var btns = document.querySelectorAll('.views__btn');
  btns.forEach(function (btn) {
    btn.addEventListener('click', function () {
      box.setAttribute('data-current', btn.getAttribute('data-view'));
      btns.forEach(function (b) {
        b.setAttribute('aria-pressed', String(b === btn));
      });
    });
  });
</script>
<style>
  #works[data-current="grid"] .index,
  #works[data-current="index"] .tiles { display: none; }
</style>
```

El preview flotante que sigue al cursor en la vista índice está en
`assets/main.js`. Se pega igual, en Before `</body>`. Cada fila necesita el
atributo `data-img` cargado con la URL del thumbnail: se hace con un **custom
attribute** en el link del Collection Item, tomando el valor del campo Thumbnail.

---

## 8. La plantilla de proyecto

Es la Collection Page de Works. El orden: back link → titular → rail de datos a
la derecha → hero a sangre → texto → módulos → credits → anterior/siguiente.

**Anterior / siguiente no existe nativo en Webflow.** Se resuelve con un
Collection List oculto que trae todos los proyectos ordenados por Order, y un
script que busca el proyecto actual y arma los dos links. Es la única parte de
la ficha que necesita código sí o sí. Si preferís evitarlo, la alternativa es
reemplazar ese bloque por "More works": un Collection List de cuatro proyectos
al azar, que es nativo y se arma en dos minutos.

---

## 9. Dónde va el código y cuánto entra

Webflow tiene tres lugares para código, todos con **límite de 50.000
caracteres**: Site settings, Page settings y el elemento **Code Embed**. El
elemento Code Embed acepta HTML, CSS en `<style>` y JS en `<script>`, y
requiere un Workspace Core, Growth, Agency o Freelancer, o que el sitio tenga un Site plan activo.

Repartilo así:

- **Site settings → Head:** las variables `:root`, los `clamp()` del type scale
  y las reglas de `font-variation-settings`. Es lo que afecta todo el sitio.
- **Page settings → Before `</body>`:** el switch de vistas (Works), el preview
  flotante (Works) y el anterior/siguiente (plantilla de proyecto).
- **Code Embed:** nada, si podés evitarlo.

Importante: el código de Page y Site settings **no se ve en el canvas del
Designer**. Publicá al staging `.webflow.io` para probarlo.

---

## 10. Slugs y SEO

Los slugs del código son los mismos que los de tu Webflow actual
(`swift-picante`, `tigo-rebranding`, `facebank`…). Si no los cambiás, **no
necesitás ninguna redirección** y no perdés posicionamiento. Si cambiás alguno,
cargá el 301 en Site settings → Publishing → 301 redirects, uno por slug viejo.

Cargá también el meta title y la meta description de cada página, y en la
plantilla de proyecto atalos a los campos: title = Name, description = los
primeros 150 caracteres de Description.

---

## 11. Responsive

Los cortes del diseño, para que los reproduzcas en los breakpoints de Webflow:

| Ancho    | Qué cambia |
|----------|------------|
| 1000px   | el rail de datos deja de ir al lado del titular y pasa abajo |
| 900px    | los bloques de Services pasan de tres columnas a una |
| 860px    | el menú se vuelve hamburguesa; se desactiva el preview flotante |
| 720px    | los módulos `pair` y `trio` se apilan |
| 560px    | la grilla de Works pasa a una columna |

---

## 12. Checklist antes de publicar

- Los 60 thumbnails cargados y coincidiendo con su proyecto.
- Anterior/siguiente funcionando en las fichas, incluida la última.
- El formulario de Contact enviando y mostrando los dos estados.
- Menú mobile: abre, cierra, y cierra con Escape.
- Foco visible al navegar con Tab (el outline rojo).
- El video del hero: que arranque muteado y no pese de más en mobile.
- Favicon, imagen de Open Graph y `alt` en las imágenes de trabajos.
- Página 404 con el mismo header y footer.
- Probar en staging `.webflow.io` antes de tocar el dominio.

---

## Orden sugerido de trabajo

1. Duplicar el proyecto y cargar variables y tipografía.
2. Armar una página Style Guide con los seis niveles de tipografía, el botón,
   el rail y los hairlines. Todo lo demás se construye con esas clases.
3. Navbar y Footer como componentes.
4. Home y Contact — son las más simples y validan el sistema.
5. Services, About, Reels.
6. Colección Project modules y plantilla de proyecto, con un solo caso cargado
   (Barça Games sirve de referencia, ya tiene el contenido real).
7. Works con las dos vistas.
8. Cargar los 59 proyectos restantes.
9. QA, staging, publicar.

Los pasos 1 a 5 son un par de días de un buen webflower. El 6 es el que define
si el sitio envejece bien: si sale la colección de módulos, cargar un caso nuevo
en dos años sigue siendo media hora de Editor y ningún ticket al desarrollador.
