<template>
  <div class="level">
    <div class="level-item">
      <div class="field has-addons">
        <div class="control">
          <input @keydown="enterKey" id="titleInput" class="input" type="text" :placeholder="title">
        </div>
        <div class="control">
          <button @click="changeTitle" class="button is-primary">Save</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'TitleChanger',
  computed: {
    title() {
      return this.$store.state.title.title
    }
  },
  methods: {
    enterKey(event) {
      if (event.keyCode === 13) {
        this.changeTitle();
      }
    },
    changeTitle() {
      let newTitle = document.getElementById("titleInput").value
      this.$store.commit('changeTitle', newTitle)
    }
  }
}
</script>