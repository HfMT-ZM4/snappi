<template>
  <v-card class="mb-5">
    <v-container>
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
              v-for="route in appStore.routesByTargetName(targetName(stream, chnum))"
              :key="`${idx}-${chnum}-${route.source}`"
              >
              <v-btn
                icon="mdi-delete"
                variant="plain"
                size="small"
                @click="appStore.removeRoute(route.source, targetName(stream, chnum))"
                />
                <span :class="{'text-disabled': !portAvailable(route.source)}">{{ route.source.split(':::').join(' - ') }}</span>
            </v-list-item>
            <v-list-item>
              <v-select
                  :placeholder="`Add channel ${chnum} input...`"
                  :items="portItems"
                  :modelValue="null"
                  density="compact"
                  variant="underlined"
                  persistent-placeholder
                  @update:modelValue="appStore.addRoute($event, targetName(stream, chnum))"
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
import { computed } from 'vue'
import { VNumberInput } from 'vuetify/labs/VNumberInput'

import { useAppStore } from '@/stores/app'
import { usePipeWireStore } from '@/stores/pipewire'

const props = defineProps(['idx'])
const appStore = useAppStore()
const stream = appStore.streams[props.idx]

const pwStore = usePipeWireStore()

function targetName(stream, channel) {
  return `${stream.name}:::input_${channel-1}`
}

function isUniqueStreamName(name) {
  const streams = appStore.streamsByName(name)
  if ((streams.length > 1) || (streams.length > 0 && streams[0] != stream)) {
    return 'Please choose a unique name for this stream'
  }
  return true
}

function setStreamName(name) {
  if (isUniqueStreamName(name) !== true) return
  stream.name = name
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
</script>

