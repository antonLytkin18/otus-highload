<template>
    <div>
        <b-container ref="container" style="height: 500px; overflow-y: scroll; overflow-x: hidden">
            <div
                    v-for="(item, index) in messages"
            >
                <v-chat-income-message
                        v-if="!item['is_current_user']"
                        :item="item"
                        :follower-url="followerUrl"
                ></v-chat-income-message>
                <v-chat-outcome-message
                        v-if="item['is_current_user']"
                        :item="item"
                        :follower-url="followerUrl"
                ></v-chat-outcome-message>
            </div>
        </b-container>
        <hr>
        <b-input-group class="mt-3">
            <b-form-input
                    v-model="message"
                    @keyup.enter="onSend"
            ></b-form-input>
            <b-input-group-append>
                <b-button
                        variant="outline-success"
                        @click="onSend"
                >
                    Send
                </b-button>
            </b-input-group-append>
        </b-input-group>
    </div>
</template>

<script>
    export default {
        props: {
            chatId: String,
            list: Object | Array,
            chatAddMessageUrl: String,
            followerUrl: String,
        },
        mounted: function () {
            this.messages = this.list;
            this.$nextTick(() => {
                let container = this.$refs.container;
                container.scrollTop = container.scrollHeight;
            });
        },
        data: () => ({
            message: '',
            messages: [],
        }),
        methods: {
            onSend: function (e) {
                if (!this.message) {
                    return;
                }
                axios
                    .post(this.populateUrl(this.chatAddMessageUrl, {id: this.chatId}), {
                        message: this.message,
                    })
                    .then(response => {
                        const {data} = response;
                        if (!data['success']) {
                            this.$emit('error', data);
                            return;
                        }
                        const {message} = data;
                        if (!message) {
                            return;
                        }
                        this.messages.push(message)
                        this.$nextTick(() => {
                            let container = this.$refs.container;
                            container.scrollTop = container.scrollHeight;
                        });
                        this.$emit('sent', message);

                    })
                    .finally(() => {
                        this.message = '';
                    })
            }
        },
    }
</script>

<style scoped>
</style>