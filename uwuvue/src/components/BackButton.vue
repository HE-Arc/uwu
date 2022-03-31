<template>
  <button v-if="visible" @click="goBack" class="m-3 btn btn-primary position-fixed">
    <i class="bi bi-arrow-left"/>
  </button>
</template>

<script>
export default {
  name : 'BackButton',

  data() {
    return {
      visible: this.$route.path != '/'
    }
  },

  created() {
    this.$watch(
      () => this.$route.path,
      () => {
        console.log(this.$route.path)
        this.visible = this.$route.path != '/'
      }
    )
  },

  methods: {
    goBack() {
      this.$router.back()
      this.visible = false
    }
  }
}
</script>
