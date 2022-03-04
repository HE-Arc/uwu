<template>
  <div class="container p-5">
    <ul>
      <li v-for="(manga, index) in mangas" :key="index">{{manga.name}}</li>
    </ul>
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
      mangas: []
    }
  },

  created() {
    api.post('/auth/', {
        username: 'admin',
        password: 'password'
      })
      .then(response => {
        console.log(response.data.token)
        this.$store.dispatch('logIn', {
          token: response.data.token
        })
      })
      .catch(error => {
        console.log(error)
      })

      api.get('/mangas/')
      .then(response => {
        this.mangas = response.data.results
      })
      .catch(error => {
        console.log(error)
      })
  }
}
</script>
