<template>
  <div class="menu bg-primary-content min-w-96 h-screen pt-8 p-0">
    <ul>
      <li
        class="btn btn-primary text-2xl border-0 mb-0.5 w-full"
        @click="showIntro"
      >
        Intro
      </li>
      <li
        v-for="topic in course.topics"
        :key="topic.id"
        class="mb-0.5 transition-all duration-300"
        :class="{
          'hover:opacity-100 bg-primary-focus transform scale-105': selectedTopic === topic.id,
        }"
      >
        <div
          class="btn btn-primary text-2xl border-0 w-full flex justify-between items-center relative"
          @click="toggleTopic(topic)"
        >
          <p>{{ topic.title }}</p>
          <svg
            class="w-6 h-6 transform transition-transform duration-300"
            :class="{ 'rotate-180': selectedTopic === topic.id }"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M19 9l-7 7-7-7"
            ></path>
          </svg>
          <div
            class="text-xl text-white absolute inset-0 rounded-full transform scale-0 transition-all duration-300 text-center p-2"
            :class="{
              'bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500 scale-105': selectedTopic === topic.id,
            }"
          ><p>{{ topic.title }}</p></div>
        </div>
        <div
          v-show="selectedTopic === topic.id"
          class="flex flex-col gap-0 p-0 transition-all duration-300 overflow-hidden"
          :class="{ 'max-h-screen': selectedTopic === topic.id }"
        >
          <div
            v-for="test in topic.test"
            :key="test.id"
            @click="selectTest(test.id)"
            class="btn text-2xl bg-white border-0 m-0 w-full transition-all duration-300 relative"
            :class="{
              'bg-indigo-200 border-2 border-spacing-1 border-primary': selectedTest === test.id,
            }"
          >
            {{ test.name }}
            <div
              class="absolute inset-0 rounded-md transform scale-0 transition-all duration-300"
              :class="{
                'bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500 scale-105 opacity-30' : selectedTest === test.id,
              }"
            ></div>
          </div>
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
      selectedTopic: null,
      topicTitle: null,
      selectedTest: null,
    };
  },
  methods: {
    toggleTopic(topic) {
      if (this.selectedTopic !== topic.id) {
        this.selectedTopic = topic.id;
        this.topicTitle = topic.title;
        this.selectedTest = null; // Reset selectedTest when a new topic is selected
      }// } else {
      //   this.selectedTopic = null; // Close the dropdown if the same topic is clicked
      // }
    },
    selectTest(id) {
      this.selectedTest = id;
      this.$store.commit('getTopic', this.topicTitle)
      this.Disclaimer(id);
    },
    showIntro() {
      this.selectedTest = null;
      this.selectedTopic = null;
      this.topicTitle = null;
      this.showIntroduction();
    },
  },
};
</script>