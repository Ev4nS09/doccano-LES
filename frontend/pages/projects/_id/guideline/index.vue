<template>
  <v-card>
    <ticket-header
      :is-project-admin="isProjectAdmin"
      :can-delete="canDelete"
      @create-rule="createRule"
      @open-ticket-dialog="showTicketDialog = true"
      @open-delete-dialog="openDeleteDialog"
    />

  <rule-create-dialog
    :show="showRuleDialog"
    :project-id="projectId"
    @close="showRuleDialog = false"
    @create="handleRuleCreated"
  />
        
    <rule-delete-dialog
      :show="dialogDelete"
      @close="dialogDelete = false"
      @confirm="deleteItems"
    />

    <v-tabs v-model="tab">
      <v-tab>Rules</v-tab>
      <v-tab>Tickets</v-tab>
    </v-tabs>

    <v-tabs-items v-model="tab">
      <v-tab-item>
        <rule-list
          v-model="selected"
          :items="rules"
          :is-loading="isLoading"
          @edit="editRule"
          @details="showDetails"
          @upvote="upvoteRule"
          @downvote="downvoteRule"
          @votes="showVotes"
        />
      </v-tab-item>
      
      <v-tab-item>
        <div class="mb-4">
          <v-tabs v-model="ticketTab">
            <v-tab>Open Tickets</v-tab>
            <v-tab>Closed Tickets</v-tab>
          </v-tabs>
        </div>

        <v-tabs-items v-model="ticketTab">
          <v-tab-item>
            <ticket-list
              :tickets="tickets"
              :rules="rules"
              :loading="isLoadingTickets"
              :is-project-admin="isProjectAdmin"
              :current-user-id="currentUserId"
              status-filter="open"
              @open-chat="openTicketChat"
             @close-ticket="closeTicket"
              @update:selectedTickets="selectedTickets = $event"
            />
          </v-tab-item>
          <v-tab-item>
            <ticket-list
              :tickets="tickets"
              :rules="rules"
              :loading="isLoadingTickets"
              :is-project-admin="isProjectAdmin"
              :current-user-id="currentUserId"
              status-filter="closed"
              @open-chat="openTicketChat"
              @update:selectedTickets="selectedTickets = $event"
            />
          </v-tab-item>
        </v-tabs-items>
      </v-tab-item>
    </v-tabs-items>

    <rule-details 
      v-if="selectedRule" 
      :rule="selectedRule" 
      :project-id="projectId"
      :show-details-dialog="showDetailsDialog"
      @close="showDetailsDialog = false"
    />

    <ticket-create-dialog
      :show="showTicketDialog"
      :rules="rules"
      :loading="isCreatingTicket"
      @close="showTicketDialog = false"
      @create="createTicket"
    />

    <ticket-chat
      v-if="selectedTicket"
      :ticket="selectedTicket"
      :comments="ticketComments"
      :show="showTicketChatDialog"
      :project-id="projectId"
      @close="showTicketChatDialog = false"
      @add-comment="addTicketComment"
      @refresh-comments="refreshTicketComments"
    />


    <v-dialog v-model="showVoteDialog" max-width="800">
      <rule-vote 
        v-if="selectedRule" 
        :rule="selectedRule"
        :project-id="projectId"
        @close="showVoteDialog = false"
        @update-rule="handleRuleUpdate"
        @error="showError"
      />
    </v-dialog>

  </v-card>

</template>

<script lang="ts">
import Vue from 'vue'
import TicketHeader from '~/components/rule/TicketHeader.vue'
import RuleDeleteDialog from '~/components/rule/RuleDeleteDialog.vue'
import TicketList from '~/components/rule/TicketList.vue'
import TicketCreateDialog from '~/components/rule/TicketCreateDialog.vue'
import RuleList from '~/components/rule/RuleList.vue'
import RuleVote from '~/components/rule/RuleVote.vue'
import RuleCreateDialog from '~/components/rule/RuleCreateDialog.vue'
import RuleDetails from '~/components/rule/RuleDetails.vue'
import TicketChat from '~/components/rule/TicketChat.vue'
import { RuleDTO } from '~/services/application/rule/ruleData'
import { TicketDTO, CommentDTO } from '~/services/application/tickets/ticketData'

export default Vue.extend({
  components: {
    TicketHeader,
    RuleDeleteDialog,
    TicketList,
    TicketCreateDialog,
    RuleList,
    RuleVote,
    RuleCreateDialog,
    RuleDetails,
    TicketChat
  },

  layout: 'project',
  middleware: ['check-auth', 'auth', 'setCurrentProject'],

  validate({ params }) {
    return /^\d+$/.test(params.id)
  },

  data() {
    return {
      tab: 0,
      ticketTab: 0,
      dialogDelete: false,
      rules: [] as RuleDTO[],
      selected: [] as RuleDTO[],
      selectedTickets: [] as TicketDTO[],
      isLoading: false,
      selectedRule: null as RuleDTO | null,
      showDetailsDialog: false,
      showTicketDialog: false,
      showTicketChatDialog: false,
      showVoteDialog: false,
      showRuleDialog: false,
      tickets: [] as TicketDTO[],
      ticketComments: [] as CommentDTO[],
      selectedTicket: null as TicketDTO | null,
      isLoadingTickets: false,
      isCreatingTicket: false,
      isProjectAdmin: false,
      currentUserId: null as number | null
    }
  },

  computed: {
    projectId(): number {
      return parseInt(this.$route.params.id)
    },
    canDelete(): boolean {
      if (this.tab === 0) return this.selected.length > 0
      if (this.tab === 1) return this.selectedTickets.length > 0
      return false
    }
  },

  async created() {
    await this.fetchUserRole()
    await this.listRules()
    await this.updateStatus()
    await this.listTickets()

          // Set up interval (e.g., every 60 seconds)
  const intervalId = setInterval(async () => {
    await this.updateStatus()
  }, 5000) // 60,000ms = 60s

  // Clear interval when component is destroyed to avoid memory leaks
  this.$once('hook:beforeDestroy', () => {
    clearInterval(intervalId)
  })
  },

  methods: {
    handleRuleCreated(rule: RuleDTO) {
      this.rules.unshift(rule)
    },

    // Update your createRule method to:
    createRule() {
      this.showRuleDialog = true
    },
    showVotes(rule: RuleDTO) {
        this.selectedRule = rule
        this.showVoteDialog = true
        },

    handleRuleUpdate(updatedRule: RuleDTO) {
    this.rules = this.rules.map(r => 
      r.id === updatedRule.id ? updatedRule : r
    )
  },

    async refreshTicketComments() {
      if (!this.selectedTicket) return;
      
      try {
        const comments = await this.$services.ticket.getComments(
          this.projectId, 
          this.selectedTicket.id
        );
        this.ticketComments = comments.map(comment => ({
          ...comment,
          author_username: comment.author_username || 'Unknown',
          author_role: comment.author_role || 'annotator'
        }));
      } catch (e) {
        console.error('Failed to refresh comments', e);
      }
    },
    async fetchUserRole() {
      try {
        const user = await this.$repositories.member.fetchMyRole(this.projectId)
        this.isProjectAdmin = user.isProjectAdmin
        this.currentUserId = user.id
      } catch (e) {
        console.error('Failed to fetch user role', e)
      }
    },

    async listRules() {
      this.isLoading = true
      try {
        this.rules = await this.$services.rule.list(this.projectId)
      } finally {
        this.isLoading = false
      }
    },

    async updateStatus() {

    for(let i = 0; i < this.rules.length; i++)
    {
      if (this.rules[i].end_at) {
        const end = new Date(this.rules[i].end_at)
        const now = new Date()
        const timeRemaining = end.getTime() - now.getTime()
        
        if (timeRemaining < 0 && this.rules[i].status.toLowerCase() === 'on going') {
            await this.$repositories.rule.status(this.projectId, this.rules[i].id, 
                this.rules[i].upvotes > this.rules[i].downvotes ? 1 : -1
                    )
            this.listRules()
            }
        }
    }

    },

    async listTickets() {
      this.isLoadingTickets = true
      try {
        this.tickets = await this.$services.ticket.list(this.projectId)
      } catch (e) {
        console.error('Failed to fetch tickets', e)
      } finally {
        this.isLoadingTickets = false
      }
    },

    editRule(rule: RuleDTO) {
      this.$router.push(`/projects/${this.projectId}/rules/${rule.id}/edit`)
    },

    showDetails(rule: RuleDTO) {
      this.selectedRule = rule
      this.showDetailsDialog = true
    },

    async upvoteRule(rule: RuleDTO) {
      try {
        await this.$services.rule.vote(this.projectId, rule.id, 1)
        await this.listRules()
      } catch (e) {
        console.error('Failed to upvote rule', e)
      }
    },

    async downvoteRule(rule: RuleDTO) {
      try {
        await this.$services.rule.vote(this.projectId, rule.id, -1)
        await this.listRules()
      } catch (e) {
        console.error('Failed to downvote rule', e)
      }
    },

    openDeleteDialog() {
      if (this.tab === 0 && this.selected.length === 0) {
        this.$toast.error('Please select at least one rule to delete')
        return
      }
      if (this.tab === 1 && this.selectedTickets.length === 0) {
        this.$toast.error('Please select at least one ticket to delete')
        return
      }
      this.dialogDelete = true
    },

    async deleteItems() {
      try {
        if (this.tab === 0) {
          await this.$services.rule.deleteRules(this.projectId, this.selected)
          await this.listRules()
          this.selected = []
          this.selectedTickets = []
        } else if (this.tab === 1) {
          if (!this.isProjectAdmin) {
            this.$toast.error('Only admin can delete tickets')
            return
          }
          await this.$services.ticket.deleteTickets(this.projectId, this.selectedTickets)
          await this.listTickets()
          this.selected = []
          this.selectedTickets = []
        }
        this.dialogDelete = false
      } catch (e) {
        console.error('Failed to delete items', e)
      }
    },

    async createTicket({ title, description, selectedRules }) {
      if (!title.trim() || !description.trim()) {
        this.$toast.error('Title and description are required')
        return
      }

      this.isCreatingTicket = true
      try {
        const ticket = await this.$services.ticket.create(this.projectId, {
          title,
          description,
          created_by: this.currentUserId,
          author_username: this.$store.getters['auth/getUsername']
        })

        // Add current user info to the ticket before pushing to array
        const newTicket = {
          ...ticket,
          created_by: this.currentUserId,
          author_username: this.$store.getters['auth/getUsername']
        }

        if (selectedRules.length > 0) {
          const ruleIds = selectedRules.map(rule => rule.id)
          await this.$services.ticket.updateRules(this.projectId, ticket.id, ruleIds)
          newTicket.rules = ruleIds
        }

        this.tickets.unshift(newTicket)
        this.showTicketDialog = false
      } catch (e) {
        console.error('Failed to create ticket', e)
        this.$toast.error('Failed to create ticket')
      } finally {
        this.isCreatingTicket = false
      }
    },

    async openTicketChat(ticket: TicketDTO) {
      this.selectedTicket = ticket
      this.isLoadingTickets = true
      try {
        const comments = await this.$services.ticket.getComments(this.projectId, ticket.id)
        this.ticketComments = comments.map(comment => ({
          ...comment,
          author_username: comment.author_username || 'Unknown',
          author_role: comment.author_role || 'annotator'
        }))
        this.showTicketChatDialog = true
      } catch (e) {
        console.error('Failed to fetch comments', e)
        this.$toast.error('Failed to load ticket comments')
        this.ticketComments = []
      } finally {
        this.isLoadingTickets = false
      }
    },

    async addTicketComment(comment: { content: string }) {
      if (!this.selectedTicket || !comment.content.trim()) return

      try {
        const newComment = await this.$services.ticket.addComment(
          this.projectId, 
          this.selectedTicket.id, 
          comment.content
        )
        
        // Ensure complete comment data
        const completeComment = {
          ...newComment,
          author: this.currentUserId,
          author_username: this.$store.getters['auth/getUsername'],
          author_role: this.isProjectAdmin ? 'project_admin' : 'annotator',
          created_at: newComment.created_at || new Date().toISOString()
        }

        this.ticketComments = [...this.ticketComments, completeComment]
      } catch (e) {
        console.error('Failed to add comment', e)
        this.$toast.error('Failed to add comment')
      }
    },

    async closeTicket(ticket: TicketDTO) {
      if (!this.isProjectAdmin && ticket.created_by !== this.currentUserId) {
        this.$toast.error('Only the ticket creator or admin can close tickets')
        return
      }

      try {
        // Use actual comments if available in the component
        const comments = await this.$services.ticket.getComments(this.projectId, ticket.id)
        const hasComments = comments.length > 0

        if (!hasComments) {
          await this.$services.ticket.delete(this.projectId, ticket.id)
        } else {
          await this.$services.ticket.update(this.projectId, ticket.id, {
            status: 'closed'
          })
        }

        await this.listTickets()
      } catch (e) {
        console.error('Failed to close ticket', e)
        this.$toast.error('Failed to close ticket')
      }
    },
  }
})
</script>

<style scoped>
::v-deep .v-dialog {
  width: 800px;
}
</style>%  
