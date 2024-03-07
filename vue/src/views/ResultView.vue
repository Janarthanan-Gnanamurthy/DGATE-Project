<template>
  <main>
    <nav class="navbar bg-indigo-800 font-bold text-2xl text-white pl-5"> Result</nav>
    <div class="container mx-auto p-3 text-2xl w-full">
				<div class="overflow-y-auto p-10">
					<div class="mb-10 flex justify-center"><div :class="getBackgroundClasses(score)" class="radial-progress border-4  font-bold text-2xl" :style="{ '--value': score , '--size': '8rem'}" role="progressbar">{{ score }}</div></div>
					<div v-for="question in test.questions" :key="question.id" class="border-2  border-gray-600 text-2xl rounded-md mb-5" :class="{ 'bg-green-300': selectedOptions[question.id] === question.answer, 'bg-red-300': selectedOptions[question.id] !== question.answer }">
						<p class="p-1 text-xl">Question No: {{ question.id }}</p>
						<div class="border-2 border-gray-600 border-b-0 border-x-0 p-2 w-full rounded-t-md bg-slate-50">
							<p class="mb-3">{{ question.statement }}</p>
							<img v-if="!question.question_uri=='string'" :src="'/static/image/' + question.question_uri" alt="Question {{ question.id }}" width="500" class="p-3 mx-auto" />
						</div>
						<div class="flex flex-col text-xl border-2 border-gray-600 border-x-0 p-3 rounded-b-md">
							<label class="items-center mb-0.5">
								<input type="radio" :name="question.id" class="radio-xs " :value="question.option_a" v-model="selectedOptions[question.id]" disabled/>
								<span class="ml-2">{{ question.option_a }}</span>
							</label>
							<label class="items-center mb-0.5">
								<input type="radio" :name="question.id" class="radio-xs" :value="question.option_b" v-model="selectedOptions[question.id]" disabled/>
								<span class="ml-2">{{ question.option_b }}</span>
							</label>
							<label class="items-center mb-0.5">
								<input type="radio" :name="question.id" class="radio-xs" :value="question.option_c" v-model="selectedOptions[question.id]" disabled/>
								<span class="ml-2">{{ question.option_c }}</span>
							</label>
							<label class="items-center mb-0.5">
								<input type="radio" :name="question.id" class="radio-xs" :value="question.option_d" v-model="selectedOptions[question.id]" disabled/>
								<span class="ml-2">{{ question.option_d }}</span>
							</label>
						</div>
						<div v-if="selectedOptions[question.id]!==question.answer" class="text-xl w-full rounded-md">
							<p class="text-xl p-2 bg-white rounded-b-md">Correct Answer :</p>
							<div
								class="text-xl text-black p-2 w-full border-b-2 border-black rounded-md"
							>
								{{question.answer}}
							</div>
						</div>
						<div class="text-xl rounded-md w-full">
							<p class="p-1 bg-white rounded-b-md">Explanation :</p>
							<div
								class="text-xl text-black p-2 w-full rounded-md"
							>
								{{question.explanation}}
							</div>
						</div>
					</div>
					<br />
				</div>
			</div>
  </main>
</template>

<script>
export default {
  data(){
    return {
      result: this.$store.state.test_result,
      test: this.$store.state.test_result.test,
      selectedOptions: this.$store.state.test_result.selected_options,
      score: this.$store.state.test_result.score
    }
  },
  methods: {
    getBackgroundClasses(score) {
      if (score >= 80) {
        return 'bg-green-400 text-green-700 border-green-400';
      } else if (score >= 30) {
        return 'bg-green-400 text-green-700 border-green-400';
      } else {
        return 'bg-red-300 text-red-600 border-red-300';
      }
    },
  },
	beforeRouteLeave(to, from, next){
		this.$store.commit('deleteTestResult')
		next()

	}
}
</script>