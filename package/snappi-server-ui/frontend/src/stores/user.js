import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', {
  state: () => ({
    ignoredWarnings: [],
  }),

  actions: {
    ignoreWarning(id) {
      this.ignoredWarnings.push(id)
    },
  },
})


