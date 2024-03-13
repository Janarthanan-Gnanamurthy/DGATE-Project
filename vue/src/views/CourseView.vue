<script setup>
import CourseSidebar from '../components/CourseSidebar.vue'
import { RouterLink} from 'vue-router'
</script>

<template>
	<div>
		<nav class="navbar bg-indigo-800 font-bold text-2xl text-white pl-5">{{ course.title }}</nav>
		<div class="flex">
			<CourseSidebar :course="course" :showIntroduction="showIntroduction" :Disclaimer="showtheDisclaimer" />
			<transition enter-active-class="animate__animated animate__slideInDown" leave-active-class="animate__animated animate__slideOutUp">
				<div v-if="showIntro" class="container text-2xl p-20 flex flex-col items-center">
					<div class="bg-white shadow-lg rounded-lg p-8">
						<h2 class="text-4xl mb-14 text-center font-bold text-blue-600">Course Introduction</h2>
						<div class="container mx-auto relative">
							<div class="absolute -top-12 bg-blue-600 text-white px-4 py-2 rounded-t-lg">Course Overview</div>
							<!-- <div class="absolute -top-12 right-0 px-4 py-2 rounded-t-lg">CourseID: [Course ID]</div> -->
							<div class="bg-gray-100 p-6 rounded-lg mb-6">
								<div class="flex justify-between mb-6">
									<div>
										<h3 class="text-xl font-semibold mb-2">Instructors:</h3>
										<p class="text-gray-700">{{ course.instructors }}</p>
									</div>
									<div>
										<h3 class="text-xl font-semibold mb-2">Duration:</h3>
										<p class="text-gray-700">{{ course.duration }} hours</p>
									</div>
								</div>
								<ul class="list-disc pl-5 text-gray-700 mb-6">
									<li class="mb-2 flex items-center">
										<svg class="w-6 h-6 text-blue-600 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
											<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
										</svg>
										Master cutting-edge techniques and methodologies.
									</li>
									<li class="mb-2 flex items-center">
										<svg class="w-6 h-6 text-blue-600 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
											<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
										</svg>
										Develop a deep understanding of {{ course.title }} principles.
									</li>
									<li class="mb-2 flex items-center">
										<svg class="w-6 h-6 text-blue-600 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
											<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
										</svg>
										Gain practical experience through real-world case studies.
									</li>
									<li class="mb-2 flex items-center">
										<svg class="w-6 h-6 text-blue-600 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
											<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
										</svg>
										Collaborate with a diverse community of learners.
									</li>
								</ul>
								<h3 class="text-xl font-semibold mb-2">Prerequisites:</h3>
								<p class="text-gray-700 mb-6">{{ course.prerequisites }}</p>
							</div>
							<p class="text-gray-600 mb-6 text-center">Unlock your full potential and elevate your career with our expertly crafted course. Enroll now and embark on an unforgettable learning experience!</p>
						</div>
					</div>
				</div>
			</transition>
			<transition enter-active-class="animate__animated animate__slideInUp" leave-active-class="animate__animated animate__slideOutDown" mode="out-in">
				<div v-if="showDisclaimer" key="disclaimer-{{ currentTest }}" class="container text-2xl p-20 flex flex-col items-center">
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