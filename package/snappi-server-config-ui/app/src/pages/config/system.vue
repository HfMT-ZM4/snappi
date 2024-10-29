<template>
  <v-form class="pa-5">
    <v-card class="mb-5">
      <v-card-title>Audio Settings</v-card-title>
      <v-card-text>
        <v-select
          label="Sample-rate"
          :items="[44100, 48000]"
          suffix="Hz"
          v-model="store.samplerate"
          hint="The sample rate for JackTrip, Jack and all SnapCast streams"
          ></v-select>

        <v-select
          label="Bitrate"
          :items="[16, 24, 32]"
          v-model="store.bits"
          hint="The bit rate for all SnapCast streams"
          ></v-select>


        <v-select
          label="Period size"
          required
          v-model="store.periodsize"
          :items="[16, 32, 64, 128, 256, 512, 1024, 2048, 4096]"
          ></v-select>
      </v-card-text>
    </v-card>

    <v-card class="mb-5">
      <v-card-title>Streaming Settings</v-card-title>
      <v-card-text>

        <v-text-field
          label="End-to-end latency"
          required
          suffix="ms"
          v-model="store.latency"
          hint="The delay in milliseconds until Snappi clients play out the received audio. Increase this value on slow connections or high client count."
          ></v-text-field>
      </v-card-text>
    </v-card>

    <v-card class="mb-5">
      <v-card-title>Server Settings</v-card-title>
      <v-card-text>
        <v-text-field
          label="Hostname"
          hide-details
          required
          v-model="store.hostname"
          ></v-text-field>
      </v-card-text>
    </v-card>
  </v-form>
</template>

<script setup>
import { useAppStore } from '@/stores/app'

const store = useAppStore()
</script>
