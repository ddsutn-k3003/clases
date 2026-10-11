---
theme: none
addons:
  - slidev-addon-ddsi
title: X00 - Prueba de tipografías
info: |
  Diseño de Sistemas de Información - K3003 - UTN FRBA
canvasWidth: 1280
aspectRatio: 16/9
transition: fade
layout: cover
---

<div class="kicker">Prueba de diseño</div>

# Tipografías

<div class="sub">Cinco combinaciones para comparar proyectadas en el aula</div>

---

# Qué mirar

<div class="cards c3">
  <div class="card"><span class="big">Distancia</span>¿Se lee desde el fondo del aula?</div>
  <div class="card"><span class="big">Confusiones</span>0 y O, 1 y l, rn y m</div>
  <div class="card"><span class="big">Carácter</span>¿Resulta formal sin ser pesada?</div>
</div>

<p class="lead" style="margin-top:30px">Se muestra la misma diapositiva con cada combinación. Anotar cuál conviene.</p>

---
class: tipo1
---

<div class="nombre">Source Serif 4 + Source Sans 3</div>

# Diagrama de clases

<div class="muestra">
<div>
  <UmlCanvas :w="560" :h="180">
    <ClassBox x="0" y="10" :w="220" compact name="Cliente" />
    <ClassBox x="340" y="10" :w="220" compact name="Pedido" />
    <Rel from="Cliente" to="Pedido" fm="1" tm="*" />
  </UmlCanvas>
  <p class="legib">Títulos con serifa de lectura; cuerpo humanista.</p>
  <p class="legib">Ñandú, ¿qué pasó? 0O 1lI rn m — Pedido#1024</p>
</div>
<pre>public class Pedido {
  private Cliente cliente;
  private List&lt;Linea&gt; lineas;
  public double total() {
    return lineas.stream()
      .mapToDouble(Linea::subtotal)
      .sum();
  }
}</pre>
</div>

---
class: tipo2
---

<div class="nombre">Fraunces + Inter</div>

# Diagrama de clases

<div class="muestra">
<div>
  <UmlCanvas :w="560" :h="180">
    <ClassBox x="0" y="10" :w="220" compact name="Cliente" />
    <ClassBox x="340" y="10" :w="220" compact name="Pedido" />
    <Rel from="Cliente" to="Pedido" fm="1" tm="*" />
  </UmlCanvas>
  <p class="legib">Serifa de contraste suave; cuerpo neutro de pantalla.</p>
  <p class="legib">Ñandú, ¿qué pasó? 0O 1lI rn m — Pedido#1024</p>
</div>
<pre>public class Pedido {
  private Cliente cliente;
  private List&lt;Linea&gt; lineas;
  public double total() {
    return lineas.stream()
      .mapToDouble(Linea::subtotal)
      .sum();
  }
}</pre>
</div>

---
class: tipo3
---

<div class="nombre">Libre Franklin</div>

# Diagrama de clases

<div class="muestra">
<div>
  <UmlCanvas :w="560" :h="180">
    <ClassBox x="0" y="10" :w="220" compact name="Cliente" />
    <ClassBox x="340" y="10" :w="220" compact name="Pedido" />
    <Rel from="Cliente" to="Pedido" fm="1" tm="*" />
  </UmlCanvas>
  <p class="legib">Grotesca clásica, sobria y formal.</p>
  <p class="legib">Ñandú, ¿qué pasó? 0O 1lI rn m — Pedido#1024</p>
</div>
<pre>public class Pedido {
  private Cliente cliente;
  private List&lt;Linea&gt; lineas;
  public double total() {
    return lineas.stream()
      .mapToDouble(Linea::subtotal)
      .sum();
  }
}</pre>
</div>

---
class: tipo4
---

<div class="nombre">IBM Plex Serif + IBM Plex Sans</div>

# Diagrama de clases

<div class="muestra">
<div>
  <UmlCanvas :w="560" :h="180">
    <ClassBox x="0" y="10" :w="220" compact name="Cliente" />
    <ClassBox x="340" y="10" :w="220" compact name="Pedido" />
    <Rel from="Cliente" to="Pedido" fm="1" tm="*" />
  </UmlCanvas>
  <p class="legib">Familia pensada para documentación técnica.</p>
  <p class="legib">Ñandú, ¿qué pasó? 0O 1lI rn m — Pedido#1024</p>
</div>
<pre>public class Pedido {
  private Cliente cliente;
  private List&lt;Linea&gt; lineas;
  public double total() {
    return lineas.stream()
      .mapToDouble(Linea::subtotal)
      .sum();
  }
}</pre>
</div>

---
class: tipo5
---

<div class="nombre">Plus Jakarta Sans</div>

# Diagrama de clases

<div class="muestra">
<div>
  <UmlCanvas :w="560" :h="180">
    <ClassBox x="0" y="10" :w="220" compact name="Cliente" />
    <ClassBox x="340" y="10" :w="220" compact name="Pedido" />
    <Rel from="Cliente" to="Pedido" fm="1" tm="*" />
  </UmlCanvas>
  <p class="legib">Geométrica moderna, más amplia y redonda.</p>
  <p class="legib">Ñandú, ¿qué pasó? 0O 1lI rn m — Pedido#1024</p>
</div>
<pre>public class Pedido {
  private Cliente cliente;
  private List&lt;Linea&gt; lineas;
  public double total() {
    return lineas.stream()
      .mapToDouble(Linea::subtotal)
      .sum();
  }
}</pre>
</div>
