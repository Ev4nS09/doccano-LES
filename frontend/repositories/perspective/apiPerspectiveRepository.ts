import { PerspectiveItem, Perspective } from '@/domain/models/perspective/perspective'
import ApiService from '@/services/api.service'

function toModelPerspectiveItem(item: { [key: string]: any }): PerspectiveItem {
  return new PerspectiveItem(
    item.id,
    item.name,
    item.item_type,
    item.selection_list,
    item.createdAt,
    item.updatedAt,
  )
}

function toModelPerspective(item: { [key: string]: any }): Perspective {
  return new Perspective(
    item.id,
    item.name,
    item.items,
    item.createdAt,
    item.updatedAt,
  )
}

function toPayloadPerspectiveItem(item: PerspectiveItem): { [key: string]: any } {
  return {
    id: item.id,
    name: item.name,
    item_type: item.item_type,
    selection_list: item.selection_list,
    createdAt: item.createdAt,
    updatedAt: item.updatedAt,
  }
}


function toPayloadPerspective(item: Perspective): { [key: string]: any } {
  return {
    id: item.id,
    name: item.name,
    items: item.items,
    createdAt: item.createdAt,
    updatedAt: item.updatedAt,
  }
}

export class APIPerspectiveRepository {
  constructor(private readonly request = ApiService) {}
    
  async listAllPerspectiveItem(): Promise<PerspectiveItem[]> {
    const url = `perspectives/items`
    const response = await this.request.get(url)
    return response.data.results.map((item: { [key: string]: any }) => toModelPerspectiveItem(item))
  }

  async listPerspectiveItem(perspectiveId: string): Promise<PerspectiveItem[]> {
    const url = `perspectives/${perspectiveId}/items`
    const response = await this.request.get(url)
    return response.data.results.map((item: { [key: string]: any }) => toModelPerspectiveItem(item))
  }

  async listPerspective(): Promise<Perspective[]> {
    const url = `perspectives`
    const response = await this.request.get(url)
    return response.data.results.map((item: { [key: string]: any }) => toModelPerspective(item))
  }

  async createPerspectiveItem(item: PerspectiveItem): Promise<PerspectiveItem> {
    const url = `perspectives/items`
    const payload = toPayloadPerspectiveItem(item)
    const response = await this.request.post(url, payload)
    return toModelPerspectiveItem(response.data)
  }

  async createPerspective(item: Perspective): Promise<Perspective> {
    const url = `perspectives/create`
    const payload = toPayloadPerspective(item)
    const response = await this.request.post(url, payload)
    return toModelPerspective(response.data)
  }
}
