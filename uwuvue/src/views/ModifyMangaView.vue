<template>
  <div class="row">
    <div class="col-md-4 col-lg-6"/>

    <form @submit.prevent="modifyManga" class="col-md-8 col-lg-6">
      <div v-if="error" class="alert alert-info mb-2">{{error}}</div>

      <div class="form-group mb-2">
        <label for="nameInput">Manga name *</label>
        <input v-model="name" type="text" required class="form-control" id="nameInput" placeholder="manga"/>
      </div>

      <div class="form-group mb-2">
        <label for="authorInput">Author name *</label>
        <input v-model="author" type="text" required class="form-control" id="authorInput" placeholder="author"/>
      </div>

      <div class="form-group mb-2">
        <label for="dateInput">Date *</label>
        <input v-model="date" type="date" required class="form-control" id="dateInput"/>
      </div>

      <div class="form-group mb-2">
        <label for="descriptionInput">Description *</label>
        <textarea v-model="description" class="form-control" id="descriptionInput" placeholder="description"/>
      </div>

      <div class="form-group mb-3">
        <label for="pictureInput">Manga picture</label>
        <input type="file" class="form-control" accept=".jpg, .jpeg, .png" @change="pictureChanged" id="pictureInput"/>
      </div>

      <button class="btn btn-primary mb-2" type="button" disabled v-if="loading">
        <span class="spinner-border spinner-border-sm" role="status"/>
        loading...
      </button>

      <button type="submit" class="btn btn-primary mb-2 me-2" v-else>modify manga</button>
    </form>
  </div>
</template>

<script>
import api from '@/api'

export default {
  name : 'ModifyMangaView',

  data() {
    return {
      picture: null,
      name: '',
      author: '',
      date: '',
      description: '',
      url: '',
      error: '',
      loading: false
    }
  },

  created() {
    if (!this.$store.getters.isLogged) {
      this.$router.push('/404')
      return
    }

    api.get(`/users/is_admin/`, {
      headers: this.$store.getters.header
    })
    .then(response => {
      if (!response.data.is_admin) {
        this.$router.push('/404')
      }
    })
    .catch((error) => {
      console.log(error)
      this.$router.push('/404')
    })

    api.get(`/mangas/${this.$route.params.id}/`, {
      headers: this.$store.getters.header
    })
    .then(response => {
      let manga = response.data
      this.name = manga.name
      this.author = manga.author
      this.date = manga.date
      this.url = manga.url
      this.description = manga.description
    })
    .catch(error => {
      console.log(error)
      this.$router.push("/404")
    })
  },

  methods: {
    pictureChanged(event) {
      this.picture = event.target.files[0]
    },

    modifyManga() {
      if (this.name == '' || this.author == '' || this.date == '') {
        this.error = 'Inputs can\'t be empty'
        return
      }

      this.error = ''
      this.loading = true

      let data =  new FormData()
      data.append('name', this.name)
      data.append('author', this.author)
      data.append('date', this.date)
      data.append('description', this.description)

      if (this.picture) {
        data.append('image', this.picture)
      }

      let headers = this.$store.getters.header
      headers['Content-Type'] = 'multipart/form-data'

      api.put(`/mangas/${this.$route.params.id}/`, data, {
        headers: headers
      })
      .then(response => {
        let pk = response.data.pk
        this.$router.push(`/mangas/${pk}`)
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
