<template>
    <div>
        <b-card class="mb-3">
            <b-form id="filter-form" :action="url">
                <b-input-group v-for="(field, index) in form" :label-for="field['id']" class="mb-2">
                    <template v-slot:prepend>
                        <b-input-group-text>{{ field['label'] }}</b-input-group-text>
                    </template>
                    <b-form-input
                            :ref="index"
                            :id="field['id']"
                            :name="field['id']"
                            :required="field['required']"
                            :placeholder="field['placeholder']"
                            :type="field['type']"
                            v-model="field['value']"
                    ></b-form-input>
                </b-input-group>
            </b-form>
            <template v-slot:footer>
                <b-button
                        type="submit"
                        form="filter-form"
                        size="sm"
                        variant="outline-secondary"
                >
                    <b-icon icon="search"></b-icon>
                    {{ submitButtonTitle || 'Submit' }}
                </b-button>
            </template>
        </b-card>
    </div>
</template>

<script>
    export default {
        props: {
            url: String,
            form: Object,
            submitButtonTitle: String,
        },
    }
</script>

<style scoped>

</style>