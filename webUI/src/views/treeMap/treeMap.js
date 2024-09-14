import { createApp } from "vue";
import treeMap from "./treeMap.vue";
import Antd from "ant-design-vue";
import "ant-design-vue/dist/reset.css";
import "@/assets/font/font.css";

// createApp.config.productionTip = false;
createApp(treeMap).use(Antd).mount("#app");
