export class PerspectiveItem {
	constructor(
	  readonly id: number,
	  readonly name: string,
	  readonly project: number,
      readonly p_type: string,
      readonly selection_list: string[],
	  readonly createdAt: string,
	  readonly updatedAt: string
	) {}
}
