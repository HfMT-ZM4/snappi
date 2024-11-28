<template>
  <v-form class="pa-5">

    <v-card class="mb-5">
      <v-card-title>Virtual USB Audio</v-card-title>

      <v-card-text>
        The Virtual USB Audio input will enable the Snappi server to
        act as a "virtual" USB soundcard when connected to a computer via
        the USB-C port of the Raspberry Pi.

        <p>Uses a samplerate of <b>{{store.samplerate}} Hz</b> and <b>{{store.bits}} bits</b>
        (as configured in the <router-link to="/config/system">System Settings</router-link>).</p>
      </v-card-text>

      <v-card-text>

        <v-radio-group v-model="store.uac2.enable" inline>
          <v-radio label="Enabled" :value="true"></v-radio>
          <v-radio label="Disabled" :value="false"></v-radio>
        </v-radio-group>

        <v-text-field
          label="Name"
          required
          v-model="store.uac2.name"
          ></v-text-field>

        <v-number-input
          label="Number of input channels"
          required
          v-model="store.uac2.channels"
          hint="The number of channels for the virtual audio device, maximum is 27 channels."
          :min="1"
          :max="27"
          ></v-number-input>
      </v-card-text>

    </v-card>

    <v-card class="mb-5">
      <v-card-title>JackTrip</v-card-title>

      <v-card-text>

        <v-number-input
          label="Number of JackTrip input channels"
          required
          v-model="store.channels"
          hint="The number of channels this server accepts via JackTrip"
          hide-details
          ></v-number-input>

      </v-card-text>

      <v-card-text>
        <p>Configure your JackTrip client to run in <b>P2P mode</b>, with a samplerate
        of <b>{{store.samplerate}} Hz</b> and <b>{{store.bits}} bits</b>
        (as configured in the <router-link to="/config/system">System Settings</router-link>).</p>

        <p class="mt-2">Example Linux commandline:
        <pre>jacktrip -c {{store.hostname}} --sendchannels {{store.channels}} --receivechannels 1</pre>
        </p>
      </v-card-text>
    </v-card>
  </v-form>
</template>

<script setup>
import { VNumberInput } from 'vuetify/labs/VNumberInput'
import { useAppStore } from '@/stores/app'

const store = useAppStore()
</script>

