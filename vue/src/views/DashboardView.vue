<script setup>
import Sidebar from '../components/Sidebar.vue'
</script>

<template>
  <main class="flex min-h-screen bg-gradient-to-br from-primary to-secondary">
    <Sidebar />
    <div class="container mx-auto px-4 py-8 flex-1">
      <h1 class="text-4xl font-bold mb-8 text-center text-white">Progress Report</h1>
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        <!-- Course Progress -->
        <div class="card bg-base-100 shadow-xl rounded-2xl">
          <figure class="px-10 pt-10">
            <img src="../assets/course-progress.svg" alt="Course Progress" class="rounded-xl" />
          </figure>
          <div class="card-body">
            <h2 class="card-title text-primary">Course Progress</h2>
            <div v-for="course in courses" :key="course.id" class="text-sm">
              <p class="font-semibold">{{ course.title }}</p>
              <progress
                class="progress progress-primary w-full mb-4"
                :value="calculateCourseProgress(course)"
                max="100"
              >
                {{ calculateCourseProgress(course) }}%
              </progress>
            </div>
          </div>
        </div>

        <!-- Test Results -->
        <div class="card bg-base-100 shadow-xl rounded-2xl h-2/3 overflow-auto">
          <figure class="px-10 pt-10">
            <img src="../assets/test-results.svg" alt="Test Results" class="rounded-xl" />
          </figure>
          <div class="card-body">
            <h2 class="card-title text-success">Test Results</h2>
            <div v-if="results && results.length > 0" class="text-sm">
              <div v-for="result in results" :key="result.id" class="mb-4">
                <p class="font-semibold">Test: {{ result.test_id }}</p>
                <progress
                  class="progress progress-success w-full"
                  :value="result.score"
                  max="100"
                >
                  {{ result.score }}%
                </progress>
              </div>
            </div>
            <p v-else class="text-sm">No test results available</p>
          </div>
        </div>

        <!-- Topic Progress -->
        <div v-if="course && course.topics" class="card bg-base-100 shadow-xl rounded-2xl">
          <figure class="px-10 pt-10">
            <img src="../assets/topic-progress.svg" alt="Topic Progress" class="rounded-xl" />
          </figure>
          <div class="card-body">
            <h2 class="card-title text-info">Topic Progress</h2>
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              <div v-for="topic in course.topics" :key="topic.id" class="text-sm">
                <p class="font-semibold">{{ topic.title }}</p>
                <progress
                  class="progress progress-info w-full"
                  :value="calculateTopicProgress(topic)"
                  max="100"
                >
                  {{ calculateTopicProgress(topic) }}%
                </progress>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </main>
</template>

<script>
import { mapState } from 'vuex'

export default {
  computed: {
    ...mapState(['user', 'course', 'courses', 'results']),
  },
  methods: {
    calculateCourseProgress(course) {
      if (!course || !course.topics) return 0
      const totalTopics = course.topics.length
      const completedTopics = course.topics.filter(
        (topic) => this.calculateTopicProgress(topic) === 100
      ).length
      return (completedTopics / totalTopics) * 100
    },
    calculateTopicProgress(topic) {
      if (!topic || !topic.test) return 0
      const tests = topic.test.length
      let attempted = 0
      for (let i = 0; i < tests; i++) {
        if (topic.test[i].submitted) {
          attempted += 1
        }
      }
      return (attempted / tests) * 100
    },
  },
}
</script>