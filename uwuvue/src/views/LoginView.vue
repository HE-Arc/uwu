<template>
  <div class="row">
    <div class="col-md-6"/>
    <form @submit.prevent="logIn" class="col-md-6">
      <div v-if="error" class="alert alert-info m-2">{{error}}</div>

      <div class="form-group m-2">
        <label for="userInput">Username</label>
        <input v-model="username" type="text" class="form-control" id="userInput" placeholder="Username">
      </div>

      <div class="form-group m-2">
        <label for="passwordInput">Password</label>
        <input v-model="password" type="password" class="form-control" id="passwordInput" placeholder="Password">
      </div>

      <button type="submit" class="btn btn-primary m-2">Submit</button>
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
      error: ''
    }
  },

  methods: {
    logIn() {
      if (this.username == '' || this.password == '') {
        this.error = 'Inputs can\'t be empty'
        return;
      }

      this.error = ''

      api.post('/auth/', {
        username: this.username,
        password: this.password
      })
      .then(response => {
        this.$store.dispatch('logIn', {
          token: response.data.token
        })

        this.$router.push({ name: 'home' })
      })
      .catch(() => {
        this.error = 'Wrong username or password'
      })
    }
  },

  created() {
    if (this.$store.getters.isLogged) {
      this.$router.push({ name: 'home' })
    }
  }
}
</script>
