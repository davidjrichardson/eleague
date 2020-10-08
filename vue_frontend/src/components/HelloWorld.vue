<template>
  <div class="container">
    <div class="columns">
      <div class="column is-full">
        <h1 class="title is-size-1 has-text-centered">{{ title }}</h1>
      </div>
    </div>
    <div class="columns">
      <div class="column is-4 is-offset-4">
        <div class="level">
          <div class="level-item">
            <button @click="decrement" class="button is-primary">-</button>
          </div>
          <div class="level-item">
            <span class="is-size-5">Count: <strong>{{ count }}</strong></span>
          </div>
          <div class="level-item">
            <button @click="increment" class="button is-primary">+</button>
          </div>
        </div>
        <title-changer></title-changer>
      </div>
    </div>
  </div>
</template>

<script>
import TitleChanger from "@/components/TitleChanger";
export default {
  name: 'HelloWorld',
  components: {TitleChanger},
  computed: {
    count() {
      return this.$store.state.counter.count
    },
    title() {
      return this.$store.state.title.title
    }
  },
  methods: {
    increment() {
      this.$store.commit('increment')
    },
    decrement() {
      this.$store.commit('decrement')
    }
  },
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
