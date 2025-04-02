import { Perspective, PerspectiveItem } from '~/domain/models/perspective/perspective'

export class PerspectiveDTO {
  id: number
  name: string
  projectId: string
  description: string | null
  createdAt: string
  updatedAt: string

  constructor(item: Perspective) {
    this.id = item.id
    this.name = item.name
    this.projectId = item.projectId
    this.description = item.description
    this.createdAt = item.createdAt
    this.updatedAt = item.updatedAt
  }
}

export class PerspectiveItemDTO {
  id: number
  name: string
  perspectiveId: string
  createdAt: string
  updatedAt: string

  constructor(item: PerspectiveItem) {
    this.id = item.id
    this.name = item.name
    this.perspectiveId = item.perspectiveId
    this.createdAt = item.createdAt
    this.updatedAt = item.updatedAt
  }
}