import { createRouter, createWebHistory } from 'vue-router'
import Page1 from '../components/Page1/Page1.vue'
import Page2 from '../components/Page2/Page2.vue'
import Page3 from '../components/Page3.vue'
import Page4 from '../components/Page4.vue'
import Page5 from '../components/Page5.vue'
import FamilyDetailPage from '../components/Page5/FamilyDetailPage.vue'


const routes = [
  {
    path: '/',
    redirect: '/map'
  },
  {
    path: '/map',
    name: 'Page1',
    component: Page1
  },
  {
    path: '/orbit',
    name: 'Page2',
    component: Page2
  },
  {
    path: '/orbit_family',
    name: 'Page3',
    component: Page3
  },
  {
    path: '/cj',
    name: 'Page4',
    component: Page4
  },
  {
    path: '/families',
    name: 'Page5',
    component: Page5
  },
  {
    path: '/families/:familyId',
    name: 'FamilyDetailPage',
    component: FamilyDetailPage
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: '/map'
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;