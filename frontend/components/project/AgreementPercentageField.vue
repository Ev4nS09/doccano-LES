<template>
	<v-text-field
	  v-bind="$attrs"
	  :value="value"
	  label="Agreement Percentage"
	  type="number"
	  suffix="%"
	  :min="0"
	  :max="100"
	  :step="0.1"
	  required
	  :rules="rules"
	  class="agreement-percentage-field"
	  @input="handleInput"
	/>
  </template>
  
  <script lang="ts">
  import Vue from 'vue'
  
  export default Vue.extend({
	props: {
	  value: {
		type: Number,
		default: 50.0,
		required: true
	  }
	},
	data() {
	  return {
		rules: [
		  (v: number) => (v >= 0 && v <= 100) || 'Must be between 0% and 100%'
		]
	  }
	},
	methods: {
	  handleInput(value: string) {
		const numValue = value === '' ? 0 : Number(value)
		this.$emit('input', numValue)
	  }
	}
  })
  </script>

<style scoped>
.agreement-percentage-field {
  width: 150px; /* Adjust this value as needed */
}
</style>