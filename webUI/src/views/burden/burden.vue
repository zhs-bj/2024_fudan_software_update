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
            justifyContent: 'center',
            alignItems: 'center',
          }"
        >
          <div style="text-align: center; height: 85vh; width: 80vw">
            <div style="display: inline-block; height: 100%; width: 50vw">
              <a-form
                :model="formState"
                @finish="onFinish(formState.parts)"
                @finishFailed="onFinishFailed(formState.parts)"
              >
                <a-form-item style="margin-top: 24px">
                  <a-cascader
                    v-model:value="value"
                    :options="allBasicPartInfo"
                    placeholder="Select parts..."
                    :show-search="{ filter }"
                    :displayRender="() => value[0] + ' - ' + value[1].name"
                  />
                  <!-- <a-form-item
                  :name="['parts', index, 'type']"
                  label="Basic part type:"
                  :rules="{
                    required: true,
                    message: 'Missing part type',
                  }"
                >
                  <a-select
                    v-model:value="basicPart.type"
                    placeholder="Select part type..."
                    :options="basicPartTypes.map((a) => ({ value: a }))"
                    style="width: 130px"
                  ></a-select>
                </a-form-item>
                <a-form-item
                  :name="['parts', index, 'info']"
                  label="Part information:"
                  :rules="[
                    { required: true, message: 'Missing part information' },
                  ]"
                >
                  <a-select
                    v-model:value="basicPart.info"
                    placeholder="Select part..."
                    style="width: 40vw"
                    :disabled="!basicPart.type"
                    :options="
                      (console.log(allBasicPartInfo[basicPart.type]),
                      (allBasicPartInfo[basicPart.type] || []).map((item) => ({
                        value: item.name,
                      })))
                    "
                  >
                    <template #dropdownRender="{ menuNode: menu }">
                      <v-nodes :vnodes="menu" />
                      <a-divider style="margin: 4px 0" />
                      <a-space style="padding: 4px 8px">
                        <a-input
                          v-model:value="name"
                          placeholder="Enter part name..."
                        />
                        <a-input
                          v-model:value="seq"
                          placeholder="Enter part sequence..."
                        />
                        <a-button type="text" @click="addItem(basicPart.type)">
                          <PlusOutlined />
                          Add {{ basicPart.type }}
                        </a-button>
                      </a-space>
                    </template>
                  </a-select>
                </a-form-item>
                
const regex = /^[ATCGatcgUu]+$/;
if (!regex.test(values.query)) {
  message.warning("The input sequence must be a valid base sequence!");
  return;
}
                
                -->
                </a-form-item>
                <a-form-item mode="horizontal">
                  <a-button
                    type="dashed"
                    :disabled="!value"
                    @click="addPart"
                    style="width: 45%; margin-right: 2vw"
                  >
                    <PlusOutlined />
                    Add basic part
                  </a-button>
                  <a-button
                    type="dashed"
                    @click="toParthub()"
                    style="width: 45%"
                  >
                    <SearchOutlined />
                    Search in PartHub
                  </a-button>
                </a-form-item>
                <a-form-item style="max-height: 45vh; overflow-y: auto">
                  <a-space
                    v-for="basicPart in formState.parts"
                    :key="basicPart.id"
                    style="display: flex; margin-bottom: 8px"
                  >
                    <a-tooltip placement="right">
                      <template #title>
                        <b>Name:</b>&nbsp;{{
                          basicPart.info.name.length > 30
                            ? basicPart.info.name.slice(0, 27) + "..."
                            : basicPart.info.name
                        }}<br />
                        <b>Sequence:</b>&nbsp;{{
                          basicPart.info.seq.length > 30
                            ? basicPart.info.seq.slice(0, 21) +
                              "..." +
                              basicPart.info.seq.slice(-6)
                            : basicPart.info.seq
                        }}
                      </template>
                      <a-tag :color="tagColor[basicPart.type]"
                        >{{ basicPart.type }} - {{ basicPart.info.name }}
                      </a-tag>
                    </a-tooltip>
                    <MinusCircleOutlined @click="removePart(basicPart)" />
                  </a-space>
                </a-form-item>
                <a-form-item> </a-form-item>
                <a-form-item mode="horizontal">
                  <a-button
                    type="primary"
                    html-type="submit"
                    style="margin-right: 2vw"
                  >
                    Calculate
                  </a-button>
                  <a-button type="default" @click="clearAllParts()">
                    Clear all parts
                  </a-button>
                </a-form-item>
              </a-form>
            </div>
            <div
              style="
                display: inline-block;
                height: 100%;
                width: 25vw;
                margin-left: 24px;
              "
            >
              <p>Burden: xx</p>
            </div>
          </div>
        </div>
      </a-layout-content>
      <a-layout-footer
        style="text-align: center; padding-top: 12px; padding-bottom: 12px"
      >
        xxx ©2024 Created by Hongcheng Chen
      </a-layout-footer>
    </a-layout>
  </a-layout>
</template>
<script>
import headermenu from "@/components/headermenu.vue";
import {
  MinusCircleOutlined,
  PlusOutlined,
  SearchOutlined,
} from "@ant-design/icons-vue";
import { reactive } from "vue";
import axios from "axios";

export default {
  components: {
    headermenu,
    MinusCircleOutlined,
    PlusOutlined,
    SearchOutlined,
  },
  data() {
    return {
      formState: reactive({ parts: [] }),
      defaultActivate: ["2"],
      value: null,
      allBasicPartInfo: null,
      name: "",
      seq: "",
      tagColor: {
        promoter: "blue",
        RBS: "orange",
        CDS: "green",
      },
    };
  },
  beforeCreate() {
    axios
      .get("/api/burden/get_basic_part_info")
      .then((response) => {
        var res = response.data;
        this.allBasicPartInfo = [];
        for (var partType in res) {
          this.allBasicPartInfo.push({
            label: partType,
            value: partType,
            children: res[partType].map((part) => ({
              label: part.name,
              value: { name: part.name, seq: part.seq.toUpperCase() },
            })),
          });
        }
      })
      .catch((error) => {
        console.log(error);
      });
  },
  created() {
    this.formState.parts = localStorage.getItem("burdenParts");
    if (!this.formState.parts || this.formState.parts == "null") {
      this.formState.parts = [];
    } else {
      this.formState.parts = JSON.parse(this.formState.parts);
    }
    console.log(this.formState.parts);
  },
  methods: {
    onFinish(values) {
      values = JSON.parse(JSON.stringify(values));
      console.log(values);
      var parts_structure = values.map((item) => item.type[0].toUpperCase());
      const regex = /^P(RC)+$/;
      if (!regex.test(parts_structure)) {
        this.$message.warning(
          "Invalid part structure. The part should begin with a promoter, followed by one or more RBS sequences, each of which is then followed by a CDS."
        );
      }
      axios
        .post("/api/burden/calculate", values)
        .then((response) => {
          console.log(response.data);
          this.$message.success("Burden calculation completed!");
        })
        .catch((error) => {
          console.log(error);
          this.$message.error("Burden calculation failed!");
        });
    },
    onFinishFailed(errorInfo) {
      console.log(errorInfo);
    },
    addItem(part_type) {
      for (var i in this.allBasicPartInfo) {
        if (this.allBasicPartInfo[i].value == part_type) {
          this.allBasicPartInfo[i].children.push({
            label: this.name,
            value: { name: this.name, seq: this.seq.toUpperCase() },
          });
          break;
        }
      }
      this.name = "";
      this.seq = "";
    },
    removePart(part) {
      const index = this.formState.parts.indexOf(part);
      if (index !== -1) {
        this.formState.parts.splice(index, 1);
      }
      localStorage.setItem("burdenParts", JSON.stringify(this.formState.parts));
    },
    addPart() {
      this.formState.parts.push({
        type: this.value[0],
        info: JSON.parse(JSON.stringify(this.value[1])),
        id: Date.now(),
      });
      localStorage.setItem("burdenParts", JSON.stringify(this.formState.parts));
    },
    clearAllParts() {
      this.formState.parts = [];
      localStorage.setItem("burdenParts", JSON.stringify(this.formState.parts));
    },
    filter(inputValue, path) {
      return path.some(
        (option) =>
          option.label.toLowerCase().indexOf(inputValue.toLowerCase()) > -1
      );
    },
    toParthub() {
      window.location.href = "/parthub";
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
