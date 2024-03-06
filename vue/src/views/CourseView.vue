<script setup>
import CourseSidebar from '../components/CourseSidebar.vue'
import { RouterLink} from 'vue-router'
</script>

<template>
  <div>
    <nav class="navbar bg-indigo-800 font-bold text-2xl text-white pl-5">{{ course.title }}</nav>
    
    <div class="flex">
      <CourseSidebar :course="course" :showIntroduction="showIntroduction" :Disclaimer="showtheDisclaimer" />

      <p v-if="showIntro" class="p-5 text-2xl">
        Lorem ipsum dolor sit amet, consectetur adipisicing elit. Quo dolorem molestiae facilis vero, nemo quis, ipsum eius numquam placeat voluptate repudiandae quos consectetur eaque doloribus labore. Atque hic, nisi totam voluptatum esse ducimus natus fuga blanditiis ad commodi illum minus tempore consequatur obcaecati necessitatibus ipsum. Culpa nemo nobis officia sequi mollitia modi impedit id laudantium dignissimos soluta? Iusto, est provident.
      </p>
      
      <div v-if="showDisclaimer" class="container text-2xl p-20"> 
        <h2 class="text-3xl mb-4 text-center font-bold">Disclaimer</h2>
        <p class="text-2xl text-gray-600">TestID : {{ currentTest }}</p>
        
        <div class="container mx-auto">
          <ul class="list-disc pl-5 m-4">
            <li>Ensure you are in a distraction-free environment before starting the test.</li>
            <li>Complete the test within the specified time limit.</li>
            <li>Once you start the test, you cannot go back to previous questions.</li>
            <li>Do not reload the page during the test.</li>
            <li>This test is designed for informational and educational purposes only.</li>
            <li>Do not use the results for any official certification or evaluation.</li>
          </ul>
          
          <p class="text-gray-600">
            By proceeding, you acknowledge and agree to the terms mentioned above.
          </p>
          
          <div class="btn btn-primary rounded-md border-black text-2xl m-3" @click="redirect">Start</div>
        </div>
      </div>
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