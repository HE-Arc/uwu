<template>
  <div class="row">
    <div class="col-md-4 col-lg-6"/>

    <form @submit.prevent="addChapter" class="col-md-8 col-lg-6">
      <div v-if="message" class="alert alert-info mb-2">{{message}}</div>

      <div class="form-group mb-2">
        <label for="nameInput">Chapter name *</label>
        <input v-model="name" type="text" required class="form-control" id="nameInput" placeholder="chapter"/>
      </div>

      <div class="form-group mb-2">
        <label for="pagesInput">Number of pages *</label>
        <input v-model="page_nb" type="number" required class="form-control" id="pagesInput" placeholder="pages"/>
      </div>

      <div class="form-group mb-2">
        <label for="orderInput">Chapter order</label>
        <input v-model="order" type="number" class="form-control" id="orderInput" placeholder="order"/>
      </div>

      <button class="btn btn-primary mb-2" type="button" disabled v-if="loading">
        <span class="spinner-border spinner-border-sm" role="status"/>
        loading...
      </button>

      <button type="submit" class="btn btn-primary mb-2 me-2" v-else>add chapter</button>
    </form>
  </div>
</template>

<script>
import api from '@/api'

export default {
  name : 'AddChapterView',

  data() {
    return {
      name: '',
      order: '',
      page_nb: null,
      message: '',
      loading: false
    }
  },

  methods: {
    addChapter() {
      if (this.name == '' || this.page_nb == '') {
        this.error = 'Inputs can\'t be empty'
        return
      }

      this.message = ''
      this.loading = true

      let data = {
        'title': this.name,
        'page_nb': this.page_nb
      }

      if (this.order != '') {
        data['order'] = this.order
      }

      api.post(`/mangas/${this.$route.params.id}/add_chapter/`, data, {
        headers: this.$store.getters.header
      })
      .then(() => {
        this.name = '',
        this.order = null,
        this.page_nb = null,
        this.message = "Chapter added"
        this.loading = false
      })
      .catch(error => {
        console.log(error)
        this.loading = false
      })
    }
  }
}
</script>
