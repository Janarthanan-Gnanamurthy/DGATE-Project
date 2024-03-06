<script setup>
import { RouterLink, RouterView } from 'vue-router'
import Sidebar from './components/Sidebar.vue'
</script>

<template>
  <div>
    <!-- <HelloWorld msg="You did it!" /> -->

    <nav class="navbar bg-primary p-5">
      <RouterLink to="/" class="text-2xl font-bold text-white">Placement Module</RouterLink>
    </nav>
    <RouterView />
  </div>
</template>

<script>
export default {
  components: { Sidebar },
  data(){
    return {
      courses: this.$store.state.courses,
      showsidebar: false,
    }
  },
  beforeCreate(){
    this.$store.dispatch('getCourses')
  }
}

</script>

