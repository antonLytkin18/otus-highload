<template>
    <div>
        <b-alert show>asdasd</b-alert>
        <b-button v-b-modal.modal-1>{{title}}</b-button>
        <b-modal id="modal-1" title="BootstrapVue">
            <p class="my-4">Hello from modal!</p>
        </b-modal>
    </div>
</template>

<script>
    export default {
        props: {
            title: String
        }
    }
</script>

<style scoped>

</style>