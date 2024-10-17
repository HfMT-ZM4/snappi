<template>
      <v-row>
        <v-col>
          <v-text-field
              label="Stream Name"
              :modelValue="map.name"
              @change="map.name = $event.target.value"
              hide-details
          />
        </v-col>
        <v-col>
          <v-select
              label="Input Ports"
              :items="portItems"
              v-model="map.ports"
              multiple
              clearable
              hide-details
          >
          </v-select>
        </v-col>
        <v-col cols="1">
          <v-btn
            variant="text"
            prepend-icon="mdi-delete"
            size="x-large"
            @click="appStore.removeStream(props.idx)"
            />
        </v-col>
      </v-row>
</template>

<script setup>
import { useAppStore } from '@/stores/app'
import { usePipeWireStore } from '@/stores/pipewire'

import { computed } from 'vue'

const props = defineProps(['idx'])
const appStore = useAppStore()
const map = appStore.streams[props.idx]

const pwStore = usePipeWireStore()

const portItems = computed(() => {
  return pwStore.ports.map(port => {
    return {
      title: `${port.description} - ${port.name}`,
      value: port.path,
    }
  })
})
</script>

