<template>
  <div class="row">
    <div class="col-4 col-md-2">
      <favorite-icon :manga="manga"/>
      <img :src="manga.image" class="img-fluid rounded mb-4"/>
    </div>

    <div class="col-8 col-md-7 col-lg-8 mb-4">
      <h1 class="text-primary">{{manga.name}}</h1>
      <p>{{manga.author}} - {{manga.date}}</p>
      <p>{{manga.description}}</p>
    </div>

    <div class="col mb-4" v-if="isAdmin">
      <div class="row mb-2">
        <router-link :to="'/mangas/' + this.$route.params.id + '/edit/'" class="btn btn-primary">
          edit manga
        </router-link>
      </div>

      <div class="row">
        <router-link :to="'/mangas/' + this.$route.params.id + '/add/'" class="btn btn-primary">
          add chapter
        </router-link>
      </div>
    </div>
  </div>

  <div class="row mb-4">
    <div class="col">
      <progress-bar :manga="manga"/>
    </div>
  </div>

  <div class="row gy-4 gx-3 gx-md-4">
    <div v-for="(chapter, index) in chapters" :key="index" class="col-6 col-sm-4  col-md-3 col-lg-2 d-flex align-items-stretch">
      <chapter-button :chapter="chapter" @toggle="fetch"/>
    </div>
  </div>
</template>

<script>
import api from '@/api'

import ChapterButton from '@/components/ChapterButton.vue'
import ProgressBar from '@/components/ProgressBar.vue'
import FavoriteIcon from '@/components/FavoriteIcon.vue'

export default {
  name : 'MangaView',

  components: {
    ChapterButton,
    ProgressBar,
    FavoriteIcon
  },

  data() {
    return {
      manga: {},
      chapters: {},
      isAdmin: false
    }
  },

  created() {
    this.fetch()
    this.checkAdmin()
  },

  methods: {
    fetch() {
      api.get(`/mangas/${this.$route.params.id}/`, {
        headers: this.$store.getters.header
      })
      .then(response => {
        this.manga = response.data
      })
      .catch(error => {
        console.log(error)
        this.$router.push('/404')
      })

      api.get(`/mangas/${this.$route.params.id}/get_chapters/`, {
        headers: this.$store.getters.header
      })
      .then(response => {
        this.chapters = response.data
      })
      .catch(error => {
        console.log(error)
      })
    },

    checkAdmin() {
      if (!this.$store.getters.isLogged) {
        this.isAdmin = false
        return
      }

      api.get(`/users/is_admin/`, {
        headers: this.$store.getters.header
      })
      .then(response => {
        this.isAdmin = response.data.is_admin
      })
      .catch((error) => {
        console.log(error);
      })
    }
  }
}
</script>
