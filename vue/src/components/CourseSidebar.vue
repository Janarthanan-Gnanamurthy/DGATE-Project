<template>
  <div class="menu bg-primary-content min-w-96 h-screen pt-8 p-0">
    <ul>
      <li class="btn btn-primary text-2xl border-0 mb-0.5 w-full" @click="showIntroduction">Intro</li>
      <li v-for="topic in course.topics" :key="topic.id" @click="toggleTests(topic)" class="mb-0.5">
        <div class="btn btn-primary text-2xl border-0"><p>{{ topic.title }}</p></div>
        <div v-show="selectedTopic === topic.id" class="flex flex-col gap-0 p-0">
          <div v-for="test in topic.test" :key="test.id" @click="Disclaimer(test.id)" class="btn bg-white text-2xl border-0 m-0 w-full ">{{ test.name }}</div>
        </div>
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  props: ['course', 'showIntroduction', 'Disclaimer'],
  data() {
    return {
      selectedTopic: null
    };
  },
  methods: {
    toggleTests(topic) {
      if (this.selectedTopic !== topic.id) {
        this.selectedTopic = topic.id;
        this.$store.commit('getTopic', topic.title)
      }
    }
  }
};
</script>
