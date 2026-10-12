<script setup lang="ts">
// Rótulo "Incorrecto" / "Correcto" con símbolo (el estado nunca depende solo del color).
defineProps<{ ok?: boolean }>()
</script>

<template>
  <span class="verdict" :class="ok ? 'ok' : 'no'">
    <svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="3.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
      <path v-if="ok" d="M4 13 L10 19 L20 6" />
      <path v-else d="M5 5 L19 19 M19 5 L5 19" />
    </svg>
    {{ ok ? 'Correcto' : 'Incorrecto' }}
  </span>
</template>

<style>
.verdict { display: inline-flex; align-items: center; gap: 8px; font-family: var(--font-mono); font-size: 22px; font-weight: 700; padding: 3px 14px 3px 10px; border: 3px solid currentColor; border-radius: 8px; }
.verdict.no { color: var(--rojo); }
.verdict.ok { color: var(--ink); }
</style>
