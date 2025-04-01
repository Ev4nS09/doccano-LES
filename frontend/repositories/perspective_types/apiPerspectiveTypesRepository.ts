import ApiService from '@/services/api.service'
import { PerspectiveType } from '~/domain/models/perspective_types/perspective_types'
// import { PerspectiveItem } from '~/domain/models/perspective_types/perspective_types'


function toModelPerspectiveType(item: { [key: string]: any }): PerspectiveType {
  return new PerspectiveType(
        item.id,
        item.name,
        item.project,
        item.description,
    )
}

/* function toModelPerspectiveItem(item: { [key: string]: any }): PerspectiveItem{
  return new PerspectiveItem(
        item.id,
        item.name,
        item.perspective,
    )
} */

export class APIPerspectiveTypesRepository {
  constructor(private readonly request = ApiService) {}

  async list(perspective_id: number): Promise<PerspectiveType[]> {
    const url = `perspective-category-types/?q=${perspective_id}`
    const response = await this.request.get(url)
    return response.data.map((item: { [key: string]: any }) => toModelPerspectiveType(item))
  }
}
