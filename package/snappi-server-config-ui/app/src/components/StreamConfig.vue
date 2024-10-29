<template>
  <v-card class="mb-5">
    <v-container fluid>
      <v-row>
        <v-col cols="8">
          <v-text-field
              label="Stream Name"
              :modelValue="stream.name"
              @change="setStreamName($event.target.value)"
              :rules="[isUniqueStreamName]"
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
          <h4>Channel {{chnum}} Inputs</h4>
          <v-list>
            <v-list-item
                v-for="input in appStore.streamChannelInputs(idx, chnum)"
                :key="`${idx}-${chnum}-${input.port}`"
                >
                <v-btn
                    icon="mdi-delete"
                    variant="plain"
                    size="small"
                    @click="appStore.removeStreamChannelInput(idx, chnum, input.port)"
                    />
                  <span :class="{'text-disabled': !portAvailable(input.port)}">{{ input.port.split(':::').join(' - ') }}</span>
            </v-list-item>
            <v-list-item>
              <v-select
                  :placeholder="`Add channel ${chnum} input...`"
                  :items="portItems"
                  :modelValue="null"
                  density="compact"
                  variant="underlined"
                  persistent-placeholder
                  @update:modelValue="appStore.addStreamChannelInput(idx, chnum, $event)"
                  hide-details
                  />
            </v-list-item>
          </v-list>

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
import { computed, toRef } from 'vue'
import { VNumberInput } from 'vuetify/labs/VNumberInput'

import { useAppStore } from '@/stores/app'
import { usePipeWireStore } from '@/stores/pipewire'

const props = defineProps(['idx'])
const appStore = useAppStore()
const pwStore = usePipeWireStore()

function isUniqueStreamName(name) {
  const streams = appStore.streamsByName(name)
  if ((streams.length > 1) || (streams.length > 0 && streams[0] != stream.value)) {
    return 'Please choose a unique name for this stream'
  }
  return true
}

function setStreamName(name) {
  if (isUniqueStreamName(name) !== true) return
  stream.value.name = name
}

const portItems = computed(() => {
  return pwStore.ports.map(port => {
    return {
      title: `${port.node_description} - ${port.name}`,
      value: port.port_path,
    }
  })
})

const portAvailable = computed(() => {
  return (path) => {
    return pwStore.findByPath(path) ? true : false
  }
})

const stream = computed(() => {
  return appStore.streams[props.idx]
})
</script>

