<template>
  <v-form>
    <v-card class="pa-5">
      <v-card-title>System Settings</v-card-title>
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
