<template>
  <div class="row">
    <div class="col-md-4 col-lg-6"/>
    <form @submit.prevent="logIn" class="col-md-8 col-lg-6">
      <div v-if="error" class="alert alert-info mb-2">{{error}}</div>

      <div class="form-group mb-2">
        <label for="userInput">Username</label>
        <input v-model="username" type="text" class="form-control" id="userInput" placeholder="username">
      </div>

      <div class="form-group mb-2">
        <label for="passwordInput">Password</label>
        <input v-model="password" type="password" class="form-control" id="passwordInput" placeholder="password">
      </div>

      <button class="btn btn-primary mb-2" type="button" disabled v-if="loading">
        <span class="spinner-border spinner-border-sm" role="status"></span>
        loading...
      </button>
      <button type="submit" class="btn btn-primary mb-2" v-else>login</button>
    </form>
  </div>
</template>

<script>
import api from '@/api'

export default {
  name : 'MangaView',

  components: {
  },

  data() {
    return {
      username: '',
      password: '',
      error: '',
      loading: false
    }
  },

  methods: {
    logIn() {
      if (this.username == '' || this.password == '') {
        this.error = 'Inputs can\'t be empty'
        return;
      }

      this.error = ''
      this.loading = true

      api.post('/auth/', {
        username: this.username,
        password: this.password
      })
      .then(response => {
        this.$store.dispatch('logIn', {
          token: response.data.token
        })

        this.$router.go(-1)
        this.loading = false
      })
      .catch(() => {
        this.error = 'Wrong username or password'
        this.loading = false
      })
    }
  },

  created() {
    if (this.$store.getters.isLogged) {
      this.$router.go(-1)
    }
  }
}
</script>
