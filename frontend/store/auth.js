export const state = () => ({
  username: null,
  firstName: null, 
  lastName: null, 
  id: null,
  email: null,
  isAuthenticated: false,
  isStaff: false
})

export const mutations = {
  setUsername(state, username) {
    state.username = username
  },
  setEmail(state, email) {
    state.email = email
  },
  setUserId(state, userId) {
    state.id = userId
  },
  clearUsername(state) {
    state.username = null
  },
  clearEmail(state) {
    state.email = null
  },
  setAuthenticated(state, isAuthenticated) {
    state.isAuthenticated = isAuthenticated
  },
  setIsStaff(state, isStaff) {
    state.isStaff = isStaff
  },
  setFirstName(state, firstName) {
    state.firstName = firstName
  },
  setLastName(state, lastName) {
      state.lastName = lastName
  },
  clearFirstName(state) {
      state.firstName = null
  },
  clearLastName(state) {
      state.lastName = null
  }
}

export const getters = {
  isAuthenticated(state) {
    return state.isAuthenticated
  },
  getUsername(state) {
    return state.username
  },
  getEmail(state) {
    return state.email
  },
  getUserId(state) {
    return state.id
  },
  isStaff(state) {
    return state.isStaff
  },
  getFirstName(state) {
    return state.firstName
  },
  getLastName(state) {
      return state.lastName
  }
}

export const actions = {
  async authenticateUser({ commit }, authData) {
    try {
      await this.$repositories.auth.login(authData.username, authData.password)
      commit('setAuthenticated', true)
    } catch (error) {
      throw new Error('The credential is invalid')
    }
  },
  async fetchSocialLink() {
    return await this.$repositories.auth.socialLink()
  },
  async initAuth({ commit }) {
    try {
      const user = await this.$repositories.user.getProfile()
      commit('setAuthenticated', true)
      commit('setUsername', user.username)
      commit('setFirstName', user.firstName) 
      commit('setLastName', user.lastName)   
      commit('setEmail', user.email)
      commit('setUserId', user.id)
      commit('setIsStaff', user.isStaff)
    } catch {
      commit('setAuthenticated', false)
      commit('setIsStaff', false)
    }
  },
  async logout({ commit }) {
    await this.$repositories.auth.logout()
    commit('setAuthenticated', false)
    commit('setIsStaff', false)
    commit('clearUsername')
  },
  async updateUsername({ commit }, newUsername) {
    try {
      await this.$repositories.user.updateUsername(newUsername)
      commit('setUsername', newUsername)
    } catch (error) {
      throw new Error('Erro ao atualizar nome de usuário')
    }
  },
  async updatePassword(_, { oldPassword, newPassword }) {
    try {
      await this.$repositories.user.updatePassword(oldPassword, newPassword);
    } catch (error) {
      throw new Error('Erro ao atualizar senha');
    }
  },  
  async updateEmail({ commit }, newEmail) {
    try {
      await this.$repositories.user.updateEmail(newEmail)  // Chama o backend
      commit('setEmail', newEmail)  // Atualiza no Vuex
    } catch (error) {
      throw new Error('Erro ao atualizar email')
    }
  },
  async updateFirstName({ commit }, newFirstName) {
    try {
        await this.$repositories.user.updateFirstName(newFirstName)
        commit('setFirstName', newFirstName)
    } catch (error) {
        throw new Error('Error updating first name')
    }
  },
  async updateLastName({ commit }, newLastName) {
      try {
          await this.$repositories.user.updateLastName(newLastName)
          commit('setLastName', newLastName)
      } catch (error) {
          throw new Error('Error updating last name')
      }
  },
}
