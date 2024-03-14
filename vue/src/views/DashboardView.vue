<script setup>
import Sidebar from '../components/Sidebar.vue'
</script>

<template>
  <main class="flex bg-gray-100 min-h-screen">
    <!-- Adjust the Sidebar component as needed -->
    <Sidebar />
    <div class="bg-white rounded-lg shadow-md p-6 w-full">
      <h2 class="text-xl font-bold mb-4">My Progress</h2>

      <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
        <div class="bg-gray-100 rounded-lg p-4">
          <h3 class="text-lg font-semibold mb-2">Overall Progress</h3>
          <div class="h-4 w-full bg-gray-300 rounded-full overflow-hidden">
            <div class="bg-blue-500 h-4" :style="{ width: `${overallProgress}%` }"></div>
          </div>
          <p class="mt-2 text-gray-600">{{ overallProgress }}% Complete</p>
        </div>

        <div class="bg-gray-100 rounded-lg p-4">
          <h3 class="text-lg font-semibold mb-2">Completed Courses</h3>
          <p class="text-4xl font-bold text-blue-500">{{ completedCourses }}</p>
        </div>

        <div class="bg-gray-100 rounded-lg p-4">
          <h3 class="text-lg font-semibold mb-2">Completed Tests</h3>
          <p class="text-4xl font-bold text-blue-500">{{ completedTests }}</p>
        </div>
      </div>

      <div class="mt-8">
        <h3 class="text-lg font-semibold mb-4">Course Progress</h3>
        <div v-for="course in courses" :key="course.id" class="mb-4">
          <h4 class="text-base font-semibold">{{ course.name }}</h4>
          <div class="h-4 w-full bg-gray-300 rounded-full overflow-hidden">
            <div class="bg-blue-500 h-4" :style="{ width: `${course.progress}%` }"></div>
          </div>
          <p class="mt-2 text-gray-600">{{ course.progress }}% Complete</p>
        </div>
      </div>
    </div>
  </main>


  
</template>

<script>

export default {
  data() {
    return {
      currentTopic: null
    }
  },
}
</script>
