import { APITicketRepository } from '@/repositories/tickets/apiTicketRepository'
import { Ticket } from '@/domain/models/tickets/ticket'
import { TicketComment } from '@/domain/models/tickets/comment'
import { TicketDTO } from '@/services/application/tickets/ticketData'

export class TicketService {
  constructor(private readonly repository: APITicketRepository) {}

  async list(projectId: number): Promise<TicketDTO[]> {
    const tickets = await this.repository.list(projectId)
    return tickets.map(ticket => this.toDTO(ticket))
  }

  async create(projectId: number, 
    data: { title: string; description: string; status?: string, 
      created_by: number, author_username: string }): 
    Promise<TicketDTO> {
    console.log('Data ticket:', data)
    const ticket = await this.repository.create(projectId, {
      project: projectId,
      created_by: data.created_by,
      title: data.title,
      description: data.description,
      status: data.status || 'open',
      author_username: data.author_username,
      rules: []
    })
    console.log('Created ticket:', ticket)
    return this.toDTO(ticket)
  }

  async update(projectId: number, ticketId: number, data: Partial<TicketDTO>): Promise<TicketDTO> {
    const ticket = await this.repository.update(projectId, ticketId, data)
    return this.toDTO(ticket)
  }

  async delete(projectId: number, ticketId: number): Promise<void> {
    await this.repository.delete(projectId, ticketId)
  }

  async deleteTickets(projectId: number, tickets: TicketDTO[]): Promise<void> {
    const ticketIds = tickets.map(ticket => ticket.id)
    await Promise.all(
      ticketIds.map(id => this.repository.delete(projectId, id)))
  }

  async addComment(projectId: number, ticketId: number, content: string): Promise<TicketComment> {
    const comment = await this.repository.addComment(projectId, ticketId, content)
    return comment
  }

  async getComments(projectId: number, ticketId: number): Promise<TicketDTO['comments']> {
    const comments = await this.repository.getComments(projectId, ticketId)
    return comments.map(comment => ({
      id: comment.id,
      author: comment.author,
      author_role: comment.author_role,
      author_username: comment.author_username,
      content: comment.content,
      created_at: comment.created_at,
      updated_at: comment.updated_at
    }))
  }

  async updateRules(projectId: number, ticketId: number, ruleIds: number[]): Promise<void> {
    await this.repository.updateRules(projectId, ticketId, ruleIds)
  }

  async removeRules(projectId: number, ticketId: number, ruleIds: number[]): Promise<void> {
    await this.repository.removeRules(projectId, ticketId, ruleIds)
  }

  private toDTO(ticket: Ticket): TicketDTO {
    return {
      id: ticket.id,
      project: ticket.project,
      created_by: ticket.created_by,
      author_username: ticket.author_username || '',
      title: ticket.title,
      description: ticket.description,
      status: ticket.status,
      rules: ticket.rules || [],
      rule_count: ticket.rules?.length || 0,
      comments: (ticket as any).comments || [],
      created_at: ticket.created_at,
      updated_at: ticket.updated_at
    }
  }

  private toDomain(dto: TicketDTO): Ticket {
    return Ticket.create(
      dto.id,
      dto.project,
      dto.created_by,
      dto.title,
      dto.description,
      dto.status,
      dto.author_username,
      dto.rules,
      dto.created_at,
      dto.updated_at
    )
  }
}