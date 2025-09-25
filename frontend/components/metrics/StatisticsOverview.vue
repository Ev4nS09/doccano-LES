<template>
	<v-card id="statisticsOverview">
	  <v-card-title>General Statistics</v-card-title>
	  <v-divider />
	  <v-card-text>
		<v-row>
		  <v-col cols="12" md="3">
			<stat-card 
			  title="Total Examples" 
			  :value="stats.totalExamples" 
			  :icon="mdiFileDocumentMultiple"
			  tooltip="The total number of examples in the Dataset"
			/>
		  </v-col>
		  <v-col cols="12" md="3">
			<stat-card 
				title="Analyzed Examples"
			  :value="stats.annotatedExamples" 
			  :icon="mdiMagnify"
			  tooltip="The total number of locked examples"
			/>
		  </v-col>
		  <v-col cols="12" md="3">
			<stat-card 
			  title="Avg. Participation Rate" 
			  :value="stats.participationRate + '%'" 
			  :icon="mdiAccountGroup"
			  tooltip="Average percentage of members who have annotated at least 
			  one value in each example"
			/>
		  </v-col>
		  <v-col cols="12" md="3">
			<stat-card 
			  title="Avg. Full Participation" 
			  :value="stats.fullParticipationRate + '%'" 
			  :icon="mdiAccountCheck"
			  tooltip="Average percentage of examples that have been annotated by all members"
			/>
		  </v-col>
		</v-row>
	  </v-card-text>
	</v-card>
  </template>
  
  <script>

import {
	mdiFileDocumentMultiple,
	mdiMagnify,
	mdiAccountGroup,
	mdiAccountCheck,
  } from '@mdi/js'
  import StatCard from './StatCard.vue'
  
  export default {
	components: { StatCard },
	props: {
	  projectId: {
		type: String,
		required: true
	  },
	  stats: {
		type: Object,
		required: true
	  }
	},

	data() {
		return {
			mdiFileDocumentMultiple,
			mdiMagnify,
			mdiAccountGroup,
			mdiAccountCheck,
		}
	},
  }
  </script>