<template>
  <v-app-bar>
    <v-app-bar-nav-icon
      variant="text"
      @click.stop="userStore.showSidebar = !userStore.showSidebar"
      />

    <template v-if="!showControls">
      SnapCast Clients
    </template>

    <v-btn
      :disabled="!store.isDirty"
      color="primary"
      @click="store.saveConfig()"
      v-if="showControls"
    >
      Save Config
    </v-btn>

    <v-btn
      :disabled="!store.isDirty"
      color="warning"
      class="ml-auto"
      @click="store.resetChanges()"
      v-if="showControls"
    >
      Reset Changes
    </v-btn>
  </v-app-bar>
</template>

<script setup>
import { useAppStore } from '@/stores/app'
import { useUserStore } from '@/stores/user'
import { computed } from 'vue'
import { useRoute } from 'vue-router';

const store = useAppStore()
const userStore = useUserStore()
const route = useRoute()
const showControls = computed(() => {
  console.log(route.name)
  return route.name != '/snapcast'
})
</script>
