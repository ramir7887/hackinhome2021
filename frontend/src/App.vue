<template>
  <!-- App.vue -->

  <v-app>
    <v-overlay
          :absolute="absolute"
          :opacity="opacity"
          :value="overlay"
        >
        <auth-card></auth-card>
        </v-overlay>
    <v-navigation-drawer app permanent expand-on-hover>
      <!-- -->
      <v-list>
        <v-list-item class="px-2">
          <v-list-item-avatar>
            <v-img
              src="https://yt3.ggpht.com/ytc/AAUvwngJKdCwwRuxyeZiPK4LxKw450-vWSO8VTkQRaDdEA=s900-c-k-c0x00ffffff-no-rj"
            ></v-img>
          </v-list-item-avatar>
        </v-list-item>

        <v-list-item link to="/">
          <v-list-item-content>
            <v-list-item-title class="title">
              Сотрудник 
            </v-list-item-title>
            <v-list-item-subtitle>ramazan@gmail.com</v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>
      </v-list>

      <v-divider></v-divider>

      <v-list nav dense>
        <v-list-item
          v-for="item in items"
          :key="item.title"
          link
          :to="item.link"
        >
          <v-list-item-icon>
            <v-icon>{{ item.icon }}</v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title>{{ item.title }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>

    <v-app-bar app>
      <!-- -->Система бота
    </v-app-bar>

    <!-- Sizes your content based upon application components -->
    <v-main >
      <!-- Provides the application the proper gutter -->
      <v-container fluid>
        <!-- If using vue-router -->
        <router-view></router-view>
      </v-container>
    </v-main>

    <v-footer app>
      <!-- -->
    </v-footer>
  </v-app>
</template>

<script>
import AuthCard from './components/auth/AuthCard'

export default {
  name: "App",

  components: {
    AuthCard
  },

  data () {
    return {
      absolute: true,
      opacity: 1,
      overlay: false,
      items: [
        {
          icon: 'mdi-chart-bar',
          title: 'Отчеты',
          link: '/report'
        },
        {
          icon: 'mdi-cog',
          title: 'Администрирование',
          link: '/admin'
        },
      ]
    }
  },
  methods: {
    showOverlay (auth) {
      console.log(auth)

    }
  }
};
</script>
