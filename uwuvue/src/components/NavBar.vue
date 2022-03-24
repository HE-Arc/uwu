<template>
  <nav class="navbar sticky-top navbar-expand-md navbar-dark bg-dark">
    <div class="container-fluid">
      <router-link to="/" class="navbar-brand text-primary" @click="hideNavBar">uwu</router-link>

      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarCollapse" id="lol">
        <span class="navbar-toggler-icon"/>
      </button>

      <div class="collapse navbar-collapse" id="navbarCollapse">
        <div class="navbar-nav me-auto" @click="hideNavBar">
          <router-link to="/about" class="nav-link">about</router-link>
          <router-link to="/search/users" class="nav-link">search users</router-link>
          <router-link to="/user" v-if="this.$store.getters.isLogged" class="nav-link">user</router-link>
        </div>
        
        <div class="navbar-nav">
          <form v-if="$route.name != 'search'" @submit.prevent="searchPressed" class="mb-2 mb-md-0 me-md-2">
            <div class="input-group">
              <input v-model="query" class="form-control" type="search" placeholder="Search mangas"/>
              <button class="btn btn-primary" type="submit" @click="hideNavBar">search</button>
            </div>
          </form>

          <button @click="logOut" v-if="this. $store.getters.isLogged" class="btn btn-outline-primary">logout</button>
          <router-link to="/login" v-else class="btn btn-outline-primary" @click="hideNavBar">login</router-link>
        </div>
      </div>
    </div>
  </nav>
</template>

<script>
import { Collapse } from 'bootstrap'

export default {
  name : 'NavBar',

  data() {
    return {
      query: ''
    }
  },

  mounted() {
    let navbar = document.getElementById('navbarCollapse')
    this.collapse = new Collapse(navbar, { toggle: false })
  },

  methods: {
    hideNavBar() {
      this.collapse.hide()
    },

    logOut() {
      this.$store.dispatch('logout')
      this.collapse.hide()
    },

    searchPressed() {
      this.$router.push({
        name: 'search',
        params: {
          query: this.query
        }
      })

      this.query = ''
    }
  }
}
</script>

<style scoped>
.navbar-toggler-icon {
   background-image: url("data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 30 30'><path stroke='rgba(255, 222, 222, 1)' stroke-linecap='round' stroke-miterlimit='10' stroke-width='2' d='M4 7h22M4 15h22M4 23h22'/></svg>") !important;
}
</style>