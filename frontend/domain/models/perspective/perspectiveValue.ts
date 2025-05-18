import { PerspectiveItem } from '~/domain/models/perspective/perspectiveItem'

export class PerspectiveValue {
	constructor(
	  readonly id: number,
	  readonly member: string,
      readonly item: PerspectiveItem,
      readonly value: string,
	  readonly createdAt: string,
    )
    {}
}
