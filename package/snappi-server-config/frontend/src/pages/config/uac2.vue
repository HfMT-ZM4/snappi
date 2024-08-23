<template>
  <v-form class="pa-5">
    <v-card>
      <v-card-title>Virtual USB Audio Settings</v-card-title>
      <v-card-text>

        <v-radio-group v-model="store.uac2.enable">
          <v-radio label="Enable" :value="true"></v-radio>
          <v-radio label="Disable" :value="false"></v-radio>
        </v-radio-group>

        <v-text-field
          label="Name"
          required
          v-model="store.uac2.name"
          ></v-text-field>

        <v-text-field
          label="Serial Number"
          required
          v-model="store.uac2.serial"
          hint="Change the serial number for Windows to detect a new configuration"
          ></v-text-field>

        <v-number-input
          label="Number of input channels"
          required
          v-model="store.uac2.channels"
          hint="The number of channels for the virtual audio device. Maximum is 27 channels at 44100Hz."
          ></v-number-input>

        <v-select
          label="Sample-rate"
          :items="[44100, 48000]"
          suffix="Hz"
          v-model="store.uac2.samplerate"
          ></v-select>

        <v-select
          label="Bitrate"
          :items="[16, 24, 32]"
          v-model="store.uac2.bits"
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

