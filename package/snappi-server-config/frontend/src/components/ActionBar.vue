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
      :color="store.isDirty ? 'primary' : ''"
      @click="store.saveConfig()"
      v-if="showControls"
    >
      Save Config
    </v-btn>

    <v-btn
      :color="store.isDirty ? 'warning' : ''"
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
  return route.name != '/snapcast'
})
</script>
