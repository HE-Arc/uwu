<template>
  <nav class="navbar fixed-top navbar-expand-lg navbar-dark bg-dark">
    <div class="container-fluid">
      <router-link to="/" class="navbar-brand text-primary">uwu</router-link>

      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarToggle">
        <span class="navbar-toggler-icon text-primary"></span>
      </button>

      <div class="collapse navbar-collapse" id="navbarToggle">
        <div class="navbar-nav">
          <router-link to="/about" class="nav-link">About</router-link>

          <router-link to="/mangas" class="nav-link">Mangas</router-link>
        </div>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  name : 'NavBar',
}
</script>