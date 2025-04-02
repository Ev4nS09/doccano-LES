// ~/repositories/perspective/apiPerspectiveRepository.ts
import { PerspectiveRepository } from '~/domain/models/perspective/perspectiveRepository'
import { Perspective, PerspectiveItem } from '~/domain/models/perspective/perspective'
import ApiService from '@/services/api.service'

export class ApiPerspectiveRepository implements PerspectiveRepository {
  private request = ApiService

  private toPerspective(item: any, projectId: string): Perspective {
    return new Perspective(
      item.id,
      item.name,
      projectId,
      item.description,
      item.created_at,
      item.updated_at
    )
  }

  private toPerspectiveItem(item: any, perspectiveId: string): PerspectiveItem {
    return new PerspectiveItem(
      item.id,
      item.name,
      perspectiveId,
      item.created_at,
      item.updated_at
    )
  }

  // Lista de perspetivas do projeto
  async list(projectId: string): Promise<Perspective[]> {
    const url = `/projects/${projectId}/perspectives`
    const response = await this.request.get(url)
    return response.data.map((item: any) => this.toPerspective(item, projectId))
  }

  // Lista de items de uma perspetiva do projeto
  async get(projectId: string, perspectiveId: string): Promise<PerspectiveItem[]> {
    const url = `/projects/${projectId}/perspective/${perspectiveId}/items`
    const response = await this.request.get(url)
    return response.data.map((item: any) => this.toPerspectiveItem(item, projectId))
  }

  // Lista de perspetivas associadas ao utilizador logado no example fornecido
  async getExamplesPerspectives(projectId: string, example_id: string): Promise<Perspective[]> {
    const url = `/projects/${projectId}/examples/${example_id}/p-categories`
    const response = await this.request.get(url)
    
    return response.data.map((item: any) => ({
        id: item.id,
        exampleId: item.example,
        userId: item.user,
        perspectiveId: item.perspective,
        itemId: item.item
    }))
  }

  // Daqui para baixo não foi testado (Pode até ter coisas a + ou a -)
  async create(projectId: string, perspective: Perspective): Promise<Perspective> {
    const url = `/projects/${projectId}/perspectives`
    const response = await this.request.post(url, {
      name: perspective.name,
      description: perspective.description
    })
    return this.toPerspective(response.data, projectId)
  }

  async update(
    projectId: string,
    perspectiveId: string,
    name: string,
    description?: string
  ): Promise<Perspective> {
    const url = `/projects/${projectId}/perspectives/${perspectiveId}`
    const response = await this.request.put(url, {
      name,
      description
    })
    return this.toPerspective(response.data, projectId)
  }

  async delete(projectId: string, perspectiveId: string): Promise<void> {
    const url = `/projects/${projectId}/perspectives/${perspectiveId}`
    await this.request.delete(url)
  }

  async bulkDelete(projectId: string, perspectiveIds: number[]): Promise<void> {
    const url = `/projects/${projectId}/perspectives/bulk-delete`
    await this.request.delete(url, { data: { ids: perspectiveIds } })
  }

  // Perspective Items
  async listItems(perspectiveId: string): Promise<PerspectiveItem[]> {
    const url = `/perspectives/${perspectiveId}/items`
    const response = await this.request.get(url)
    return response.data.map((item: any) => this.toPerspectiveItem(item, perspectiveId))
  }

  async getItem(perspectiveId: string, itemId: number): Promise<PerspectiveItem> {
    const url = `/perspectives/${perspectiveId}/items/${itemId}`
    const response = await this.request.get(url)
    return this.toPerspectiveItem(response.data, perspectiveId)
  }

  async createItem(perspectiveId: string, item: PerspectiveItem): Promise<PerspectiveItem> {
    const url = `/perspectives/${perspectiveId}/items`
    const response = await this.request.post(url, {
      name: item.name
    })
    return this.toPerspectiveItem(response.data, perspectiveId)
  }

  async updateItem(
    perspectiveId: string,
    itemId: number,
    name: string
  ): Promise<PerspectiveItem> {
    const url = `/perspectives/${perspectiveId}/items/${itemId}`
    const response = await this.request.put(url, { name })
    return this.toPerspectiveItem(response.data, perspectiveId)
  }

  async deleteItem(perspectiveId: string, itemId: number): Promise<void> {
    const url = `/perspectives/${perspectiveId}/items/${itemId}`
    await this.request.delete(url)
  }

  async bulkDeleteItems(perspectiveId: string, itemIds: number[]): Promise<void> {
    const url = `/perspectives/${perspectiveId}/items/bulk-delete`
    await this.request.delete(url, { data: { ids: itemIds } })
  }
}