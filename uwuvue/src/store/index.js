import { createStore } from 'vuex'

export default createStore({
  state: {
    token: ''
  },

  getters: {
    isLogged(state) {
      return state.token != '';
    },

    headerToken(state) {
      return `Token ${state.token}`
    },

    header(state, getters) {
      if (getters.isLogged) {
        return {
          Authorization: getters.headerToken
        }
      }

      return {}
    }
  },

  mutations: {
    INITIALIZE(state) {
      if (localStorage.getItem('token')) {
        state.token = localStorage.getItem('token')
      }
    },

    SET_TOKEN(state, token) {
      state.token = token
      localStorage.setItem('token', token)
    },

    UNSET_TOKEN(state) {
      state.token = ''
      localStorage.removeItem('token')
    }
  },

  actions: {
    initialize({ commit }) {
      commit('INITIALIZE')
    },

    login({ commit }, payload) {
      commit('SET_TOKEN', payload.token)
    },

    logout({ commit }) {
      commit('UNSET_TOKEN')
    }
  },

  modules: {
  }
})
