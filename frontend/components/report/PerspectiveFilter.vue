<template>
  <div>
    <v-btn color="primary" @click="showDialog = true">
      Filter by Perspective
    </v-btn>

    <v-dialog v-model="showDialog" max-width="600">
      <v-card>
        <v-card-title>Filter by Perspective</v-card-title>
        <v-card-text>
          <v-form ref="form">
            <v-container>
              <template v-for="(item, index) in perspectiveItems">
                <!-- Integer/Float Input -->
                <template v-if="isNumberType(item.item_type) && filters[item.id]">
                  <v-row :key="`range-${index}`">
                    <v-col cols="12">
                      <h3>{{ item.name }}</h3>
                    </v-col>
                    <v-col cols="6">
                      <v-text-field
                        v-model.number="filters[item.id].min"
                        :label="'Min ' + item.name"
                        type="number"
                        :step="item.item_type === 'int' ? 1 : 0.01"
                      ></v-text-field>
                    </v-col>
                    <v-col cols="6">
                      <v-text-field
                        v-model.number="filters[item.id].max"
                        :label="'Max ' + item.name"
                        type="number"
                        :step="item.item_type === 'int' ? 1 : 0.01"
                        :rules="[
                          val => !filters[item.id].min || 
                                val >= filters[item.id].min 
                                || 'Must be greater than min'
                        ]"
                      ></v-text-field>
                    </v-col>
                  </v-row>
                </template>

                <!-- Boolean Input -->
                <template v-else-if="item.item_type === 'bool' && filters[item.id]">
                  <v-row :key="`bool-${index}`">
                    <v-col cols="12">
                      <h3>{{ item.name }}</h3>
                      <v-radio-group v-model="filters[item.id].value" row>
                        <v-radio label="True" :value="true"></v-radio>
                        <v-radio label="False" :value="false"></v-radio>
                      </v-radio-group>
                    </v-col>
                  </v-row>
                </template>

                <!-- List Input -->
                <template v-else-if="item.item_type === 'list' && filters[item.id]">
                  <v-row :key="`list-${index}`">
                    <v-col cols="12">
                      <h3>{{ item.name }}</h3>
                      <v-select
                        v-model="filters[item.id].values"
                        :items="item.selection_list"
                        multiple
                        chips
                        clearable
                      ></v-select>
                    </v-col>
                  </v-row>
                </template>
              </template>
            </v-container>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-btn text @click="resetFilters">Reset</v-btn>
          <v-spacer></v-spacer>
          <v-btn text @click="showDialog = false">Cancel</v-btn>
          <v-btn color="primary" @click="applyFilters">Apply</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'
import { PerspectiveItem } from '~/domain/models/perspective/perspective'

interface Filter {
  type: string;
  min?: number | null;
  max?: number | null;
  value?: boolean | null;
  values?: string[];
}

export default Vue.extend({
  props: {
    perspectiveId: {
      type: Number,
      required: true
    }
  },

  data() {
    return {
      showDialog: false,
      perspectiveItems: [] as PerspectiveItem[],
      filters: {} as Record<number, Filter>
    }
  },

  async created() {
    await this.loadPerspectiveItems()
    this.initializeFilters()
  },

  methods: {
    isNumberType(type: string): boolean {
      return ['int', 'float'].includes(type)
    },

    async loadPerspectiveItems() {
      try {
        this.perspectiveItems = 
                    await this.$repositories.perspective.listPerspectiveItem(this.perspectiveId)
      } catch (error) {
        console.error('Error loading perspective items:', error)
        this.perspectiveItems = []
      }
    },

    initializeFilters() {
      const newFilters: Record<number, Filter> = {}
      
      this.perspectiveItems.forEach(item => {
        if (this.isNumberType(item.item_type)) {
          newFilters[item.id] = {
            type: item.item_type,
            min: null,
            max: null
          }
        } else if (item.item_type === 'bool') {
          newFilters[item.id] = {
            type: item.item_type,
            value: null
          }
        } else if (item.item_type === 'list') {
          newFilters[item.id] = {
            type: item.item_type,
            values: []
          }
        }
      })

      this.filters = newFilters
    },

    resetFilters() {
      this.initializeFilters()
      const form = this.$refs.form as any
      if (form) {
        form.resetValidation()
      }
    },

    applyFilters() {
      const form = this.$refs.form as any
      if (form && form.validate()) {
        // Create a clean copy of filters
        const cleanedFilters: Record<number, Filter> = {}
        
        Object.entries(this.filters).forEach(([key, filter]) => {
          const id = Number(key)
          cleanedFilters[id] = { ...filter }
        })

        this.$emit('filter', cleanedFilters)
        this.showDialog = false
      }
    }
  }
})
</script>
