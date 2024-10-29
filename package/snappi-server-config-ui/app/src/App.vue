<template>
  <v-app>
    <v-main>
      <router-view />
    </v-main>
  </v-app>
</template>

<script setup>
import { useAppStore } from '@/stores/app'
import { useUserStore } from '@/stores/user'
import { usePipeWireStore } from '@/stores/pipewire'


const userStore = useUserStore()

const appStore = useAppStore()
appStore.loadConfig()

appStore.$subscribe((mutation, state) => {
  console.log('subscribe', mutation, state)
})

const pwStore = usePipeWireStore()
pwStore.updatePorts()
pwStore.startMonitor()
</script>
