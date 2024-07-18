<template>
  <v-alert
    v-for="error in store.configErrors"
    class="mx-2 mt-2"
    :text="error.text"
    :type="error.type"
    >
    <v-btn
        v-if="error.id"
        variant="outlined"
        class="float-right"
        @click="userStore.ignoreWarning(error.id)"
        density="compact"
    >
      Ignore
    </v-btn>
  </v-alert>
</template>

<script setup>
import { useAppStore } from '@/stores/app'
import { useUserStore } from '@/stores/user'
const store = useAppStore()
const userStore = useUserStore()
</script>
