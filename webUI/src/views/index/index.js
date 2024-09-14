import { createApp } from "vue";
import index from "./index.vue";
import Antd from "ant-design-vue";
import "ant-design-vue/dist/reset.css";
import "@/assets/font/font.css";

// createApp.config.productionTip = false;
createApp(index).use(Antd).mount("#app");
