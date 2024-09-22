<template>
  <a-layout-header
    :collapsed="collapsed"
    @toggle="collapsed = !collapsed"
    height="50"
  >
    <div class="logo"></div>
    <a-menu
      :default-selected-keys="defaultActivate"
      theme="dark"
      mode="horizontal"
      :style="{ lineHeight: '64px' }"
    >
      <a-menu-item key="1" @click="toHome()">
        <HomeFilled />&nbsp;Home
      </a-menu-item>
      <a-menu-item key="2" @click="toBurden()">
        <AppstoreFilled />&nbsp;Burden Predictor
      </a-menu-item>
      <a-menu-item key="3" @click="toParthub()">
        <DatabaseFilled />&nbsp;PartHub
      </a-menu-item>
      <a-menu-item key="4" @click="toGitlab()">
        <GitlabFilled />&nbsp;Gitlab
      </a-menu-item>
    </a-menu>
  </a-layout-header>
</template>
<script>
import {
  HomeFilled,
  AppstoreFilled,
  GitlabFilled,
  DatabaseFilled,
} from "@ant-design/icons-vue";
export default {
  data() {
    return {
      collapsed: false,
    };
  },
  props: ["defaultActivate"],
  methods: {
    toHome() {
      window.location.href = "/";
    },
    toBurden() {
      window.location.href = "/burden";
    },
    toParthub() {
      window.location.href = "/parthub";
    },
    toGitlab() {
      window.open("https://gitlab.igem.org/2024/software-tools/fudan");
    },
  },
  components: {
    HomeFilled,
    AppstoreFilled,
    DatabaseFilled,
    GitlabFilled,
  },
};
</script>
