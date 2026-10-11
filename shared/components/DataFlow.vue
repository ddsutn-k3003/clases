<script setup lang="ts">
// Flujo de datos animado entre componentes. Uso en una slide:
//   <DataFlow :nodes="['Cliente', 'API', 'Base']" />
const props = withDefaults(defineProps<{ nodes?: string[]; duration?: number }>(), {
  nodes: () => ['Cliente', 'Servidor', 'Base de datos'],
  duration: 3,
})
</script>

<template>
  <div class="flow">
    <template v-for="(n, i) in props.nodes" :key="n">
      <div class="node">{{ n }}</div>
      <div v-if="i < props.nodes.length - 1" class="link">
        <span class="dot" :style="{ animationDuration: `${props.duration}s`, animationDelay: `${i * 0.4}s` }" />
      </div>
    </template>
  </div>
</template>

<style scoped>
.flow { display: flex; align-items: center; justify-content: center; gap: 0; margin: 2rem 0; }
.node { border: 2px solid currentColor; border-radius: 10px; padding: .8rem 1.2rem; font-weight: 600; white-space: nowrap; }
.link { position: relative; width: 120px; height: 2px; background: currentColor; opacity: .7; }
.dot { position: absolute; top: -5px; left: 0; width: 12px; height: 12px; border-radius: 50%; background: #e4572e; animation: move linear infinite; }
@keyframes move { from { left: 0; } to { left: calc(100% - 12px); } }
</style>
