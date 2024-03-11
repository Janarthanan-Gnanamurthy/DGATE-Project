<template>
	<main>
		<nav class="navbar bg-indigo-800 font-bold text-2xl text-white pl-5">{{ $store.state.course.title }} : {{ $store.state.topic }}</nav>
		<nav class="navbar justify-center bg-indigo-900 font-bold text-2xl text-white pl-5" >
			<p>Time remaining:</p>
			<div class="mx-2 bg-white text-black rounded-md p-1 px-2">
				<span class="countdown font-mono text-3xl">
					<span :style="{'--value': minutes }"></span>:
					<span :style="{'--value': seconds }"></span>
				</span>
			</div>
		</nav>
		<div v-if="test.submitted" class="container mx-auto text-center text-4xl mt-28 p-5 font-bold">Test already attempted!</div>
		<div class="flex">
			<div class="w-3/4">
				<div v-if="showQuestions && !test.submitted" class="p-3 text-2xl w-full">
						<div class="overflow-y-auto p-10">
							<div v-if="currentQuestionIndex < test.questions.length">
								<div :key="test.questions[currentQuestionIndex].id" class="border-2 border-gray-600 bg-primary-content text-2xl rounded-md mb-5">
									<p class="p-1 text-xl">Question No: {{currentQuestionIndex + 1}}</p>
									<div class="border-2 border-gray-600 border-b-0 border-x-0 p-2 w-full rounded-t-md bg-slate-50">
										<p class="mb-3">{{ test.questions[currentQuestionIndex].statement }}</p>
										<img v-if="!test.questions[currentQuestionIndex].question_uri=='string'" :src="'/static/image/' + test.questions[currentQuestionIndex].question_uri" alt="Question {{ test.questions[currentQuestionIndex].id }}" width="500" class="p-3 mx-auto" />
									</div>
									<div class="flex flex-col text-xl border-2 border-gray-600 border-b-0 border-x-0 p-3 rounded-b-md">
										<label class="items-center mb-0.5">
											<input type="radio" :name="test.questions[currentQuestionIndex].id" class="radio-xs" :value="test.questions[currentQuestionIndex].option_a" v-model="selectedOptions[test.questions[currentQuestionIndex].id]" required @change="answerQuestion(currentQuestionIndex)"/>
											<span class="ml-2">{{ test.questions[currentQuestionIndex].option_a }}</span>
										</label>
										<label class="items-center mb-0.5">
											<input type="radio" :name="test.questions[currentQuestionIndex].id" class="radio-xs" :value="test.questions[currentQuestionIndex].option_b" v-model="selectedOptions[test.questions[currentQuestionIndex].id]" required @change="answerQuestion(currentQuestionIndex)"/>
											<span class="ml-2">{{ test.questions[currentQuestionIndex].option_b }}</span>
										</label>
										<label class="items-center mb-0.5">
											<input type="radio" :name="test.questions[currentQuestionIndex].id" class="radio-xs" :value="test.questions[currentQuestionIndex].option_c" v-model="selectedOptions[test.questions[currentQuestionIndex].id]" required @change="answerQuestion(currentQuestionIndex)"/>
											<span class="ml-2">{{ test.questions[currentQuestionIndex].option_c }}</span>
										</label>
										<label class="items-center mb-0.5">
											<input type="radio" :name="test.questions[currentQuestionIndex].id" class="radio-xs" :value="test.questions[currentQuestionIndex].option_d" v-model="selectedOptions[test.questions[currentQuestionIndex].id]" required @change="answerQuestion(currentQuestionIndex)"/>
											<span class="ml-2">{{ test.questions[currentQuestionIndex].option_d }}</span>
										</label>
									</div>
								</div>
								<br />
								<button @click="previousQuestion" :disabled="currentQuestionIndex === 0" type="button" class="btn btn-primary text-xl">Previous</button>
								<button
									class="btn btn-primary text-xl mx-2"
									@click="markForReview(currentQuestionIndex)"
								>
									Mark for Review
								</button>
								<button v-if="currentQuestionIndex !== test.questions.length -1 " @click="nextQuestion" type="button" class="btn btn-primary text-xl">Next</button>
								<button v-if="currentQuestionIndex == test.questions.length -1 " type="submit" class="btn btn-primary text-xl" @click="SubmitForm">Submit</button>
							</div>
						</div>
				</div>
			</div>
			<div v-if="showQuestions && !test.submitted" class="bg-gray-200 w-1/4 p-4 h-screen">
				<div class="grid grid-cols-4 gap-2">
					<h3 class="text-xl font-bold mb-4 col-span-4">Questions</h3>
					<div v-for="(question, index) in test.questions" :key="question.id" class="flex items-center justify-center rounded-full text-2xl font-bold cursor-pointer" :class="{
							'bg-green-500 text-white': questionStatus[index] === 'answered',
							'bg-yellow-500 text-white': questionStatus[index] === 'markedForReview',
							'bg-red-500 text-white': questionStatus[index] === 'unanswered',
							'bg-gray-400 text-white': questionStatus[index] === 'unvisited',
							'bg-cyan-500  text-white': questionStatus[index] === 'answeredAndMarked' // Add this line
						}" @click="navigateToQuestion(index)">
						<div class="w-12 h-12 flex items-center justify-center">
							<svg v-if="questionStatus[index] === 'unanswered'" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-6 h-6">
								<path fill-rule="evenodd" d="M2.25 12c0-5.385 4.365-9.75 9.75-9.75s9.75 4.365 9.75 9.75-4.365 9.75-9.75 9.75S2.25 17.385 2.25 12zM12 8.25a.75.75 0 01.75.75v3.75a.75.75 0 01-1.5 0V9a.75.75 0 01.75-.75zm0 8.25a.75.75 0 100-1.5.75.75 0 000 1.5z" clip-rule="evenodd" />
							</svg>
							<svg v-else-if="questionStatus[index] === 'answered'" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-6 h-6">
								<path fill-rule="evenodd" d="M19.916 4.626a.75.75 0 01.208 1.04l-9 13.5a.75.75 0 01-1.154.114l-6-6a.75.75 0 011.06-1.06l5.353 5.354 8.493-12.739a.75.75 0 011.04-.208z" clip-rule="evenodd" />
							</svg>
							<svg v-else-if="questionStatus[index] === 'markedForReview'" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-6 h-6">
								<path fill-rule="evenodd" d="M8.25 6.75a3.75 3.75 0 117.5 0 3.75 3.75 0 01-7.5 0zM15.75 9.75a3 3 0 116 0 3 3 0 01-6 0zM2.25 9.75a3 3 0 116 0 3 3 0 01-6 0zM6.31 15.117A6.745 6.745 0 0112 12a6.745 6.745 0 016.709 7.498.75.75 0 01-.372.568A12.696 12.696 0 0112 21.75c-2.305 0-4.47-.612-6.337-1.684a.75.75 0 01.372-.568 6.787 6.787 0 011.955-3.38z" clip-rule="evenodd" />
							</svg>
							<svg v-else-if="questionStatus[index] === 'answeredAndMarked'" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-6 h-6">
								<path d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
							</svg>
							<svg v-else xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-6 h-6">
								<path d="M12 15a3 3 0 100-6 3 3 0 000 6z" />
								<path fill-rule="evenodd" d="M1.323 11.447C2.811 6.976 7.028 3.75 12.001 3.75c4.97 0 9.185 3.223 10.675 7.69.12.362.12.752 0 1.113-1.487 4.471-5.705 7.697-10.677 7.697-4.97 0-9.186-3.223-10.675-7.69a1.762 1.762 0 010-1.113zM17.25 12a5.25 5.25 0 11-10.5 0 5.25 5.25 0 0110.5 0z" clip-rule="evenodd" />
							</svg>
							{{ index + 1 }}
						</div>
					</div>
				</div>
			</div>
		</div>
		<div v-if="showResult" class="container mx-auto p-3 text-2xl w-full">
			<div class="overflow-y-auto p-10">
				<div class="mb-10 flex justify-center"><div :class="getBackgroundClasses(score)" class="radial-progress border-4  font-bold text-2xl" :style="{ '--value': score , '--size': '8rem'}" role="progressbar">{{ score }}</div></div>
				<div v-for=" [ index, question] of test.questions.entries()" :key="question.id" class="border-2  border-gray-600 text-2xl rounded-md mb-5" :class="{ 'bg-green-300': selectedOptions[question.id] === question.answer, 'bg-red-300': selectedOptions[question.id] !== question.answer }">
					<p class="p-1 text-xl">Question No: {{ index + 1}}</p>
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
			test_id: this.$route.params.testId,
			test: this.$store.state.test,
			showQuestions: true,
			showResult: false,
			timerInterval: null,
			currentQuestionIndex: 0,
      selectedOptions: {},
      totalTimePerQuestion: 60,
			totaltime: 0,
			timer: 0,
			questionStatus: []
		}
	},
	methods:{
		initQuestionStatus() {
			this.questionStatus = Array(this.test.questions.length).fill('unvisited');
			this.questionStatus[0] = 'unanswered'
		},
		updateQuestionStatus(index, status) {
			this.questionStatus.splice(index, 1, status);
		},
		markForReview(index) {
			if (this.questionStatus[index] == 'answered'){
				this.updateQuestionStatus(index, 'answeredAndMarked')
			} else {
				this.updateQuestionStatus(index, 'markedForReview');
			}
		},
		answerQuestion(index) {
			const questionId = this.test.questions[index].id;
			if (this.selectedOptions[questionId]) {
				this.updateQuestionStatus(index, 'answered');
			} else {
				this.updateQuestionStatus(index, 'unanswered');
			}
		},
		navigateToQuestion(index) {
			this.currentQuestionIndex = index;
			if (this.questionStatus[index]=='unvisited'){
				this.updateQuestionStatus(index, 'unanswered')
			}
		},
    nextQuestion() {
      // Move to the next question
      this.currentQuestionIndex++;
			if (!this.selectedOptions[this.currentQuestionIndex]) {
				this.updateQuestionStatus(this.currentQuestionIndex, 'unanswered')
			}
    },
		previousQuestion(){
      if (this.currentQuestionIndex > 0) {
        this.currentQuestionIndex--;
      }
		},
    Timer() {
			if ( !this.test.submitted) {
				this.timer = this.totalTime
				clearInterval(this.timerInterval);
				this.timerInterval = setInterval(() => {
					if (this.timer > 0) {
						this.timer--;
					} else {
						this.currentQuestionIndex = this.test.questions.length
						// this.SubmitForm();
					}
				}, 1000);
			}
    },
    getBackgroundClasses(score) {
      if (score >= 80) {
        return 'bg-green-400 text-green-700 border-green-400';
      } else if (score >= 30) {
        return 'bg-green-400 text-green-700 border-green-400';
      } else {
        return 'bg-red-300 text-red-600 border-red-300';
      }
    },
		calculateScore() {
			let correctCount = 0;

			this.test.questions.forEach((question) => {
				const selectedOption = this.selectedOptions[question.id];
				const correctAnswer = question.answer;

				if (selectedOption === correctAnswer) {
					correctCount++;
				}
			});

			// Calculate percentage
			const totalQuestions = this.test.questions.length;
			const percentage = (correctCount / totalQuestions) * 100;
			this.score = percentage.toFixed(2)

			return percentage.toFixed(2); // Display up to 2 decimal places
  	},
		async SubmitForm(){
			clearInterval(this.timerInterval);
			this.timer = 0;
			const formdata = {
				user_id: 1,
				test_id: this.test_id,
				score: parseFloat(this.calculateScore()),
				selected_options: this.selectedOptions,
				metrics: {course: this.$store.state.course.title, topic: this.$store.state.topic}
			}
			console.log(formdata)
			fetch(`http://localhost:8000/results`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
					// Add other headers if needed
				},
				body: JSON.stringify(formdata)
			})
				.then(response => {
					if (!response.ok) {
						throw new Error(`HTTP error! Status: ${response.status}`);
					}
					return response.json();
				})
				.then(responseData => {
					console.log('Form submitted successfully:', responseData);
					this.showQuestions = false;
					this.showResult = true;

					// PUT request
					return fetch(`http://localhost:8000/test/${this.test_id}`, {
						method: 'PUT'
					});
				})
				.then(putResponse => {
					if (!putResponse.ok) {
						throw new Error(`PUT request error! Status: ${putResponse.status}`);
					}
					// Optionally, handle PUT response
					console.log('PUT request successful:', putResponse);
				})
				.catch(error => {
					console.error('Error submitting form:', error.message);
					// Handle error, show a message to the user, etc.
				});
		},
		handleBeforeUnload(event) {
      // Display an alert or confirmation message
      const confirmationMessage = "Are you sure you want to Reload? Your changes may not be saved.";
      event.returnValue = confirmationMessage; // Standard for most browsers
      return confirmationMessage; // For some older browsers
    },
	},	
	computed: {
    minutes() {
      return Math.floor(this.timer / 60);
    },
    seconds() {
      return this.timer % 60;
    },
	},
	async beforeMount() {
		clearInterval(this.timerInterval);

		const questionsCount = this.test.questions.length;
		this.totalTime = questionsCount > 0 ? this.totalTimePerQuestion * questionsCount : 0;
		
		// Assuming you have a Timer function defined
		this.Timer();
	},
	mounted() {
		this.initQuestionStatus();
		if (this.showQuestions && !this.test.submitted){
			// Prevent going back and reloading the page
			window.addEventListener('beforeunload', this.handleBeforeUnload);
		}
  },
	beforeRouteLeave(to, from, next) {

    if (this.showQuestions && !this.test.submitted) {
      // Display a confirmation message
      const confirmationMessage = "Warning: Your Test will be auto Submitted. If you leave this page.";
      if (window.confirm(confirmationMessage)) {
        // this.SubmitForm();
				clearInterval(this.timerInterval);
				this.$store.commit('deleteTest')
				window.removeEventListener('beforeunload', this.handleBeforeUnload);

        next();
      } else {
        // User canceled, prevent navigation
        next(false);
      }
    } else {
      // Allow navigation in other cases
			window.removeEventListener('beforeunload', this.handleBeforeUnload);
			clearInterval(this.timerInterval);
      next();
    }
  },
}
</script>