import { defineStore } from 'pinia'
import API from '@/api'

const defaultStatus = {
  jackd: 'unknown',
  jacktrip: 'unknown',
  snapserver: 'unknown',
}

export const useSystemStore = defineStore('system', {
  state: () => ({
    status: defaultStatus,
    statusTime: new Date(),
    busy: false,
  }),

  getters: {
    serviceNames: () => {
      return Object.keys(defaultStatus)
    },
  },

  actions: {
    async updateStatus() {
      try {
        this.busy = true
        const response = await API.getServiceStatus()
        this.status = response.data
        this.statusTime = new Date()
        this.busy = false
      }
      catch (error) {
        this.busy = false
        this.status = defaultStatus
        console.log(error)
      }
    },
  },
})



