<template>
  <div class="row">
    <div class="col-12 col-md-9 col-lg-10">
      <h1 class="text-primary">uwu</h1>
    </div>

    <div class="col mb-4" v-if="isAdmin">
      <div class="row mb-2">
        <router-link :to="'/mangas/add/'" class="btn btn-primary">add manga</router-link>
      </div>
    </div>
  </div>

  <h2>Recently updated</h2>

  <div v-if="mangas.length > 0 || loading" class="row mt-4">
    <div v-for="(manga, index) in mangas" :key="index" class="col-6 col-md-3 col-lg-2">
      <manga-thumbnail :manga="manga"/>
    </div>
  </div>

  <div v-else class="row">
    <div class="alert alert-primary col-lg-6" role="alert">No result</div>
  </div>

  <div v-if="next" class="text-center">
    <button @click="moreResult" class="btn btn-primary mt-4">
      more results
    </button>
  </div>
</template>

<script>
import api from '@/api'

import MangaThumbnail from '@/components/MangaThumbnail.vue'

export default {
  name: 'HomeView',

  components: {
    MangaThumbnail
  },

  data() {
    return {
      mangas: [],
      query: this.$route.params.query,
      loading: false,
      isAdmin: false,
      next: null
    } 
  },

  created() {
    this.fetch()
    this.checkAdmin()

    this.$watch(
      () => this.$store.getters.isLogged,
      () => {
        this.checkAdmin()
      }
    )
  },

  methods: {
    fetch() {
      this.loading = true

      api.get('/mangas/', {
        headers: this.$store.getters.header
      })
      .then(response => {
        this.mangas = response.data.results
        this.next = response.data.next
        this.loading = false
      })
      .catch(() =>
        this.loading = false
      )
    },

    moreResult() {
      this.loading = true

      api.get(this.next, {
        headers: this.$store.getters.header
      })
      .then(response => {
        this.mangas.push.apply(this.mangas, response.data.results)
        this.next = response.data.next
        this.loading = false
      })
      .catch(() =>
        this.loading = false
      )
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
