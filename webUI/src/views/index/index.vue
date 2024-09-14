<template>
  <a-layout id="app" style="min-height: 100vh">
    <a-layout>
      <headermenu :default-activate="defaultActivate"></headermenu>
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
import headermenu from "@/components/headermenu.vue";
export default {
  components: {
    headermenu
  },
  data() {
    return {
      defaultActivate: ['1'],
    };
  },
}
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
