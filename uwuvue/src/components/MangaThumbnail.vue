<template>
  <div>
    <router-link v-bind:to="'/mangas/' + manga.id">
      <img v-bind:src="manga.image" class="img-fluid rounded mb-3"/>
    </router-link>

    <div v-if="manga.progress && manga.progress > 0" class="progress">
      <div v-bind:style="progressStyle()" class="progress-bar bg-info" role="progressbar"/>
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