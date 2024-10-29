<template>
  <v-alert
      v-if="restartRequired"
      class="mx-2 mt-2"
      icon="$info"
      type="warning"
    >
      <p v-if="systemRestart">
        The Snappi server needs to be restarted for the changes to take effect.
        Press the button below to restart now.
      </p>
      <p v-else>
        The Snappi server audio system need to be restarted for the changes to take effect.
        Press the button below to restart the audio system now.
      </p>

      <div class="mt-2">
        <v-btn
            color="primary"
            density="compact"
            :disabled="store.restartInProgress"
            @click="store.restartServices()"
        >
          <template v-if="systemRestart">Restart Snappi server</template>
          <template v-else>Restart audio system</template>
        </v-btn>
        <v-btn
            variant="outlined"
            class="ml-2"
            @click="store.serviceRestart = []"
            density="compact"
            :disabled="store.restartInProgress"
        >
          Dismiss
        </v-btn>
      </div>

      <div class="mt-5" v-if="store.restartInProgress">
        Restarting...
        <v-progress-linear
            :indeterminate="true"
        />
      </div>
  </v-alert>
</template>

<script setup>
import { computed } from 'vue'
import { useUserStore } from '@/stores/user'

const store = useUserStore()

const systemRestart = computed(() => {
  return store.serviceRestart.includes('system')
})

const restartRequired = computed(() => {
  return store.serviceRestart.length > 0
})
</script>
