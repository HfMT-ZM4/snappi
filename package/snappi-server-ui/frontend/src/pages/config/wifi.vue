<template>
  <v-form class="pa-5">
    <v-card>
      <v-card-title>Wifi Settings</v-card-title>
      <v-card-text>

        <v-text-field
          label="SSID"
          required
          v-model="store.wifiSSID"
          ></v-text-field>

        <v-text-field
          label="Password"
          required
          v-model="store.wifiPassword"
          ></v-text-field>

        <v-radio-group v-model="store.wifiMode">
          <v-radio label="Act as access point" value="ap"></v-radio>
          <v-radio label="Connect to existing network" value="client"></v-radio>
        </v-radio-group>

      </v-card-text>
    </v-card>
  </v-form>
</template>

<script setup>
import { useAppStore } from '@/stores/app'

const store = useAppStore()
</script>
