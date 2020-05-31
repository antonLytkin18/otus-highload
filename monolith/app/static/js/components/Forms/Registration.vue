<template>
    <div>
        <h1 class="display-4 text-center">Регистрация</h1>
        <b-form @submit="onSubmit">
            <div class="alert alert-danger error-container" v-if="errors.length">
                <ul class="m-0"><li v-for="error in errors">{{ error }}</li></ul>
            </div>
            <b-form-group label="Имя" label-for="name">
                <b-form-input
                        id="name"
                        v-model="form.name"
                        required
                        placeholder="Введите имя"
                ></b-form-input>
            </b-form-group>
            <b-form-group label="Фамилия" label-for="input-2">
                <b-form-input
                        id="input-2"
                        v-model="form.lastName"
                        required
                        placeholder="Введите фамилию"
                ></b-form-input>
            </b-form-group>
            <b-form-group label="E-mail" label-for="input-3">
                <b-form-input
                        id="input-3"
                        type="email"
                        v-model="form.email"
                        required
                        placeholder="Введите email"
                ></b-form-input>
            </b-form-group>
            <b-form-group label="Пароль">
                <b-form-input
                        type="password"
                        v-model="form.password"
                        required
                        placeholder="Введите пароль"
                ></b-form-input>
            </b-form-group>
            <b-form-group label="Подтвердите пароль">
                <b-form-input
                        type="password"
                        v-model="form.confirmPassword"
                        required
                        placeholder="Подтвердите пароль"
                ></b-form-input>
            </b-form-group>
            <b-form-group label="Возраст" label-for="input-4">
                <b-form-input
                        id="input-4"
                        v-model="form.age"
                        required
                        placeholder="Укажите возраст"
                ></b-form-input>
            </b-form-group>
            <b-form-group label="Пол" label-for="input-5">
                <b-form-select
                        id="input-5"
                        v-model="form.gender"
                        :options="form.genderOptions"
                        required
                ></b-form-select>
            </b-form-group>
            <b-form-group label="Интересы" label-for="input-6">
                <b-form-textarea
                        id="input-6"
                        v-model="form.interests"
                        required
                        placeholder="Укажите свои интересы"
                ></b-form-textarea>
            </b-form-group>
            <b-form-group label="Город" label-for="input-7">
                <b-form-input
                        id="input-7"
                        v-model="form.city"
                        required
                        placeholder="Укажите город"
                ></b-form-input>
            </b-form-group>
            <b-button type="submit" variant="primary">Зарегистрироваться</b-button>
        </b-form>
    </div>
</template>

<script>
    export default {
        props: {
            url: String,
        },
        data: () => ({
            form: {},
            errors: [],
        }),
        mounted: function () {
            this.form = this.getForm();
        },
        methods: {
            onSubmit: function (e) {
                e.preventDefault();
                let that = this;
                this.errors = [];
                axios.post(this.url, that.form).then(response => {
                    const {data} = response;
                    for (let name in data['errors']) {
                        this.errors.push(data['errors'][name]);
                    }
                })
            },
            getForm: function (attrs) {
                let form = {
                    name: null,
                    lastName: null,
                    email: null,
                    password: null,
                    confirmPassword: null,
                    age: null,
                    gender: null,
                    genderOptions: {
                        male: 'Мужской',
                        female: 'Женский'
                    },
                    interests: null,
                    city: null,
                };
                if (attrs) {
                    for (let name in form) {
                        if (attrs.hasOwnProperty(name)) {
                            form[name] = attrs[name];
                        }
                    }
                }
                return form;
            }
        },
    }
</script>

<style scoped>

</style>