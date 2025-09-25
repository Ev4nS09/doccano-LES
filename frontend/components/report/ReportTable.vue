<template>
  <v-card>
    <v-card-title>
      <span class="headline">Report</span>
      <v-spacer />
      <v-btn class="mr-2" @click="exportToPDF" color="primary" small>Export to PDF</v-btn>
      <v-btn icon @click="$emit('close')">
        <v-icon>mdi-close</v-icon>
      </v-btn>
    </v-card-title>

    <v-card-text>
      <div ref="tableToExport">
        <v-data-table
          :headers="headers"
          :items="visibleTableData"
          :loading="loading"
          :items-per-page="10"
          :footer-props="{
            'items-per-page-options': [10, 25, 50],
            'showFirstLastPage': true
          }"
          class="elevation-1"
        >
          <template slot="item.text" slot-scope="{ item }">
            <div class="text-truncate" style="max-width: 400px">{{ item.text }}</div>
          </template>
        </v-data-table>
      </div>
    </v-card-text>
  </v-card>
</template>

<script lang="ts">
import Vue from 'vue'
import { jsPDF } from 'jspdf'
import 'jspdf-autotable'
import { ExampleItem } from '~/domain/models/example/example'
import { LabelItem } from '~/domain/models/label/label'

export default Vue.extend({
  props: {
    projectId: {
      type: String,
      required: true
    },
    filters: {
      type: Object,
      default: () => ({})
    }
  },

  data() {
    return {
      loading: false,
      examples: [] as ExampleItem[],
      labels: [] as LabelItem[],
      labelCounts: {} as Record<string, Record<string, number>>,
      dataLoaded: false
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
        ...labelHeaders,
        {
          text: 'No Labels',
          value: 'noLabels',
          align: 'center',
          sortable: true,
          width: '150px'
        },
        {
          text: 'Total',
          value: 'totalVotes',
          align: 'center',
          sortable: true,
          width: '150px'
        }
      ]
    },

    visibleTableData() {
      if (!this.dataLoaded) return []

      return this.examples.map(example => {
        const row: any = {
          id: example.id,
          text: example.text,
        }

        const counts = this.labelCounts[example.id] || {}
        let totalLabelVotes = 0

        this.labels.forEach(label => {
          const count = counts[label.id] || 0
          row[`label_${label.id}`] = count
          totalLabelVotes += count
        })

        const totalAnnotators = example.assignments.length
        const noLabelsCount = Math.max(0, totalAnnotators - totalLabelVotes)
        row.noLabels = noLabelsCount
        row.totalVotes = totalAnnotators

        return row
      }).filter(row => {
        return !this.hasFilters() ||
          this.labels.some(label => row[`label_${label.id}`] > 0) ||
          row.noLabels > 0
      })
    }
  },

  watch: {
    filters: {
      handler() {
        this.loadLabelCounts()
      },
      deep: true
    }
  },

  async mounted() {
    await this.loadData()
    this.dataLoaded = true
  },

  methods: {
    exportToPDF() {
      try {
        // eslint-disable-next-line new-cap
        const doc = new jsPDF('p', 'pt', 'a4')
        
        // Layout configuration
        const leftMargin = 50
        const rightMargin = doc.internal.pageSize.width - 50
        const valueCol = 250 // Fixed right-aligned position for all numbers
        
        let yPosition = 50
        
        // Title Section
        doc.setFontSize(20)
        doc.setTextColor(63, 81, 181)
        doc.setFont('helvetica', 'bold')
        doc.text('Report', leftMargin, yPosition)
        yPosition += 25
        
        // Date Section
        doc.setFontSize(12)
        doc.setTextColor(120, 120, 120)
        doc.setFont('helvetica', 'normal')
        doc.text(`Generated on ${new Date().toLocaleDateString()}`, leftMargin, yPosition)
        yPosition += 40
        
        // Examples Section
        doc.setFontSize(11)
        
        this.visibleTableData.forEach((example, index) => {
          // Page break check
          if (yPosition > doc.internal.pageSize.height - 100) {
            doc.addPage()
            yPosition = 50
          }
          
          // Example Header Only
          doc.setFillColor(245, 245, 245)
          doc.rect(leftMargin, yPosition - 10, rightMargin - leftMargin, 20, 'F')
          doc.setFont('helvetica', 'bold')
          doc.setTextColor(63, 81, 181)
          doc.text(`Example ${index + 1}: ${example.text.substring(0, 80)}${example.text.length > 80 ? '...' : ''}`, 
                  leftMargin + 10, yPosition + 5)
          yPosition += 30
          
          // Calculate max label width for this example
          let maxLabelWidth = 0
          this.labels.forEach(label => {
            const width = doc.getStringUnitWidth(label.text) * doc.internal.scaleFactor
            if (width > maxLabelWidth) maxLabelWidth = width
          })
          
          // Labels Section - All numbers right-aligned at valueCol
          this.labels.forEach(label => {
            const count = example[`label_${label.id}`] || 0
            
            // Label name
            doc.setFont('helvetica', 'normal')
            doc.setTextColor(70, 70, 70)
            doc.text(`${label.text}:`, leftMargin + 20, yPosition)
            
            // Count value (right-aligned)
            doc.setFont('helvetica', 'bold')
            doc.setTextColor(63, 81, 181)
            doc.text(count.toString(), valueCol, yPosition, { align: 'right' })
            
            yPosition += 18
          })
          
          // Summary Section
          doc.setDrawColor(220, 220, 220)
          doc.line(leftMargin + 10, yPosition, rightMargin - 10, yPosition)
          yPosition += 15
          
          // No Labels (right-aligned)
          doc.setFont('helvetica', 'normal')
          doc.setTextColor(70, 70, 70)
          doc.text('No Labels:', leftMargin + 20, yPosition)
          doc.setFont('helvetica', 'bold')
          doc.setTextColor(63, 81, 181)
          doc.text(example.noLabels.toString(), valueCol, yPosition, { align: 'right' })
          yPosition += 18
          
          // Total Votes (right-aligned)
          doc.setFont('helvetica', 'bold')
          doc.setTextColor(40, 40, 40)
          doc.text('Total:', leftMargin + 20, yPosition)
          doc.setTextColor(63, 81, 181)
          doc.text(example.totalVotes.toString(), valueCol, yPosition, { align: 'right' })
          yPosition += 30
          
          // Separator
          if (index < this.visibleTableData.length - 1) {
            doc.setDrawColor(230, 230, 230)
            doc.line(leftMargin, yPosition, rightMargin, yPosition)
            yPosition += 20
          }
        })
        
        // Footer
        doc.setFontSize(10)
        doc.setTextColor(150, 150, 150)
        doc.text('Generated by Doccano', leftMargin, doc.internal.pageSize.height - 30)
        
        doc.save(`label-report-${new Date().toISOString().slice(0, 10)}.pdf`)
      } catch (err) {
        console.error('Error exporting to PDF:', err)
        this.$toast.error('Failed to generate PDF report')
      }
    },
        hasFilters() {
      return this.filters && Object.keys(this.filters).length > 0
    },

    async loadData() {
      this.loading = true
      try {
        const [labels, exampleResponse] = await Promise.all([
          this.$repositories.categoryType.list(this.projectId),
          this.$repositories.example.list(this.projectId, {
            limit: '100',
            offset: '0',
            q: '',
            isChecked: '',
            ordering: ''
          })
        ])
        this.labels = labels
        this.examples = exampleResponse.items
        await this.loadLabelCounts()
      } catch (error) {
        console.error('Failed to load report data:', error)
      } finally {
        this.loading = false
      }
    },

    async loadLabelCounts() {
      try {
        const counts: Record<string, Record<string, number>> = {}

        await Promise.all(this.examples.map(async example => {
          counts[example.id] = {}
          const categories = await this.$repositories.category.listAll(
            this.projectId,
            example.id
          )

          await Promise.all(categories.map(async category => {
            const member = await this.$repositories.member.list(this.projectId).then(members =>
              members.find(m => m.user === category.user)
            )
            const memberId = member?.id
            const labelId = category.label

            const isValid = await this.validateMemberAgainstFilters(memberId)

            if (isValid) {
              if (!counts[example.id][labelId]) {
                counts[example.id][labelId] = 0
              }
              counts[example.id][labelId]++
            }
          }))
        }))

        this.labelCounts = counts
        await this.updateTableData()
      } catch (error) {
        console.error('Failed to load label counts:', error)
      }
    },

    async validateMemberAgainstFilters(memberId: number): Promise<boolean> {
      if (!this.hasFilters() || !memberId) return true

      try {
        const memberValues = await this.$repositories.perspective.findValueById(
          memberId.toString()
        )


        return Object.entries(this.filters).every(([itemId, filter]) => {
          const perspectiveValue = memberValues.find(v =>
            v.item.toString() === itemId.toString()
          )
          if (!perspectiveValue) return false
          const value = perspectiveValue.value
          if (value === undefined) return false

          if (filter.type === 'int' || filter.type === 'float') {
            if (filter.min !== null && value < filter.min) return false
            if (filter.max !== null && value > filter.max) return false
          } else if (filter.type === 'bool') {
                if (filter.value !== null) {
          // Convert both values to proper booleans
          const filterBool = filter.value === true || filter.value === 'true'
          const valueBool = value === true || value === 'true'
          return filterBool === valueBool
        }
      }else if (filter.type === 'list' && filter.values.length > 0 && !filter.values.includes(value)) {
            return false
          }
          return true
        })
      } catch (error) {
        console.error(`Failed to validate member ${memberId}:`, error)
        return false
      }
    },

    async getTotalAssigneesFiltered(example: ExampleItem): Promise<number> {
      if (!this.hasFilters()) return example.assignments.length

      try {
        const members = await this.$repositories.member.list(this.projectId)
        let validCount = 0
        await Promise.all(
          example.assignments.map(async assignment => {
            const member = members.find(m => m.user === assignment.assignee_id)
            if (member && await this.validateMemberAgainstFilters(member.id)) {
              validCount++
            }
          })
        )
        return validCount
      } catch (error) {
        console.error('Failed to count filtered assignees:', error)
        return 0
      }
    },

    async updateTableData() {
      await Promise.all(this.examples.map(async example => {
        const totalAssigneesFiltered = await this.getTotalAssigneesFiltered(example)
        const counts = this.labelCounts[example.id] || {}
        let totalLabelVotes = 0

        this.labels.forEach(label => {
          totalLabelVotes += counts[label.id] || 0
        })

        const noLabelsCount = Math.max(0, totalAssigneesFiltered - totalLabelVotes)
        const row = this.visibleTableData.find(r => r.id === example.id)
        if (row) {
          row.noLabels = noLabelsCount
          row.totalVotes = totalAssigneesFiltered
        }
      }))
    }
  }
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

