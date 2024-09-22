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
            flexDirection: 'column',
            justifyContent: 'flex-start',
            alignItems: 'center',
          }"
        >
          <div
            style="
              text-align: center;
              height: 100%;
              margin-top: 2vh;
              padding-bottom: 1.5rem;
              display: inline-flex;
              align-items: center;
            "
          >
            <a-form
              layout="inline"
              :model="formState"
              @finish="onFinish(formState)"
              @finishFailed="onFinishFailed(formState)"
            >
              <a-form-item
                mode="horizontal"
                :rules="{
                  initialValue: searchQuery,
                  rules: [
                    { required: true, message: 'Please input your query!' },
                  ],
                }"
              >
                <a-input
                  v-model:value="formState.query"
                  :defaultValue="searchQuery"
                  placeholder="..."
                >
                </a-input>
                <a-button slot="suffix" type="primary" html-type="submit">
                  Search
                </a-button>
              </a-form-item>
              <a-form-item
                :rules="{
                  initialValue: searchType,
                  rules: [
                    { required: true, message: 'Please select a search type!' },
                  ],
                }"
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
          </div>
          <a-spin v-if="loading" tip="loading" size="large"></a-spin>
          <partcard
            v-else
            :list-data="listData"
            :search-query="searchQuery"
            style="width: 95%"
            @clickTitle="showPart"
          >
          </partcard>
        </div>
      </a-layout-content>
      <a-layout-footer
        style="text-align: center; padding-top: 12px; padding-bottom: 12px"
      >
        xxx ©2024 Created by Hongchen Chen
      </a-layout-footer>
    </a-layout>
  </a-layout>
</template>
<script>
import headermenu from "@/components/headermenu.vue";
import partcard from "@/components/partcard.vue";
import axios from "axios";
import { reactive } from "vue";
import { message } from "ant-design-vue";
const listData = [];
const formState = reactive({
  query: "",
  type: "",
});
export default {
  created() {
    const searchType = localStorage.getItem("partHubType");
    const searchQuery = localStorage.getItem("partHubQuery");
    if (!searchType || !searchQuery) {
      window.location.href = "/parthub";
    }
    axios
      .post("/api/parthub/search", {
        partHubType: searchType,
        partHubQuery: searchQuery,
      })
      .then((response) => {
        console.log(response.data);
        if (response.data.message) {
          message.info(response.data.message);
        } else {
          this.listData = response.data;
        }
        this.loading = false;
      })
      .catch((error) => {
        console.error(error);
        message.error(error.message);
        this.loading = false;
      });
  },
  components: {
    partcard,
    headermenu,
  },
  data() {
    return {
      formState,
      defaultActivate: ["3"],
      searchResults: [],
      searchType: localStorage.getItem("partHubType"),
      searchQuery: localStorage.getItem("partHubQuery"),
      listData,
      loading: true,
      number: "",
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
    showPart(num) {
      localStorage.setItem("curPart", num);
      window.open("/treemap");
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
