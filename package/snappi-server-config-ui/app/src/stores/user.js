import { defineStore } from 'pinia'
import API from '@/api'

export const useUserStore = defineStore('user', {
  state: () => ({
    ignoredWarnings: [],
    serviceRestart: [],
    restartInProgress: false,
    showSidebar: true,
  }),

  actions: {
    ignoreWarning(id) {
      this.ignoredWarnings.push(id)
    },

    async restartServices(services) {
      try {
        this.restartInProgress = true
        await API.restartServices(this.serviceRestart)
        this.restartInProgress = false
        this.serviceRestart = []
      }
      catch (error) {
        this.restartInProgress = false
        alert(error)
        console.log(error)
      }
    },
  },
})


