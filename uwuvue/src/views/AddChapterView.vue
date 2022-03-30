<template>
  <div class="row">
    <div class="col-md-4 col-lg-6"/>

    <form @submit.prevent="addChapter" class="col-md-8 col-lg-6">
      <div v-if="message" class="alert alert-info mb-2">{{message}}</div>

      <div class="form-group mb-2">
        <label for="nameInput">Chapter name</label>
        <input v-model="name" type="text" required class="form-control" id="nameInput" placeholder="chapter"/>
      </div>

      <div class="form-group mb-2">
        <label for="orderInput">Chapter order</label>
        <input v-model="order" type="number" required class="form-control" id="orderInput" placeholder="order"/>
      </div>

      <div class="form-group mb-2">
        <label for="pagesInput">Chapter order</label>
        <input v-model="page_nb" type="number" required class="form-control" id="pagesInput" placeholder="pages"/>
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
      page_nb: '',
      message: '',
      loading: false
    }
  },

  methods: {
    addChapter() {
      if (this.name == '' || this.order == '' || this.page_nb == '') {
        this.error = 'Inputs can\'t be empty'
        return
      }

      this.message = ''
      this.loading = true

      let data = {
        'manga_id': this.$route.params.id,
        'title': this.name,
        'order': this.order,
        'page_nb': this.page_nb
      }

      api.post('/chapters/', data, {
        headers: this.$store.getters.header
      })
      .then(() => {
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
