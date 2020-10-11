import {publicPath} from "../../vue.config";
import axios from 'axios';

export default {
    namespaced: true,
    state: {
        allArchers: [],
        displayed: [],
        isLoading: false,
    },
    mutations: {
        filter: (state, filterFn) => state.displayed = state.allArchers.filter(filterFn),
        startLoading: (state) => state.isLoading = true,
        endLoading: (state) => state.isLoading = false,
        getArchers: (state, archers) => {
            state.allArchers = archers;
            state.displayed = state.allArchers;
        }
    },
    actions: {
        async refreshArchers(context) {
            let apiPath = publicPath.replace('8080/', '8000');
            context.commit('startLoading');
            await axios.get(`${apiPath}/dashboard/api/archers`)
                .then(response => {
                    context.commit('endLoading');
                    context.commit('getArchers', response.data);
                }).catch(error => {
                    context.commit('endLoading');
                    console.log(error);
            });
        },
        async searchArcherList(context, searchStr) {
            console.log(searchStr);
            let filterFn = (archer) => archer.full_name.toLowerCase().indexOf(searchStr.toLowerCase()) > -1;
            context.commit('filter', filterFn);
        }
    }
}