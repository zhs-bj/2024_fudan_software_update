<template>
    <a-layout id="app" style="min-height: 100vh">
        <a-layout>
            <headermenu :default-activate="defaultActivate"></headermenu>
            <a-layout-content style="margin: 0">
                <div
                    :style="{ padding: '0', background: '#fff6f0', minHeight: '100%', display: 'flex', justifyContent: 'center', alignItems: 'center' }">
                    <div style="text-align: center;height: 100%;width: 40%">
                        <a-form :model="formState" @finish="onFinish(formState)"
                            @finishFailed="onFinishFailed(formState)">
                            <a-space v-for="(basicPart, index) in formState.basicParts" :key="basicPart.id"
                                style="display: flex; margin-bottom: 8px">
                                <a-form-item :name="['basic', index, 'type']" label="Basic part type:" :rules="{
                                    required: true,
                                    message: 'Missing part type',
                                }">
                                    <a-select v-model:value="basicPart.type" placeholder="Select part type..."
                                        :options="basicPartTypes.map(a => ({ value: a }))"
                                        style="width: 130px"></a-select>
                                </a-form-item>
                                <a-form-item :name="['basic', index, 'info']" label="Part information:"
                                    :rules="[{ required: true, message: 'Missing part information' }]">
                                    <a-select v-model:value="basicPart.info" placeholder="Select promoter..."
                                        style="width: 200px" :disabled="!basicPart.type"
                                        :options="allBasicParts[basicPart.type].map(item => ({ value: item }))">
                                        <template #dropdownRender="{ menuNode: menu }">
                                            <v-nodes :vnodes="menu" />
                                            <a-divider style="margin: 4px 0" />
                                            <a-space style="padding: 4px 8px">
                                                <a-input ref="inputRef" v-model:value="name"
                                                    placeholder="Enter part name..." />
                                                <a-input ref="inputRef" v-model:value="seq"
                                                    placeholder="Enter part sequence..." />
                                                <a-button type="text" @click="addItem">
                                                    <PlusOutlined />
                                                    Add promoter
                                                </a-button>
                                            </a-space>
                                        </template>
                                    </a-select>
                                    <MinusCircleOutlined @click="removeSight(sight)" />
                                </a-form-item>
                            </a-space>
                            <a-button slot="suffix" type="primary" html-type="submit">
                                Calculate
                            </a-button>
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
import headermenu from "@/components/headermenu.vue";
import { MinusCircleOutlined, PlusOutlined } from "@ant-design/icons-vue";
import { reactive } from 'vue';
const formState = reactive({
    prom: '',
    rbs: '',
    cds: '',
});
const allBasicParts = {
    promoter: ['P1', 'P2', 'P3'],
    RBS: ['RBS1', 'RBS2', 'RBS3'],
    CDS: ['CDS1', 'CDS2', 'CDS3'],
};
const basicPartTypes = ['promoter', 'RBS', 'CDS'];
export default {
    components: {
        headermenu,
        MinusCircleOutlined,
        PlusOutlined,
    },
    data() {
        return {
            formState,
            defaultActivate: ['2'],
        };
    },
    methods: {
        onFinish(values) {
            console.log(values)
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
