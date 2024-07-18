<template>
  <v-app-bar>
    <v-btn
      :disabled="!store.isDirty"
      color="primary"
    >
      Apply Config &amp; Restart
    </v-btn>

    <v-btn
      :disabled="!store.isDirty"
      color="warning"
      class="ml-auto"
      @click="store.resetChanges()"
    >
      Reset Changes
    </v-btn>
  </v-app-bar>
</template>

<script setup>
import { useAppStore } from '@/stores/app'
const store = useAppStore()
</script>
