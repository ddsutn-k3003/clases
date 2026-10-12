<script setup lang="ts">
// Marca estándar de "esto se usa en el TPA". Va en la esquina superior derecha de la diapositiva.
// nota: texto breve opcional a la izquierda de la marca.
defineProps<{ nota?: string }>()
</script>

<template>
  <div class="tpa-tag">
    <span v-if="nota" class="tpa-nota">{{ nota }}</span>
    <svg viewBox="0 0 64 90" width="54" height="76" role="img" aria-label="TPA">
      <path d="M0 0 H64 V90 L32 68 L0 90 Z" fill="#b4182d" />
      <rect x="0" y="0" width="64" height="7" fill="#6d1327" />
      <text x="32" y="45" text-anchor="middle" class="tpa-txt">TPA</text>
    </svg>
  </div>
</template>

<style>
.tpa-tag { position: absolute; top: 0; right: 44px; display: flex; align-items: flex-start; gap: 12px; z-index: 5; }
.tpa-nota { margin-top: 16px; font-size: 19px; line-height: 1.2; font-weight: 600; color: var(--bordo); text-align: right; max-width: 280px; }
.tpa-tag svg text.tpa-txt { font-family: var(--font-display); font-weight: 800; font-size: 19px; fill: #fff; letter-spacing: .02em; }
</style>
