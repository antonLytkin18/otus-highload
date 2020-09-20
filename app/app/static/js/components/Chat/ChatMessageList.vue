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
            userId: String,
            followerUrl: String,
            chatAppUrl: String,
        },
        mounted: function () {
            this
                .makeChatAppRequest('post', '/api/v1/chats', {
                    user_id: this.userId,
                }, this.chatAppUrl)
                .then(response => {
                    const {data} = response;
                    this.chatId = data['item']['id'];
                    this.fillMessages();
            });
        },
        data: () => ({
            message: '',
            messages: [],
            chatId: null,

        }),
        methods: {
            fillMessages: function () {
                this.makeChatAppRequest('get', '/api/v1/chats/' + this.chatId + '/messages', {}, this.chatAppUrl)
                    .then(response => {
                        const {data} = response;
                        this.messages = data['list'];
                    })
                    .finally(() => {
                        this.$nextTick(() => {
                            let container = this.$refs.container;
                            container.scrollTop = container.scrollHeight;
                        });
                        this.messages
                            .filter(message => !message['is_read'])
                            .forEach(this.markMessageAsRead);
                    })
            },
            markMessageAsRead: function (message) {
                this.makeChatAppRequest('post', '/api/v1/messages/' + message['id'] + '/read', {}, this.chatAppUrl)
                    .then(response => {})
            },
            onSend: function (e) {
                if (!this.message) {
                    return;
                }
                this.makeChatAppRequest('post', '/api/v1/chats/' + this.chatId + '/messages', {
                        message: this.message,
                    }, this.chatAppUrl)
                    .then(response => {
                        const {data} = response;
                        if (!data['success']) {
                            this.$emit('error', data);
                            return;
                        }
                        const {item} = data;
                        if (!item) {
                            return;
                        }
                        this.messages.push(item);
                        this.$nextTick(() => {
                            let container = this.$refs.container;
                            container.scrollTop = container.scrollHeight;
                        });
                        this.$emit('sent', item);

                    })
                    .finally(() => {
                        this.message = '';
                    });
            }
        },
    }
</script>

<style scoped>
</style>