<template>
  <nav-bar/>
  
  <main class="container p-5 p">
    <router-view/>
  </main>

  <top-button/>
</template>

<script>
import NavBar from '@/components/NavBar.vue'
import TopButton from '@/components/TopButton.vue'

export default {
  components: {
    NavBar,
    TopButton
  },

  created() {
    this.$store.dispatch('initialize')
  }
}
</script>

