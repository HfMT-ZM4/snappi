<template>
  <v-app>
    <v-main>
      <router-view />
    </v-main>
  </v-app>
</template>

<script setup>
import { useAppStore } from '@/stores/app'
const store = useAppStore()
store.saveCleanState()
</script>
