<template>
    <a-drawer
            :title= "number"
            placement="right"
            width="80%"
            :visible="visible"
            @close="onClose"
            :handle="mounted"
    >
        <div id="viz"></div>
    </a-drawer>
</template>
<script>
import NeoVis from 'neovis.js';
export default {
    props:['number','visible'],
    data() {
        return {
            //loading:true,
        }
    },
    mounted() {
        this.draw();
    },
    methods:{
        onClose() {
            this.$emit('onClose', false);
        },
        draw() {
            var viz;
            var config = {
                containerId: "viz",
                neo4j: {
                    serverUrl: "bolt://54.169.242.254:7687",
                    serverUser: "neo4j",
                    serverPassword: "igem2023"
                },
                visConfig: {
                    nodes: {
                        shape: 'dot',
                    },
                    edges: {
                        arrows: {
                            to: {enabled: true}
                        },
                        color:'#CCC',
                    },
                },
                labels: {
                    Part: {
                        label: "number",
                        color:'color',
                    }
                },
                relationships: {
                    'refers to':{
                        [NeoVis.NEOVIS_ADVANCED_CONFIG]: {
                            static:{
                                label: 'refers to',
                            },
                        },
                    },
                    'twins':{
                        [NeoVis.NEOVIS_ADVANCED_CONFIG]: {
                            static:{
                                label: 'twins',
                            },
                        },
                    },
                },
                initialCypher: "MATCH p=()-->() RETURN p LIMIT 25"
            };
            viz = new NeoVis(config);
            viz.render();
        }
    },
}
</script>
<style scoped>
#viz {
    width: 900px;
    height: 700px;
    border: 1px solid lightgray;
}
</style>