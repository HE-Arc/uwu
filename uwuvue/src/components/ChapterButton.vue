<template>
  <button @click="toggle" :class="buttonClass" class="btn flex-fill overflow-hidden">
    <div class="p-2">
      <span v-if="loading" class="spinner-border" role="status"/>
      <h2 v-else>{{chapter.order}}</h2>
      
      <h6>{{chapter.title}}</h6>
      <p>{{chapter.page_nb}} pages</p>  
    </div>
  </button>
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
      if (!this.$store.getters.isLogged) {
        return
      }

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