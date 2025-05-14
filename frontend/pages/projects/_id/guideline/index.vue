<template>
  <v-card>
    <v-card-title>
      <rule-action-menu @create="createRule" />
      <v-btn
        class="text-capitalize ms-2"
        :disabled="!canDelete"
        outlined
        @click.stop="dialogDelete = true"
      >
        {{ $t('generic.delete') }}
      </v-btn>
      <v-dialog v-model="dialogDelete">
        <v-card>
          <v-card-title>Delete Rules</v-card-title>
          <v-card-text>
            Are you sure you want to delete the selected rules?
          </v-card-text>
          <v-card-actions>
            <v-spacer />
            <v-btn text @click="dialogDelete = false">Cancel</v-btn>
            <v-btn color="error" text @click="remove">Delete</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-card-title>
    <rule-list
      v-model="selected"
      :items="rules"
      :is-loading="isLoading"
      @edit="editRule"
      @details="showDetails"
      @chat="openChat"
      @upvote="upvoteRule"
      @downvote="downvoteRule"
      @status="updateStatus"
    />

    <!-- Details Dialog -->
    <v-dialog v-model="showDetailsDialog" max-width="800">
      <rule-details 
        v-if="selectedRule" 
        :rule="selectedRule" 
        :project-id="projectId"
        @close="showDetailsDialog = false"
      />
    </v-dialog>
    
    <!-- Chat Dialog -->
    <v-dialog v-model="showChatDialog" max-width="800">
      <rule-chat 
        v-if="selectedRule" 
        :rule="selectedRule"
        :project-id="projectId"
        @close="showChatDialog = false"
        @refresh="refreshRule"
      />
    </v-dialog>
  </v-card>
</template>

<script lang="ts">
import Vue from 'vue'
import RuleActionMenu from '~/components/rule/ActionMenu.vue'
import RuleList from '~/components/rule/RuleList.vue'
import RuleDetails from '~/components/rule/RuleDetails.vue'
import RuleChat from '~/components/rule/RuleChat.vue'
import { RuleDTO } from '~/services/application/rule/ruleData'

export default Vue.extend({
  components: {
    RuleActionMenu,
    RuleList,
    RuleDetails,
    RuleChat
  },

  layout: 'project',

  middleware: ['check-auth', 'auth', 'setCurrentProject'],

  validate({ params }) {
    return /^\d+$/.test(params.id)
  },

  data() {
    return {
      dialogDelete: false,
      rules: [] as RuleDTO[],
      selected: [] as RuleDTO[],
      isLoading: false,
      selectedRule: null as RuleDTO | null,
      showDetailsDialog: false,
      showChatDialog: false
    }
  },

  computed: {
    projectId(): string {
      return this.$route.params.id
    },

    canDelete(): boolean {
      return this.selected.length > 0
    }
  },

  async created() {
    await this.listRules()
  },

  methods: {
    async listRules() {
      this.isLoading = true
      try {
        this.rules = await this.$services.rule.list(parseInt(this.projectId))
      } finally {
        this.isLoading = false
      }
    },

    createRule() {
      this.$router.push(`/projects/${this.projectId}/rules/create`)
    },

    editRule(rule: RuleDTO) {
      this.$router.push(`/projects/${this.projectId}/rules/${rule.id}/edit`)
    },

    showDetails(rule: RuleDTO) {
      this.selectedRule = rule
      this.showDetailsDialog = true
    },

    async openChat(rule: RuleDTO) {
      try {
        // Load the rule with its comments
        const ruleWithComments = await this.$services.rule.getWithComments(
          parseInt(this.projectId),
          rule.id
        )
        this.selectedRule = ruleWithComments
        this.showChatDialog = true
      } catch (error) {
        console.error('Failed to load rule with comments:', error)
        // Fallback to basic rule data if comments fail to load
        this.selectedRule = rule
        this.showChatDialog = true
      }
    },

    async refreshRule() {
      if (this.selectedRule) {
        try {
          const refreshedRule = await this.$services.rule.getWithComments(
            parseInt(this.projectId),
            this.selectedRule.id
          )
          this.selectedRule = refreshedRule
          // Also update the rule in the main list
          this.rules = this.rules.map(r => 
            r.id === refreshedRule.id ? refreshedRule : r
          )
        } catch (error) {
          console.error('Failed to refresh rule:', error)
        }
      }
    },

    async upvoteRule(rule: RuleDTO) {
      try {
        await this.$services.rule.vote(parseInt(this.projectId), rule.id, 1)
        await this.listRules()
      } catch (e) {
        console.error('Failed to upvote rule', e)
      }
    },

    async downvoteRule(rule: RuleDTO) {
      try {
        await this.$services.rule.vote(parseInt(this.projectId), rule.id, -1)
        await this.listRules()
      } catch (e) {
        console.error('Failed to downvote rule', e)
      }
    },


    async updateStatus(rule: RuleDTO) {
      try {
        if(rule.score > 0)
            await this.$services.rule.status(parseInt(this.projectId), rule.id, 1)
        else 
            await this.$services.rule.status(parseInt(this.projectId), rule.id, -1)

        await this.listRules()
      } catch (e) {
        console.error('Failed to update status', e)
      }
    },

    async remove() {
      try {
        await this.$services.rule.deleteRules(parseInt(this.projectId), this.selected)
        await this.listRules()
        this.dialogDelete = false
        this.selected = []
      } catch (e) {
        console.error('Failed to delete rules', e)
      }
    }
  }
})
</script>

<style scoped>
::v-deep .v-dialog {
  width: 800px;
}
</style>% 
