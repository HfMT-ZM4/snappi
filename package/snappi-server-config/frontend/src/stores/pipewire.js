import { defineStore } from 'pinia'
import API from '@/api'

export const usePipeWireStore = defineStore('pipewire', {
  state: () => ({
    ports: [],
    busy: false,
  }),

  actions: {
    async updatePorts() {
      try {
        this.busy = true
        const response = await API.getPorts()
        this.ports = response.data
        this.busy = false
      }
      catch (error) {
        this.busy = false
        this.ports = []
        console.log(error)
      }
    },
  },
})



