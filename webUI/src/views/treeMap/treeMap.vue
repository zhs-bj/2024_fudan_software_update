<template>
    <a-layout id="app" style="min-height: 100vh">
        <a-layout>
            <a-layout-content style="margin: 0">
                <div
                    :style="{ padding: '0', background: '#fff6f0', minHeight: '100%', display: 'flex', flexDirection: 'row', justifyContent: 'flex-start', alignItems: 'center' }">
                    <div style="margin-left: 1rem;width: 60%">
                        <h1 style="color: #e37654">Your Part map of {{ curPart }}:</h1>
                        <p>Scroll to zoom the canvas and drag to move the nodes. Click the circle to display the part
                            details and double click to go to the part page.</p>
                        <div style="display: flex;flex-direction: column;align-items: center;position: relative;">
                            <div id="viz"
                                style="display: flex;justify-content: center; align-items: center;flex-direction: column; ">
                                <a-spin :spinning="loading" tip="loading" size="large">
                                </a-spin>
                            </div>
                        </div>
                    </div>
                    <div style="margin-left: 1rem;width: 35%">
                        <a-card>
                            <p slot="title" id="title"></p>
                            <p id="name"></p>
                            <p id="type"></p>
                            <p id="date"></p>
                            <p id="team"></p>
                            <p id="designer"></p>
                            <p id="length"></p>
                            <p id="contents"></p>
                            <p id></p>
                            <template slot="actions">
                                <a id="sequence"><a-icon type="download" /> Download sequence</a>
                                <a id="url"><a-icon type="link" /> View in iGEM Parts Registry</a>
                            </template>
                        </a-card>
                    </div>
                </div>
            </a-layout-content>
            <a-layout-footer style="text-align: center;padding-top: 12px;padding-bottom: 12px">
                xxx ©2024 Created by Hongchen Chen
            </a-layout-footer>
        </a-layout>
    </a-layout>
</template>
<script>
import NeoVis from 'neovis.js';
import axios from "axios";
function createTable(info) {
    var idobj = document.getElementById('title');
    idobj.innerText = info.number;
    var nameobj = document.getElementById('name');
    nameobj.innerText = "Name: " + info.name;
    var conobj = document.getElementById('contents');
    if (info.contents.length > 600) {
        conobj.innerText = info.contents.slice(0, 600) + '...';
    }
    else {
        conobj.innerText = info.contents;
    }
    var typeobj = document.getElementById('type');
    typeobj.innerText = "Type: " + info.type;
    var dateobj = document.getElementById('date');
    dateobj.innerText = "Date: " + info.date;
    var teamobj = document.getElementById('team');
    teamobj.innerText = "Team: " + info.team;
    var dsnobj = document.getElementById('designer');
    dsnobj.innerText = "Designer: " + info.designer;
    var seqobj = document.getElementById('sequence');
    seqobj.href = "/seq/download/" + info.number;
    seqobj.target = "_blank";
    var lobj = document.getElementById('length');
    lobj.innerText = "Length: " + info.length + 'bp';
    var urlobj = document.getElementById('url');
    urlobj.href = info.url;
    urlobj.target = "_blank";
}
export default {
    components: {
    },
    created() {
        const curPart = localStorage.getItem('curPart');
        if (!curPart) {
            window.location.href = '/parts';
        }
        else {
            this.curPart = curPart;
        }
    },
    data() {
        return {
            defaultActivate: ['10'],
            curPart: null,
            loading: true,
            node: null,
        };
    },
    mounted() {
        this.draw();
    },
    methods: {
        draw() {
            axios.post('/api/parthub/config', {
                'curPart': this.curPart
            })
                .then(response => {
                    var neo4jConfig = response.data.config;
                    var ids = [parseInt(response.data.id)];
                    var viz;
                    var config = {
                        containerId: "viz",
                        neo4j: neo4jConfig,
                        visConfig: {
                            nodes: {
                                shape: 'dot',
                                font: {
                                    face: 'HarmonyOS_Sans',
                                },
                            },
                            edges: {
                                color: '#CCC',
                                font: {
                                    face: 'HarmonyOS_Sans',
                                },
                            },
                        },
                        labels: {
                            Part: {
                                label: "number",
                                color: 'color',
                                size: 'nodesize',
                                [NeoVis.NEOVIS_ADVANCED_CONFIG]: {
                                    function: {
                                        title: (props) => NeoVis.objectToTitleHtml(props, ["name", "type", "length", "team", "designer", "date"])
                                    },
                                },
                            }
                        },
                        relationships: {
                            'refers to': {
                                [NeoVis.NEOVIS_ADVANCED_CONFIG]: {
                                    static: {
                                        label: 'refers to',
                                        width: 7,
                                        arrows: 'to'
                                    },
                                },
                            },
                            'twins': {
                                [NeoVis.NEOVIS_ADVANCED_CONFIG]: {
                                    static: {
                                        label: 'twins',
                                        width: 3,
                                    },
                                },
                            },
                        },
                        initialCypher: `MATCH (n)-[r*0..]->(m:Part{number:'${this.curPart}'}) RETURN n,r,m UNION MATCH (n:Part{number:'${this.curPart}'})-[r*0..]->(m) RETURN n,r,m LIMIT 150`
                    };
                    viz = new NeoVis(config);
                    var doubleClickLocked = false;
                    var selectNodeLocked = false;
                    viz.registerOnEvent("clickNode", () => {
                        viz.network.on('selectNode', function (properties) {
                            if (!selectNodeLocked) {
                                selectNodeLocked = true;
                                var ids = properties.nodes;
                                var clickedNodes = viz.nodes.get(ids);
                                if (clickedNodes) {
                                    createTable(clickedNodes[0].raw.properties);
                                }
                                console.log(this.node)
                                setTimeout(function () {
                                    selectNodeLocked = false;
                                }, 300);
                            }
                        });
                        viz.network.on('doubleClick', function (properties) {
                            if (!doubleClickLocked) {
                                doubleClickLocked = true;
                                var ids = properties.nodes;
                                var clickedNodes = viz.nodes.get(ids);
                                if (clickedNodes) {
                                    window.open(clickedNodes[0].raw.properties.url);
                                }
                                setTimeout(function () {
                                    doubleClickLocked = false;
                                }, 300);
                            }
                        });
                    });
                    viz.registerOnEvent("completed", () => {
                        viz.network.on('stabilizationIterationsDone', function () {
                            this.loading = false;
                            viz.network.selectNodes(ids);
                            var selectedNodes = viz.nodes.get(ids);
                            if (selectedNodes) {
                                createTable(selectedNodes[0].raw.properties);
                            }
                        });
                    });
                    viz.render();
                })
                .catch(error => {
                    console.error(error);
                    this.$message.error(error.message);
                });
        },
    }
}
</script>
<style scoped>
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

#viz {
    width: 100%;
    height: 800px;
    border: 0.2rem solid #e37654;
    border-radius: 5px;
}
</style>