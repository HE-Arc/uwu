<template>
  <div class="row">
    <form @submit.prevent="searchPressed" class="col-md-9 col-lg-6">
      <div class="input-group mb-4">
        <input v-model="query" type="search" class="form-control form-control-lg" placeholder="Search mangas">
        
        <button class="btn btn-primary" type="button" disabled v-if="loading">
          <span class="spinner-border spinner-border-sm" role="status"></span>
          loading...
        </button>

        <button type="submit" class="btn btn-primary" v-else>search</button>
      </div>
    </form>

    <div class="col-6 col-md-3 mb-4 ms-auto mt-auto">
      <select v-model="order" @change="search" class="form-select">
        <option value="" selected>Order by</option>
        <option value="name">Name ↑</option>
        <option value="-name">Name ↓</option>
        <option value="date">Date ↑</option>
        <option value="-date">Date ↓</option>
      </select>
    </div>
  </div>

  <div v-if="mangas.length > 0 || loading" class="row">
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
  name : 'SearchView',

  components: {
    MangaThumbnail
  },

  data() {
    return {
      mangas: [],
      query: this.$route.params.query,
      order: '',
      loading: false,
      next: null
    }
  },

  created() {
    this.search()
  },

  methods: {
    searchPressed() {
      this.$router.push({
        name: 'search',
        params: {
          query: this.query
        }
      })
    },

    search() {
      this.loading = true

      api.get('/mangas/', {
        params: {
          search: this.$route.params.query,
          ordering: this.order
        },

        headers: this.$store.getters.header
      })
      .then(response => {
        this.mangas = response.data.results
        this.next = response.data.next
        this.loading = false
      })
      .catch(() => {
        this.loading = false
      })
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
      .catch(() => {
        this.loading = false
      })
    }
  },
}
</script>
