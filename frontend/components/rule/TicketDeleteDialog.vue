<template>
	<v-dialog :value="show" max-width="500" @input="$emit('close')">
	  <v-card>
		<v-card-title>Delete Tickets</v-card-title>
		<v-card-text>
		  Are you sure you want to delete the selected tickets?
		</v-card-text>
		<v-card-actions>
		  <v-spacer />
		  <v-btn text @click="$emit('close')">Cancel</v-btn>
		  <v-btn color="error" text @click="$emit('confirm')">Delete</v-btn>
		</v-card-actions>
	  </v-card>
	</v-dialog>
  </template>
  
  <script lang="ts">
  import Vue from 'vue'
  
  export default Vue.extend({
	props: {
	  show: {
		type: Boolean,
		required: true
	  }
	}
  })
  </script>