// domain/models/tickets/comment.ts
export class TicketComment {
	constructor(
	  readonly id: number,
	  readonly ticket: number,
	  readonly author: number,
	  readonly author_role: string,
	  readonly author_username: string,
	  readonly content: string,
	  readonly created_at: string,
	  readonly updated_at: string
	) {
	  if (!content.trim()) throw new Error('Comment cannot be empty')
	}
  }