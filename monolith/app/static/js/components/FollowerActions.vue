<template>
    <div>
        <small v-if="item['is_current']" class="text-muted">
            <b-icon-check-circle variant="success"></b-icon-check-circle>
            It's you
        </small>
        <small v-else-if="item['is_friend']" class="text-muted">
            <b-icon-check-circle variant="success"></b-icon-check-circle>
            Your follower
        </small>
        <small v-else-if="item['is_sent']" class="text-muted">
            <b-icon icon="exclamation-circle-fill" variant="warning"></b-icon>
            Waiting for acceptance
        </small>
        <b-button
                v-else-if="item['is_received']"
                size="sm"
                variant="outline-success"
                @click="onAccept($event, item)"
        >
            <b-icon
                    v-if="buttonAcceptPressed"
                    icon="arrow-clockwise"
                    animation="spin"
            ></b-icon>
            Accept invite
        </b-button>
        <b-button
                v-else-if="item['can_send']"
                size="sm"
                variant="success"
                @click="onSend($event, item)"
        >
            <b-icon
                    v-if="buttonSendPressed"
                    icon="arrow-clockwise"
                    animation="spin"
            ></b-icon>
            Send invite
        </b-button>
    </div>
</template>

<script>
    export default {
        props: {
            title: String,
            item: Object,
            sendUrl: String,
            acceptUrl: String
        },
        data: () => ({
            buttonSendPressed: false,
            buttonAcceptPressed: false,
        }),
        methods: {
            onAccept: function (e, item) {
                this.buttonAcceptPressed = true;
                axios.post(this.populateUrl(this.acceptUrl, {id: item['id']}))
                    .then(response => {
                        this.buttonAcceptPressed = false;
                        this.$emit('accepted', response);
                    });
            },
            onSend: function (e, item) {
                this.buttonSendPressed = true;
                axios.post(this.populateUrl(this.sendUrl, {id: item['id']}))
                    .then(response => {
                        this.buttonSendPressed = false;
                        this.$emit('sent', response);
                    });
            },
        }
    }
</script>

<style scoped>

</style>