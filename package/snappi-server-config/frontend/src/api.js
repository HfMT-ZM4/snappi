import axios from 'axios'

const api = axios.create({
  //baseURL: 'http://' + window.location.hostname + '/api',
  baseURL: 'http://127.0.0.1:8000/api',
})

async function loadConfig() {
  return api.get('/config')
}

async function getPorts() {
  return api.get('/ports')
}

async function saveConfig(config) {
    return api.post('/config', config)
}

async function restartServices(services) {
    return api.post('/restart', services)
}

async function getServiceStatus(services) {
    return api.get('/status')
}

async function getLogs(services, numLines) {
    return api.get('/logs', {
      params: {
        services: services,
        num_lines: numLines,
      },
      paramsSerializer: {
        indexes: null,
      },
    })
}

export default {
  loadConfig,
  saveConfig,
  restartServices,
  getServiceStatus,
  getLogs,
  getPorts,
}
