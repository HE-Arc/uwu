<template>
  <nav class="navbar sticky-top navbar-expand-md navbar-dark bg-dark">
    <div class="container-fluid">
      <router-link to="/" class="navbar-brand text-primary">uwu</router-link>

      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarToggle">
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse" id="navbarToggle">
        <div class="navbar-nav me-auto">
          <router-link to="/about" class="nav-link">about</router-link>
          <router-link to="/user" v-if="this.$store.getters.isLogged" class="nav-link">user</router-link>
        </div>
        
        <div class="navbar-nav">
          <form v-if="$route.name != 'search'" @submit.prevent="searchPressed" class="mb-2 mb-md-0 me-md-2">
            <div class="input-group">
              <input v-model="query" class="form-control" type="search" placeholder="Search mangas"/>
              <button class="btn btn-primary" type="submit">search</button>
            </div>
          </form>

          <button v-on:click="logOut" v-if="this.$store.getters.isLogged" class="btn btn-outline-primary">logout</button>
          <router-link to="/login" v-else class="btn btn-outline-primary">login</router-link>
        </div>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  name : 'NavBar',

  data() {
    return {
      query: ''
    }
  },

  methods: {
    logOut() {
      this.$store.dispatch('logOut')
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