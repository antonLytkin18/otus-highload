<template>
    <b-card
            style="margin-bottom: 5px"
            no-body
    >
        <b-tabs card>
            <b-tab title="Profile" active>
                <b-card-body class="small text-muted">
                    <b-row>
                        <b-col cols="1">
                            <b-avatar
                                    variant="secondary"
                                    :size="60"
                                    class="align-center"
                            ></b-avatar>
                        </b-col>
                        <b-col cols="11">
                            {{ item['name'] }}
                            <div>Возраст: {{ item['age'] }}</div>
                            <div>Город: {{ item['city'] }}</div>
                        </b-col>
                    </b-row>
                </b-card-body>
            </b-tab>
            <b-tab title="Followers" v-bind:disabled="!followers.length">
                <b-list-group>
                    <b-list-group-item
                            v-for="(follower, index) in followers"
                            :href="populateUrl(urls['profile'], {id: follower['id']})"
                            target="_blank"
                    >
                        <b-avatar
                                variant="secondary"
                                class="align-center"
                        ></b-avatar>
                        {{ follower['name'] }}
                    </b-list-group-item>
                </b-list-group>
            </b-tab>
        </b-tabs>
        <template v-slot:footer>
            <div v-if="!item['is_friend']">
                <b-button
                        v-if="item['can_send']"
                        size="sm"
                        variant="success"
                        @click="onRequest($event, index, item)"
                >
                    <b-icon
                            v-if="buttonsPressed['request' + index]"
                            icon="arrow-clockwise"
                            animation="spin"
                    ></b-icon>
                    Отправить приглашение
                </b-button>
                <b-button
                        v-if="item['is_received']"
                        size="sm"
                        variant="outline-success"
                        @click="onAccept($event, index, item)"
                >
                    <b-icon
                            v-if="buttonsPressed['accept' + index]"
                            icon="arrow-clockwise"
                            animation="spin"
                    ></b-icon>
                    Принять приглашение
                </b-button>
            </div>

            <small v-if="item['is_current']" class="text-muted">
                <b-icon-check-circle variant="success"></b-icon-check-circle>
                It's you
            </small>
            <small v-if="item['is_sent'] && !item['is_friend']" class="text-muted">
                <b-icon icon="exclamation-circle-fill" variant="warning"></b-icon>
                Запрос отправлен
            </small>
            <small v-if="item['is_friend'] && !item['is_current']" class="text-muted">
                <b-icon-check-circle variant="success"></b-icon-check-circle>
                Ваш друг
            </small>
        </template>
    </b-card>
</template>

<script>
    export default {
        props: {
            title: String,
            item: Object,
            followers: Array | Object,
            urls: Object
        },
        data: () => ({
            buttonsPressed: [],
        }),
        mounted() {
            console.log('vvv', this.item);
        },
        methods: {
            onRequest: function (e, index, item) {
                this.setButtonSpinnerStatus('request', index, true);
                axios.post(this.urls['request'], {'id': item['id']})
                    .then(response => {
                        this.setButtonSpinnerStatus('request', index, false);
                        const {data} = response;
                        console.log('data', data);
                        this.list[index]['is_sent'] = true;
                        this.list[index]['can_send'] = false;
                    });
            },
            onAccept: function (e, index, item) {
                this.setButtonSpinnerStatus('accept', index, true);
                axios.post(this.urls['accept'], {'id': item['id']})
                    .then(response => {
                        this.setButtonSpinnerStatus('accept', index, false);
                        const {data} = response;
                        console.log('data', data);
                        this.list[index]['is_received'] = false;
                        this.list[index]['is_friend'] = true;
                    });
            },
            onProfileClick: function (e, id) {
                window.open(this.populateUrl(this.urls['profile'], {id: id}), '_blank');
            },
            setButtonSpinnerStatus: function (type, id, active) {
                this.$set(this.buttonsPressed, type + id, active)
            }
        }
    }
</script>

<style scoped>

</style>