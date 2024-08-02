<template>
  <div class="pa-5">
    <div class="text-h6">
      Snappi Status
    </div>
    <v-table density="compact">
      <thead>
        <tr class="text-disabled">
          <th>Service</th>
          <th>Status</th>
          <th>Timestamp</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(status, name) in store.status">
          <td>{{ name }}</td>
          <td :class="statusClass(status)">{{ status }}</td>
          <td>{{ formattedTime }}</td>
        </tr>
      </tbody>
    </v-table>
    <div class="text-h6 mt-2">
      Log Messages
    </div>
    <div class="d-flex align-center">
        <v-btn
          @click="updateLogs()"
          class="mr-2"
          :disabled="busy"
          color="primary"
        >
          Show
        </v-btn>
        <v-switch
          label="Newest entries first"
          color="primary"
          v-model="inverted"
          density="compact"
          hide-details
          class="mx-2"
          :disabled="busy"
          />
        <v-number-input
          v-model="numLines"
          label="Number of lines"
          density="compact"
          hide-details
          class="mx-2"
          :disabled="busy"
          />
        <v-select
          v-model="services"
          label="Services (leave empty for all)"
          :items="store.serviceNames"
          :clearable="true"
          density="compact"
          multiple
          hide-details
          class="ml-2"
          :disabled="busy"
          />
    </div>
    <v-textarea
      :model-value="logLinesDisplay"
      readonly
      :loading="busy"
      rows=15
      />
  </div>
</template>

<script setup>
import { VNumberInput } from 'vuetify/labs/VNumberInput'
import { useSystemStore } from '@/stores/system'
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import API from '@/api'

const store = useSystemStore()

const formattedTime = computed(() => {
  const options = {
    year: "numeric",
    month: "numeric",
    day: "numeric",
    hour: 'numeric',
    minute: 'numeric',
    second: 'numeric',
  }
  return new Intl.DateTimeFormat("de-DE", options).format(store.statusTime)
})

const logLinesDisplay = computed(() => {
  if (inverted.value) {
    return logLines.value.split('\n').reverse().join('\n')
  }
  return logLines.value
})

const logLines = ref('- no entries -')
const inverted = ref(true)
const numLines = ref(1000)
const services = ref([])
const busy = ref(false)

let interval

onMounted(() => {
  interval = setInterval(store.updateStatus, 1000)
})

onBeforeUnmount(() => {
  clearInterval(interval)
})

function statusClass(status) {
  if (status == 'active') {
    return 'text-green'
  }
  else if (status == 'inactive') {
    return 'text-red font-weight-bold'
  }
}

async function updateLogs() {
  try {
    busy.value = true
    const response = await API.getLogs(services.value, numLines.value)
    logLines.value = response.data
    busy.value = false
  }
  catch (error) {
    busy.value = false
    logLines.value = error
  }
}

</script>

