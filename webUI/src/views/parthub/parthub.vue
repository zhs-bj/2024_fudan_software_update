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
              width: 40%;
              margin-top: 4vh;
            "
          >
            <a-form
              :model="formState"
              @finish="onFinish(formState)"
              @finishFailed="onFinishFailed(formState)"
            >
              <a-form-item
                mode="horizontal"
                style="margin-top: 2vh"
                :rules="[
                  { required: true, message: 'Please input your query!' },
                ]"
              >
                <a-input
                  v-model:value="formState.query"
                  style="width: 80%"
                  placeholder="Enter search content..."
                >
                </a-input>
                <a-button slot="suffix" type="primary" html-type="submit">
                  Search
                </a-button>
              </a-form-item>
              <a-form-item
                :rules="[
                  { required: true, message: 'Please select a search type!' },
                ]"
              >
                Search parts by:
                <a-radio-group
                  v-model:value="formState.type"
                  :default-value="searchType"
                >
                  <a-radio-button value="number"> ID </a-radio-button>
                  <a-radio-button value="name"> Name </a-radio-button>
                  <a-radio-button value="sequence"> Sequence </a-radio-button>
                  <a-radio-button value="designer"> Designer </a-radio-button>
                  <a-radio-button value="team"> Team </a-radio-button>
                  <a-radio-button value="contents"> Content </a-radio-button>
                </a-radio-group>
              </a-form-item>
            </a-form>
            <p style="margin-top: 10vh; margin-bottom: 2vh">
              To search for similar parts of your own part, <br />
              please upload a part sequence file from your computer:
            </p>
            <a-select
              v-model:value="uploadPartType"
              style="width: 80%; margin-top: 2vh"
              @focus="focus"
              placeholder="Select part type"
            >
              <a-select-option value="promoter">promoter</a-select-option>
              <a-select-option value="rbs">RBS</a-select-option>
              <a-select-option value="cds">CDS</a-select-option>
            </a-select>
            <a-upload-dragger
              v-model:fileList="fileList"
              name="file"
              :max-count="1"
              :multiple="false"
              :disabled="!uploadPartType"
              :action="'/api/parthub/upload_part_file/' + uploadPartType"
              @change="handleChange"
              style="margin-top: 2vh; max-height: 25vh; display: block"
            >
              <p class="ant-upload-drag-icon">
                <InboxOutlined />
              </p>
              <p class="ant-upload-text">
                Click or drag file to this area to upload
              </p>
              <p class="ant-upload-hint">
                Please upload a single .gb or .fasta file
              </p>
            </a-upload-dragger>
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
import { reactive } from "vue";
import { message } from "ant-design-vue";
import { InboxOutlined } from "@ant-design/icons-vue";
const formState = reactive({
  query: "",
  type: "",
});
export default {
  components: {
    headermenu,
    InboxOutlined,
  },
  data() {
    return {
      searchType: "id",
      formState,
      defaultActivate: ["3"],
      fileList: [],
      uploadPartType: null,
    };
  },
  methods: {
    onFinish(values) {
      console.log(values);
      if (values.type === "sequence") {
        const regex = /^[ATCGatcgUu]+$/;
        if (!regex.test(values.query)) {
          message.warning("The input sequence must be a valid base sequence!");
          return;
        }
      }
      localStorage.setItem("partHubQuery", values.query);
      localStorage.setItem("partHubType", values.type);
      window.location.href = "/parts";
    },
    onFinishFailed(errorInfo) {
      console.log(errorInfo);
    },
    handleChange(info) {
      const status = info.file.status;
      if (status !== "uploading") {
        console.log(info.file, info.fileList);
      }
      if (status === "done") {
        message.success(`${info.file.name} file uploaded successfully.`);
        localStorage.setItem("curPart", info.file.response.part_id);
        window.location.href = "/treemap";
      } else if (status === "error") {
        message.error(`${info.file.name} file upload failed.`);
      }
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
