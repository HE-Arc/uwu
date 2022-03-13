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

          <router-link to="/search" class="nav-link">search</router-link>
        </div>
        
        <div class="navbar-nav">
          <router-link to="/user" v-if="this.$store.getters.isLogged" class="nav-link">user</router-link>
          <a @click="logOut()" href="#" v-if="this.$store.getters.isLogged" class="nav-link">logout</a>
          <router-link to="/login" v-else class="nav-link">login</router-link>
        </div>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  name : 'NavBar',

  methods: {
    logOut() {
      this.$store.dispatch('logOut')
    }
  }
}
</script>