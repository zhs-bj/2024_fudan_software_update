import { createApp } from "vue";
import burden from "./burden.vue";
import Antd from "ant-design-vue";
import "ant-design-vue/dist/reset.css";
import "@/assets/font/font.css";

// createApp.config.productionTip = false;
createApp(burden).use(Antd).mount("#app");
