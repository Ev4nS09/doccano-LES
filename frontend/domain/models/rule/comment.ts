export class Comment {
	constructor(
	  readonly id: number,
	  readonly rule: number,
	  readonly author: number,
	  readonly content: string,
	  readonly created_at: string,
	  readonly updated_at: string
	) {
	  if (!content.trim()) throw new Error('Comment cannot be empty')
	}
  }