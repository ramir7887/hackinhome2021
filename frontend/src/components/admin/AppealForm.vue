<template>
  <v-card
    class="mx-auto my-1 "
    max-width="780"
  >
  <v-card-title>
      Обращение #{{appeal.chat_id}}
  </v-card-title>
  <v-card-subtitle>
      {{appeal.text}}
      </v-card-subtitle>

      <v-text-field
            v-model="message"
            class="mx-6"
            label="Комментарий к обращению"
            outlined
            clearable
          ></v-text-field>
    <v-card-actions>
      <v-btn
        text
        color="teal accent-4"
        @click="answer_appeal"
      >
        Ответить
      </v-btn>
       <v-btn
        text
        color="teal accent-4"
        @click="close_appeal"
      >
        Закрыть таск
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
const axios = require('axios')
export default {
  name: 'AppealForm',
  props: ['appeal'],
  data () {
    return {
      items: [],
      message: ""
    }
  },
  methods: {
    answer_appeal (){
      const request = {
          chat_id: this.appeal.chat_id , 
          message_id: this.appeal.message_id, 
          response: this.message,
          status: this.appeal.state,
          appeal_id: this.appeal.id
      };
      //const json = JSON.stringify(request);
      axios
        .post('http://pmelikov.ru:5000/response_appeal', request)
        .then((res) => {
        console.log('response_answer', res);
      }
      );
    },
    close_appeal () {
       const request = {
          chat_id: this.appeal.chat_id , 
          message_id: this.appeal.message_id, 
          response: "Закрыто",
          status: 3,
          appeal_id: this.appeal.id
      };
      //const json = JSON.stringify(request);
      axios
        .post('http://pmelikov.ru:5000/response_appeal', request)
        .then((res) => {
        console.log('response_answer', res);
      }
      );
    }
  }
}
</script>
