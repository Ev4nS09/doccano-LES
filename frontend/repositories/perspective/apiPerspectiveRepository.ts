import { PerspectiveItem } from '@/domain/models/perspective/perspectiveItem'
import ApiService from '@/services/api.service'

function toModel(item: { [key: string]: any }): PerspectiveItem {
  return new PerspectiveItem(
    item.id,
    item.name,
    item.project,
    item.item_type,
    item.selection_list,
    item.createdAt,
    item.updatedAt,
  )
}

function toPayload(item: PerspectiveItem): { [key: string]: any } {
  return {
    id: item.id,
    name: item.name,
    project: item.project,
    item_type: item.item_type,
    selection_list: item.selection_list,
    createdAt: item.createdAt,
    updatedAt: item.updatedAt,
  }
}

export class APIPerspectiveRepository {
  constructor(private readonly request = ApiService) {}
    
  async list(projectId: string): Promise<PerspectiveItem[]> {
    const url = `/projects/${projectId}/perspectives`
    const response = await this.request.get(url)
    return response.data.results.map((item: { [key: string]: any }) => toModel(item))
  }

  async create(projectId: string, item: PerspectiveItem): Promise<PerspectiveItem> {
    const url = `/projects/${projectId}/perspectives`
    const payload = toPayload(item)
    const response = await this.request.post(url, payload)
    return toModel(response.data)
  }
}
