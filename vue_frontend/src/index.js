import Vue from "vue/dist/vue.js";
import Vuex from "vuex";
import storePlugin from "./vuex/vuex_store_as_plugin";
import HelloWorld from "./components/HelloWorld";

Vue.use(Vuex);
Vue.use(storePlugin);
Vue.config.productionTip = false;

new Vue({
  el: "#app",
  components: {HelloWorld}
});