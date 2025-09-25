
<template>
  <v-card>
    <v-card-title>
      <span class="headline">Label Usage Statistics</span>
      <v-spacer />
      <v-btn icon @click="$emit('close')">
        <v-icon>mdi-close</v-icon>
      </v-btn>
    </v-card-title>

    <v-card-text>
      <v-data-table
        :headers="headers"
        :items="tableData"
        :loading="loading"
        :items-per-page="10"
        :footer-props="{
          'items-per-page-options': [10, 25, 50],
          showFirstLastPage: true
        }"
        class="elevation-1"
      >
        <!-- Fixed slot syntax -->
        <template slot="item.text" slot-scope="{ item }">
          <div class="text-truncate" style="max-width: 400px">{{ item.text }}</div>
        </template>
      </v-data-table>
    </v-card-text>
  </v-card>
</template>

<script lang="ts">
import Vue from 'vue'
import { ExampleItem } from '~/domain/models/example/example'
import { LabelItem } from '~/domain/models/label/label'
import { Category } from '~/domain/models/tasks/category'

export default Vue.extend({
  props: {
    projectId: {
      type: String,
      required: true
    }
  },

  data() {
    return {
      loading: false,
      examples: [] as ExampleItem[],
      labels: [] as LabelItem[],
      categories: [] as Category[],
      labelCounts: {} as Record<string, Record<string, number>>, // { exampleId: { labelId: count }}
    }
  },

  computed: {
    headers() {
      const labelHeaders = this.labels.map(label => ({
        text: label.text,
        value: `label_${label.id}`,
        align: 'center',
        sortable: true,
        width: '150px'
      }))

      return [
        { 
          text: 'Example', 
          value: 'text', 
          sortable: true,
          width: '400px'
        },
        ...labelHeaders
      ]
    },

    tableData() {
      return this.examples.map(example => {
        const row: any = {
          id: example.id,
          text: example.text,
        }

        // Add label counts for each label
        this.labels.forEach(label => {
          const count = this.labelCounts[example.id]?.[label.id] || 0
          row[`label_${label.id}`] = count
        })

        return row
      })
    }
  },

  async mounted() {
    await this.loadData()
  },

  methods: {
    async loadData() {
      this.loading = true
      try {
        // Load labels
        this.labels = await this.$repositories.categoryType.list(this.projectId)

        // Load examples
        const exampleResponse = await this.$repositories.example.list(this.projectId, {
          limit: '100',
          offset: '0',
          q: '',
          isChecked: '',
          ordering: ''
        })
        this.examples = exampleResponse.items

        // Load categories (annotations) to count label usage
        await this.loadLabelCounts()
        
      } catch (error) {
        console.error('Failed to load report data', error)
      } finally {
        this.loading = false
      }
    },

     async loadLabelCounts() {
      try {
        const counts: Record<string, Record<string, number>> = {}

        // Process each example to get its categories
        await Promise.all(this.examples.map(async example => {
          const categories = await this.$repositories.category.listAll(this.projectId, example.id)
          
          if (!counts[example.id]) {
            counts[example.id] = {}
          }

          // Count label occurrences for this example
          categories.forEach(category => {
            if (!counts[example.id][category.label]) {
              counts[example.id][category.label] = 0
            }
            counts[example.id][category.label]++
          })
        }))

        this.labelCounts = counts
      } catch (error) {
        console.error('Failed to load label counts', error)
      }
    }}
})
</script>

<style scoped>
.text-truncate {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.v-chip {
  min-width: 36px;
  justify-content: center;
}
</style>
