import Vue from "vue/dist/vue.js";
import Vuex from "vuex";

import createPersistedState from "vuex-persistedstate";
import DashboardArcherTableModule from "@/vuex/DashboardArcherTableModule";

Vue.use(Vuex);

let plugins = [];
plugins.push(createPersistedState({
        paths: []
    }
));

let store = new Vuex.Store({
    plugins: plugins,
    modules: {
        dashboard: DashboardArcherTableModule
    },
    strict: process.env.NODE_ENV !== "production",
});

export default {
    store,
    install(Vue) { //resetting the default store to use this store
        Vue.prototype.$store = store;
    }
}
