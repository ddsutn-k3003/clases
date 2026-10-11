<script setup lang="ts">
// Lienzo SVG para diagramas UML. Define los marcadores de las relaciones y registra las cajas
// (ClassBox) para que Rel pueda unirlas por nombre.
import { provide } from 'vue'
const props = withDefaults(defineProps<{ w?: number; h?: number }>(), { w: 1136, h: 500 })
const uid = 'u' + Math.random().toString(36).slice(2, 8)
provide('umlRegistry', {} as Record<string, any>)
provide('umlUid', uid)
</script>

<template>
  <svg class="uml" :viewBox="`0 0 ${props.w} ${props.h}`" xmlns="http://www.w3.org/2000/svg">
    <defs>
      <marker :id="`${uid}-tri`" viewBox="0 0 26 26" refX="24" refY="13" markerWidth="26" markerHeight="26" orient="auto" markerUnits="userSpaceOnUse">
        <path d="M3 3 L24 13 L3 23 Z" fill="#fff" stroke="#7a1f2b" stroke-width="3" stroke-linejoin="round" />
      </marker>
      <marker :id="`${uid}-dia-open`" viewBox="0 0 34 26" refX="2" refY="13" markerWidth="34" markerHeight="26" orient="auto" markerUnits="userSpaceOnUse">
        <path d="M2 13 L17 3 L32 13 L17 23 Z" fill="#fff" stroke="#7a1f2b" stroke-width="3" stroke-linejoin="round" />
      </marker>
      <marker :id="`${uid}-dia-fill`" viewBox="0 0 34 26" refX="2" refY="13" markerWidth="34" markerHeight="26" orient="auto" markerUnits="userSpaceOnUse">
        <path d="M2 13 L17 3 L32 13 L17 23 Z" fill="#7a1f2b" stroke="#7a1f2b" stroke-width="3" stroke-linejoin="round" />
      </marker>
      <marker :id="`${uid}-arrow`" viewBox="0 0 26 26" refX="24" refY="13" markerWidth="26" markerHeight="26" orient="auto" markerUnits="userSpaceOnUse">
        <path d="M3 3 L24 13 L3 23" fill="none" stroke="#7a1f2b" stroke-width="3" stroke-linejoin="round" stroke-linecap="round" />
      </marker>
      <marker :id="`${uid}-arrow-fill`" viewBox="0 0 26 26" refX="24" refY="13" markerWidth="26" markerHeight="26" orient="auto" markerUnits="userSpaceOnUse">
        <path d="M3 3 L24 13 L3 23 Z" fill="#7a1f2b" stroke="#7a1f2b" stroke-width="3" stroke-linejoin="round" />
      </marker>
    </defs>
    <slot />
  </svg>
</template>
