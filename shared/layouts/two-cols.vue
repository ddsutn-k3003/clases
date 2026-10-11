<template>
  <div class="slidev-layout two-cols">
    <div class="cols-head"><slot /></div>
    <div class="layout-cols">
      <div><slot name="left" /></div>
      <div><slot name="right" /></div>
    </div>
    <div class="layout-foot"><span>Diseño de Sistemas de Información · K3003 · UTN FRBA</span><span class="num"><SlideCurrentNo /></span></div>
  </div>
</template>
