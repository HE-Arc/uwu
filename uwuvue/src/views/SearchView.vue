<template>
  <div class="row">
    <form @submit.prevent="searchPressed" class="col-md-9 col-lg-6">
      <div class="input-group mb-3">
          <input v-model="query" type="text" class="form-control form-control-lg" placeholder="Search mangas">
          
          <button class="btn btn-primary" type="button" disabled v-if="loading">
            <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
            loading...
          </button>
          <button type="submit" class="btn btn-primary" v-else>search</button>
      </div>
    </form>
  </div>

  <div class="row">
    <div v-for="(manga, index) in mangas" :key="index" class="col-6 col-md-3 col-lg-2">
      <div class="image">
        <router-link v-bind:to="'/mangas/' + manga.id">
          <img v-bind:src="manga.image" class="img-fluid rounded"/>
        </router-link>

        <p class="p-1">{{manga.name}}</p>
      </div>
    </div>
  </div>
</template>

<script>
import api from '@/api'

export default {
  name : 'SearchView',

  data() {
    return {
      mangas: [],
      query: '',
      loading: false
    }
  },

  created() {
    this.search()

    this.$watch(
      () => this.$route.params,
      () => {
        this.search()
      }
    )
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
          search: this.$route.params.query
        }
      })
      .then(response => {
        this.mangas = response.data.results
        this.loading = false
      })
      .catch(() =>
        this.loading = false
      )
    }
  },
}
</script>
