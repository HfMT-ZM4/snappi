<template>
  <v-row>
    <v-col>
      <b>{{ stream.name }}</b>
    </v-col>
    <v-col>
      <v-select
          label="Input Ports"
          :items="portItems"
          v-model="map.ports"
          multiple
          clearable
          hide-details
          />
    </v-col>
        <v-col cols="1">
          <v-btn
              variant="text"
              prepend-icon="mdi-clear"
              size="x-large"
              />
        </v-col>
  </v-row>
</template>

<script setup>
import { computed } from 'vue'
import { useAppStore } from '@/stores/app'
import { usePipeWireStore } from '@/stores/pipewire'

const props = defineProps(['streamName'])
const appStore = useAppStore()
const stream = appStore.streamByName(props.streamName)

const pwStore = usePipeWireStore()
const portItems = computed(() => {
  return pwStore.ports.map(port => {
    return {
      title: `${port.node_description} - ${port.name}`,
      value: port.port_path,
    }
  })
})
</script>


