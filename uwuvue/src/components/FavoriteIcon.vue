<template>
  <div class="position-relative">
    <a @click.prevent="toggleFavorite" :class="favoriteClass" href="toggle-fav" v-if="$store.getters.isLogged" 
      class="position-absolute m-2 top-0 start-0 fs-3" role="img"/>
  </div>
</template>

<script>
import api from '@/api'

export default {
  name: 'FavoriteIcon',

  props: {
    manga: Object
  },

  data() {
    return {
      isFavorite: this.manga.isFavorite
    }
  },

  created() {
    this.$watch(
      () => this.manga,
      () => {
        this.isFavorite = this.manga.isFavorite
      }
    )
  },

  computed: {
    favoriteClass: function() {
      if (this.isFavorite) {
        return "bi bi-heart-fill"
      }

      return "bi bi-heart"
    }
  },

  methods: {
    toggleFavorite() {
      api.post(`/mangas/${this.manga.pk}/add_remove_fav/`, {}, {
        headers: this.$store.getters.header
      })
      .then(() => {
        this.isFavorite = !this.isFavorite
      })
    }
  }
}
</script>
