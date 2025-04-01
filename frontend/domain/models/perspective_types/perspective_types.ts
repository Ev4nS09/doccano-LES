import { Project } from '~/domain/models/project/project'

export class PerspectiveType
{
    constructor(
        readonly id: number,
        readonly name: string,
        readonly project: Project,
        readonly description: string,
        readonly created_at: string = '',
        readonly updated_at: string = '',
    ){}
}

export class PerspectiveItem 
{
    constructor(
        readonly id: number,
        readonly name: string,
        readonly perspective: PerspectiveType,
    ){}
}

export class CategoryType 
{
    constructor(
        readonly perspective: PerspectiveType,
    ){}
}
