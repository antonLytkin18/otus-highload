<template>
    <div>
        <h1 class="display-4 text-center">Авторизация</h1>
        <b-form @submit="onSubmit">
            <div class="alert alert-danger error-container" v-if="errors.length">
                <ul class="m-0"><li v-for="error in errors">{{ error }}</li></ul>
            </div>
            <b-form-group label="E-mail" label-for="email">
                <b-form-input
                        id="email"
                        v-model="form.email"
                        required
                        placeholder="Введите E-mail"
                ></b-form-input>
            </b-form-group>
            <b-form-group label="Пароль" label-for="input-2">
                <b-form-input
                        id="input-2"
                        v-model="form.password"
                        type="password"
                        required
                        placeholder="Введите фамилию"
                ></b-form-input>
            </b-form-group>
            <b-button type="submit" variant="primary">Войти</b-button>
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
                    email: null,
                    password: null,
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