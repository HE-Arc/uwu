<template>
  <ul>
    <li v-for="(manga, index) in mangas" :key="index">{{manga.name}}</li>
  </ul>
</template>

<script>
import api from '@/api'

export default {
  name : 'MangaView',

  components: {
  },

  data() {
    return {
      manga: null
    }
  },

  created() {
      api.get('/mangas/', {
        headers: {
          Authorization: this.$store.getters.headerToken
        }
      })
      .then(response => {
        console.log(response.data.results)
        this.mangas = response.data.results
      })
      .catch(error => {
        console.log(error.response.data)
      })
  }
}
</script>
