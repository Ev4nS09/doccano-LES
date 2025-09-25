<template>
	<v-dialog :value="show" max-width="800" persistent @input="$emit('update:show', $event)">
	  <v-card class="ticket-chat" flat>
		<v-card-title class="chat-header primary white--text">
		  <v-icon left class="white--text">{{ mdiTicket }}</v-icon>
		  Ticket: {{ ticket.title }}
		  <v-spacer />
		  <v-btn icon dark @click="$emit('close')">
			<v-icon>{{ mdiClose }}</v-icon>
		  </v-btn>
		</v-card-title>
  
		<v-card-text class="chat-container">
			<div class="messages-container" ref="messagesContainer">
			<template v-if="validComments.length > 0">
				<div
				v-for="comment in validComments"
				:key="comment.id"
				class="message"
				:class="{ 'current-user': isCurrentUser(comment) }"
				>
				<div class="message-content">
				  <div class="message-header">
					<span class="username font-weight-bold">
					  <v-icon
						left
						v-if="getRoleIcon(comment)"
						class="role-icon"
						small
					  >
						{{ getRoleIcon(comment) }}
					  </v-icon>
					  {{ comment.author_username }}
					</span>
					<span class="timestamp">{{ formatDate(comment.created_at) }}</span>
				  </div>
				  <div class="message-text">
					{{ comment.content }}
				  </div>
				</div>
			  </div>
			</template>
			<div v-else class="empty-state">
			  <v-icon large class="empty-icon">{{ mdiMessageOutline }}</v-icon>
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
				:placeholder="ticket.status === 'open' ? 'Write your message...' 
				: 'This ticket is closed. You can\'t add new comments.'"
				:disabled="ticket.status !== 'open'"
				class="input-field"
				@keydown.enter.exact.prevent="addComment"
			></v-textarea>
			<v-btn
				icon
				color="primary"
				class="send-icon"
				@click="addComment"
				:disabled="ticket.status !== 'open' || !newComment.trim()"
			>
				<v-icon>{{ mdiSend }}</v-icon>
			</v-btn>
		  </div>
		</v-card-text>
	  </v-card>
	</v-dialog>
  </template>
  
  <script lang="ts">
  import Vue from 'vue'
  import {
	mdiClose,
	mdiTicket,
	mdiMessageOutline,
	mdiSend,
	mdiPencil,
	mdiMagnify,
	mdiShield
  } from '@mdi/js'
  import { mapGetters } from 'vuex'
  import { TicketDTO, CommentDTO } from '~/services/application/tickets/ticketData'
  
  export default Vue.extend({
	props: {
	  ticket: {
		type: Object as () => TicketDTO,
		required: true
	  },
	  comments: {
		type: Array as () => CommentDTO[],
		required: true
	  },
	  show: {
		type: Boolean,
		required: true
	  },
	  projectId: {
		type: Number,
		required: true
	  }
	},

	watch: {
		comments: {
			handler() {
				this.scrollToBottom();
			},
			deep: true
		},
		show(newVal: boolean) {
			if (newVal) {
				this.startPolling();
			} else {
				this.stopPolling();
			}
			if (!newVal) {
				this.newComment = '';
			}
		}
	},

  
	data() {
	  return {
		newComment: '',
		mdiSend,
		mdiMessageOutline,
		mdiClose,
		mdiTicket,
		mdiPencil,
		mdiMagnify,
		mdiShield,
		pollingInterval: null as NodeJS.Timeout | null,
      	pollInterval: 3000
	  }
	},

	beforeDestroy() {
		this.stopPolling();
	},
  
	computed: {
		...mapGetters('auth', ['getUsername', 'getUserId']),
		currentUserId(): number | null {
			return this.getUserId
		},
		validComments(): CommentDTO[] {
			return (this.comments || []).filter(comment => 
				comment && 
				comment.id && 
				comment.content &&
				comment.created_at
			)
		}
	},

	created() {
		this.scrollToBottom()
	},
  
	methods: {
		startPolling() {
			this.stopPolling(); // Clear any existing interval
			this.pollingInterval = setInterval(() => {
				this.$emit('refresh-comments');
			}, this.pollInterval);
		},

		stopPolling() {
			if (this.pollingInterval) {
				clearInterval(this.pollingInterval);
				this.pollingInterval = null;
			}
		},
	  isCurrentUser(comment: CommentDTO): boolean {
		return comment.author_username === this.getUsername || comment.author === this.currentUserId
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
  
	  addComment() {
		if (this.newComment.trim()) {
		  this.$emit('add-comment', {
			content: this.newComment
		  })
		  this.newComment = ''
		}
	  },

	  scrollToBottom() {
		this.$nextTick(() => {
		  const container = this.$refs.messagesContainer as HTMLElement
		  if (container) {
			container.scrollTop = container.scrollHeight
		  }
		})
	  },
	  
  
	  getRoleIcon(comment: CommentDTO): string {
  
		if (comment.author_role === 'annotator') {
		  return this.mdiPencil
		} else if (comment.author_role === 'annotation_approver') {
		  return this.mdiMagnify
		} else if (comment.author_role === 'project_admin') {
		  return this.mdiShield
		}
		return ''
	  }
	}
  })
  </script>
  
  <style scoped>
  .ticket-chat {
	--primary-color: #1976D2;
	--primary-light: #E3F2FD;
	--background-color: #FFFFFF;
	--message-bg: #F5F5F5;
	--current-user-bg: #E3F2FD;
	--text-color: #333333;
	--text-secondary: #666666;
	--border-color: #E0E0E0;
	--shadow-color: rgba(0, 0, 0, 0.1);
	--scrollbar-thumb: var(--primary-color);
	--scrollbar-track: var(--background-color);
	height: auto;
	display: flex;
	flex-direction: column;
	background-color: var(--background-color);
  }
  
  .theme--dark .ticket-chat {
	--primary-color: #31D1F1;
	--primary-light: rgba(49, 209, 241, 0.1);
	--background-color: #121212;
	--message-bg: #1E1E1E;
	--current-user-bg: rgba(49, 209, 241, 0.2);
	--text-color: #FFFFFF;
	--text-secondary: #B0B0B0;
	--border-color: #333333;
	--shadow-color: rgba(255, 255, 255, 0.05);
	--scrollbar-thumb: #31D1F1;
	--scrollbar-track: var(--background-color);
  }
  
  .chat-header {
	padding: 16px 24px;
	border-top-left-radius: 4px;
	border-top-right-radius: 4px;
  }
  
  .chat-container {
	max-height: 80vh;
	min-height: 300px;
	display: flex;
	flex-direction: column;
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
	align-items: center;
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
  
  @media (max-width: 600px) {
	.chat-container {
	  height: 400px;
	}
  
	.message-content {
	  max-width: 90%;
	}
  }
  
  .role-icon {
	margin-right: 8px;
  }
  </style>
  