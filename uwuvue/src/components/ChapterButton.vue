<template>
  <div class="d-grid">
    <button v-on:click="toggle" class="btn btn-primary overflow-hidden">
      <h2>1</h2>
      
      <p class="small">{{chapter}}</p>
    </button>
  </div>
</template>

<script>
export default {
  name: 'ChapterButton',

  props: {
    chapter: Object
  },

  methods: {
    toggle() {
      
    }
  }
}
</script>
