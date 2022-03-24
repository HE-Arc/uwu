<template>
  <div class="row">
    <div class="col-md-4 col-lg-6"/>
    <form @submit.prevent="signup" class="col-md-8 col-lg-6">
      <div v-if="error" class="alert alert-info mb-2">{{error}}</div>

      <div class="form-group mb-2">
        <label for="pictureInput">Profile picture</label>
        <input type="file" class="form-control" accept=".jpg, .jpeg, .png" @change="pictureChanged" id="pictureInput">
      </div>

      <div class="form-group mb-2">
        <label for="userInput">Username</label>
        <input v-model="username" type="text" required class="form-control" id="userInput" placeholder="username">
      </div>

      <div class="form-group mb-2">
        <label for="passwordInput">Password</label>
        <input v-model="password" type="password" required class="form-control" id="passwordInput" placeholder="password">
      </div>

      <div class="form-group mb-2">
        <label for="repeatInput">Repeat password</label>
        <input v-model="repeatPassword" type="password" required class="form-control" id="repeatInput" placeholder="password">
      </div>

      <button class="btn btn-primary mb-2" type="button" disabled v-if="loading">
        <span class="spinner-border spinner-border-sm" role="status"></span>
        loading...
      </button>
      <button type="submit" class="btn btn-primary mb-2 me-2" v-else>sign up</button>
      <router-link to="/login">Already have an account?</router-link>
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
      picture: null,
      username: '',
      password: '',
      repeatPassword: '',
      error: '',
      loading: false
    }
  },

  methods: {
    pictureChanged(event) {
      this.picture = event.target.files[0]
    },

    signup() {
      if (this.username == '' || this.password == '' || this.repeatPassword == '') {
        this.error = 'Inputs can\'t be empty'
        return;
      }

      if (this.password != this.repeatPassword) {
        this.error = 'Passwords don\'t match'
        return;
      }

      this.error = ''
      this.loading = true

      let data =  new FormData();
      data.append('username', this.username)
      data.append('password', this.password)

      if (this.picture) {
        data.append('image', this.picture)
      }

      api.post('/users/', data, {
        headers: { "Content-Type": "multipart/form-data" }
      })
      .then(response => {
        this.$store.dispatch('login', {
          token: response.data.token
        })

        this.$router.go(-1)
        this.loading = false
      })
      .catch(error => {
        if (error.response) {
          this.error = error.response.data.status
        }

        this.loading = false
      })
    }
  }
}
</script>
