<template>
    <div>
        <h1 class="display-4 text-center">{{ title }}</h1>
        <hr>
        <b-card v-for="(item, index) in list"
                style="margin-bottom: 5px"
                no-body
        >
            <b-card-body class="small text-muted">
                <b-row>
                    <b-col cols="1">
                        <b-avatar
                                button
                                variant="secondary"
                                :size="60"
                                class="align-center"
                                @click="onProfileClick($event, item['id'])"
                        ></b-avatar>
                    </b-col>
                    <b-col cols="11">
                        <b-link
                                class="follower-link"
                                @click="onProfileClick($event, item['id'])"
                        >{{ item['name'] }}
                        </b-link>
                        <div>Возраст: {{ item['age'] }}</div>
                        <div>Город: {{ item['city'] }}</div>
                    </b-col>
                </b-row>
            </b-card-body>
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
                            v-if="item['is_received'] && !item['is_current']"
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
                <small v-if="item['is_sent'] && !item['is_friend']" class="text-muted">
                    <b-icon icon="exclamation-circle-fill" variant="warning"></b-icon>
                    Запрос отправлен
                </small>
                <small v-if="item['is_friend']" class="text-muted">
                    <b-icon-check-circle variant="success"></b-icon-check-circle>
                    Ваш друг
                </small>
            </template>
        </b-card>
    </div>
</template>

<script>
    export default {
        props: {
            title: String,
            list: Object | Array,
            urls: Object
        },
        data: () => ({
            buttonsPressed: [],
        }),
        mounted() {
            console.log('list', this.list);
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
    .follower-link {
        color: rgba(0, 0, 0, 0.5);
        font-weight: bold;
        font-size: 18px;
    }
</style>