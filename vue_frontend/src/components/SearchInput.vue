<template>
  <div class="archer-search-container">
    <div class="field">
      <div class="control has-icons-left has-icons-right">
        <input class="input" type="text" placeholder="Search archer names" id="archerSearch"
               @input="updateText">
        <span class="icon is-small is-left">
          <i class="fas fa-search"></i>
        </span>
      </div>
    </div>
    <a href="#" class="clear-text-button" id="clearText" data-for="archerSearch"
       @click="clearSearch">
      <span class="icon">
        <i class="fas fa-times-circle"></i>
      </span>
    </a>
  </div>
</template>

<script>
import {debounce} from "debounce";

export default {
  name: 'SearchInput',
  methods: {
    clearSearch() {
      this.$store.dispatch('dashboard/searchArcherList', "");
      document.getElementById("archerSearch").value = "";
    },
    updateText: debounce(function(e) {
      this.$store.dispatch('dashboard/searchArcherList', e.target.value);
    }, 250)
  },
}
</script>

<style scoped></style>