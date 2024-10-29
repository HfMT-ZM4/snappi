import { defineStore } from 'pinia'
import API from '@/api'

export const usePipeWireStore = defineStore('pipewire', {
  state: () => ({
    ports: [],
    busy: false,
  }),

  getters: {
    findByPath: (state) => {
      return (path) => {
        return state.ports.find(port => port.port_path === path)
      }
    },
  },

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

    startMonitor() {
        this.ws = API.createWebSocket()
        this.ws.onmessage = this.wsMessage
        this.ws.onerror = this.wsError
        this.ws.onclose = this.wsClosed
    },

    wsMessage(evt) {
      if (evt.data == 'pipewire_changed') {
        this.updatePorts()
      }
    },

    wsClosed() {
      console.log('Socket is closed. Attempting to reconnect')
      setTimeout(() => { this.startMonitor() }, 1000)
    },

    wsError(err) {
      console.error('Socket encountered error: ', err.message, 'Closing socket');
      this.ws.close();
    },
  },
})



