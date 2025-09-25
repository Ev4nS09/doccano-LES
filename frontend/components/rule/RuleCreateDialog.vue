<template>
  <v-dialog v-model="showDialog" max-width="600" persistent>
    <v-card class="pa-4">
      <v-card-title class="headline text-center justify-center py-4">
        Create New Rule
      </v-card-title>
      
      <v-card-text>
        <v-form ref="form" @submit.prevent="create">
          <v-row class="d-flex justify-center">
            <!-- Title Field -->
            <v-col cols="11" class="py-1">
              <v-text-field
                v-model="title"
                label="Title"
                :rules="[v => !!v || 'Title is required']"
                required
                outlined
                dense
              ></v-text-field>
            </v-col>

            <!-- Description Field -->
            <v-col cols="11" class="py-1">
              <v-textarea
                v-model="description"
                label="Description"
                :rules="[v => !!v || 'Description is required']"
                required
                outlined
                rows="3"
                dense
              ></v-textarea>
            </v-col>

            <!-- Date/Time Pickers -->
            <v-col cols="11" md="5" class="py-1 mx-auto">
              <v-menu
                ref="startMenu"
                v-model="startMenu"
                :close-on-content-click="false"
                transition="scale-transition"
                offset-y
                min-width="auto"
              >
                <template v-slot:activator="{ on, attrs }">
                  <v-text-field
                    v-model="startDisplay"
                    label="Start At"
                    prepend-icon="mdi-calendar-clock"
                    readonly
                    v-bind="attrs"
                    v-on="on"
                    outlined
                    dense
                  ></v-text-field>
                </template>
                <v-card>
                  <v-date-picker
                    v-model="startDate"
                    no-title
                    scrollable
                  ></v-date-picker>
                  <v-time-picker
                    v-model="startTime"
                    format="24hr"
                    scrollable
                    full-width
                  ></v-time-picker>
                  <v-card-actions class="justify-end">
                    <v-btn text color="primary" @click="startMenu = false">
                      OK
                    </v-btn>
                  </v-card-actions>
                </v-card>
              </v-menu>
            </v-col>

            <v-col cols="11" md="5" class="py-1 mx-auto">
              <v-menu
                ref="endMenu"
                v-model="endMenu"
                :close-on-content-click="false"
                transition="scale-transition"
                offset-y
                min-width="auto"
              >
                <template v-slot:activator="{ on, attrs }">
                  <v-text-field
                    v-model="endDisplay"
                    label="End At"
                    prepend-icon="mdi-calendar-clock"
                    readonly
                    v-bind="attrs"
                    v-on="on"
                    outlined
                    dense
                  ></v-text-field>
                </template>
                <v-card>
                  <v-date-picker
                    v-model="endDate"
                    no-title
                    scrollable
                    :min="startDate"
                  ></v-date-picker>
                  <v-time-picker
                    v-model="endTime"
                    format="24hr"
                    scrollable
                    full-width
                  ></v-time-picker>
                  <v-card-actions class="justify-end">
                    <v-btn text color="primary" @click="endMenu = false">
                      OK
                    </v-btn>
                  </v-card-actions>
                </v-card>
              </v-menu>
            </v-col>
          </v-row>
        </v-form>
      </v-card-text>

      <v-card-actions class="justify-center pb-4">
        <v-btn
          color="grey"
          text
          @click="close"
          class="mx-2"
        >
          Cancel
        </v-btn>
        <v-btn
          color="primary"
          depressed
          @click="create"
          :loading="isLoading"
          class="mx-2"
        >
          Create Rule
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script lang="ts">
import Vue from 'vue'
import { RuleDTO } from '~/services/application/rule/ruleData'
// import { Rule } from '~/domain/models/rule/rule'

export default Vue.extend({
  props: {
    show: {
      type: Boolean,
      default: false
    },
    projectId: {
      type: Number,
      required: true
    }
  },

  data() {
    return {
      showDialog: this.show,
      title: '',
      description: '',
      startDate: '',
      startTime: '00:00',
      endDate: '',
      endTime: '00:00',
      startMenu: false,
      endMenu: false,
      isLoading: false
    }
  },

  computed: {
    startDisplay(): string {
      if (!this.startDate) return ''
      return `${this.startDate} ${this.startTime}`
    },
    endDisplay(): string {
      if (!this.endDate) return ''
      return `${this.endDate} ${this.endTime}`
    },
    start_at(): string {
      return `${this.startDate}T${this.startTime}:00`
    },
    end_at(): string {
      return `${this.endDate}T${this.endTime}:00`
    }
  },

  watch: {
    show(newVal) {
      this.showDialog = newVal
    },
    showDialog(newVal) {
      if (!newVal) {
        this.$emit('close')
      }
    }
  },

  methods: {
    close() {
      this.showDialog = false
      this.resetForm()
    },

    resetForm() {
      this.title = ''
      this.description = ''
      this.startDate = ''
      this.startTime = '00:00'
      this.endDate = ''
      this.endTime = '00:00'
      if (this.$refs.form) {
        (this.$refs.form as any).resetValidation()
      }
    },

    async create() {
      if (!(this.$refs.form as any).validate()) return

      this.isLoading = true
      try {
        const rule = await this.$repositories.rule.create(this.projectId, {
          title: this.title,
          description: this.description,
          project: this.projectId,
          created_by: this.$store.getters['auth/getUserId'],
          start_at: this.start_at,
          end_at: this.end_at,
          upvotes: [],
          downvotes: [],
          status: 'On going'
        } as RuleDTO)


        this.$emit('create', rule)
        this.close()
      } catch (e) {
        console.error('Failed to create rule')
        console.error('Failed to create rule', e)
      } finally {
        this.isLoading = false
      }
    }
  }
})
</script>

<style scoped>
.v-card {
  border-radius: 12px !important;
}
.v-text-field, .v-textarea {
  margin: 4px 0;
}
.v-picker {
  border-radius: 8px !important;
}
.v-card__actions {
  padding: 0 16px 16px;
}
</style>
