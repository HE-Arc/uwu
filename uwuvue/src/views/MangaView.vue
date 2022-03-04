<template>
  <div>
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
