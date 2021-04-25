<template>
  <v-card
    class="mx-4"
    max-width="600"
    min-width="600"
  >
    <v-card-title>
      Департамент: {{item.departament_name}}
    </v-card-title>
    <v-card-subtitle>
      Необработанных обращений: 
      <v-chip
      class="ma-2"
      color="green"
      outlined

    >{{appeals.length}} </v-chip>
    </v-card-subtitle>
    <v-card-actions>
      <v-spacer></v-spacer>
      <v-btn
        icon
        @click="show = !show"
      >
        <v-icon>{{ show ? 'mdi-chevron-up' : 'mdi-chevron-down' }}</v-icon>
      </v-btn>
    </v-card-actions>

    <v-expand-transition>
      <div v-show="show">
        <v-divider></v-divider>
        <div v-for="(appeal, i) in appeals" :key="i" class="pa-1">
          <appeal-form :appeal="appeal"></appeal-form>
        </div>
      </div>
    </v-expand-transition>
  </v-card>
</template>


<script>

import AppealForm from './AppealForm';
//import axios from 'axios'

export default {
  components: { AppealForm },
    name: 'Panel',
    props: ['item'],
    data () {
        return {
            show: false,
            count: 10,
            appeals: []
        }
    },
    methods: {

    },
    mounted () {
      const id = this.item.id;
      setInterval(
        // axios
        //   .get(`http://pmelikov.ru:5000/get_appeal?id=${id}`)
        //   .then((res) => {
        //   this.appeals = res.data['appeals']
        //   })
        async () => {
        const f = await fetch(
          `http://pmelikov.ru:5000/get_appeal?id=${id}`
        );
        const data = await f.json();
        this.appeals = data['appeals'];
        }
        , 2000 );
      console.log('AAAAAAAAAAAAAAA', this.appeals);
    }
}
</script>
