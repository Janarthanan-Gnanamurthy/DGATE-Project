<script setup>
import Sidebar from '../components/Sidebar.vue'
</script>

<template>
  <main class="flex bg-gray-100 min-h-screen">
    <!-- Adjust the Sidebar component as needed -->
    <Sidebar />

    <div class="flex-1 p-6">
      <h1 class="text-3xl font-semibold mb-6">Courses</h1>

      <div class="flex flex-wrap gap-4">
        <div
          v-for="course in courses"
          :key="course.id"
          class="card w-96 h-60 bg-primary text-primary-content shadow-md hover:cursor-pointer hover:opacity-75"
          @click="selectCourse(course.id)"
        >
          <div class="card-body">
            <h2 class="card-title text-2xl font-semibold">{{ course.title }}</h2>
            <p class="text-gray-300 mt-2">{{ course.description }}</p>
          </div>
        </div>
      </div>

      <div v-if="showLoader" class="fixed z-50 inset-0 overflow-y-auto">
        <div class="flex items-center justify-center min-h-screen bg-black bg-opacity-15">
          <div class="loader-container">
            <div class="loader">
              <span class="loading loading-spinner loading-lg"></span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </main>
</template>



<script>
export default {
  data(){
    return {
      courses: this.$store.state.courses,
      showLoader: false
    }
  },
  methods:{
    async selectCourse(courseId) {
			try {
        this.showLoader = true
				await this.$store.dispatch('getCourse', courseId);

        this.$router.push('/course');
			} catch (error) {
				console.error('Error in redirect method:', error);
			}
		}
  }
}

</script>