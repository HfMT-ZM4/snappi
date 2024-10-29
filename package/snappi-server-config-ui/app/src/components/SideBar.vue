<template>
  <v-navigation-drawer
    v-model="store.showSidebar"
    >
    <v-list-item title="Snappi Server" subtitle="Configuration"/>
    <v-divider></v-divider>
    <v-list-item link to="/config/inputs" title="Audio Input Setup"/>
    <v-list-item link to="/config/streams" title="Stream Setup"/>
    <v-list-item link to="/snapcast" title="SnapCast Clients"/>
    <v-divider></v-divider>
    <v-list-item link to="/config/wifi" title="Wifi"/>
    <v-list-item link to="/config/system" title="System Settings"/>
    <v-divider></v-divider>
    <v-list-item link to="/status" title="Status &amp; Logs"/>
  </v-navigation-drawer>
</template>

<script setup>
import { useUserStore } from '@/stores/user'

const store = useUserStore()
</script>
