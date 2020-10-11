<template>
  <div>
    <div class="spinner" id="loadingSpinner" v-if="false">
      <div class="dot1"></div>
      <div class="dot2"></div>
    </div>
    <SearchInput/>
    <EmptyState v-if="archersList.length === 0 && !isLoading"
                title="No archers registered"
                description="Start registering archers for this academic year "
                v-bind:call-to-action="{
                  text: 'here',
                  link: '#'
                }"/>
    <div id="archersContainer"
         v-if="archersList.length > 0">
      <div class="archers-table">
        <div class="columns reversed-columns">
          <div class="column is-one-quarter is-offset-three-quarters"></div>
          <div class="column is-three-quarters">
            <!-- TODO: Say how many archers that are being displayed -->
            <p class="dash-subtitle subtitle">Displaying {{ archersList.length }} archer</p>
            <div class="table-container">
              <table class="table is-fullwidth is-hoverable">
                <thead>
                <tr>
                  <th>Name</th>
                  <th>Sex</th>
                  <th>Experience</th>
                </tr>
                </thead>
                <tbody>
                <tr v-for="archer in archersList"
                    v-bind:key="archer.id">
                  <td>{{ archer.full_name }}</td>
                  <td>{{ archer.get_sex_display }}</td>
                  <td>{{ archer.get_experience_display }}</td>
                </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import SearchInput from './SearchInput';
import EmptyState from './EmptyState';

export default {
  name: 'DashboardArcherTable',
  computed: {
    archersList() {
      return this.$store.state.dashboard.displayed;
    },
    isLoading() {
      return this.$store.state.dashboard.isLoading;
    }
  },
  methods: {},
  mounted() {
    // Get the latest archer list from the backend
    // TODO: Show/hide the spinner
    this.$store.dispatch('dashboard/refreshArchers');
  },
  components: {
    EmptyState, SearchInput
  },
}
</script>

<style scoped></style>