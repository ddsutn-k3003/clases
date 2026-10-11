<script setup lang="ts">
// Relación UML entre dos ClassBox, por id (o nombre). Los lados son top | bottom | left | right,
// y fromAt / toAt (0 a 1) indican la posición a lo largo del lado. via = puntos intermedios.
import { computed, inject } from 'vue'

type Kind = 'association' | 'navigable' | 'aggregation' | 'composition' | 'generalization' | 'realization' | 'dependency' | 'link'
const props = withDefaults(
  defineProps<{
    from: string
    to: string
    fromSide?: 'top' | 'bottom' | 'left' | 'right'
    toSide?: 'top' | 'bottom' | 'left' | 'right'
    fromAt?: number
    toAt?: number
    via?: [number, number][]
    kind?: Kind
    label?: string
    fm?: string
    tm?: string
    labelDx?: number
    labelDy?: number
  }>(),
  { fromSide: 'right', toSide: 'left', fromAt: 0.5, toAt: 0.5, kind: 'association', labelDx: 0, labelDy: 0 },
)
const reg = inject<Record<string, any>>('umlRegistry', {})
const uid = inject<string>('umlUid', 'u')

const anchor = (id: string, side: string, at: number): [number, number] => {
  const r = reg[id]?.value
  if (!r) return [0, 0]
  if (side === 'top') return [r.x + r.w * at, r.y]
  if (side === 'bottom') return [r.x + r.w * at, r.y + r.h]
  if (side === 'left') return [r.x, r.y + r.h * at]
  return [r.x + r.w, r.y + r.h * at]
}
const pts = computed<[number, number][]>(() => [
  anchor(props.from, props.fromSide, props.fromAt),
  ...(props.via ?? []),
  anchor(props.to, props.toSide, props.toAt),
])
const d = computed(() => pts.value.map((p, i) => `${i ? 'L' : 'M'}${p[0]} ${p[1]}`).join(' '))

const dashed = computed(() => props.kind === 'realization' || props.kind === 'dependency')
const markerStart = computed(() =>
  props.kind === 'aggregation' ? `url(#${uid}-dia-open)` : props.kind === 'composition' ? `url(#${uid}-dia-fill)` : undefined,
)
const markerEnd = computed(() =>
  props.kind === 'generalization' || props.kind === 'realization'
    ? `url(#${uid}-tri)`
    : props.kind === 'navigable' || props.kind === 'dependency'
      ? `url(#${uid}-arrow)`
      : undefined,
)

// Posición de un texto cerca de un extremo: a t px del punto a lo largo del segmento, y n px hacia el costado.
const near = (a: [number, number], b: [number, number], t: number, n: number) => {
  const dx = b[0] - a[0]
  const dy = b[1] - a[1]
  const len = Math.hypot(dx, dy) || 1
  const ux = dx / len
  const uy = dy / len
  return { x: a[0] + ux * t - uy * n, y: a[1] + uy * t + ux * n }
}
const fmPos = computed(() => near(pts.value[0], pts.value[1], 34, -22))
const tmPos = computed(() => {
  const n = pts.value.length
  return near(pts.value[n - 1], pts.value[n - 2], 34, 22)
})
const lblPos = computed(() => {
  // punto medio del segmento más largo
  let best = 0
  let bl = -1
  for (let i = 0; i < pts.value.length - 1; i++) {
    const l = Math.hypot(pts.value[i + 1][0] - pts.value[i][0], pts.value[i + 1][1] - pts.value[i][1])
    if (l > bl) {
      bl = l
      best = i
    }
  }
  const a = pts.value[best]
  const b = pts.value[best + 1]
  const horiz = Math.abs(b[0] - a[0]) >= Math.abs(b[1] - a[1])
  return { x: (a[0] + b[0]) / 2 + props.labelDx, y: (a[1] + b[1]) / 2 + (horiz ? -14 : 0) + props.labelDy, anchor: horiz ? 'middle' : 'start' }
})
</script>

<template>
  <g>
    <path
      :d="d"
      fill="none"
      stroke="#7a1f2b"
      stroke-width="3.5"
      stroke-linejoin="round"
      :stroke-dasharray="dashed ? '12 9' : undefined"
      :marker-start="markerStart"
      :marker-end="markerEnd"
    />
    <text v-if="fm" :x="fmPos.x" :y="fmPos.y + 8" text-anchor="middle" class="t-mult halo">{{ fm }}</text>
    <text v-if="fm" :x="fmPos.x" :y="fmPos.y + 8" text-anchor="middle" class="t-mult">{{ fm }}</text>
    <text v-if="tm" :x="tmPos.x" :y="tmPos.y + 8" text-anchor="middle" class="t-mult halo">{{ tm }}</text>
    <text v-if="tm" :x="tmPos.x" :y="tmPos.y + 8" text-anchor="middle" class="t-mult">{{ tm }}</text>
    <text v-if="label" :x="lblPos.x" :y="lblPos.y" :text-anchor="lblPos.anchor" class="t-lbl halo" style="font-style: italic">{{ label }}</text>
    <text v-if="label" :x="lblPos.x" :y="lblPos.y" :text-anchor="lblPos.anchor" class="t-lbl" style="font-style: italic">{{ label }}</text>
  </g>
</template>
