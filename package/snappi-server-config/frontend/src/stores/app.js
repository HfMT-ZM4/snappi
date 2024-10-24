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
      channels: 3,
      inputs: [],
    }],
    routes: [],
    uac2: {
      enable: false,
      name: 'SnappiAudio',
      serial: 1,
      channels: 2,
      samplerate: 44100,
      bits: 16,
    },
  }),

  getters: {
    streamByName: (state) => {
      return (name) => {
        return state.streams.find(stream => stream.name === name)
      }
    },

    streamsByName: (state) => {
      return (name) => {
        return state.streams.filter(stream => stream.name === name)
      }
    },

    streamNames: (state) => {
      return state.streams.map(stream => stream.name)
    },

    routesByTargetName: (state) => {
      return (name) => {
        return state.routes.filter(route => route.target === name)
      }
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
            channels: 1,
         })
      }

      for (let i = 0; i < Math.floor(this.channels / 2); i++) {
         this.streams.push({
            name: 'Stereo-' + (i+1),
            channels: 2,
         })
      }
    },

    addRoute (source, target) {
      if (this.routes.find(route => {
        return route.target === target && route.source === source
      })) return
      this.routes.push({
        target: target,
        source: source,
      })
    },

    removeRoute (source, target) {
      const idx = this.routes.findIndex(route => {
        return route.target === target && route.source === source
      })
      if (idx < 0) return
      this.routes.splice(idx, 1)
    },

    addStream() {
      this.streams.push({
        name: this.uniqueStreamName,
        channels: 1,
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
        const result = await API.loadConfig()
        const data = result.data

        for (const stream of data.streams) {
          stream.inputs = []
        }
        for (const route of data.routes) {
            const streamName = route.target.split(':::')[0]
            const stream = data.streams.find(s => s.name === streamName)
            if (!stream) continue
            console.log(streamName, stream)
            stream.inputs.push(route.source)
        }

        Object.assign(this, data)
        this.saveCleanState()
      }
      catch (error) {
        alert(error)
        console.log(error)
        this.saveCleanState()
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
