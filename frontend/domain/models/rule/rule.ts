export class Rule {
	constructor(
	  readonly id: number,
	  readonly project: number,
	  readonly created_by: number,
	  readonly title: string,
	  readonly description: string,
	  readonly upvotes: number[],
	  readonly downvotes: number[],
	  readonly created_at: string,
	  readonly updated_at: string,
      readonly status: string
	) {
	  if (!title.trim()) throw new Error('Title is required')
	  if (!description.trim()) throw new Error('Description is required')
	}
  
	// Computed property only (no declare)
	get score(): number {
	  return this.upvotes.length - this.downvotes.length
	}
  
	static create(
	  id: number,
	  project: number,
	  created_by: number,
	  title: string,
	  description: string,
	  upvotes: number[] = [],
	  downvotes: number[] = [],
	  created_at: string = '',
	  updated_at: string = '',
      status: string = 'On going',
	): Rule {
	  return new Rule(
		id,
		project,
		created_by,
		title,
		description,
		upvotes,
		downvotes,
		created_at,
		updated_at,
        status,
	  )
	}
  }
