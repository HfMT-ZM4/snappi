import axios from 'axios'

let host = window.location.hostname
let port = 80

if (import.meta.env.MODE === 'development') {
  host = '127.0.0.1'
  port = 8000
}

const api = axios.create({
  //baseURL: 'http://' + window.location.hostname + '/api',
  baseURL: `http://${host}:${port}/api`,
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

function createWebSocket() {
    return new WebSocket(`ws://${host}:${port}/api/ws`)
}

export default {
  loadConfig,
  saveConfig,
  restartServices,
  getServiceStatus,
  getLogs,
  getPorts,
  createWebSocket,
}
