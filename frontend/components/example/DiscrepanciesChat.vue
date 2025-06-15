<template>
  <v-card class="discrepancies-chat" flat>
    <v-card-title class="chat-header primary white--text">
      <v-icon left>mdi-message-text</v-icon>
      Discussion: Document #{{ example.id }}
      <v-spacer />
      <v-btn icon dark @click="$emit('close')">
        <v-icon>mdi-close</v-icon>
      </v-btn>
    </v-card-title>
    
    <v-card-text class="chat-container">
      <div class="chat-layout">
        <div class="messages-container" ref="messagesContainer">
          <template v-if="comments.length > 0">
            <div 
              v-for="comment in comments" 
              :key="comment.id" 
              class="message"
              :class="{ 'current-user': isCurrentUser(comment) }"
            >
              <div class="message-content">
                <div class="message-header">
                  <span class="username font-weight-bold">{{ comment.username }}</span>
                  <span class="timestamp">{{ formatDate(comment.createdAt) }}</span>
                </div>
                <div class="message-text">
                  {{ comment.text }}
                </div>
              </div>
            </div>
          </template>
          <div v-else class="empty-state">
            <v-icon large class="empty-icon">mdi-message-outline</v-icon>
            <p>No messages yet. Start the discussion!</p>
          </div>
        </div>
        
        <div class="labels-sidebar">
          <div class="labels-header">
            <v-icon left color="primary">mdi-tag-multiple</v-icon>
            <span class="font-weight-medium">Label Usage</span>
            <v-tooltip right>
              <template v-slot:activator="{ on }">
                <v-icon small color="grey" v-on="on">mdi-information</v-icon>
              </template>
              <span>% of assigned users who applied this label</span>
            </v-tooltip>
          </div>

          <v-slide-y-transition group tag="div" class="labels-list">
            <div 
              v-for="stat in labelStats" 
              :key="stat.labelId" 
              class="label-item"
            >
              <div class="label-meta">
                <v-avatar
                  :color="stat.backgroundColor"
                  size="12"
                  class="mr-2"
                ></v-avatar>
                <span class="label-name">{{ stat.labelName }}</span>
                <span class="percentage">{{ Math.round(stat.percentage) }}%</span>
              </div>
              <v-progress-linear
                :value="stat.percentage"
                height="8"
                :color="stat.backgroundColor"
                :background-color="lightenColor(stat.backgroundColor)"
                rounded
              />
            </div>

            <div v-if="labelStats.length === 0" class="empty-state">
              <v-icon color="grey lighten-1">mdi-tag-off</v-icon>
              <span>No labels applied</span>
            </div>
          </v-slide-y-transition>
        </div>
      </div>

      <div class="message-input">
        <v-textarea
          v-model="newComment"
          outlined
          auto-grow
          rows="1"
          hide-details
          placeholder="Write your message..."
          class="input-field"
          @keydown.enter.exact.prevent="addComment"
        ></v-textarea>
        <v-btn
          icon
          color="primary"
          class="send-icon"
          @click="addComment"
          :disabled="!newComment.trim()"
          :loading="isPosting"
        >
          <v-icon>{{ mdiArrowRight }}</v-icon>
        </v-btn>
      </div>
    </v-card-text>
  </v-card>
</template>

<script lang="ts">
import { mdiArrowRight } from '@mdi/js'
import Vue from 'vue'
import { mapGetters } from 'vuex'
import { CommentItem } from '~/domain/models/comment/comment'

interface LabelStat {
  labelId: number;
  labelName: string;
  percentage: number;
  backgroundColor: string;
  textColor: string;
}

export default Vue.extend({
  props: {
    example: {
      type: Object as () => { id: number },
      required: true
    },
    projectId: {
      type: [Number, String],
      required: true
    }
  },

  data() {
    return {
      newComment: '',
      isPosting: false,
      comments: [] as CommentItem[],
      isLoadingComments: false,
      isLoadingLabels: false,
      labelStats: [] as LabelStat[],
      exampleDetails: null as ExampleItem | null,
      mdiArrowRight
    }
  },

  computed: {
    ...mapGetters('auth', ['getUsername', 'getUserId'])
  },

  async created() {
    await Promise.all([
      this.loadComments(),
      this.loadLabelStats()
    ])
    this.scrollToBottom()
  },

  methods: {
    lightenColor(hex: string): string {
      // Simple color lightening for progress bar background
      return hex + '30'; // Add 30% opacity
    },

    async loadLabelStats() {
      this.isLoadingLabels = true;
      this.labelStats = [];
      
      try {
        this.exampleDetails = await this.$repositories.example.findById(
          this.projectId.toString(),
          this.example.id
        );
        
        const categories = await this.$repositories.category.list(
          this.projectId.toString(),
          this.example.id
        );
        
        const allLabels = await this.$repositories.categoryType.list(
          this.projectId.toString()
        );
        
        const totalAssignees = this.exampleDetails.assignments.length;
        const labelCounts: Record<number, number> = {};
        
        categories.forEach(category => {
          labelCounts[category.label] = (labelCounts[category.label] || 0) + 1;
        });
        
        this.labelStats = Object.entries(labelCounts).map(([labelId, userCount]) => {
          const labelIdNum = parseInt(labelId);
          const label = allLabels.find(l => l.id === labelIdNum);
          return {
            labelId: labelIdNum,
            labelName: label?.text || 'Unknown',
            percentage: totalAssignees > 0 ? (userCount / totalAssignees) * 100 : 0,
            backgroundColor: label?.backgroundColor || '#1976D2',
            textColor: label?.textColor || '#FFFFFF',
          };
        });
      } catch (error) {
        console.error('Failed to load labels:', error);
      } finally {
        this.isLoadingLabels = false;
      }
    },

    async loadComments() {
      this.isLoadingComments = true;
      try {
        this.comments = await this.$repositories.comment.list(
          this.projectId.toString(), 
          this.example.id
        );
      } catch (error) {
        console.error('Failed to load comments:', error);
        this.comments = [];
      } finally {
        this.isLoadingComments = false;
      }
    },

    isCurrentUser(comment: CommentItem): boolean {
      return comment.user === this.getUserId;
    },

    formatDate(dateString: string): string {
      return new Date(dateString).toLocaleString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      });
    },

    scrollToBottom() {
      this.$nextTick(() => {
        const container = this.$refs.messagesContainer as HTMLElement;
        if (container) {
          container.scrollTop = container.scrollHeight;
        }
      });
    },

    async addComment() {
      if (!this.newComment.trim()) return;
      
      this.isPosting = true;
      try {
        const newComment = await this.$repositories.comment.create(
          this.projectId.toString(),
          this.example.id,
          this.newComment
        );
        this.newComment = '';
        this.comments.push(newComment);
        this.$emit('refresh');
        this.scrollToBottom();
      } catch (error) {
        console.error('Failed to post comment:', error);
      } finally {
        this.isPosting = false;
      }
    }
  }
});
</script>

<style scoped>
.discrepancies-chat {
  --primary-color: #1976D2;
  --primary-light: #E3F2FD;
  --background-color: #FFFFFF;
  --message-bg: #F5F5F5;
  --current-user-bg: #E3F2FD;
  --text-color: #333333;
  --text-secondary: #666666;
  --border-color: #E0E0E0;
  --shadow-color: rgba(0,0,0,0.1);
  --scrollbar-thumb: var(--primary-color);
  --scrollbar-track: var(--background-color);
}

.theme--dark .discrepancies-chat {
  --primary-color: #31D1F1;
  --primary-light: rgba(49, 209, 241, 0.1);
  --background-color: #121212;
  --message-bg: #1E1E1E;
  --current-user-bg: rgba(49, 209, 241, 0.2);
  --text-color: #FFFFFF;
  --text-secondary: #B0B0B0;
  --border-color: #333333;
  --shadow-color: rgba(255,255,255,0.05);
  --scrollbar-thumb: #31D1F1;
  --scrollbar-track: var(--background-color);
}

.chat-header {
  padding: 16px 24px;
  border-top-left-radius: 4px;
  border-top-right-radius: 4px;
}

.chat-container {
  max-height: 900px;
  min-height: 200px;
  display: flex;
  flex-direction: column;
  padding: 0;
  background-color: var(--background-color);
}

.chat-layout {
  display: flex;
  flex: 1;
  overflow: hidden;
}

.messages-container {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
  scrollbar-width: thin;
  scrollbar-color: var(--scrollbar-thumb) var(--scrollbar-track);
}

.labels-sidebar {
  width: 280px;
  border-left: 1px solid var(--border-color);
  background: var(--background-color);
  display: flex;
  flex-direction: column;
}

.labels-header {
  padding: 12px 16px;
  border-bottom: 1px solid var(--border-color);
  display: flex;
  align-items: center;
}

.labels-list {
  padding: 8px;
  overflow-y: auto;
  flex: 1;
}

.label-item {
  margin-bottom: 12px;
}

.label-meta {
  display: flex;
  align-items: center;
  margin-bottom: 4px;
  font-size: 0.85rem;
}

.label-name {
  flex: 1;
  margin-left: 8px;
  color: var(--text-color);
}

.percentage {
  color: var(--text-secondary);
  margin-left: 8px;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 24px;
  color: var(--text-secondary);
}

.message {
  margin-bottom: 16px;
  display: flex;
}

.message:not(.current-user) {
  justify-content: flex-start;
}

.message.current-user {
  justify-content: flex-end;
}

.message-content {
  max-width: 70%;
  width: fit-content;
  background-color: var(--message-bg);
  border-radius: 12px;
  padding: 12px 16px;
  box-shadow: 0 1px 2px var(--shadow-color);
}

.message.current-user .message-content {
  background-color: var(--current-user-bg);
}

.message-header {
  display: flex;
  align-items: baseline;
  margin-bottom: 4px;
}

.username {
  color: var(--primary-color);
  font-size: 0.875rem;
  margin-right: 8px;
}

.timestamp {
  color: var(--text-secondary);
  font-size: 0.75rem;
}

.message-text {
  color: var(--text-color);
  font-size: 0.9375rem;
  line-height: 1.4;
}

.message-input {
  display: flex;
  align-items: flex-end;
  gap: 8px;
  padding: 8px 16px;
  border-top: 1px solid var(--border-color);
  background-color: var(--background-color);
}

.input-field {
  flex-grow: 1;
  margin: 0;
}

.send-icon {
  flex-shrink: 0;
  margin-bottom: 8px;
}

@media (max-width: 800px) {
  .chat-layout {
    flex-direction: column;
  }
  
  .labels-sidebar {
    width: 100%;
    border-left: none;
    border-top: 1px solid var(--border-color);
    max-height: 150px;
  }
}

@media (max-width: 600px) {
  .chat-container {
    height: 400px;
  }
  
  .message-content {
    max-width: 90%;
  }
}
</style>
