<template>
  <a-layout id="app" style="min-height: 100vh">
    <a-layout>
      <a-layout-header>
        <div class="logo"></div>
        <a-menu :default-selected-keys="1" theme="dark" mode="horizontal" :style="{ lineHeight: '64px' }">
          <a-menu-item key="1" @click="toHome()">
            <HomeFilled />Home
          </a-menu-item>
          <a-menu-item key="2" @click="toBurden()">
            <AppstoreFilled />Burden Predictor
          </a-menu-item>
          <a-menu-item key="3" @click="toParthub()">
            <DatabaseFilled />PartHub
          </a-menu-item>
          <a-menu-item key="4" @click="toGitlab()">
            <GitlabFilled />Gitlab
          </a-menu-item>
        </a-menu>
      </a-layout-header>
      <a-layout-content style="padding: 0 50px;">
        <div :style="{ background: '#fff', padding: '24px', marginTop: '40px', minHeight: '280px' }">Content</div>
      </a-layout-content>
      <a-layout-footer style="text-align: center">
        xxx ©2024 Created by Hongcheng Chen
      </a-layout-footer>
    </a-layout>
  </a-layout>
</template>

<script>
import { HomeFilled, AppstoreFilled, GitlabFilled, DatabaseFilled } from '@ant-design/icons-vue';
export default {
  data() {
    return {
      collapsed: false,
    };
  },
  methods: {
    toHome() { window.location.href = '/'; },
    toBurden() { window.location.href = '/burden'; },
    toParthub() { window.location.href = '/parthub'; },
    toGitlab() {
      window.open('https://gitlab.igem.org/2024/software-tools/fudan')
    },
  },
  components: {
    HomeFilled, AppstoreFilled, DatabaseFilled, GitlabFilled
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
  background: #fff;
}

#components-layout-demo-top .logo {
  float: left;
  width: 120px;
  height: 31px;
  margin: 16px 24px 16px 0;
  background: rgba(255, 255, 255, 0.3);
}

.ant-row-rtl #components-layout-demo-top .logo {
  float: right;
  margin: 16px 0 16px 24px;
}

[data-theme='dark'] .site-layout-content {
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
