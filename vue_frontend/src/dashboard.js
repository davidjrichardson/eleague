import Vue from "vue/dist/vue.js";
import Vuex from "vuex";
import storePlugin from "./vuex/PersistedStoreAsPlugin";
import DashboardArcherTable from "./components/DashboardArcherTable";

Vue.use(Vuex);
Vue.use(storePlugin);
Vue.config.productionTip = false;

new Vue({
    el: "#app",
    components: {DashboardArcherTable},
    data: {
        archers: []
    }
});