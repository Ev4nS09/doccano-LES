// ~/services/application/perspective/perspectiveApplicationService.ts
import { PerspectiveDTO, PerspectiveItemDTO } from './perspectiveData'
import { CreatePerspectiveCommand, CreatePerspectiveItemCommand } from './perspectiveCommand'
import { PerspectiveRepository } from '~/domain/models/perspective/perspectiveRepository'
import { Perspective, PerspectiveItem } from '~/domain/models/perspective/perspective'

export class PerspectiveApplicationService {
	constructor(private readonly repository: PerspectiveRepository) { }

	// Perspectives
	// Lista de perspetivas do projeto
	async list(projectId: string): Promise<PerspectiveDTO[]> {
		const items = await this.repository.list(projectId)
		return items.map(item => new PerspectiveDTO(item))
	}

	// Lista de items de uma perspetiva do projeto
	async get(projectId: string, perspectiveId: string): Promise<PerspectiveItemDTO[]> {
		const items = await this.repository.get(projectId, perspectiveId)
		return items.map(item => new PerspectiveItemDTO(item));
	}

	// Lista de perspetivas associadas ao utilizador logado no example fornecido
	async getExamplesPerspectives(projectId: string, example_id: string): Promise<Perspective[]> {
		const items = await this.repository.getExamplesPerspectives(projectId, example_id)
		return items.map(item => new PerspectiveDTO(item))
	}

	// Não foi testado daqui para baixo
	async create(projectId: string, item: CreatePerspectiveCommand): Promise<PerspectiveDTO> {
		const perspective = Perspective.create(item.projectId, item.name, item.description)
		const created = await this.repository.create(projectId, perspective)
		return new PerspectiveDTO(created)
	}

	async update(
		projectId: string,
		perspectiveId: string,
		name: string,
		description?: string
	): Promise<PerspectiveDTO> {
		const updated = await this.repository.update(projectId, perspectiveId, name, description)
		return new PerspectiveDTO(updated)
	}

	async bulkDelete(projectId: string, items: PerspectiveDTO[]): Promise<void> {
		const ids = items.map((item) => item.id)
		await this.repository.bulkDelete(projectId, ids)
	}

	// Items
	async listItems(perspectiveId: string): Promise<PerspectiveItemDTO[]> {
		const items = await this.repository.listItems(perspectiveId)
		return items.map(item => new PerspectiveItemDTO(item))
	}

	async getItem(perspectiveId: string, itemId: number): Promise<PerspectiveItemDTO> {
		const item = await this.repository.getItem(perspectiveId, itemId)
		return new PerspectiveItemDTO(item)
	}

	async createItem(perspectiveId: string, item: CreatePerspectiveItemCommand): 
	Promise<PerspectiveItemDTO> {
		const perspectiveItem = PerspectiveItem.create(item.name, perspectiveId)
		const created = await this.repository.createItem(perspectiveId, perspectiveItem)
		return new PerspectiveItemDTO(created)
	}

	async updateItem(
		perspectiveId: string,
		itemId: number,
		name: string
	): Promise<PerspectiveItemDTO> {
		const updated = await this.repository.updateItem(perspectiveId, itemId, name)
		return new PerspectiveItemDTO(updated)
	}

	public bulkDeleteItems(projectId: string, items: PerspectiveItemDTO[]): Promise<void> {
	const ids = items.map((item) => item.id)
	return this.repository.bulkDelete(projectId, ids)
	}
}