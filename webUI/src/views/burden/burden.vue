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
                            <a-form-item :rules="[{ required: true, message: '' }]">
                                <a-select v-model:value="formState.prom" placeholder="Select promoter..."
                                    style="width: 300px" :options="items.map(item => ({ value: item }))">
                                    <template #dropdownRender="{ menuNode: menu }">
                                        <v-nodes :vnodes="menu" />
                                        <a-divider style="margin: 4px 0" />
                                        <a-space style="padding: 4px 8px">
                                            <a-input ref="inputRef" v-model:value="name"
                                                placeholder="Enter promoter sequence..." />
                                            <a-button type="text" @click="addItem">
                                                <template #icon>
                                                    <plus-outlined />
                                                </template>
                                                Add promoter
                                            </a-button>
                                        </a-space>
                                    </template>
                                </a-select>
                                <a-select v-model:value="formState.rbs" placeholder="Select RBS..." style="width: 300px"
                                    :options="items.map(item => ({ value: item }))">
                                    <template #dropdownRender="{ menuNode: menu }">
                                        <v-nodes :vnodes="menu" />
                                        <a-divider style="margin: 4px 0" />
                                        <a-space style="padding: 4px 8px">
                                            <a-input ref="inputRef" v-model:value="name"
                                                placeholder="Enter RBS sequence..." />
                                            <a-button type="text" @click="addItem">
                                                <template #icon>
                                                    <plus-outlined />
                                                </template>
                                                Add RBS
                                            </a-button>
                                        </a-space>
                                    </template>
                                </a-select>
                                <a-select v-model:value="formState.cds" placeholder="Select coding sequence..."
                                    style="width: 300px" :options="items.map(item => ({ value: item }))">
                                    <template #dropdownRender="{ menuNode: menu }">
                                        <v-nodes :vnodes="menu" />
                                        <a-divider style="margin: 4px 0" />
                                        <a-space style="padding: 4px 8px">
                                            <a-input ref="inputRef" v-model:value="name"
                                                placeholder="Enter coding sequence..." />
                                            <a-button type="text" @click="addItem">
                                                <template #icon>
                                                    <plus-outlined />
                                                </template>
                                                Add CDS
                                            </a-button>
                                        </a-space>
                                    </template>
                                </a-select>
                                <a-button slot="suffix" type="primary" html-type="submit">
                                    Calculate
                                </a-button>
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
import headermenu from "@/components/headermenu.vue";
import { reactive } from 'vue';
const formState = reactive({
    prom: '',
    rbs: '',
    cds: '',
});
export default {
    components: {
        headermenu
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
