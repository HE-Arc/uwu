<template>
  <button v-if="visible" @click="scrollToTop" class="btn btn-primary position-fixed bottom-0 end-0 m-2">back to top</button>
</template>

<script>
export default {
  name : 'TopButton',

  data() {
    return {
      visible: false
    }
  },

  mounted() {
    window.addEventListener('scroll', this.handleScroll)
  },

  methods: {
    handleScroll() {
      this.visible = window.pageYOffset > window.innerHeight
    },

    scrollToTop() {
      window.scrollTo(0, 0)
    }
  }
}
</script>
