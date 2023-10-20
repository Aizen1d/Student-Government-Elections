import { createApp, h } from 'vue'
import { createInertiaApp } from '@inertiajs/vue3'
import { router } from '@inertiajs/vue3'
import { createPinia } from 'pinia';
import NProgress from 'nprogress'
import axios from 'axios';
import { VueQueryPlugin } from '@tanstack/vue-query';
import 'bootstrap';

router.on('start', () => NProgress.start())
router.on('finish', () => NProgress.done())

axios.interceptors.request.use(config => {
  config.metadata = { startTime: new Date() };
  return config;
});

// Response interceptor
axios.interceptors.response.use(response => {
  response.config.metadata.endTime = new Date();
  response.duration = response.config.metadata.endTime - response.config.metadata.startTime;
  return response;
});

createInertiaApp({
  resolve: name => {
    const pages = import.meta.glob('./Pages/**/*.vue', { eager: true })
    return pages[`./Pages/${name}.vue`]
  },
  setup({ el, App, props, plugin }) {
    const app = createApp({ render: () => h(App, props) });
    const pinia = createPinia();
    app.use(pinia);
    app.use(plugin);
    app.use(VueQueryPlugin);
    app.mount(el);
  },
  progress: {
    delay: 250,
    color: '#e9b825',
    includeCSS: true,
    showSpinner: false,
  },
})
