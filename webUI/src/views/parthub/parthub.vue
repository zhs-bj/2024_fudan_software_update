<template>
    <a-layout id="app" style="min-height: 100vh">
        <a-layout>
            <a-layout-content style="margin: 0">
                <div
                    :style="{ padding: '0', background: '#fff6f0', minHeight: '100%', display: 'flex', justifyContent: 'center', alignItems: 'center' }">
                    <div style="text-align: center;height: 100%;width: 40%">
                        <a-form :form="form" @submit="handleSubmit">
                            <a-form-item>
                                <a-input v-decorator="[
                                    'query',
                                    { rules: [{ required: true, message: 'Please input your query!' }] },
                                ]" placeholder="...">
                                    <a-icon slot="prefix" type="search" />
                                    <a-button slot="suffix" type="primary" html-type="submit">
                                        Search
                                    </a-button>
                                </a-input>
                            </a-form-item>
                            <a-form-item>
                                Search parts by:
                                <a-radio-group v-decorator="[
                                    'type',
                                    { rules: [{ required: true, message: 'Please select a search type!' }] },
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
                </div>
            </a-layout-content>
            <a-layout-footer style="text-align: center;padding-top: 12px;padding-bottom: 12px">
                xxx ©2024 Created by Hongcheng Chen
            </a-layout-footer>
        </a-layout>
    </a-layout>
</template>
<script>
export default {
    beforeCreate() {
        this.form = this.$form.createForm(this, { name: 'search' });
    },
    components: {
    },
    data() {
        return {
            defaultActivate: ['10'],
        };
    },
    methods: {
        async handleSubmit(e) {
            e.preventDefault();
            this.form.validateFields(async (err, values) => {
                if (!err) {
                    console.log(values)
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
