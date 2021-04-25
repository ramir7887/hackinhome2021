<template>
  <v-card class="mx-auto" width="500" outlined light ma-4>
    <v-card-title>Sign in to project</v-card-title>
    <v-alert dense outlined type="error" v-if="authError">
      I'm a dense alert with the <strong>outlined</strong> prop and a
      <strong>type</strong> of error
    </v-alert>
    <v-text-field
      class="ma-4"
      label="Login"
      placeholder="Placeholder"
      outlined
      v-model="login"
      :rules="[rules.required]"
      required
      dense
    ></v-text-field>
    <v-text-field
      class="ma-4"
      placeholder="Placeholder"
      outlined
      dense
      v-model="password"
      :append-icon="show1 ? 'mdi-eye' : 'mdi-eye-off'"
      :rules="[rules.required, rules.min]"
      :type="show1 ? 'text' : 'password'"
      name="input-10-1"
      label="Password"
      hint="At least 8 characters"
      counter
      @click:append="show1 = !show1"
    ></v-text-field>

    <v-btn
      class="ml-4 mr-4 mb-4"
      width="250"
      outlined
      color="success"
      @click="auth"
    >
      Sign in
    </v-btn>
  </v-card>
</template>

<script>
export default {
  name: "AuthCard",
  data() {
    return {
      authError: false,
      show1: false,
      password: "",
      login: "",
      rules: {
        required: (value) => !!value || "Required.",
        min: (v) => v.length >= 8 || "Min 8 characters",
        emailMatch: () => `The password you entered don't match`,
      },
    };
  },
  methods: {
    async auth() {
      const user = {
        login: this.login,
        password: this.password,
      };
      const f = await fetch("http://localhost:8081/auth", {
        method: "POST",
        //headers: {
        //  'Content-Type': 'application/json;charset=utf-8'
        //},
        body: JSON.stringify(user),
      });
      if (f.ok) {
        const response = await f.json();
        // вызов родительского метода
        // установка токена куда-то
        console.log(response.token, response.login);
      } else {
        console.log(f.json());
        this.authError = true;
      }
    },
  },
};
</script>
