<template>
  <a-layout id="app" style="min-height: 100vh">
    <a-layout>
      <headermenu :default-activate="defaultActivate"></headermenu>
      <a-layout-content style="padding: 0 50px">
        <div
          :style="{
            background: '#fff',
            padding: '24px',
            marginTop: '40px',
            minHeight: '75vh',
            display: 'flex',
            flexDirection: 'column',
            flexWrap: 'wrap',
            justifyContent: 'center',
            alignItems: 'center',
          }"
        >
          <img
            src="https://static.igem.wiki/teams/5115/software/software-logo.png"
            style="width: 40%"
          />
          <h1 style="font-size: 24px; text-align: center">
            🌟&nbsp;Welcome to PartHub 3.0!&nbsp;🌟
          </h1>
          <div mode="horizontal">
            <a-button
              type="text"
              @click="toTutorial"
              style="margin-right: 4px; font-size: 16px"
              ><InfoCircleOutlined />&nbsp;Tutorial</a-button
            >
            <a-button
              type="text"
              @click="toDoc"
              style="margin-right: 4px; font-size: 16px"
              ><FileTextOutlined />&nbsp;Documentation</a-button
            >
            <a-button type="text" @click="toGitlab" style="font-size: 16px"
              ><GitlabOutlined />&nbsp;Gitlab</a-button
            >
          </div>
        </div>
      </a-layout-content>
      <a-layout-footer style="text-align: center">
        PartHub 3.0 ©2024 Created by Hongcheng Chen
      </a-layout-footer>
    </a-layout>
  </a-layout>
</template>

<script>
import headermenu from "@/components/headermenu.vue";
import {
  InfoCircleOutlined,
  FileTextOutlined,
  GitlabOutlined,
} from "@ant-design/icons-vue";
export default {
  components: {
    headermenu,
    InfoCircleOutlined,
    FileTextOutlined,
    GitlabOutlined,
  },
  data() {
    return {
      defaultActivate: ["1"],
    };
  },
  methods: {
    toTutorial() {
      window.open("https://2024.igem.wiki/fudan/software/#tutorial");
    },
    toParthub() {
      window.open("https://2024.igem.wiki/fudan/software/#document");
    },
    toGitlab() {
      window.open("https://gitlab.igem.org/2024/software-tools/fudan");
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

.site-layout-content {
  min-height: 280px;
  padding: 24px;
}

.ant-row-rtl #components-layout-demo-top .logo {
  float: right;
  margin: 16px 0 16px 24px;
}

[data-theme="dark"] .site-layout-content {
  background: #141414;
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
