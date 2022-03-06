<template>
  <nav-bar/>
  <main class="container p-5 p">
  <router-view/>
  </main>
</template>

<script>
import NavBar from '@/components/NavBar.vue'

export default {
  components: {
    NavBar,
  },

  created() {
    this.$store.dispatch('initialize')
  }
}
</script>

