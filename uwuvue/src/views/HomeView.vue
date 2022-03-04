<template>
  <div class="home">
    <img alt="Vue logo" src="../assets/logo.png">
    <HelloWorld msg="Welcome to Your Vue.js App"/>
  </div>
</template>

<script>
import HelloWorld from '@/components/HelloWorld.vue'
import api from '@/api'

export default {
  name: 'HomeView',
  components: {
    HelloWorld
  },
  created() {
    console.log(this.$store.getters.headerToken)
    api.get('/users/', {
      headers: {
        Authorization: this.$store.getters.headerToken
      }
    })
    .then(response => {
      console.log(response.data.results)
      this.mangas = response.data.results
    })
    .catch(error => {
      console.log(error)
    })
  }
}
</script>
