<template>
  <div class="p-5">
    <h1 class="btn btn-primary text-white m-5"  @click="show=!show">This is an about page</h1>
    <div v-show="show" class="text-2xl font-bold m-5">hello</div>
  </div>
</template>

<script>
export default {
  data(){
    return {
      show: false
    }
  }
}
</script>