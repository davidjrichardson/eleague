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
import gsap from 'gsap';

export default {
  name: 'SearchInput',
  methods: {
    clearSearch() {
      this.$store.dispatch('dashboard/searchArcherList', "");
      document.getElementById("archerSearch").value = "";
      // Animate the clear button out
      let clearBtn = document.getElementById('clearText');
      gsap.fromTo(clearBtn, {
          display: 'block',
          opacity: 1,
          x: 0,
        }, {
          duration: 0.3,
          ease: 'power4.in',
          opacity: 0,
          x: 8,
        }).then(() => gsap.set(clearBtn, {display: 'none'}));
    },
    updateText: debounce(function(e) {
      this.$store.dispatch('dashboard/searchArcherList', e.target.value);
      // Animate the clear button in or out
      let clearBtn = document.getElementById('clearText');
      if (e.target.value.length > 0) {
        gsap.fromTo(clearBtn, {
          display: 'block',
          opacity: 0,
          x: 8,
        }, {
          ease: 'power4.out',
          duration: 0.3,
          opacity: 1,
          x: 0,
        });
      } else {
        gsap.fromTo(clearBtn, {
          display: 'block',
          opacity: 1,
          x: 0,
        }, {
          duration: 0.3,
          ease: 'power4.in',
          opacity: 0,
          x: 8,
        }).then(() => gsap.set(clearBtn, {display: 'none'}));
      }
    }, 100)
  },
}
</script>

<style scoped></style>