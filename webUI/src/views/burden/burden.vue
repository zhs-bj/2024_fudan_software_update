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
                <a-form-item mode="horizontal" style="margin-top: 4vh">
                  <a-cascader
                    v-model:value="value"
                    style="
                      width: 70%;
                      margin-top: 3vh;
                      margin-bottom: 0;
                      margin-right: 2vw;
                    "
                    :options="allBasicPartInfo"
                    placeholder="Basic parts library (Select commonly used parts here!)"
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
                  <a-button
                    type="dashed"
                    :disabled="!value"
                    @click="addPart"
                    style="width: 20%; margin-top: 2vh; margin-bottom: 0"
                  >
                    <PlusOutlined />
                    Add basic part
                  </a-button>
                </a-form-item>
                <a-form-item mode="horizontal">
                  <a-button
                    type="dashed"
                    @click="toParthub()"
                    style="width: 90%"
                  >
                    <SearchOutlined />
                    Search in PartHub
                  </a-button>
                </a-form-item>
                <a-form-item>
                  <a-divider>Add new parts:</a-divider>
                  <div mode="horizontal" style="width: 100%; margin-top: 2vh">
                    <a-select
                      v-model:value="uploadPartType"
                      style="width: 45%; margin-right: 8%"
                      @focus="focus"
                      placeholder="Select part type"
                    >
                      <a-select-option value="promoter">
                        promoter
                      </a-select-option>
                      <a-select-option value="RBS">RBS</a-select-option>
                      <a-select-option value="CDS">CDS</a-select-option>
                    </a-select>
                    <a-input
                      v-model:value="name"
                      style="width: 45%"
                      :disabled="!uploadPartType"
                      placeholder="Enter part name..."
                    />
                  </div>
                  <div
                    mode="horizontal"
                    style="width: 100%; margin-top: 2vh; margin-bottom: 2vh"
                  >
                    <a-input
                      v-model:value="seq"
                      style="width: 45%; margin-right: 2%"
                      :disabled="!uploadPartType"
                      placeholder="Enter part sequence..."
                    />
                    <p
                      style="
                        display: inline-block;
                        width: 4%;
                        max-height: 2vh;
                        margin-right: 2%;
                      "
                    >
                      or
                    </p>
                    <div
                      style="width: 45%; display: inline-block"
                      mode="horizontal"
                    >
                      <a-upload
                        v-model:file-list="fileList"
                        :max-count="1"
                        :action="'/api/upload_part_file/' + uploadPartType"
                        style="width: 100%"
                        @change="handleChange"
                      >
                        <a-button
                          type="dashed"
                          :disabled="!uploadPartType"
                          style="width: 100%"
                        >
                          <UploadOutlined />
                          Upload a single .gb or .fasta file
                        </a-button>
                      </a-upload>
                    </div>
                  </div>
                  <a-button
                    type="dashed"
                    :disabled="!uploadPartType || !name || !seq"
                    @click="addToLibrary"
                    style="width: 90%"
                  >
                    <PlusOutlined />
                    Add to basic parts library
                  </a-button>
                </a-form-item>
                <a-divider>Current parts:</a-divider>
                <a-form-item style="height: 20vh; overflow-y: auto">
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
                        <b>Length:</b>&nbsp;{{ basicPart.info.name.length
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
                      <b>pMB1:</b>&nbsp;15-20 copies<br />
                      <b>pMB1 (derivative):</b>&nbsp;500-700 copies<br />
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
  UploadOutlined,
} from "@ant-design/icons-vue";
import { reactive } from "vue";
import { message } from "ant-design-vue";
import axios from "axios";

export default {
  components: {
    headermenu,
    MinusCircleOutlined,
    UpCircleOutlined,
    DownCircleOutlined,
    PlusOutlined,
    SearchOutlined,
    UploadOutlined,
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
      fileList: [],
      uploadPartType: null,
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
      this.formState.copy_number = parseFloat(this.formState.copy_number);
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
      message.info("Calculating burden...");
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
      console.log([this.name, this.seq]);
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
    handleChange(info) {
      const status = info.file.status;
      if (status !== "uploading") {
        console.log(info.file, info.fileList);
      }
      if (status === "done") {
        message.success(`${info.file.name} file uploaded successfully.`);
        this.seq = info.file.response.seq;
        if (!this.name) {
          this.name = info.file.name;
        }
      } else if (status === "error") {
        message.error(`${info.file.name} file upload failed.`);
      }
    },
    addToLibrary() {
      const regex = /^[ATCGatcgUu]+$/;
      if (!regex.test(this.seq)) {
        message.warning("The input sequence must be a valid base sequence!");
        return;
      }
      this.formState.parts.push({
        type: this.uploadPartType,
        info: { name: this.name, seq: this.seq },
        id: Date.now(),
      });
      localStorage.setItem("burdenParts", JSON.stringify(this.formState.parts));
      this.addItem(this.uploadPartType);
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
