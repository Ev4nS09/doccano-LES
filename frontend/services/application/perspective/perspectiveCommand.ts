import { PerspectiveDTO, PerspectiveItemDTO } from './perspectiveData'

export type CreatePerspectiveCommand = Omit<PerspectiveDTO, 'id' | 'createdAt' | 'updatedAt'>
export type UpdatePerspectiveCommand = PerspectiveDTO

export type CreatePerspectiveItemCommand = Omit<PerspectiveItemDTO, 'id' | 'createdAt' | 'updatedAt'>
export type UpdatePerspectiveItemCommand = PerspectiveItemDTO