<script setup lang="ts">
// Caja de clase (o de objeto, con obj) de un diagrama UML.
// Los miembros que terminan en " {static}" se subrayan. abstract pone el nombre en cursiva.
import { computed, inject } from 'vue'

const props = withDefaults(
  defineProps<{
    id?: string
    x: number
    y: number
    w?: number
    name: string
    stereotype?: string
    attrs?: string[]
    methods?: string[]
    abstract?: boolean
    obj?: boolean
    compact?: boolean
    tone?: 'rosa' | 'gris' | 'azul'
  }>(),
  { w: 280, attrs: () => [], methods: () => [], tone: 'rosa' },
)

const X = computed(() => Number(props.x))
const Y = computed(() => Number(props.y))
const W = computed(() => Number(props.w))
const LH = 34
const nameH = computed(() => (props.compact ? 62 : props.stereotype ? 84 : 56))
const attrsH = computed(() => (props.compact ? 0 : props.attrs.length ? props.attrs.length * LH + 16 : props.obj ? 0 : 24))
const methodsH = computed(() => (props.compact || props.obj ? 0 : props.methods.length ? props.methods.length * LH + 16 : 24))
const h = computed(() => nameH.value + attrsH.value + methodsH.value)

const reg = inject<Record<string, any>>('umlRegistry', {})
reg[props.id ?? props.name] = computed(() => ({ x: X.value, y: Y.value, w: W.value, h: h.value }))

const colors = computed(
  () =>
    ({
      rosa: { fill: '#fbe9eb', stroke: '#7a1f2b' },
      gris: { fill: '#f1efef', stroke: '#3b3b3f' },
      azul: { fill: '#e3eef8', stroke: '#1f4e79' },
    })[props.tone],
)
const member = (m: string) => ({ text: m.replace(/ \{static\}$/, ''), static: / \{static\}$/.test(m) })
</script>

<template>
  <g>
    <rect :x="X" :y="Y" :width="W" :height="h" rx="8" :fill="colors.fill" :stroke="colors.stroke" stroke-width="3.5" />
    <text v-if="stereotype" :x="X + W / 2" :y="Y + 30" text-anchor="middle" class="t-mem" style="font-style: italic">«{{ stereotype }}»</text>
    <text
      :x="X + W / 2"
      :y="Y + (stereotype ? 66 : compact ? 40 : 38)"
      text-anchor="middle"
      class="t-name"
      :style="{ fontStyle: abstract ? 'italic' : 'normal', textDecoration: obj ? 'underline' : 'none' }"
      >{{ name }}</text
    >
    <template v-if="!compact">
      <line :x1="X" :x2="X + W" :y1="Y + nameH" :y2="Y + nameH" :stroke="colors.stroke" stroke-width="3" />
      <text
        v-for="(a, i) in attrs"
        :key="'a' + i"
        :x="X + 16"
        :y="Y + nameH + 12 + (i + 1) * LH - 10"
        class="t-mem"
        :style="{ textDecoration: member(a).static ? 'underline' : 'none' }"
        >{{ member(a).text }}</text
      >
      <template v-if="!obj">
        <line :x1="X" :x2="X + W" :y1="Y + nameH + attrsH" :y2="Y + nameH + attrsH" :stroke="colors.stroke" stroke-width="3" />
        <text
          v-for="(m, i) in methods"
          :key="'m' + i"
          :x="X + 16"
          :y="Y + nameH + attrsH + 12 + (i + 1) * LH - 10"
          class="t-mem"
          :style="{ textDecoration: member(m).static ? 'underline' : 'none' }"
          >{{ member(m).text }}</text
        >
      </template>
    </template>
  </g>
</template>
