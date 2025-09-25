import { Ticket } from '@/domain/models/tickets/ticket'
import { TicketComment } from '@/domain/models/tickets/comment'
import ApiService from '@/services/api.service'

function toTicketModel(item: any): Ticket {
  return Ticket.create(
    item.id,
    item.project,
    item.created_by,
    item.title,
    item.description,
    item.status,
    item.author_username || '',
    item.rules || [],
    item.created_at,
    item.updated_at
  )
}

function toCommentModel(item: any): TicketComment {
  return new TicketComment(
    item.id,
    item.ticket || 0,
    item.author || 0,
    item.author_role || 'annotator',
    item.author_username || '',
    item.content || '',
    item.created_at || new Date().toISOString(),
    item.updated_at || new Date().toISOString()
  )
}

export class APITicketRepository {
  constructor(private readonly request = ApiService) {}

  async list(projectId: number): Promise<Ticket[]> {
    const url = `/projects/${projectId}/tickets?limit=1000`
    const response = await this.request.get(url)
    return response.data.results.map(toTicketModel)
  }

  async create(projectId: number, ticket: Omit<Ticket, 'id' | 'created_at' | 'updated_at'>): Promise<Ticket> {
    const url = `/projects/${projectId}/tickets`
    const response = await this.request.post(url, {
      title: ticket.title,
      description: ticket.description,
      status: ticket.status,
      project: ticket.project,
      created_by: ticket.created_by,
      // author_username is not needed here since it's handled by the backend
    })
    return toTicketModel(response.data)
  }

  async update(projectId: number, ticketId: number, data: Partial<Ticket>): Promise<Ticket> {
    const url = `/projects/${projectId}/tickets/${ticketId}`
    const response = await this.request.patch(url, data)
    return toTicketModel(response.data)
  }

  async delete(projectId: number, ticketId: number): Promise<void> {
    const url = `/projects/${projectId}/tickets/${ticketId}`
    await this.request.delete(url)
  }

  async getComments(projectId: number, ticketId: number): Promise<TicketComment[]> {
    const url = `/projects/${projectId}/tickets/${ticketId}/comments?limit=1000`
    try {
      const response = await this.request.get(url)
      if (!response.data || !Array.isArray(response.data.results)) {
        throw new Error('Invalid comments response format')
      }
      return response.data.results.map(toCommentModel)
    } catch (error) {
      console.error('Error fetching comments:', error)
      throw error
    }
  }

  async addComment(projectId: number, ticketId: number, content: string): Promise<TicketComment> {
    const url = `/projects/${projectId}/tickets/${ticketId}/comments`
    try {
      const response = await this.request.post(url, { content })
      if (!response.data) {
        throw new Error('Invalid comment response')
      }
      return toCommentModel(response.data)
    } catch (error) {
      console.error('Error adding comment:', error)
      throw error
    }
  }

  async updateRules(projectId: number, ticketId: number, ruleIds: number[]): Promise<void> {
    const url = `/projects/${projectId}/tickets/${ticketId}/rules`
    await this.request.post(url, { rule_ids: ruleIds })
  }

  async removeRules(projectId: number, ticketId: number, ruleIds: number[]): Promise<void> {
    const url = `/projects/${projectId}/tickets/${ticketId}/rules`
    await this.request.delete(url, { data: { rule_ids: ruleIds } })
  }
}