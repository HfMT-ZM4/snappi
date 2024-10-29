<template>
  <v-form class="pa-5">
    <v-card>
      <v-card-title>Wifi Settings</v-card-title>
      <v-card-text>

        <v-radio-group v-model="store.wifi.mode">
          <v-radio label="Connect to existing network" value="client"></v-radio>
          <v-radio label="Act as access point" value="ap"></v-radio>
        </v-radio-group>

        <v-text-field
          label="SSID"
          required
          v-model="store.wifi.ssid"
          ></v-text-field>

        <v-text-field
          label="Password"
          required
          v-model="store.wifi.password"
          ></v-text-field>

        <v-select
          label="Band"
          required
          v-model="store.wifi.band"
          :items="bandItems"
          ></v-select>

      </v-card-text>
    </v-card>
  </v-form>
</template>

<script setup>
import { VNumberInput } from 'vuetify/labs/VNumberInput'
import { useAppStore } from '@/stores/app'
import { computed } from 'vue'

const store = useAppStore()

const bandItems = computed(() => {
  return [
    {value: '', title: 'Automatic'},
    {value: 'b', title: '2.4GHz (b)'},
    {value: 'gn', title: '5GHz (gn)'},
    {value: 'bgn', title: '2.4GHz and 5GHz (bgn)'},
  ]
})
</script>
