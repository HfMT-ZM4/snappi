<template>
  <div ref="main" class="d-flex flex-column" style="height: 100%; width: 100%">
    <div ref="iframeContainer" class="flex-grow-1">
      <iframe :class="{'loaded': loaded}" @load="loaded = true" ref="iframe" :src="snapwebURL"></iframe>
    </div>
  </div>
</template>


<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'

const iframeContainer = ref()
const iframe = ref()
const loaded = ref(false)

const resizeIframe = () => {
   const height = +iframeContainer.value.offsetHeight
   const width = +iframeContainer.value.offsetWidth
   iframe.value.height = height
   iframe.value.width = width
}

const snapwebURL = computed(() => {
  return 'http://' + window.location.hostname + ':1780'
})

onMounted(() => {
  window.addEventListener('resize', resizeIframe)
  resizeIframe()
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', resizeIframe)
})
</script>

<style scoped>
  iframe {
    position: absolute;
    border: 0;
    padding: 0;
    margin: 0;
    visibility: hidden;
  }
  iframe.loaded {
    visibility: visible;
  }
</style>

