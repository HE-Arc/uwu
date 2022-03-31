<template>
<div>
    <favorite-icon :manga="manga" v-if="!simple"/>

    <router-link :to="'/mangas/' + manga.pk">
      <img :src="manga.image" class="img-fluid rounded mb-3">
    </router-link>

    <progress-bar :manga="manga"/>

    <p class="p-1 text-center">{{manga.name}}</p>
  </div>
</template>

<script>
import ProgressBar from '@/components/ProgressBar.vue'
import FavoriteIcon from '@/components/FavoriteIcon.vue'

export default {
  name: 'MangaThumbnail',

  components: {
    ProgressBar,
    FavoriteIcon
  },

  props: {
    manga: Object,
    simple: Boolean
  }
}
</script>