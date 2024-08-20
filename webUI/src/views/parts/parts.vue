<template>
    <a-layout id="app" style="min-height: 100vh">
        <a-layout>
            <a-layout-content style="margin: 0">
                <div
                    :style="{ padding: '0', background: '#fff6f0', minHeight: '100%', display: 'flex', flexDirection: 'column', justifyContent: 'flex-start', alignItems: 'center' }">
                    <div
                        style="text-align: center;height: 100%;padding-bottom: 1.5rem;display: inline-flex;align-items:center;">
                        <a-form layout="inline" :form="form" @submit="handleSubmit">
                            <a-form-item>
                                <a-input :defaultValue="searchQuery" v-decorator="[
                                    'query',
                                    { initialValue: searchQuery, rules: [{ required: true, message: 'Please input your query!' }] },
                                ]" placeholder="...">
                                    <a-icon slot="prefix" type="search" />
                                    <a-button slot="suffix" type="primary" html-type="submit">
                                        Search
                                    </a-button>
                                </a-input>
                            </a-form-item>
                            <a-form-item>
                                Search parts by:
                                <a-radio-group :default-value="searchType" v-decorator="[
                                    'type',
                                    { initialValue: searchType, rules: [{ required: true, message: 'Please select a search type!' }] },
                                ]">
                                    <a-radio-button value="number">
                                        ID
                                    </a-radio-button>
                                    <a-radio-button value="name">
                                        Name
                                    </a-radio-button>
                                    <a-radio-button value="sequence">
                                        Sequence
                                    </a-radio-button>
                                    <a-radio-button value="designer">
                                        Designer
                                    </a-radio-button>
                                    <a-radio-button value="team">
                                        Team
                                    </a-radio-button>
                                    <a-radio-button value="contents">
                                        Content
                                    </a-radio-button>
                                </a-radio-group>
                            </a-form-item>
                        </a-form>
                    </div>
                    <a-spin v-if="loading" tip="loading" size="large"></a-spin>
                    <partcard v-else :list-data="listData" :search-query="searchQuery" style="width: 95%"
                        @clickTitle="showPart">
                    </partcard>
                </div>
            </a-layout-content>
            <a-layout-footer style="text-align: center;padding-top: 12px;padding-bottom: 12px">
                xxx ©2024 Created by Hongchen Chen
            </a-layout-footer>
        </a-layout>
    </a-layout>
</template>
<script>
import partcard from "@/components/partcard.vue";
import axios from "axios";
const listData = []
export default {
    beforeCreate() {
        this.form = this.$form.createForm(this, { name: 'search' });
    },
    created() {
        const searchType = localStorage.getItem('partHubType');
        const searchQuery = localStorage.getItem('partHubQuery');
        if (!searchType || !searchQuery) {
            window.location.href = '/parthub';
        }
        axios.post('/api/parthub/search', {
            'partHubType': searchType,
            'partHubQuery': searchQuery
        })
            .then(response => {
                this.listData = response.data;
                if (response.data.message) {
                    this.$message.info(response.data.message);
                }
                this.loading = false;
            })
            .catch(error => {
                console.error(error);
                this.$message.error(error.message);
                this.loading = false;
            });
    },
    components: {
        partcard
    },
    data() {
        return {
            defaultActivate: ['10'],
            searchResults: [],
            searchType: localStorage.getItem('partHubType'),
            searchQuery: localStorage.getItem('partHubQuery'),
            listData,
            loading: true,
            number: ''
        };
    },
    methods: {
        async handleSubmit(e) {
            e.preventDefault();
            this.form.validateFields(async (err, values) => {
                if (!err) {
                    if (values.type === 'sequence') {
                        const regex = /^[ATCGatcgUu]+$/;
                        if (!regex.test(values.query)) {
                            this.$message.warn('The input sequence must be a valid base sequence!');
                            return;
                        }
                    }
                    localStorage.setItem('partHubQuery', values.query);
                    localStorage.setItem('partHubType', values.type);
                    window.location.href = '/parts'
                }
            });
        },
        showPart(num) {
            localStorage.setItem('curPart', num);
            window.open('/treemap');
        },
    }
};
</script>

<style>
#app {
    font-family: HarmonyOS_Sans, Helvetica, Arial, sans-serif;
    font-weight: 500;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
}

::-webkit-scrollbar {
    width: 5px;
    height: 5px;
}

::-webkit-scrollbar-thumb:vertical {
    height: 5px;
    background-color: #e37654;
}

::-webkit-scrollbar-thumb:horizontal {
    width: 5px;
    background-color: #e37654;
}
</style>
