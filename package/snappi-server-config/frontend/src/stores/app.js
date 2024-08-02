import { defineStore } from 'pinia'
import { useUserStore } from '@/stores/user'
import axios from 'axios'
import API from '@/api'

let _serializedCleanState = ''

export const useAppStore = defineStore('app', {

  state: () => ({
    hostname: 'snapserver',
    channels: 8,
    samplerate: 48000,
    bits: 16,
    periodsize: 512,
    latency: 600,
    wifi: {
      ssid: 'Snappi',
      password: '12345678',
      mode: 'ap',
      band: 'auto',
    },
    streams: [{
      name: 'Three',
      channels: [1, 7, 3],
    }],
  }),

  getters: {
    streamNames: (state) => {
      return state.streams.map(stream => stream.name)
    },

    uniqueStreamName: (state) => {
      for (let i=state.streams.length + 1; i < 1000; i++) {
        const name = `Stream ${i}`
        if (!state.streamNames.includes(name)) {
          return name
        }
      }
      return 'New Stream'
    },

    isDirty: (state) => {
      return _serializedCleanState != JSON.stringify(state.$state)
    },

    streamError: (state) => {
      return (idx) => {
        const stream = state.streams[idx]
        for (const channel of stream.channels) {
          if (channel > state.channels) {
            return true
          }
        }
      }
    },

    configErrors: (state) => {
      const user = useUserStore()
      const errors = []

      if (
        (state.periodsize >= 2048 && state.channels > 15) ||
        (state.periodsize >= 1024 && state.channels > 30) ||
        (state.periodsize >= 512 && state.channels > 60)
      ) {
        errors.push({
          type: 'error',
          text: 'The number of channels is too large for the configured ' +
          'Jack period size. Use less channels to set a lower period size.',
        })
      }

      if (state.channels > 70) {
        errors.push({
          id: 'high-channel-count',
          type: 'warning',
          text: 'Very high channel count, this might not work as expected!',
        })
      }

      if (state.latency < 400) {
        errors.push({
          id: 'low-latency',
          type: 'info',
          text: 'Latencies below 400ms might cause problems with Android devices.',
        })
      }

      if (state.periodsize < 512) {
        errors.push({
          id: 'low-periodsize',
          type: 'info',
          text: 'Period sizes below 512 will require a very stable and fast network connection.',
        })
      }

      let missingChannel = false
      for (const idx in state.streams) {
        if (state.streamError(idx)) {
          missingChannel = true
          break
        }
      }
      if (missingChannel) {
        errors.push({
          type: 'error',
          text: 'Your stream setup contains channels that are not available anymore!',
        })
      }

      let unusedChannels = [...Array(state.channels).keys()].map(i =>i+1)
      for (const stream of state.streams) {
        for (const channel of stream.channels) {
          const idx = unusedChannels.indexOf(channel)
          if (idx >= 0) {
            unusedChannels.splice(idx, 1)
          }
        }
      }
      if (unusedChannels.length) {
        errors.push({
          id: 'missing-channels',
          type: 'info',
          text: 'The following input channels are unused in your stream setup: ' + unusedChannels.join(', '),
        })
      }

      return errors.filter(el => {
        return (!el.id || !user.ignoredWarnings.includes(el.id))
      })
    },
  },

  actions: {
    addDefaultStreams() {
      for (let i = 0; i < this.channels; i++) {
         this.streams.push({
            name: 'Mono-' + (i+1),
            channels: [i+1],
         })
      }

      for (let i = 0; i < Math.floor(this.channels / 2); i++) {
         this.streams.push({
            name: 'Stereo-' + (i+1),
            channels: [(i * 2) + 1, (i * 2) + 2],
         })
      }
    },

    addStream() {
      this.streams.push({
        name: this.uniqueStreamName,
        channels: [],
      })
    },

    removeStream(idx) {
      this.streams.splice(idx, 1)
    },

    clearStreams() {
      this.streams = []
    },

    saveCleanState() {
      _serializedCleanState = JSON.stringify(this.$state)
    },

    resetChanges() {
      Object.assign(this, JSON.parse(_serializedCleanState))
    },

    async loadConfig() {
      try {
        const data = await API.loadConfig()
        Object.assign(this, data.data)
        this.saveCleanState()
      }
      catch (error) {
        alert(error)
        console.log(error)
      }
    },

    async saveConfig() {
      try {
        const response = await API.saveConfig(this.$state)
        const user = useUserStore()
        user.serviceRestart = response.data || []
        this.loadConfig()
      }
      catch (error) {
        alert(error)
        console.log(error)
      }
    },
  },
})
