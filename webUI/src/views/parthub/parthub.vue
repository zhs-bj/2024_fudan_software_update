<template>
    <a-layout id="app" style="min-height: 100vh">
        <a-layout>
            <a-layout-content style="margin: 0">
                <div
                    :style="{ padding: '0', background: '#fff6f0', minHeight: '100%', display: 'flex', justifyContent: 'center', alignItems: 'center' }">
                    <div style="text-align: center;height: 100%;width: 40%">
                        <a-form :model="formState" @finish="onFinish(formState)"
                            @finishFailed="onFinishFailed(formState)">
                            <a-form-item :rules="[{ required: true, message: 'Please input your query!' }]">
                                <a-input v-model:value="formState.query" placeholder="...">
                                </a-input>
                                <a-button slot="suffix" type="primary" html-type="submit">
                                    Search
                                </a-button>
                            </a-form-item>
                            <a-form-item :rules="[{ required: true, message: 'Please select a search type!' }]">
                                Search parts by:
                                <a-radio-group v-model:value="formState.type">
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
                </div>
            </a-layout-content>
            <a-layout-footer style="text-align: center;padding-top: 12px;padding-bottom: 12px">
                xxx ©2024 Created by Hongcheng Chen
            </a-layout-footer>
        </a-layout>
    </a-layout>
</template>
<script>
import { reactive } from 'vue';
import { message } from 'ant-design-vue';
const formState = reactive({
    query: '',
    type: ''
});
export default {
    data() {
        return {
            formState,
            defaultActivate: ['10'],
        };
    },
    methods: {
        onFinish(values) {
            console.log(values);
            if (values.type === 'sequence') {
                const regex = /^[ATCGatcgUu]+$/;
                if (!regex.test(values.query)) {
                    message.warning('The input sequence must be a valid base sequence!');
                    return;
                }
            }
            localStorage.setItem('partHubQuery', values.query);
            localStorage.setItem('partHubType', values.type);
            window.location.href = '/parts'
        },
        onFinishFailed(errorInfo) {
            console.log(errorInfo);
        }
    },
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
