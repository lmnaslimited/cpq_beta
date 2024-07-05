export function getCustomRoutes(){
    return [
        {
        path: '/designs',
        name: 'Designs',
        component: () => import('@/pages/Designs.vue'),
        meta: { scrollPos: { top: 0, left: 0 } },
      },
      {
        path: '/designs/:designId',
        name: 'Design',
        component: () => import('@/pages/Design.vue'),
        props: true,
      }
    ]
  }