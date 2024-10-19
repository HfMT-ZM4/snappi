<template>
  <v-card class="mb-5">
    <v-container>
      <v-row>
        <v-col cols="8">
      <v-text-field
          label="Stream Name"
          :modelValue="stream.name"
          @change="stream.name = $event.target.value"
          hide-details
          />
        </v-col>
        <v-col cols="4">
        <v-number-input
            label="Number of Channels"
            required
            v-model="stream.channels"
            hint="The number of channels in this stream. 1 for mono, 2 for stereo, or more..."
            hide-details
            :min=1
            :max=100
            />
        </v-col>
      </v-row>
      <v-row v-for="chnum in stream.channels" :key="`${idx}-${chnum}`">
        <v-col>
          <v-select
              :label="`Channel ${chnum} Input`"
              :items="portItems"
              clearable
              hide-details
              />
        </v-col>
      </v-row>
    </v-container>

    <v-card-actions>
      <v-btn
          variant="text"
          prepend-icon="mdi-delete"
          size="small"
          @click="appStore.removeStream(props.idx)"
          >Remove</v-btn>
    </v-card-actions>
  </v-card>
</template>

<script setup>
import { computed } from 'vue'
import { VNumberInput } from 'vuetify/labs/VNumberInput'

import { useAppStore } from '@/stores/app'
import { usePipeWireStore } from '@/stores/pipewire'

const props = defineProps(['idx'])
const appStore = useAppStore()
const stream = appStore.streams[props.idx]

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

