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

  async filterMembers(projectId: string, filters: Record<string, string | number>): 
  Promise<number[]>
  {
    const query = new URLSearchParams()

    for (const [key, value] of Object.entries(filters)) {
      query.append(key, value.toString())
    }

    const url = `projects/${projectId}/perspectives/filter-members/?${query.toString()}`
    const response = await this.request.get(url)

    return Array.isArray(response.data?.member_ids) ? response.data.member_ids : 
         Array.isArray(response.data?.user_ids) ? response.data.user_ids : 
         []
  }

  private formatStatsForCSV(
    general: Record<string, any>,
    perspectiveStats: {
      perspectiveFilters?: Array<{perspective: string, type: string, value: any}>,
      labelDistribution?: Record<string, Record<string, number>>
    }
  ): string {
    // Format general stats
    const generalLines = [
      'SECTION,KEY,VALUE',
      ...Object.entries(general).map(([key, value]) => `GENERAL,${this.escapeCsvValue(key)},${this.escapeCsvValue(value)}`)
    ];

    // Format perspective filters if they exist
    const filterLines = [];
    if (perspectiveStats.perspectiveFilters && perspectiveStats.perspectiveFilters.length > 0) {
      filterLines.push(
        '\nSECTION,PERSPECTIVE,TYPE,MIN,MAX,VALUE',
        ...perspectiveStats.perspectiveFilters.map(filter => {
          if (typeof filter.value === 'object' && filter.value !== null) {
            // Handle numeric range filters
            return `FILTER,${this.escapeCsvValue(filter.perspective)},${this.escapeCsvValue(filter.type)},${filter.value.min ?? ''},${filter.value.max ?? ''},`;
          } else {
            // Handle simple value filters
            return `FILTER,${this.escapeCsvValue(filter.perspective)},${this.escapeCsvValue(filter.type)},,,${this.escapeCsvValue(filter.value)}`;
          }
        })
      );
    }

    // Format label distribution if it exists
    const labelLines = [];
    if (perspectiveStats.labelDistribution) {
      labelLines.push(
        '\nSECTION,EXAMPLE,LABEL,PERCENTAGE',
        ...Object.entries(perspectiveStats.labelDistribution).flatMap(([example, labels]) => 
          Object.entries(labels).map(([label, percentage]) => 
            `LABEL,${this.escapeCsvValue(example)},${this.escapeCsvValue(label)},${percentage}`
          )
      ));
    }

    // Add export timestamp
    const timestampLine = `\nMETA,exportedAt,${new Date().toISOString()}`;

    // Combine all lines
    return [...generalLines, ...filterLines, ...labelLines, timestampLine].join('\n');
  }

  public exportStatsAsCSV(
    general: Record<string, any>, 
    perspectiveStats: {
      perspectiveFilters?: Array<{perspective: string, type: string, value: any}>,
      labelDistribution?: Record<string, Record<string, number>>
    }
  ) {
    const csvContent = this.formatStatsForCSV(general, perspectiveStats);
    this.triggerDownload(csvContent, 'csv');
  }

  // Helper method to properly escape CSV values
  private escapeCsvValue(value: any): string {
    if (value === null || value === undefined) return '';
    const str = String(value);
    if (str.includes(',') || str.includes('"') || str.includes('\n') || str.includes('\r')) {
      return `"${str.replace(/"/g, '""')}"`;
    }
    return str;
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
		  const response = await this.exportAsPDF(data);
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

    
  async exportAsPDF(data: any): Promise<any> {
    const url = `/projects/${data.projectId}/download-pdf`;
    const response = await this.request.post(url, data, {
      responseType: 'blob'
    });
    return response.data;
  }
}
