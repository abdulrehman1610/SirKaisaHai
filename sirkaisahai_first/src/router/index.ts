import { createRouter, createWebHistory } from 'vue-router';
import HomePage from '../pages/HomePage.vue';
import AuthPage from '../pages/AuthPage.vue';
import SearchResultsPage from '../pages/SearchResultsPage.vue';
import ProfessorPage from '../pages/ProfessorPage.vue';
import CoursePage from '../pages/CoursePage.vue';
import SubmitReviewPage from '../pages/SubmitReviewPage.vue';
import BrowseCoursesPage from '../pages/BrowseCoursesPage.vue';
import PrivacyPage from '../pages/PrivacyPage.vue';
import TermsPage from '../pages/TermsPage.vue';
import { useAuthStore } from '../stores/auth';

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomePage
    },
    {
      path: '/auth',
      name: 'auth',
      component: AuthPage,
      meta: { hideFooter: true }
    },
    {
      path: '/search',
      name: 'search',
      component: SearchResultsPage
    },
    {
      path: '/courses',
      name: 'browse-courses',
      component: BrowseCoursesPage
    },
    {
      path: '/professor/:id',
      name: 'professor-detail',
      component: ProfessorPage
    },
    {
      path: '/course/:id',
      name: 'course-detail',
      component: CoursePage
    },
    {
      path: '/review/new',
      name: 'submit-review',
      component: SubmitReviewPage
    },
    {
      path: '/privacy',
      name: 'privacy',
      component: PrivacyPage
    },
    {
      path: '/terms',
      name: 'terms',
      component: TermsPage
    },
    {
      path: '/:pathMatch(.*)*',
      redirect: '/'
    }
  ],
  scrollBehavior() {
    return { top: 0 };
  }
});

router.beforeEach((to, _from, next) => {
  const authStore = useAuthStore();
  if (to.path === '/review/new' && !authStore.isVerified) {
    next({ path: '/auth', query: { redirect: to.fullPath || '/review/new' } });
  } else {
    next();
  }
});

export default router;
