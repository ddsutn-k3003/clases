<script setup lang="ts">
// Diagrama de secuencia UML animado: cada mensaje aparece con un clic (el mensaje i con el clic i + 1).
// participants: [{ id, label, actor? }]
// messages: [{ from, to, text, kind?: 'sync' | 'async' | 'return' | 'create', destroy? }]  (from === to es un mensaje a sí mismo)
// activations: [{ p, from, to }]  (índices de mensajes)
// fragments: [{ op, guard, from, to, p1, p2 }]  (índices de mensajes y de participantes)
import { computed } from 'vue'

type P = { id: string; label: string; actor?: boolean }
type M = { from: string; to: string; text: string; kind?: 'sync' | 'async' | 'return' | 'create'; destroy?: boolean }
type A = { p: string; from: number; to: number }
type F = { op: string; guard?: string; from: number; to: number; p1: string; p2: string }

const props = withDefaults(
  defineProps<{ participants: P[]; messages: M[]; activations?: A[]; fragments?: F[]; w?: number; rowH?: number; startClick?: number }>(),
  { activations: () => [], fragments: () => [], w: 1136, rowH: 76, startClick: 1 },
)

const uid = 's' + Math.random().toString(36).slice(2, 8)
const HEAD = 104
const colW = computed(() => props.w / props.participants.length)
const px = (id: string) => colW.value * (props.participants.findIndex((p) => p.id === id) + 0.5)
const rowY = (i: number) => HEAD + 52 + i * props.rowH
const hTotal = computed(() => rowY(props.messages.length) + 20)
const boxW = computed(() => Math.min(colW.value - 16, 230))
const click = (i: number) => props.startClick + i

const created = computed(() => {
  const r: Record<string, number> = {}
  props.messages.forEach((m, i) => {
    if (m.kind === 'create') r[m.to] = i
  })
  return r
})
const destroyed = computed(() => {
  const r: Record<string, number> = {}
  props.messages.forEach((m, i) => {
    if (m.destroy) r[m.to] = i
  })
  return r
})
const lifeline = (p: P) => {
  const y1 = p.id in created.value ? rowY(created.value[p.id]) + 30 : HEAD
  const y2 = p.id in destroyed.value ? rowY(destroyed.value[p.id]) : hTotal.value - 10
  return { y1, y2 }
}

const geom = (m: M, i: number) => {
  const y = rowY(i)
  const a = px(m.from)
  const b = px(m.to)
  if (m.from === m.to) {
    const x0 = a + 9
    return { self: true, d: `M${x0} ${y - 16} L${x0 + 70} ${y - 16} L${x0 + 70} ${y + 22} L${x0 + 9} ${y + 22}`, tx: x0 + 84, ty: y + 4, y }
  }
  const dir = b > a ? 1 : -1
  const x1 = a + dir * 9
  let x2 = b - dir * 9
  if (m.kind === 'create') x2 = b - dir * (boxW.value / 2)
  return { self: false, d: `M${x1} ${y} L${x2} ${y}`, tx: (x1 + x2) / 2, ty: y - 14, y }
}
const dash = (m: M) => (m.kind === 'return' || m.kind === 'create' ? '12 9' : undefined)
const frag = (f: F) => {
  const x1 = Math.min(px(f.p1), px(f.p2)) - 78
  const x2 = Math.max(px(f.p1), px(f.p2)) + 78
  const y1 = rowY(f.from) - 68
  const y2 = rowY(f.to) + 38
  return { x1, y1, w: x2 - x1, h: y2 - y1 }
}
</script>

<template>
  <svg class="uml" :viewBox="`0 0 ${w} ${hTotal}`" xmlns="http://www.w3.org/2000/svg">
    <defs>
      <marker :id="`${uid}-a`" viewBox="0 0 26 26" refX="24" refY="13" markerWidth="26" markerHeight="26" orient="auto" markerUnits="userSpaceOnUse">
        <path d="M3 3 L24 13 L3 23" fill="none" stroke="#3b3b3f" stroke-width="3" stroke-linejoin="round" stroke-linecap="round" />
      </marker>
      <marker :id="`${uid}-af`" viewBox="0 0 26 26" refX="24" refY="13" markerWidth="26" markerHeight="26" orient="auto" markerUnits="userSpaceOnUse">
        <path d="M3 3 L24 13 L3 23 Z" fill="#3b3b3f" stroke="#3b3b3f" stroke-width="3" stroke-linejoin="round" />
      </marker>
    </defs>

    <!-- líneas de vida y cabeceras -->
    <g v-for="p in participants" :key="p.id">
      <g v-if="!(p.id in created)">
        <template v-if="p.actor">
          <circle :cx="px(p.id)" cy="14" r="11" fill="#fbe9eb" stroke="#7a1f2b" stroke-width="3.5" />
          <path :d="`M${px(p.id)} 25 V52 M${px(p.id) - 22} 36 H${px(p.id) + 22} M${px(p.id)} 52 L${px(p.id) - 18} 76 M${px(p.id)} 52 L${px(p.id) + 18} 76`" fill="none" stroke="#7a1f2b" stroke-width="3.5" stroke-linecap="round" />
          <text :x="px(p.id)" y="100" text-anchor="middle" class="t-name" style="font-size: 25px">{{ p.label }}</text>
        </template>
        <template v-else>
          <rect :x="px(p.id) - boxW / 2" y="6" :width="boxW" height="58" rx="8" fill="#fbe9eb" stroke="#7a1f2b" stroke-width="3.5" />
          <text :x="px(p.id)" y="44" text-anchor="middle" class="t-name" style="font-size: 25px">{{ p.label }}</text>
        </template>
      </g>
      <line :x1="px(p.id)" :x2="px(p.id)" :y1="lifeline(p).y1" :y2="lifeline(p).y2" stroke="#6f6f6f" stroke-width="3" stroke-dasharray="11 9" />
    </g>

    <!-- fragmentos -->
    <g v-for="(f, i) in fragments" :key="'f' + i" v-click="click(f.from)">
      <rect :x="frag(f).x1" :y="frag(f).y1" :width="frag(f).w" :height="frag(f).h" fill="none" stroke="#555" stroke-width="3" />
      <path :d="`M${frag(f).x1} ${frag(f).y1} h96 v22 l-14 14 h-82 z`" fill="#f3e4e6" stroke="#555" stroke-width="3" />
      <text :x="frag(f).x1 + 12" :y="frag(f).y1 + 28" class="t-lbl" style="font-weight: 700">{{ f.op }}</text>
      <text v-if="f.guard" :x="frag(f).x1 + 112" :y="frag(f).y1 + 30" class="t-lbl" style="font-style: italic">{{ f.guard }}</text>
    </g>

    <!-- activaciones -->
    <rect
      v-for="(a, i) in activations"
      :key="'a' + i"
      v-click="click(a.from)"
      :x="px(a.p) - 9"
      :y="rowY(a.from) - 20"
      width="18"
      :height="rowY(a.to) - rowY(a.from) + 40"
      fill="#f7e6e7"
      stroke="#7a1f2b"
      stroke-width="3"
    />

    <!-- mensajes -->
    <g v-for="(m, i) in messages" :key="'m' + i" v-click="click(i)">
      <!-- cabecera de un objeto creado -->
      <g v-if="m.kind === 'create'">
        <rect :x="px(m.to) - boxW / 2" :y="rowY(i) - 31" :width="boxW" height="62" rx="8" fill="#fbe9eb" stroke="#7a1f2b" stroke-width="3.5" />
        <text :x="px(m.to)" :y="rowY(i) + 9" text-anchor="middle" class="t-name" style="font-size: 25px">{{ participants.find((p) => p.id === m.to)?.label }}</text>
      </g>
      <path
        :d="geom(m, i).d"
        fill="none"
        stroke="#3b3b3f"
        stroke-width="3.5"
        stroke-linejoin="round"
        :stroke-dasharray="dash(m)"
        :marker-end="m.kind === 'sync' || m.kind === undefined ? `url(#${uid}-af)` : `url(#${uid}-a)`"
      />
      <text
        :x="geom(m, i).tx"
        :y="geom(m, i).ty"
        :text-anchor="geom(m, i).self ? 'start' : 'middle'"
        class="t-lbl halo"
        :style="{ fontStyle: m.kind === 'return' ? 'italic' : 'normal' }"
        >{{ m.kind === 'create' ? '«create» ' : '' }}{{ m.text }}</text
      >
      <text
        :x="geom(m, i).tx"
        :y="geom(m, i).ty"
        :text-anchor="geom(m, i).self ? 'start' : 'middle'"
        class="t-lbl"
        :style="{ fontStyle: m.kind === 'return' ? 'italic' : 'normal' }"
        >{{ m.kind === 'create' ? '«create» ' : '' }}{{ m.text }}</text
      >
      <g v-if="m.destroy">
        <path :d="`M${px(m.to) - 16} ${rowY(i) - 16} L${px(m.to) + 16} ${rowY(i) + 16} M${px(m.to) + 16} ${rowY(i) - 16} L${px(m.to) - 16} ${rowY(i) + 16}`" stroke="#b4182d" stroke-width="6" stroke-linecap="round" />
      </g>
    </g>
  </svg>
</template>
