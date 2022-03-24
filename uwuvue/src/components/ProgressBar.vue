<template>
  <div v-if="manga.progress != null" class="progress">
    <div :class="progressClass" :style="progressStyle" class="progress-bar" role="progressbar"/>
  </div>
</template>

<script>
export default {
  name: 'ProgressBar',

  props: {
    manga: Object
  },

  computed: {
    progressStyle: function() {
      return 'width: ' + this.manga.progress + '%'
    },

    progressClass: function() {
      if (this.manga.progress == 100) {
        return 'bg-primary'
      }

      return 'bg-info'
    }
  }
}
</script>