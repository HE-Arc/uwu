<template>
  <div>
    <router-link :to="'/mangas/' + manga.pk">
      <img :src="manga.image" class="img-fluid rounded mb-3"/>
    </router-link>

    <div v-if="manga.progress != null" class="progress">
      <div v-if="manga.progress == 100" :style="progressStyle()" class="progress-bar bg-primary" role="progressbar"/>
      <div v-else :style="progressStyle()" class="progress-bar bg-info" role="progressbar"/>
    </div>

    <p class="p-1">{{manga.name}}</p>
  </div>
</template>

<script>
export default {
  name: 'MangaThumbnail',

  props: {
    manga: Object
  },

  methods: {
    progressStyle() {
      return 'width: ' + this.manga.progress + '%'
    }
  }
}
</script>