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
              label="Input Channels"
              :items="channelItems"
              v-model="map.channels"
              multiple
              clearable
              hide-details
              :bg-color="invalid ? 'error' : ''"
          >
          </v-select>
        </v-col>
        <v-col cols="1">
          <v-btn
            variant="text"
            prepend-icon="mdi-delete"
            size="x-large"
            @click="store.removeStream(props.idx)"
            />
        </v-col>
      </v-row>
</template>

<script setup>
import { useAppStore } from '@/stores/app'
import { computed } from 'vue'

const props = defineProps(['idx'])
const store = useAppStore()
const map = store.streams[props.idx]

const channelItems = computed(() => {
  return [...Array(store.channels).keys()].map(i => i + 1)
})

const invalid = computed(() => {
  return store.streamError(props.idx)
})
</script>

