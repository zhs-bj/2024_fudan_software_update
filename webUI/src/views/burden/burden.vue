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
                @finish="onFinish(formState)"
                @finishFailed="onFinishFailed(formState)"
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
                <a-form-item
                  style="display: flex; justify-content: space-around"
                >
                  <a-button
                    type="dashed"
                    block
                    :disabled="!value"
                    style="width: 60%"
                    @click="addPart"
                  >
                    <PlusOutlined />
                    Add basic part
                  </a-button>
                  <p style="margin: 0 2vw">Or</p>
                  <a-select
                    v-model:value="valueSearch"
                    show-search
                    placeholder="Search parts in registry"
                    style="width: 20vw"
                    :default-active-first-option="false"
                    :show-arrow="false"
                    :filter-option="false"
                    :not-found-content="null"
                    :options="registryParts"
                    @search="handleSearch"
                    @change="handleChange"
                  ></a-select>
                </a-form-item>
                <a-form-item style="max-height: 45vh; overflow-y: auto">
                  <a-space
                    v-for="basicPart in formState.parts"
                    :key="basicPart.id"
                    style="display: flex; margin-bottom: 8px"
                  >
                    <p>{{ basicPart.type }} - {{ basicPart.info.name }}</p>
                    <MinusCircleOutlined @click="removePart(basicPart)" />
                  </a-space>
                </a-form-item>
                <a-form-item>
                  <a-button type="primary" html-type="submit">
                    Calculate
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
import { MinusCircleOutlined, PlusOutlined } from "@ant-design/icons-vue";
import { reactive } from "vue";
import axios from "axios";

export default {
  components: {
    headermenu,
    MinusCircleOutlined,
    PlusOutlined,
    UploadOutlined,
  },
  data() {
    return {
      formState: reactive({ parts: [] }),
      defaultActivate: ["2"],
      value: null,
      allBasicPartInfo: null,
      name: "",
      seq: "",
      registryParts: [],
      valueSearch: null,
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
              value: { name: part.name, seq: part.seq },
            })),
          });
        }
        console.log(this.allBasicPartInfo);
      })
      .catch((error) => {
        console.log(error);
      });
  },
  methods: {
    onFinish(values) {
      console.log(values);
    },
    onFinishFailed(errorInfo) {
      console.log(errorInfo);
    },
    addItem(part_type) {
      console.log(this.allBasicPartInfo);
      console.log([this.name, this.seq]);
      this.allBasicPartInfo[part_type].push({
        name: this.name,
        seq: [this.name, this.seq],
      });
      this.name = "";
      this.seq = "";
    },
    removePart(part) {
      const index = this.formState.parts.indexOf(part);
      if (index !== -1) {
        this.formState.parts.splice(index, 1);
      }
    },
    addPart() {
      console.log(this.value);
      this.formState.parts.push({
        type: this.value[0],
        info: JSON.parse(JSON.stringify(this.value[1])),
        id: Date.now(),
      });
    },
    filter(inputValue, path) {
      return path.some(
        (option) =>
          option.label.toLowerCase().indexOf(inputValue.toLowerCase()) > -1
      );
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
