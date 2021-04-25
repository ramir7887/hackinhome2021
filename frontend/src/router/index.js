import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
//import TestCard from '../components/test/TestCard'
import AppealForm from '../components/admin/AppealForm'
import Panel from '../components/admin/Panel'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/about',
    name: 'About',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
  },
  {
    path: '/report',
    name: 'Panel',
    component: Panel
  },
  {
    path: '/admin',
    name: 'Form',
    component: AppealForm
  }

]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
