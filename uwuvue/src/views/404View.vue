<template>
  <div class="row">
    <div class="col-md">
      <h1>404 Page not found</h1>

      <router-link to="/" class="btn btn-primary">back to home</router-link>
    </div>

    <div class="col-md">
      <img class="img-fluid" src="/404.png"/>
    </div>
  </div>
</template>

<script>
export default {
  name : '404View'
}
</script>