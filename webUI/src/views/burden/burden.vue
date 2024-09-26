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
          <div
            style="
              text-align: center;
              height: 85vh;
              width: 80vw;
              display: flex;
              flex-direction: row;
            "
          >
            <div style="height: 100%; width: 50vw">
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
                    :displayRender="
                      () =>
                        value[0] +
                        ' - ' +
                        value[1].name +
                        ' (' +
                        valueName[value[0]] +
                        ': ' +
                        value[1].value.toFixed(4) +
                        ')'
                    "
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
                <a-form-item style="height: 45vh; overflow-y: auto">
                  <a-space
                    v-for="basicPart in formState.parts"
                    :key="basicPart.id"
                    style="display: flex; margin-bottom: 8px"
                  >
                    <a-tooltip placement="right">
                      <template #title>
                        <b>Name:</b>&nbsp;{{
                          basicPart.info.name.length > 50
                            ? basicPart.info.name.slice(0, 47) + "..."
                            : basicPart.info.name
                        }}<br />
                        <b>Sequence:</b>&nbsp;{{
                          basicPart.info.seq.length > 50
                            ? basicPart.info.seq.slice(0, 41) +
                              "..." +
                              basicPart.info.seq.slice(-6)
                            : basicPart.info.seq
                        }}
                      </template>
                      <a-tag :color="tagColor[basicPart.type]"
                        >{{ basicPart.type }} - {{ basicPart.info.name }}
                      </a-tag>
                      <a-tag v-if="basicPart.info.value" :color="yellow">
                        {{ valueName[basicPart.type] }}:
                        {{ basicPart.info.value }}
                      </a-tag>
                    </a-tooltip>
                    <MinusCircleOutlined @click="removePart(basicPart)" />
                    <UpCircleOutlined @click="moveUpPart(basicPart)" />
                    <DownCircleOutlined @click="moveDownPart(basicPart)" />
                  </a-space>
                </a-form-item>
                <a-form-item mode="horizontal">
                  <a-tooltip placement="bottomLeft">
                    <template #title>
                      <b>Copy numbers for common plasmids:</b>
                      <br />
                      <b>Average Low:</b>&nbsp;15-20 copies<br />
                      <b>Average Medium:</b>&nbsp;20-100 copies<br />
                      <b>Average High:</b>&nbsp;500-700 copies<br />
                      <b>pSB1C3, pSB1A2:</b>&nbsp;100-300 copies<br />
                      <b>J61002:</b>&nbsp;25-30 copies<br />
                    </template>
                    <a-input
                      v-model:value="formState.copy_number"
                      placeholder="Enter copy number"
                      overlay-class-name="numeric-input"
                      addon-before="Copy number:"
                      style="width: 40%; margin-right: 2vw"
                      :rules="[
                        { required: true, message: 'Missing copy number' },
                      ]"
                      @change="changeCopyNumber"
                    >
                    </a-input>
                  </a-tooltip>
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
                display: flex;
                flex-direction: column;
                flex-wrap: wrap;
                justify-content: center;
                height: 100%;
                width: 25vw;
                margin-left: 24px;
              "
            >
              <p style="font-size: 24px; margin-bottom: 12px">Burden</p>
              <p
                :style="{
                  fontSize: '36px',
                  marginBottom: '50px',
                  color: burdenValue
                    ? burdenValue <= 0.1
                      ? 'green'
                      : burdenValue <= 0.2
                      ? '#ffdc54'
                      : burdenValue <= 0.4
                      ? '#ffa44b'
                      : 'red'
                    : 'lightgray',
                  fontWeight: burdenValue && burdenValue > 0.2 ? 'bold' : '',
                }"
              >
                {{
                  burdenValue
                    ? (burdenValue * 100).toFixed(4) + "%"
                    : "Not calculated yet"
                }}
              </p>
              <p style="font-size: 16px; color: #707070; text-align: justify">
                {{
                  burdenValue
                    ? burdenValue <= 0.1
                      ? "These BioBricks are generally well-tolerated by the host cells, with minimal impact on growth and stability. They are suitable for most applications and have a low risk of mutational inactivation."
                      : burdenValue <= 0.2
                      ? "These BioBricks can moderately affect cell growth and may show some instability over time. Users should monitor for potential mutations, especially in larger cultures or over multiple cell divisions."
                      : burdenValue <= 0.4
                      ? "These BioBricks significantly impact cell growth and are at a higher risk of mutational inactivation. Careful monitoring and frequent re-cloning are recommended to maintain functionality."
                      : "These BioBricks are highly burdensome and are likely to mutate rapidly, making them unclonable and unsuitable for most applications. Avoid using these unless absolutely necessary and with strict controls."
                    : ""
                }}
              </p>
            </div>
          </div>
        </div>
      </a-layout-content>
      <a-layout-footer
        style="text-align: center; padding-top: 12px; padding-bottom: 12px"
      >
        PartHub 3.0 ©2024 Created by Hongcheng Chen
      </a-layout-footer>
    </a-layout>
  </a-layout>
</template>
<script>
import headermenu from "@/components/headermenu.vue";
import {
  MinusCircleOutlined,
  UpCircleOutlined,
  DownCircleOutlined,
  PlusOutlined,
  SearchOutlined,
} from "@ant-design/icons-vue";
import { reactive } from "vue";
import axios from "axios";

export default {
  components: {
    headermenu,
    MinusCircleOutlined,
    UpCircleOutlined,
    DownCircleOutlined,
    PlusOutlined,
    SearchOutlined,
  },
  data() {
    return {
      formState: reactive({ parts: [], copy_number: null }),
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
      valueName: {
        promoter: "Relative promoter strength",
        RBS: "Relative RBS strength",
        CDS: "Length (AA)",
      },
      burdenValue: null,
    };
  },
  beforeCreate() {
    axios
      .get("/api/burden/get_basic_part_info")
      .then((response) => {
        var res = response.data.result;
        this.allBasicPartInfo = [];
        for (var partType in res) {
          this.allBasicPartInfo.push({
            label: partType,
            value: partType,
            children: res[partType].map((part) => ({
              label: part.name,
              value: {
                name: part.name,
                value: part.value,
                seq: part.seq.toUpperCase(),
              },
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
    this.formState.copy_number = localStorage.getItem("burdenCopyNumber");
    if (!this.formState.copy_number || this.formState.copy_number == "null") {
      this.formState.copy_number = 15;
    } else {
      this.formState.copy_number = parseInt(this.formState.copy_number);
    }
    console.log(this.formState.parts);
  },
  methods: {
    onFinish(values) {
      values = JSON.parse(JSON.stringify(values));
      console.log(values);
      var parts_structure = values
        .map((item) => item.type[0].toUpperCase())
        .join("");
      console.log(parts_structure);
      const regex = /^P(RC)+$/;
      if (!regex.test(parts_structure)) {
        this.$message.warning(
          "Invalid part structure. The part should begin with a promoter, followed by one or more RBS sequences, each of which is then followed by a CDS."
        );
        return;
      }
      axios
        .post("/api/burden/calculate", {
          parts: values,
          copy_number: this.formState.copy_number,
        })
        .then((response) => {
          console.log(response.data);
          this.burdenValue = response.data.result;
          for (var i in response.data.values) {
            this.formState.parts[i].info.value = response.data.values[i];
          }
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
            value: {
              name: this.name,
              seq: this.seq.toUpperCase(),
            },
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
    moveUpPart(part) {
      const index = this.formState.parts.indexOf(part);
      if (index !== -1 && index !== 0) {
        this.formState.parts.splice(index, 1);
        this.formState.parts.splice(index - 1, 0, part);
        localStorage.setItem(
          "burdenParts",
          JSON.stringify(this.formState.parts)
        );
      }
    },
    moveDownPart(part) {
      const index = this.formState.parts.indexOf(part);
      if (index !== -1 && index !== this.formState.parts.length - 1) {
        this.formState.parts.splice(index, 1);
        this.formState.parts.splice(index + 1, 0, part);
        localStorage.setItem(
          "burdenParts",
          JSON.stringify(this.formState.parts)
        );
      }
    },
    clearAllParts() {
      this.formState.parts = [];
      localStorage.setItem("burdenParts", JSON.stringify(this.formState.parts));
    },
    changeCopyNumber() {
      localStorage.setItem("burdenCopyNumber", this.formState.copy_number);
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
