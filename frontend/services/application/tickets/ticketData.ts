export interface CommentDTO {
	id: number
	author: number
	author_role: string
	author_username: string
	content: string
	created_at: string
	updated_at: string
  }
  
  export interface TicketDTO {
	id: number
	project: number
	created_by: number
	author_username: string
	title: string
	description: string
	status: string
	rules: number[]
	rule_count: number
	comments: CommentDTO[]
	created_at: string
	updated_at: string
  }