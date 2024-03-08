<script setup>
import CourseSidebar from '../components/CourseSidebar.vue'
import { RouterLink} from 'vue-router'
</script>

<template>
	<div>
		<nav class="navbar bg-indigo-800 font-bold text-2xl text-white pl-5">{{ course.title }}</nav>
		<div class="flex">
			<CourseSidebar :course="course" :showIntroduction="showIntroduction" :Disclaimer="showtheDisclaimer" />
			<transition name="" mode="out-in">
				<p v-if="showIntro" class="p-5 text-2xl">
					Lorem ipsum dolor sit amet, consectetur adipisicing elit. Quo dolorem molestiae facilis vero, nemo quis, ipsum eius numquam placeat voluptate repudiandae quos consectetur eaque doloribus labore. Atque hic, nisi totam voluptatum esse ducimus natus fuga blanditiis ad commodi illum minus tempore consequatur obcaecati necessitatibus ipsum. Culpa nemo nobis officia sequi mollitia modi impedit id laudantium dignissimos soluta? Iusto, est provident.
				</p>
			</transition>
			<transition enter-active-class="animate__animated animate__slideInUp" leave-active-class="animate__animated animate__slideOutDown" >
				<div v-if="showDisclaimer" class="container text-2xl p-20 flex flex-col items-center">
					<div class="bg-white shadow-lg rounded-lg p-8 ">
						<h2 class="text-4xl mb-20 text-center font-bold text-indigo-800">Disclaimer</h2>
						<p class="text-2xl text-gray-600 mb-6 text-center"></p>
						<div class="container mx-auto relative">
							<div class="absolute -top-12 bg-indigo-600 text-white px-4 py-2 rounded-t-lg">Terms & Conditions</div>
							<div class="absolute -top-12 right-0 px-4 py-2 rounded-t-lg">TestID: {{ currentTest }}</div>
							<div class="bg-gray-100 p-6 rounded-lg mb-6">
								
								<ul class="list-disc pl-5 text-gray-700">
									<li class="mb-2 flex items-center">
										<svg class="w-6 h-6 text-indigo-600 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
											<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
										</svg>
										Ensure you are in a distraction-free environment before starting the test.
									</li>
									<li class="mb-2 flex items-center">
										<svg class="w-6 h-6 text-indigo-600 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
											<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
										</svg>
										Complete the test within the specified time limit.
									</li>
									<li class="mb-2 flex items-center">
										<svg class="w-6 h-6 text-indigo-600 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
											<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
										</svg>
										Once you start the test, you cannot go back to previous questions.
									</li>
									<li class="mb-2 flex items-center">
										<svg class="w-6 h-6 text-indigo-600 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
											<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
										</svg>
										Do not reload the page during the test.
									</li>
									<li class="mb-2 flex items-center">
										<svg class="w-6 h-6 text-indigo-600 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
											<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
										</svg>
										This test is designed for informational and educational purposes only.
									</li>
									<li class="mb-2 flex items-center">
										<svg class="w-6 h-6 text-indigo-600 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
											<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
										</svg>
										Do not use the results for any official certification or evaluation.
									</li>
								</ul>
							</div>
							<p class="text-gray-600 mb-6 text-center">By clicking "Start", you agree to the terms and conditions mentioned above.</p>
							<div class="flex justify-center">
								<button
									class="btn btn-primary text-2xl font-semibold "
									@click="redirect"
								>
									Start
								</button>
							</div>
						</div>
					</div>
				</div>
			</transition>
		</div>
	</div>
 </template>

<script>
export default {
	data(){
		return{
			course: this.$store.state.course,
			showIntro: true,
			showDisclaimer: false,
			showQuestions: false,
			showResult: false,
			currentTopic: 0,
			score: null,
			currentTest: null,
			isDisclaimerEntering: false,
		}
	},
	watch: {
		currentTest(newValue, oldValue) {
			// Set isDisclaimerEntering to true when currentTest changes
			this.isDisclaimerEntering = true;
		}
	},
	methods: {
		showIntroduction(){
			this.showQuestions =false;
			this.showResult=false;
			this.showDisclaimer=false;
			this.showIntro=true;
		},
		showtheDisclaimer(id){
			this.currentTest=id
			this.showIntro=false
			this.showDisclaimer =true
		},
		async redirect() {
			try {
				// Wait for the getTest action to complete
				const data = await this.$store.dispatch('getTest', this.currentTest);
				console.log('Data:', data);

				// Check if the data is successfully fetched before navigating
				if (data) {
					this.$router.push({ name: 'test', params: { testId: this.currentTest } });
				}
			} catch (error) {
				console.error('Error in redirect method:', error);
			}
		}
	}
}

</script>

<style scoped>

.fade-leave-to {
  transform: translateY(100);
}
</style>