<template>
<v-container class="grey lighten-5">
<v-row>
    <v-col class="pa-2 mx-1">
        
 <v-card
    class="mx-4 my-1"
    max-width="800"
  >
  <v-card-title>
      Создать опрос
  </v-card-title>
  <v-card-subtitle>
      Для создания опроса заполните следущие поля
      </v-card-subtitle>
      <v-text-field
        v-model="quiz.name"
            class="mx-4"
            label="Название опроса"
            outlined
            clearable
            dense
          ></v-text-field>
          <v-text-field
          v-model="quiz.url"
            class="mx-4"
            label="Ссылка на форму"
            outlined
            clearable
            dense
          ></v-text-field>
          <v-text-field
          v-model="quiz.description"
          class="mx-4"
            label="Описание проводимого опроса"
            outlined
            clearable
            dense
          ></v-text-field>
    <v-card-actions>
      <v-btn
        text
        color="teal accent-4"
        @click="send_quiz"
      >
        Создать опрос
      </v-btn>
    </v-card-actions>
  </v-card>
    
    </v-col>
    <v-col class="pa-2 mx-1">
         <v-card
            class="mx-4 my-1"
            max-width="800"
        >
  <v-card-title>
      Список опросов
  </v-card-title>
  <v-list>
      <v-list-item>
        Удовлетворенность студентов учебным процессов Осень 2019
      </v-list-item>
       <v-list-item>
          Удовлетворенность студентов учебным процессов Весна 2019
      </v-list-item>
     <v-list-item>
        Удовлетворенность студентов учебным процессов Осень 2020
      </v-list-item>
       <v-list-item>
          Удовлетворенность студентов учебным процессов Весна 2020
      </v-list-item>
      <v-list-item>
        Удовлетворенность студентов учебным процессов Осень 2021
      </v-list-item>
       <v-list-item>
          Удовлетворенность студентов учебным процессов Весна 2021
      </v-list-item>
  </v-list>
    <v-card-actions>
      <v-btn
        text
        color="teal accent-4"
      >
        Редактировать
      </v-btn>
    </v-card-actions>
  </v-card>
    </v-col>
</v-row>
    <v-row>
    <v-col
       v-for="(item) in items"
          :key="item.id">
        <department :item="item"></department>
    </v-col>
    </v-row>
  </v-container>
</template>
<script>

import Department from './Department'
import axios from 'axios'
export default {
    name: 'Panel',
    props: ['item'],
    components: {
        Department
    },
    data () {
        return {
            items:[],
            quiz: {
                name: "",
                url: "",
                description: ""
            }
            }
    },
    methods: {
        
        send_quiz(){
            const request = this.quiz;
             axios
                .post('http://pmelikov.ru:5000/quiz', request)
                .then((res) => {
                    console.log('response_answer', res);
                }
                );
        }
    },
    mounted () {
        axios
        .get('http://pmelikov.ru:5000/get_departments')
        .then((res) => {
        this.items = res.data['departments']
        console.log('AAAAAAAAAAAAAAA', this.items)
      }
      );
      console.log('mounted panel');
    }
}
</script>