import { createApp } from "vue";
import parts from "./parts.vue";
import Antd from "ant-design-vue";
import "ant-design-vue/dist/reset.css";
import "@/assets/font/font.css";

// createApp.config.productionTip = false;
createApp(parts).use(Antd).mount("#app");
