// services/application/perspective/perspectiveApplicationService.ts
import {
	ItemDTO,
	ValueDTO,
	CreateItemCommand,
	UpdateItemCommand,
	CreateValueCommand,
	UpdateValueCommand,
	ExamplePerspectiveStatsDTO
  } from './perspectiveData'
  import { PerspectiveRepository } from '~/domain/models/perspective/perspectiveRepository'
  
  export class PerspectiveApplicationService {
	constructor(private readonly repository: PerspectiveRepository) {}
  
	public async listItems(projectId: string): Promise<ItemDTO[]> {
	  const items = await this.repository.listItems(projectId)
	  return items.map(item => ItemDTO.fromDomain(item))
	}
  
	public async createItem(projectId: string, command: CreateItemCommand): Promise<ItemDTO> {
	  const created = await this.repository.createItem(projectId, command)
	  return ItemDTO.fromDomain(created)
	}
  
	public async updateItem(projectId: string, command: UpdateItemCommand): Promise<ItemDTO> {
	  const updated = await this.repository.updateItem(projectId, {
		id: command.id,
		project: command.project,
		name: command.name,
		created_at: '', // Will be overwritten
		updated_at: '', // Will be overwritten
		predefined_values: [] // Will be overwritten
	  })
	  return ItemDTO.fromDomain(updated)
	}
  
	public async listValues(projectId: string, exampleId: string): Promise<ValueDTO[]> {
	  const values = await this.repository.listValues(projectId, exampleId)
	  return values.map(value => ValueDTO.fromDomain(value))
	}
  
	public async createValue(projectId: string, exampleId: string, 
		command: CreateValueCommand): Promise<ValueDTO> {
	  const created = await this.repository.createValue(projectId, exampleId, command)
	  return ValueDTO.fromDomain(created)
	}
  
	public async updateValue(projectId: string, exampleId: string, 
		command: UpdateValueCommand): Promise<ValueDTO> {
	  const updated = await this.repository.updateValue(projectId, exampleId, command.id, command)
	  return ValueDTO.fromDomain(updated)
	}
  
	public async deleteValue(projectId: string, exampleId: string, valueId: number): Promise<void> {
	  await this.repository.deleteValue(projectId, exampleId, valueId)
	}

	public async getExamplePerspectiveStats(projectId: string, 
		exampleId: string): Promise<ExamplePerspectiveStatsDTO> {
		const stats = await this.repository.getExamplePerspectiveStats(projectId, exampleId);
		return ExamplePerspectiveStatsDTO.fromDomain(stats);
	  }
	
	private formatStatsForCSV(general: Record<string, any>, 
		perspectiveItemStats: Record<string, any>): string {
		// Format general stats
		const generalLines = [
		'General Statistics',
		...Object.entries(general).map(([key, value]) => `${key},${value}`)
		];
		
		// Format perspective stats
		const perspectiveLines = ['\nPerspective Statistics'];
		for (const [itemName, stats] of Object.entries(perspectiveItemStats)) {
		perspectiveLines.push(`\n${itemName}`);
		for (const [metric, data] of Object.entries(stats)) {
			perspectiveLines.push(`${metric},${data.percentage}%,${data.count}`);
		}
		}
		
		// Combine all lines
		return [...generalLines, ...perspectiveLines].join('\n');
	}

	public exportStatsAsCSV(general: Record<string, any>, perspectiveItemStats: Record<string, any>) {
		const csvContent = this.formatStatsForCSV(general, perspectiveItemStats);
		this.triggerDownload(csvContent, 'csv');
	}
	  
	public exportStatsAsJSON(general: Record<string, any>, 
		perspectiveItemStats: Record<string, any>) {
		const data = {
		  generalStatistics: general,
		  perspectiveStatistics: perspectiveItemStats,
		  exportedAt: new Date().toISOString()
		};
		this.triggerDownload(JSON.stringify(data, null, 2), 'json');
	}
	  
	  private triggerDownload(content: string, format: 'csv' | 'json') {
		const blob = new Blob([content], { type: format === 'csv' ? 'text/csv' : 'application/json' });
		const url = window.URL.createObjectURL(blob);
		const link = document.createElement('a');
		link.href = url;
		link.setAttribute('download', `perspective_stats_${new Date().toISOString().split('T')[0]}.${format}`);
		document.body.appendChild(link);
		link.click();
		document.body.removeChild(link);
	  }

	  public async exportStatsAsPDF(
		general: Record<string, any>, 
		perspectiveItemStats: Record<string, any>,
		projectId: string
	  ): Promise<void> {
		const data = {
		  generalStats: general,
		  perspectiveStats: perspectiveItemStats,
		  projectId // Using property shorthand since variable name matches property name
		};
	  
		try {
		  const response = await this.repository.exportAsPDF(data);
		  const blob = new Blob([response], { type: 'application/pdf' });
		  const url = window.URL.createObjectURL(blob);
		  const link = document.createElement('a');
		  link.href = url;
		  link.setAttribute('download', `perspective_stats_${new Date().toISOString().split('T')[0]}.pdf`);
		  document.body.appendChild(link);
		  link.click();
		  document.body.removeChild(link);
		} catch (error) {
		  console.error('PDF export failed:', error);
		  throw error;
		}
	  }
  }