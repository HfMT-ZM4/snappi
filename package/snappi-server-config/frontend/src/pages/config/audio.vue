<template>
  <v-form class="pa-5">
    <v-card class="mb-5">
      <v-card-title>Audio Channels</v-card-title>
      <v-card-text>

        <v-number-input
          label="Number of input channels"
          required
          v-model="store.channels"
          hint="The number of channels this server accepts via JackTrip"
          ></v-number-input>

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

      </v-card-text>
    </v-card>

    <v-card class="mb-5">
      <v-card-title>SnapCast Setup</v-card-title>
      <v-card-text>

        <v-text-field
          label="End-to-end latency"
          required
          suffix="ms"
          v-model="store.latency"
          hint="The delay in milliseconds until SnapCast clients play out the received audio"
          ></v-text-field>
      </v-card-text>
    </v-card>

    <v-card class="mb-5">
      <v-card-title>Jack Setup</v-card-title>
      <v-card-text>

        <v-select
          label="Jack period size"
          required
          v-model="store.periodsize"
          :items="[16, 32, 64, 128, 256, 512, 1024, 2048, 4096]"
          ></v-select>
      </v-card-text>
    </v-card>

  </v-form>
</template>

<script setup>
import { VNumberInput } from 'vuetify/labs/VNumberInput'
import { useAppStore } from '@/stores/app'

const store = useAppStore()
</script>
