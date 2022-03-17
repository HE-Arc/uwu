<template>
  <div class="d-grid">
    <button v-on:click="toggle" :class="buttonClass" :disabled="loading || !$store.getters.isLogged" 
      class="btn square-box">
      <div class="square-content p-2">
        <span v-if="loading" class="spinner-border" role="status"/>
        <h2 v-else>{{chapter.order}}</h2>
        
        <p class="small">{{chapter.title}}</p>
      </div>
    </button>
  </div>
</template>

<script>
import api from '@/api'

export default {
  name: 'ChapterButton',

  props: {
    chapter: Object
  },

  data() {
    return {
      loading: false
    }
  },

  computed: {
    buttonClass: function() {
      if (this.chapter.isReaded)
      {
        return 'btn-primary'
      }

      return 'btn-secondary'
    }
  },

  methods: {
    toggle() {
      this.loading = true

      api.post(`/chapters/${this.chapter.pk}/add_remove_to_read/`, {}, {
        headers: this.$store.getters.header
      })
      .then(() => {
        this.loading = false
        this.$emit('toggle')
      })
      .catch(error => {
        this.loading = false
        console.log(error)
      })
    }
  }
}
</script>

<style scoped>
/* black magic from http://jsfiddle.net/38Tnx/1425/ */

.square-box {
  position: relative;
  overflow: hidden;
}

.square-box:before {
  content: "";
  display: block;
  padding-top: 100%;
}

.square-content {
  position: absolute;
  top: 0;
  left: 0;
  bottom: 0;
  right: 0;
}
</style>