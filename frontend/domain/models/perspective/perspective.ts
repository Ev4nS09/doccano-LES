// ~/domain/models/perspective/perspectiveTypes.ts

export class Perspective {
	constructor(
	  readonly id: number,
	  readonly name: string,
	  readonly projectId: string,
	  readonly description: string | null,
	  readonly createdAt: string,
	  readonly updatedAt: string
	) {}
  
	static create(
	  name: string,
	  projectId: string,
	  description: string | null = null
	): Perspective {
	  const now = new Date().toISOString()
	  return new Perspective(0, name, projectId, description, now, now)
	}
  }
  
  export class PerspectiveItem {
	constructor(
	  readonly id: number,
	  readonly name: string,
	  readonly perspectiveId: string,
	  readonly createdAt: string,
	  readonly updatedAt: string
	) {}
  
	static create(name: string, perspectiveId: string): PerspectiveItem {
	  const now = new Date().toISOString()
	  return new PerspectiveItem(0, name, perspectiveId, now, now)
	}
  }