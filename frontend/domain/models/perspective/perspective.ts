export class PerspectiveItem {
	constructor(
	  readonly id: number,
	  readonly name: string,
      readonly item_type: string,
      readonly selection_list: string[],
	  readonly createdAt: string,
	  readonly updatedAt: string
	) {}
}

export class Perspective {
    constructor(
	  readonly id: number,
	  readonly name: string,
      readonly items: number[],
	  readonly createdAt: string,
	  readonly updatedAt: string
    ){}
}

export class PerspectiveValue {
	constructor(
	  readonly id: number,
	  readonly member: string,
      readonly item: number,
      readonly value: string,
	  readonly createdAt: string,
    ){}
}
