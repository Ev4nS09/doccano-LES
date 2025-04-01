import { ExampleItem } from '~/domain/models/example/example'
import { UserItem } from '~/domain/models/user/user'
import { PerspectiveItem, PerspectiveType } from '~/domain/models/perspective_types/perspective_types'

export class CategoryPerspective
{
    constructor(
        readonly id: number,
        readonly user: UserItem,
        readonly example: ExampleItem,
        readonly perspective: PerspectiveType,
        readonly perspective_item: PerspectiveItem,
        readonly created_at: string = '',
        readonly updated_at: string = '',
    ){} 
}
