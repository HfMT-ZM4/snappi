<template>
  <v-container class="pa-5">
    <h2>Audio Streams</h2>

    <StreamConfig
        v-for="stream, idx in store.streams"
        :key="stream.name + idx"
        :idx="idx"
        />

    <v-row>
      <v-col>
        <v-btn color="primary" @click="store.addStream()">Add stream</v-btn>
        <v-btn class="ml-3" color="warning" @click="store.clearStreams()">Clear</v-btn>
        <v-btn class="ml-3" @click="store.addDefaultStreams()">Add default stream setup</v-btn>
      </v-col>
    </v-row>

  </v-container>
</template>

<script setup>
  import { useAppStore } from '@/stores/app'

const store = useAppStore()
</script>
