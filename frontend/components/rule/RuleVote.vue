<template>
  <v-card>
    <v-card-title class="d-flex justify-space-between align-center">
      <span>Voting: {{ rule.title }}</span>
      <v-btn icon @click="$emit('close')">
        <v-icon>mdi-close</v-icon>
      </v-btn>
    </v-card-title>

    <v-card-text>
      <v-simple-table>
        <template #default>
          <thead>
            <tr>
              <th class="text-left">Metric</th>
              <th class="text-left">Value</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><strong>Status</strong></td>
              <td>
                <v-chip :color="getVotingStatusColor()" dark>
                  {{ getVotingStatus() }}
                </v-chip>
              </td>
            </tr>
            <tr>
              <td><strong>Result</strong></td>
              <td>
                <v-chip :color="getResultColor(displayStatus)" dark>
                  {{ formatStatus(displayStatus) }}
                </v-chip>
              </td>
            </tr>
            <tr>
              <td><strong>Current Score</strong></td>
              <td>
                <v-chip :color="getScoreColor(displayScore)" dark>
                  {{ displayScore }}
                </v-chip>
              </td>
            </tr>
            <tr>
              <td><strong>Your Vote</strong></td>
              <td>
                <v-btn 
                  icon 
                  :color="displayUserVote === 1 ? 'green' : ''"
                  :loading="loading.upvote"
                  @click="handleVote(1)"
                  :disabled="!canVote || loading.downvote"
                >
                  <v-icon>{{ mdiThumbUp }}</v-icon>
                </v-btn>
                <v-btn 
                  icon 
                  :color="displayUserVote === -1 ? 'red' : ''"
                  :loading="loading.downvote"
                  @click="handleVote(-1)"
                  class="ml-2"
                  :disabled="!canVote || loading.upvote"
                >
                  <v-icon>{{ mdiThumbDown }}</v-icon>
                </v-btn>
                <v-tooltip v-if="!canVote" top>
                  <template v-slot:activator="{ on }">
                    <v-icon small color="grey" class="ml-2" v-on="on">
                      mdi-information
                    </v-icon>
                  </template>
                  <span>Voting is only allowed during the ongoing period</span>
                </v-tooltip>
              </td>
            </tr>
            <tr>
              <td><strong>Voting Start</strong></td>
              <td>
                {{ rule.start_at ? formatDateTime(rule.start_at) : 'Not scheduled' }}
              </td>
            </tr>
            <tr>
              <td><strong>Voting End</strong></td>
              <td>
                {{ rule.end_at ? formatDateTime(rule.end_at) : 'Not scheduled' }}
              </td>
            </tr>
            <tr>
              <td><strong>Time Remaining</strong></td>
              <td>
                {{ getTimeRemaining() }}
              </td>
            </tr>
          </tbody>
        </template>
      </v-simple-table>
    </v-card-text>

    <v-card-actions>
      <v-spacer></v-spacer>
      <v-btn color="primary" @click="$emit('close')">
        Close
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script lang="ts">
import Vue from 'vue'
import { mdiThumbUp, mdiThumbDown } from '@mdi/js'
import { RuleDTO } from '~/services/application/rule/ruleData'

export default Vue.extend({
  props: {
    rule: {
      type: Object as () => RuleDTO,
      required: true
    },
    projectId: {
      type: [Number, String],
      required: true
    }
  },

  data() {
    return {
      mdiThumbUp,
      mdiThumbDown,
      loading: {
        upvote: false,
        downvote: false,
        status: false
      },
      voteState: {
        user_vote: 0,
        score: 0,
        status: ''
      },
      statusCheckInterval: null as NodeJS.Timeout | null
    }
  },

  created() {
    this.voteState = {
      user_vote: this.rule.user_vote,
      score: this.rule.score,
      status: this.rule.status
    }
    this.setupStatusCheck()
  },

  beforeDestroy() {
    this.cleanupStatusCheck()
  },

  computed: {
    displayScore(): number {
      return this.voteState.score
    },
    displayUserVote(): number {
      return this.voteState.user_vote
    },
    displayStatus(): string {
      return this.voteState.status
    },
    canVote(): boolean {
      if (!this.rule.start_at || !this.rule.end_at) return false
      const now = new Date()
      const start = new Date(this.rule.start_at)
      const end = new Date(this.rule.end_at)
      return now >= start && now <= end && 
             this.voteState.status.toLowerCase() === 'on going'
    }
  },

  methods: {
    setupStatusCheck() {
      this.cleanupStatusCheck()
      if (this.rule.end_at) {
        const end = new Date(this.rule.end_at)
        const now = new Date()
        const timeRemaining = end.getTime() - now.getTime()
        
        if (timeRemaining > 0) {
          this.statusCheckInterval = setTimeout(() => {
            this.updateRuleStatus()
          }, timeRemaining)
        } else if (this.getVotingStatus() === 'Finished') {
          this.updateRuleStatus()
        }
      }
    },

    cleanupStatusCheck() {
      if (this.statusCheckInterval) {
        clearTimeout(this.statusCheckInterval)
        this.statusCheckInterval = null
      }
    },

    async updateRuleStatus() {
      if (this.loading.status || this.getVotingStatus() !== 'Finished') return
      
      try {
        this.loading.status = true
        const newStatus = this.voteState.score > 0 ? 'accepted' : 'rejected'
        
        if (this.voteState.status.toLowerCase() !== newStatus) {
          await this.$services.rule.status(
            parseInt(this.projectId.toString()),
            this.rule.id,
            newStatus === 'accepted' ? 1 : -1
          )
          
          this.voteState.status = newStatus
          this.$emit('update-rule', {
            ...this.rule,
            status: newStatus,
            score: this.voteState.score,
            user_vote: this.voteState.user_vote
          })
        }
      } catch (error) {
        console.error('Status update failed:', error)
        this.$emit('error', 'Failed to update rule status')
      } finally {
        this.loading.status = false
      }
    },

    async handleVote(vote: number) {
      if (!this.canVote) return

      const voteType = vote === 1 ? 'upvote' : 'downvote'
      this.loading[voteType] = true

      const originalVote = this.voteState.user_vote
      const originalScore = this.voteState.score

      try {
        const newVote = originalVote === vote ? 0 : vote
        this.voteState.user_vote = newVote

        if (newVote === 0) {
          this.voteState.score -= vote
        } else {
          if (originalVote === 1) this.voteState.score -= 1
          else if (originalVote === -1) this.voteState.score += 1
          if (newVote === 1) this.voteState.score += 1
          else if (newVote === -1) this.voteState.score -= 1
        }

        await this.$services.rule.vote(
          parseInt(this.projectId.toString()),
          this.rule.id,
          newVote
        )

        this.$emit('update-rule', {
          ...this.rule,
          user_vote: newVote,
          score: this.voteState.score,
          status: this.voteState.status
        })

      } catch (error) {
        this.voteState.user_vote = originalVote
        this.voteState.score = originalScore
        console.error('Vote failed:', error)
        this.$emit('error', 'Failed to submit vote')
      } finally {
        this.loading.upvote = false
        this.loading.downvote = false
      }
    },

    formatDateTime(dateString: string): string {
      if (!dateString) return ''
      const date = new Date(dateString)
      return date.toLocaleString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    },

    getScoreColor(score: number): string {
      if (score > 0) return 'green'
      if (score < 0) return 'red'
      return 'grey'
    },

    getVotingStatus(): string {
      if (!this.rule.start_at || !this.rule.end_at) return 'Not scheduled'
      const now = new Date()
      const start = new Date(this.rule.start_at)
      const end = new Date(this.rule.end_at)
      if (now < start) return 'About to Start'
      if (now > end) return 'Finished'
      return 'Ongoing'    
    },

    getVotingStatusColor(): string {
      const status = this.getVotingStatus()
      switch(status) {
        case 'About to Start': return 'orange'
        case 'Ongoing': return 'green'
        case 'Finished': return 'red'
        default: return 'grey'
      }
    },

    getResultColor(status: string): string {
      switch((status || '').toLowerCase()) {
        case 'accepted': return 'green'
        case 'rejected': return 'red'
        case 'on going': return 'yellow'
        default: return 'yellow'
      }
    },

    formatStatus(status: string): string {
      if (!status) return 'Pending'
      return status.charAt(0).toUpperCase() + status.slice(1)
    },

    getTimeRemaining(): string {
      if (!this.rule.end_at) return 'No end time set'
      const now = new Date()
      const end = new Date(this.rule.end_at)
      if (now > end) return 'Voting period has ended'
      const diff = end.getTime() - now.getTime()
      const days = Math.floor(diff / (1000 * 60 * 60 * 24))
      const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60))
      const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60))
      return `${days}d ${hours}h ${minutes}m remaining`
    }
  }
})
</script>

<style scoped>
.v-card {
  min-width: 500px;
}
.v-chip {
  font-weight: bold;
}
.v-btn {
  transition: all 0.3s ease;
}
.v-chip--yellow {
  background-color: #FFD600 !important;
  color: #000000 !important;
}
</style>
