<template>
  <v-app>
    <v-main>
      <router-view />
    </v-main>
  </v-app>
</template>

<script setup>
import { useAppStore } from '@/stores/app'
import { usePipeWireStore } from '@/stores/pipewire'

const userStore = useAppStore()
userStore.loadConfig()

const pwStore = usePipeWireStore()
pwStore.updatePorts()
</script>
