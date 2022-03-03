<template>
  <div>
    <ul>
      <li v-for="(manga, index) in mangas" :key="index">{{manga.name}}</li>
    </ul>
    <n-button>lol</n-button>
  </div>
</template>

<script>
import api from '@/api'
import { NButton } from 'naive-ui'

export default {
  name : 'MangaView',

  components: {
    NButton
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
