<template>
  <div class="error-container m-2">
    <div class="content">
      <h2 class="title is-size-2">{{ title }}</h2>
      <p v-if="description">{{ description }}<a v-if="callToAction" :href="callToAction.link">{{
          callToAction.text
        }}</a>.</p>
    </div>
    <EmptyGraphic/>
  </div>
</template>

<script>
import EmptyGraphic from './svg/EmptyGraphic';

export default {
  name: 'ErrorState',
  props: {
    title: {
      type: String,
      required: true,
    },
    description: String,
    callToAction: {
      type: Object,
      validator: (value) => ('text' in value) && ('link' in value)
    }
  },
  components: {
    EmptyGraphic
  }
}
</script>