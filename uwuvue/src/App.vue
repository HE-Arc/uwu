<template>
  <nav-bar/>
  <back-button/>
  
  <main class="container p-5">
    <router-view/>
  </main>

  <top-button/>
</template>

<script>
import NavBar from '@/components/NavBar.vue'
import BackButton from '@/components/BackButton.vue'
import TopButton from '@/components/TopButton.vue'

export default {
  components: {
    NavBar,
    BackButton,
    TopButton
  },

  created() {
    this.$store.dispatch('initialize')
  }
}
</script>

