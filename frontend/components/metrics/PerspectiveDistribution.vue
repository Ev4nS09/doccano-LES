<template>
  <v-card>
    <v-card-title>Statistics</v-card-title>
    <v-divider />
    <v-card-text>
      <v-row>
        <v-col cols="12">
          <v-card
            v-for="(example, exampleId) in examples"
            :key="exampleId"
            :class="['Stats-Card', theme]"
            class="mb-4"
          >
            <v-card-title>{{ example.filename }}</v-card-title>
            <v-card-subtitle v-if="example.id">ID: {{ example.id }}</v-card-subtitle>
            <v-card-text>
              <v-row dense>
                <v-col
                  v-for="(percentage, labelId) in exampleStats[example.id]"
                  :key="labelId"
                  cols="12"
                  class="mb-3"
                >
                  <div class="d-flex justify-space-between mb-1">
                    <span>{{ getLabelText(labelId) }}</span>
                    <span>{{ percentage }}%</span>
                  </div>
                  <v-progress-linear
                    :value="percentage"
                    :color="getLabelColor(labelId)"
                    height="16"
                    rounded
					          striped
                  />
                </v-col>
              </v-row>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-card-text>
  </v-card>
</template>

<script lang="ts">
import Vue from 'vue'
import { computed, useContext } from '@nuxtjs/composition-api'

export default Vue.extend({
  props: {
    exampleStats: {
      type: Object as () => Record<string, Record<string, number>>,
      required: true
    },
    examples: {
      type: Array as () => any[],
      required: true
    },
    labels: {
      type: Array as () => Array<{
        id: number
        text: string
        background_color: string
      }>,
      required: true
    }
  },
  setup() {
    const { $vuetify } = useContext()
    const theme = computed(() => ($vuetify.theme.dark ? 'dark' : 'light'))
    return {
      theme
    }
  },
  methods: {
    getLabelText(labelId: string): string {
      const label = this.labels.find(l => l.id === parseInt(labelId))
      return label ? label.text : `Label ${labelId}`
    },
    getLabelColor(labelId: string): string {
      const label = this.labels.find(l => l.id === parseInt(labelId))
	  console.log(label)
	  console.log('Exemplos recebidos:', this.examples)
      return label ? label.backgroundColor : 'primary'
    },
    getSelectedItemsStats() {
      // First, get perspective filters from parent component
      const perspectiveFilters = this.$parent.$refs.perspectiveFilters?.addedFilters || [];
      
      // Then transform label distribution
      const labelDistribution = {};
      
      for (const [exampleId, labelStats] of Object.entries(this.exampleStats)) {
        const example = this.examples.find(e => e.id === parseInt(exampleId));
        
        const exampleKey = example 
          ? `${example.filename || 'Unknown'} (ID: ${exampleId})` 
          : `Example ${exampleId}`;
        
        labelDistribution[exampleKey] = {};
        
        for (const [labelId, percentage] of Object.entries(labelStats)) {
          const label = this.labels.find(l => l.id === parseInt(labelId));
          const labelText = label ? label.text : `Label ${labelId}`;
          labelDistribution[exampleKey][labelText] = percentage;
        }
      }
      
      // Return with perspective filters at the top
      return {
        perspectiveFilters: perspectiveFilters.map(filter => ({
          perspective: filter.itemName,
          type: filter.itemType,
          value: this.isNumericType(filter.itemType) 
            ? { 
                min: filter.min !== undefined ? filter.min : null,
                max: filter.max !== undefined ? filter.max : null
              }
            : filter.value
        })),
        labelDistribution
      };
    },
    isNumericType(type: string): boolean {
      return type === 'int' || type === 'float';
    }
  }
})
</script>

<style scoped>
.Stats-Card.light {
  background-color: #e0e0e038;
}
.Stats-Card.dark {
  background-color: #252525;
}
</style>