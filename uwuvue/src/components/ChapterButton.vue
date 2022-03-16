<template>
  <div class="d-grid">
    <button v-on:click="toggle" v-bind:class="buttonClass" :disabled="loading" class="btn overflow-hidden">
      <span v-if="loading" class="spinner-border" role="status"/>
      <h2 v-else>{{chapter.order}}</h2>
      
      <p class="small">{{chapter.title}}</p>
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
