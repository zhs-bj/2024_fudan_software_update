<template>
  <a-layout id="app" style="min-height: 100vh">
    <a-layout>
      <headermenu :default-activate="defaultActivate"></headermenu>
      <a-layout-content style="margin: 0">
        <div
          :style="{
            padding: '0',
            background: '#fff6f0',
            minHeight: '100%',
            display: 'flex',
            flexDirection: 'row',
            justifyContent: 'flex-start',
          }"
        >
          <div style="margin-left: 1rem; width: 60%">
            <h1 style="color: #e37654">Your Part map of {{ curPart }}:</h1>
            <p>
              Scroll to zoom the canvas and drag to move the nodes. Click the
              circle to display the part details and double click to go to the
              part page. You can <b>toggle between similar parts</b> and
              <b>part/relationship information</b> by clicking on the tabs.
            </p>
            <div
              style="
                display: flex;
                flex-direction: column;
                align-items: center;
                position: relative;
              "
            >
              <div
                id="viz"
                style="
                  display: flex;
                  justify-content: center;
                  align-items: center;
                  flex-direction: column;
                "
              >
                <a-spin :spinning="loading" tip="loading" size="large">
                </a-spin>
              </div>
            </div>
          </div>
          <div style="margin-left: 1rem; width: 35%">
            <a-tabs v-model:activeKey="activeKey">
              <a-tab-pane key="1" tab="Similarity">
                <a-list
                  item-layout="horizontal"
                  :data-source="similarNodes"
                  style="max-height: 90vh; overflow-y: auto"
                >
                  <template #renderItem="{ item }">
                    <a-list-item>
                      <a
                        :href="
                          'https://parts.igem.org/wiki/index.php?title=Part:' +
                          item.part
                        "
                      >
                        <h3 style="color: #e37654">{{ item.part }}</h3>
                      </a>
                      {{
                        item.name.length <= 70
                          ? item.name
                          : item.name.slice(0, 67) + "..."
                      }}
                      <br />
                      <b>Overall similarity:</b>&nbsp;{{
                        item.overall_score.toFixed(2)
                      }}
                      <br />
                      <b>Sequence similarity:</b>&nbsp;{{
                        item.seq_score.toFixed(2)
                      }}
                      <br />
                      <b>Category similarity:</b>&nbsp;{{
                        item.cat_score.toFixed(2)
                      }}
                      <br />
                    </a-list-item>
                  </template>
                </a-list>
              </a-tab-pane>
              <a-tab-pane key="2" tab="Part/Relationship info" force-render>
                <a-card style="max-height: 90vh; overflow-y: auto">
                  <p slot="title" id="title"></p>
                  <p id="name"></p>
                  <p id="type"></p>
                  <p id="date"></p>
                  <p id="team"></p>
                  <p id="designer"></p>
                  <p id="length"></p>
                  <p id="contents"></p>
                  <p id="category"></p>
                  <a id="sequence"> <DownloadOutlined /> Download sequence </a>
                  <a id="url"> <LinkOutlined /> View in iGEM Parts Registry </a>
                </a-card>
              </a-tab-pane>
            </a-tabs>
          </div>
        </div>
      </a-layout-content>
      <a-layout-footer
        style="text-align: center; padding-top: 12px; padding-bottom: 12px"
      >
        PartHub 3.0 ©2024 Created by Hongchen Chen
      </a-layout-footer>
    </a-layout>
  </a-layout>
</template>
<script>
import headermenu from "@/components/headermenu.vue";
import NeoVis from "neovis.js";
import axios from "axios";
import { DownloadOutlined, LinkOutlined } from "@ant-design/icons-vue";
function createTable(info) {
  var idobj = document.getElementById("title");
  idobj.innerText = info.number;
  var nameobj = document.getElementById("name");
  nameobj.innerText = "Name: " + info.name;
  var conobj = document.getElementById("contents");
  conobj.style.display = "block";
  if (info.contents.length > 600) {
    conobj.innerText = info.contents.slice(0, 600) + "...";
  } else {
    conobj.innerText = info.contents;
  }
  var typeobj = document.getElementById("type");
  typeobj.innerText = "Type: " + info.type;
  var dateobj = document.getElementById("date");
  dateobj.innerText = "Date: " + info.date;
  var teamobj = document.getElementById("team");
  teamobj.innerText = "Team: " + info.team;
  var dsnobj = document.getElementById("designer");
  dsnobj.innerText = "Designer: " + info.designer;
  var catobj = document.getElementById("category");
  catobj.style.display = "block";
  catobj.innerText = "Category: " + info.category;
  var seqobj = document.getElementById("sequence");
  seqobj.style.display = "block";
  seqobj.href = "/seq/download/" + info.number;
  seqobj.target = "_blank";
  var lobj = document.getElementById("length");
  lobj.style.display = "block";
  lobj.innerText = "Length: " + info.length + "bp";
  var urlobj = document.getElementById("url");
  urlobj.style.display = "block";
  urlobj.href = info.url;
  urlobj.target = "_blank";
}
function createEdgeTable(info, startNode, endNode) {
  var idobj = document.getElementById("title");
  idobj.innerText = "Relationship: " + info.type;
  var nameobj = document.getElementById("name");
  nameobj.innerText = "From: " + startNode.number + " - " + startNode.name;
  var typeobj = document.getElementById("type");
  typeobj.innerText = "To: " + endNode.number + " - " + endNode.name;
  var dateobj = document.getElementById("date");
  var teamobj = document.getElementById("team");
  var dsnobj = document.getElementById("designer");
  if (info.type == "similar") {
    var scores = info.properties;
    dateobj.innerText = "Sequence similarity: " + scores.seq_score.toFixed(2);
    teamobj.innerText = "Category similarity: " + scores.cat_score.toFixed(2);
    dsnobj.innerText = "Overall similarity: " + scores.overall_score.toFixed(2);
  } else {
    dateobj.innerText = "";
    teamobj.innerText = "";
    dsnobj.innerText = "";
  }
  // hide the <p> elements that have id "length", "contents", "category", "sequence", "url":
  var lobj = document.getElementById("length");
  lobj.style.display = "none";
  var conobj = document.getElementById("contents");
  conobj.style.display = "none";
  var catobj = document.getElementById("category");
  catobj.style.display = "none";
  var seqobj = document.getElementById("sequence");
  seqobj.style.display = "none";
  var urlobj = document.getElementById("url");
  urlobj.style.display = "none";
}
export default {
  components: {
    DownloadOutlined,
    LinkOutlined,
    headermenu,
  },
  created() {
    const curPart = localStorage.getItem("curPart");
    if (!curPart) {
      window.location.href = "/parts";
    } else {
      this.curPart = curPart;
    }
  },
  data() {
    return {
      defaultActivate: ["3"],
      curPart: null,
      loading: true,
      node: null,
      similarNodes: null,
      similarNodes_graph: null,
      activeKey: "1",
    };
  },
  mounted() {
    this.query_similarity();
  },
  methods: {
    query_similarity() {
      axios
        .post("/api/parthub/query_similarity", {
          curPart: this.curPart,
        })
        .then((response) => {
          this.similarNodes = response.data.result;
          this.similarNodes_graph = this.similarNodes
            .map((item) => item.part)
            .slice(0, 30);
          this.similarNodes_graph.push(this.curPart);
          this.similarNodes_graph = JSON.stringify(this.similarNodes_graph);
          this.draw();
        })
        .catch((error) => {
          console.error(error);
          this.$message.error(error.message);
        });
    },
    draw() {
      axios
        .post("/api/parthub/config", {
          curPart: this.curPart,
        })
        .then((response) => {
          var neo4jConfig = response.data.config;
          var ids = [parseInt(response.data.id)];
          var viz;
          var config = {
            containerId: "viz",
            neo4j: neo4jConfig,
            visConfig: {
              nodes: {
                shape: "dot",
                font: {
                  face: "HarmonyOS_Sans",
                  size: 10,
                },
                size: 15,
              },
              edges: {
                font: {
                  face: "HarmonyOS_Sans",
                  size: 8,
                },
              },
              interaction: {
                selectConnectedEdges: false,
              },
            },
            labels: {
              Part: {
                label: "number",
                color: "color",
                size: "nodesize",
                [NeoVis.NEOVIS_ADVANCED_CONFIG]: {
                  function: {
                    title: (props) =>
                      NeoVis.objectToTitleHtml(props, [
                        "name",
                        "type",
                        "length",
                        "team",
                        "designer",
                        "date",
                      ]),
                  },
                },
              },
            },
            relationships: {
              "refers to": {
                color: "#CCCCCC",
                [NeoVis.NEOVIS_ADVANCED_CONFIG]: {
                  static: {
                    label: "refers to",
                    width: 2,
                    arrows: "to",
                  },
                },
              },
              twins: {
                color: "#CCCCCC",
                [NeoVis.NEOVIS_ADVANCED_CONFIG]: {
                  static: {
                    label: "twins",
                    width: 1.5,
                  },
                },
              },
              similar: {
                color: "#F1DEA6",
                [NeoVis.NEOVIS_ADVANCED_CONFIG]: {
                  static: {
                    label: "similar",
                    width: 4,
                  },
                },
              },
            },
            initialCypher:
              `MATCH (n)<-[r:\`refers to\`|twins]-{1,3}(m) WHERE n.number IN ${this.similarNodes_graph} RETURN n,r,m LIMIT 120 ` +
              `UNION MATCH (n)-[r:\`refers to\`|twins]->{1,3}(m) WHERE n.number IN ${this.similarNodes_graph} RETURN n,r,m LIMIT 120 ` +
              `UNION MATCH (n:Part{number:'${this.curPart}'})-[r:similar]-(m) WHERE n.number IN ${this.similarNodes_graph} RETURN n,r,m LIMIT 50`,
          };
          console.log(config.initialCypher);
          viz = new NeoVis(config);
          var doubleClickLocked = false;
          var selectNodeLocked = false;
          var selectEdgeLocked = false;
          viz.registerOnEvent("clickNode", () => {
            viz.network.on("selectNode", function (properties) {
              if (!selectNodeLocked) {
                selectNodeLocked = true;
                var ids = properties.nodes;
                var clickedNodes = viz.nodes.get(ids);
                if (clickedNodes) {
                  createTable(clickedNodes[0].raw.properties);
                }
                setTimeout(function () {
                  selectNodeLocked = false;
                }, 300);
              }
            });
            viz.network.on("doubleClick", function (properties) {
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
          viz.registerOnEvent("clickEdge", () => {
            viz.network.on("selectEdge", function (properties) {
              if (!selectEdgeLocked) {
                selectEdgeLocked = true;
                var ids = properties.edges;
                var clickedEdges = viz.edges.get(ids);
                if (clickedEdges) {
                  var info = clickedEdges[0].raw;
                  var edgeNodes = viz.nodes.get([info.start, info.end]);
                  var startNode = edgeNodes[0].raw.properties;
                  var endNode = edgeNodes[1].raw.properties;
                  createEdgeTable(info, startNode, endNode);
                }
                setTimeout(function () {
                  selectEdgeLocked = false;
                }, 300);
              }
            });
          });
          viz.registerOnEvent("completed", () => {
            viz.network.on("stabilizationIterationsDone", function () {
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
        .catch((error) => {
          console.error(error);
          this.$message.error(error.message);
        });
    },
  },
};
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
