export class Ticket {
	constructor(
	  readonly id: number,
	  readonly project: number,
	  readonly created_by: number,
	  readonly title: string,
	  readonly description: string,
	  readonly status: string,
	  readonly author_username: string,  // Moved after status to match create()
	  readonly rules: number[],
	  readonly created_at: string,
	  readonly updated_at: string
	) {
	  if (!title.trim()) throw new Error('Title is required')
	  if (!description.trim()) throw new Error('Description is required')
	  if (!['open', 'in_progress', 'resolved', 'closed'].includes(status)) {
		throw new Error('Invalid status value')
	  }
	}
  
	static create(
		id: number,
		project: number,
		created_by: number,
		title: string,
		description: string,
		status: string = 'open',
		author_username: string = '',  // Added here
		rules: number[] = [],
		created_at: string = '',
		updated_at: string = ''
	  ): Ticket {
		return new Ticket(
		  id,
		  project,
		  created_by,
		  title,
		  description,
		  status,
		  author_username,  // Added here
		  rules,
		  created_at,
		  updated_at
		)
	  }
	}