import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import CourseView from '../views/CourseView.vue'
import TestView from '../views/TestView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/scores',
      name: 'scores',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/ScoresView.vue')
    },
    {
      path: '/login',
      name: 'login',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/LoginView.vue')
    },
    {
      path:'/course',
      name: 'course',
      component: CourseView
    },
    {
      path: '/test/:testId',
      name: 'test',
      component: TestView
    },
    {
      path:'/result',
      name:'result',
      component: () => import('../views/ResultView.vue')
    },
    {
      path:'/upload',
      name:'upload',
      component: () => import('../views/UploadView.vue')
    }
  ]
})

export default router
