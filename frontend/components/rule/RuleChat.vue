<template>
	<v-card class="rule-chat" flat>
	  <v-card-title class="chat-header primary white--text">
		<v-icon left>mdi-message-text</v-icon>
		Discussion: {{ rule.title }}
		<v-spacer />
		<v-btn icon dark @click="$emit('close')">
		  <v-icon>mdi-close</v-icon>
		</v-btn>
	  </v-card-title>
	  
	  <v-card-text class="chat-container">
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
				  <span class="username font-weight-bold">{{ getAuthorName(comment) }}</span>
				  <span class="timestamp">{{ formatDate(comment.created_at) }}</span>
				</div>
				<div class="message-text">
				  {{ comment.content }}
				</div>
			  </div>
			</div>
		  </template>
		  <div v-else class="empty-state">
			<v-icon large class="empty-icon">mdi-message-outline</v-icon>
			<p>No messages yet. Start the discussion!</p>
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
				style="align-self: flex-end"
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
		newComment: '',
		isPosting: false,
		comments: [] as any[],
		isLoadingComments: false,
		members: [] as any[],
		isLoadingMembers: false,
		mdiArrowRight
	  }
	},
  
	computed: {
	  ...mapGetters('auth', ['getUsername'])
	},
  
	async created() {
	  await this.fetchMembers()
	  this.loadComments()
	  this.scrollToBottom()
	},
  
	watch: {
	  'rule.comments': {
		immediate: true,
		handler() {
		  this.loadComments()
		}
	  }
	},
  
	methods: {
	  async fetchMembers() {
		try {
		  this.isLoadingMembers = true
		  this.members = await this.$repositories.member.list(this.projectId.toString())
		} catch (e) {
		  console.error('Failed to fetch members', e)
		} finally {
		  this.isLoadingMembers = false
		}
	  },
  
	  isCurrentUser(comment: any): boolean {
		return this.getAuthorName(comment) === this.getUsername
	},
  
	  getAuthorName(comment: any): string {
		if (comment.author_username) {
		  return comment.author_username
		}
		
		if (comment.author && this.members.length > 0) {
		  const member = this.members.find(m => m.user === comment.author)
		  if (member) {
			return member.username || `User ${comment.author}`
		  }
		}
		
		if (comment.author) {
		  return `User ${comment.author}`
		}
		
		return 'Unknown user'
	  },
  
 async loadComments() {
  this.isLoadingComments = true;
  try {
    this.comments = []; // reset before fetching

    const freshData = await this.$services.rule.getWithComments(
      Number(this.projectId),
      this.rule.id
    );

    // Assign just the comments, not the whole DTO
    this.comments = [...freshData.comments];

    // This is safe and helpful for debugging
    console.log("Comments loaded:", this.comments.length);
  } catch (error) {
    console.error('Failed to load comments:', error);
    this.comments = this.rule.comments ? [...this.rule.comments] : [];
  } finally {
    this.isLoadingComments = false;
  }
}, 
	  formatDate(dateString: string): string {
		return new Date(dateString).toLocaleString('en-US', {
		  year: 'numeric',
		  month: 'short',
		  day: 'numeric',
		  hour: '2-digit',
		  minute: '2-digit'
		})
	  },
	  
	  scrollToBottom() {
		this.$nextTick(() => {
		  const container = this.$refs.messagesContainer as HTMLElement
		  if (container) {
			container.scrollTop = container.scrollHeight
		  }
		})
	  },
	  
	  async addComment() {
		if (this.newComment.trim()) {
		  this.isPosting = true
		  try {
			await this.$services.rule.comment(
			  Number(this.projectId),
			  this.rule.id,
			  this.newComment
			)
			this.newComment = ''
			await this.loadComments()
			this.$emit('refresh')
		  } catch (error) {
			console.error('Failed to post comment:', error)
		  } finally {
			this.isPosting = false
		  }
		}
	  }
	}
  })
  </script>
  
  <style scoped>
  /* Base variables - light theme */
  .rule-chat {
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
  
  /* Dark theme override */
  .theme--dark .rule-chat {
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
  
  .messages-container {
	flex: 1;
	overflow-y: auto;
	padding: 16px;
	scrollbar-width: thin;
	scrollbar-color: var(--scrollbar-thumb) var(--scrollbar-track);
  }
  
  .messages-container::-webkit-scrollbar {
	background: var(--scrollbar-track);
	width: 6px;
  }
  
  .messages-container::-webkit-scrollbar-track {
	background: var(--scrollbar-track);
  }
  
  .messages-container::-webkit-scrollbar-thumb {
	background-color: var(--scrollbar-thumb);
	border-radius: 3px;
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
  
  .empty-state {
	display: flex;
	flex-direction: column;
	align-items: center;
	justify-content: center;
	height: 100%;
	color: var(--text-secondary);
  }
  
  .empty-icon {
	color: var(--text-secondary);
	margin-bottom: 16px;
	opacity: 0.5;
  }
  
  /* Responsive adjustments */
  @media (max-width: 600px) {
	.chat-container {
	  height: 400px;
	}
	
	.message-content {
	  max-width: 90%;
	}
  }

  .chat-container {
  max-height: 80vh;
  min-height: 300px;
  display: flex;
  flex-direction: column;
  background-color: var(--background-color);
}

.message-input {
  display: flex;
  align-items: flex-end;  /* Changed from center to flex-end */
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
  margin-bottom: 8px;  /* Added to maintain consistent bottom spacing */
}

</style>
