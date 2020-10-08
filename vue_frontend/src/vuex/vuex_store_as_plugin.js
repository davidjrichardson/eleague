import Vue from "vue/dist/vue.js";
import Vuex from "vuex";
import createPersistedState from "vuex-persistedstate";
import CounterModule from "./vuex_module_counter";
import TitleModule from "./vuex_module_title";

Vue.use(Vuex);
let plugins = [];
plugins.push(createPersistedState({
        paths: ["counter.count", "title.title"]
    }
));

let store = new Vuex.Store({
    plugins: plugins,
    modules: {
        counter: CounterModule,
        title: TitleModule,
    },
    strict: process.env.NODE_ENV !== "production",
});

export default {
    store,
    install(Vue) { //resetting the default store to use this store
        Vue.prototype.$store = store;
    }
}
