<template>
  <v-navigation-drawer
    v-model="store.showSidebar"
    >
    <v-list-item title="Snappi Server" subtitle="Configuration"></v-list-item>
    <v-divider></v-divider>
    <v-list-item link to="/snapcast" title="SnapCast Clients"></v-list-item>
    <v-divider></v-divider>
    <v-list-item link to="/config/audio" title="Audio"></v-list-item>
    <v-list-item link to="/config/streams" title="Stream Setup"></v-list-item>
    <v-list-item link to="/config/wifi" title="Wifi"></v-list-item>
    <v-list-item link to="/config/system" title="System"></v-list-item>
    <v-divider></v-divider>
    <v-list-item link to="/status" title="Status &amp; Logs"></v-list-item>
  </v-navigation-drawer>
</template>

<script setup>
import { useUserStore } from '@/stores/user'

const store = useUserStore()
</script>
