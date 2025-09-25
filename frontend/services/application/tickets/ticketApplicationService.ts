import { TicketDTO } from './ticketData'
import { TicketService } from './ticketService'

export class TicketApplicationService {
  constructor(private readonly service: TicketService) {}

  async list(projectId: number): Promise<TicketDTO[]> {
    try {
      return await this.service.list(projectId)
    } catch (e) {
      throw new Error('Failed to fetch tickets')
    }
  }

  async create(projectId: number, data: { title: string; description: string, 
    status?: string, created_by: number, author_username: string }): 
  Promise<TicketDTO> {
    if (!data.title.trim() || !data.description.trim()) {
      throw new Error('Title and description are required')
    }
    return await this.service.create(projectId, data)
  }

  async update(
    projectId: number,
    ticketId: number,
    data: { title?: string; description?: string; status?: string }
  ): Promise<TicketDTO> {
    if (data.title && !data.title.trim()) {
      throw new Error('Title cannot be empty')
    }
    if (data.description && !data.description.trim()) {
      throw new Error('Description cannot be empty')
    }
    return await this.service.update(projectId, ticketId, data)
  }

  async delete(projectId: number, ticketId: number): Promise<void> {
    await this.service.delete(projectId, ticketId)
  }

  async deleteTickets(projectId: number, tickets: TicketDTO[]): Promise<void> {
    const ticketIds = tickets.map(ticket => ticket.id)
    await Promise.all(
      ticketIds.map(id => this.service.delete(projectId, id)))
  }

  async getComments(projectId: number, ticketId: number): Promise<any[]> {
    try {
      const comments = await this.service.getComments(projectId, ticketId)
      return comments.map(comment => ({
        id: comment.id,
        author: comment.author,
        author_role: comment.author_role,
        author_username: comment.author_username,
        content: comment.content,
        created_at: comment.created_at,
        updated_at: comment.updated_at
      }))
    } catch (e) {
      console.error('Failed to fetch comments:', e)
      throw new Error('Failed to fetch comments')
    }
  }

  async addComment(projectId: number, ticketId: number, content: string): Promise<any> {
    try {
      if (!content.trim()) {
        throw new Error('Comment cannot be empty')
      }
      const comment = await this.service.addComment(projectId, ticketId, content)
      return {
        ...comment,
        author_username: comment.author_username || '',
        author_role: comment.author_role || 'annotator'
      }
    } catch (e) {
      console.error('Failed to add comment:', e)
      throw e
    }
  }

  async updateRules(projectId: number, ticketId: number, ruleIds: number[]): Promise<void> {
    if (!ruleIds.length) {
      throw new Error('No rules selected')
    }
    await this.service.updateRules(projectId, ticketId, ruleIds)
  }

  async removeRules(projectId: number, ticketId: number, ruleIds: number[]): Promise<void> {
    if (!ruleIds.length) {
      throw new Error('No rules selected')
    }
    await this.service.removeRules(projectId, ticketId, ruleIds)
  }
}