<template>
    <div>
        <b-form @submit="onSubmit">
            <div class="alert alert-danger error-container" v-if="errors.length">
                <ul class="m-0">
                    <li v-for="error in errors">{{ error }}</li>
                </ul>
            </div>
            <b-form-group v-for="(field, index) in form" :label="field['label']" :label-for="field['id']">
                <b-form-input
                        :ref="index"
                        :id="field['id']"
                        :required="field['required']"
                        :placeholder="field['placeholder']"
                        :type="field['type']"
                        v-model="field['value']"
                        v-bind:class="{ 'is-invalid': formErrors[index] }"
                ></b-form-input>
                <b-form-invalid-feedback v-if="formErrors[index]" :state="true">
                    {{ formErrors[index] }}
                </b-form-invalid-feedback>
            </b-form-group>
            <b-button type="submit" variant="outline-secondary">{{ submitButtonTitle || 'Submit' }}</b-button>
        </b-form>
    </div>
</template>

<script>
    export default {
        props: {
            url: String,
            backUrl: String,
            form: Object,
            submitButtonTitle: String,
        },
        data: () => ({
            errors: [],
            formErrors: {},
        }),
        methods: {
            onSubmit: function (e) {
                e.preventDefault();
                this.errors = [];
                this.formErrors = {};
                const values = Object
                    .keys(this.form)
                    .reduce((values, name) => {
                        values[name] = this.form[name]['value'];
                        return values;
                    }, {});
                axios
                    .post(this.url, values)
                    .then(response => {
                        const {data} = response;
                        if (data['success']) {
                            this.$emit('success', data);
                            return;
                        }
                        for (let name in data['errors']) {
                            let error = data['errors'][name];
                            error = Array.isArray(error) ? error[0] : error
                            if (name in this.form) {
                                this.$set(this.formErrors, name, error);
                                continue;
                            }
                            this.errors.push(error);
                        }
                    });

            },
        },
    }
</script>

<style scoped>

</style>