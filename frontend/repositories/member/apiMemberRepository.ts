import { MemberItem } from '@/domain/models/member/member'
import ApiService from '@/services/api.service'

function toModel(item: { [key: string]: any }): MemberItem {
  return new MemberItem(item.id, item.user, item.email, item.role, item.username, item.rolename)
}

function toPayload(item: MemberItem): { [key: string]: any } {
  return {
    id: item.id,
    user: item.user,
    role: item.role,
    username: item.username,
    rolename: item.rolename
  }
}

export class APIMemberRepository {
  constructor(private readonly request = ApiService) {}

  async list(projectId: string): Promise<MemberItem[]> {
    const url = `/projects/${projectId}/members`
    const response = await this.request.get(url)
    return response.data.map((item: { [key: string]: any }) => toModel(item))
  }

  async create(projectId: string, item: MemberItem): Promise<MemberItem> {
    const url = `/projects/${projectId}/members`
    const payload = toPayload(item)
    const response = await this.request.post(url, payload)
    return toModel(response.data)
  }

  async update(projectId: string, item: MemberItem): Promise<MemberItem> {
    const url = `/projects/${projectId}/members/${item.id}`
    const payload = toPayload(item)
    const response = await this.request.patch(url, payload)
    return toModel(response.data)
  }

  async bulkDelete(projectId: string, members: MemberItem[]): Promise<void> {
    const url = `/projects/${projectId}/members`
    const ids = members.map((member) => member.id)
    await this.request.delete(url, { ids })
  }

  async fetchMyRole(projectId: string): Promise<MemberItem> {
    const url = `/projects/${projectId}/my-role`
    const response = await this.request.get(url)
    return toModel(response.data)
  }

  async listExampleMembers(projectId: string, exampleId: string): Promise<any[]> {
    const url = `/projects/${projectId}/examples/${exampleId}/members?limit=1000`;
    const response = await this.request.get(url);
    return response.data.results.map((assignment: any) => ({
      id: assignment.id,
      assignee: assignment.assignee,
      example: assignment.example,
      assignee_username: assignment.assignee_username,
      created_at: assignment.created_at,
      updated_at: assignment.updated_at
    }));
  }

  async listProjectMembers(projectId: string): Promise<any[]> {
    const url = `/projects/${projectId}/members`
    const response = await this.request.get(url)
    return response.data // Assuming the response contains an array of members with roles
  }

  async fetchMembersWithLabels(projectId: string, exampleId: string): Promise<any[]> {
    const url = `/projects/${projectId}/examples/${exampleId}/members-with-labels`
    try {
      const response = await this.request.get(url)
      return response.data
    } catch (error) {
      console.error('Failed to fetch members with labels:', error)
      throw error
    }
  }
}
