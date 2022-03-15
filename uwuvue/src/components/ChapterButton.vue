<template>
  <div class="d-grid">
    <button class="btn btn-primary square">
      {{chapter}}
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
  }
}
</script>
