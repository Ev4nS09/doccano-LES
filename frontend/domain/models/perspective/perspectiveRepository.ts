// ~/domain/models/perspective/perspectiveRepository.ts
import { Perspective, PerspectiveItem } from '~/domain/models/perspective/perspective'

export interface PerspectiveRepository {
  // Perspective CRUD
  list(projectId: string): Promise<Perspective[]>
  get(projectId: string, perspectiveId: string): Promise<PerspectiveItem[]>
  getExamplesPerspectives(projectId: string, example_id: string): Promise<Perspective[]>
  create(projectId: string, perspective: Perspective): Promise<Perspective>
  update(
    projectId: string, 
    perspectiveId: string,
    name: string,
    description?: string
  ): Promise<Perspective>
  delete(projectId: string, perspectiveId: string): Promise<void>
  bulkDelete(projectId: string, perspectiveIds: number[]): Promise<void>

  // Perspective Items CRUD
  listItems(perspectiveId: string): Promise<PerspectiveItem[]>
  getItem(perspectiveId: string, itemId: number): Promise<PerspectiveItem>
  createItem(perspectiveId: string, perspectiveItem: PerspectiveItem): Promise<PerspectiveItem>
  updateItem(perspectiveId: string, itemId: number, name: string): Promise<PerspectiveItem>
  deleteItem(perspectiveId: string, itemId: number): Promise<void>
  bulkDeleteItems(perspectiveId: string, itemIds: number[]): Promise<void>
}