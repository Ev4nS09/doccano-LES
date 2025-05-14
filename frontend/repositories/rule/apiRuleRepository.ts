import { Rule } from '@/domain/models/rule/rule'
import { Comment } from '@/domain/models/rule/comment'
import ApiService from '@/services/api.service'

function toRuleModel(item: any): Rule {
  return Rule.create(
    item.id,
    item.project,
    item.created_by,
    item.title,
    item.description,
    item.upvotes || [],
    item.downvotes || [],
    item.created_at,
    item.updated_at,
    item.status,
  )
}

function toCommentModel(item: any): Comment {
  return new Comment(
    item.id,
    item.rule,
    item.author,
    item.content,
    item.created_at,
    item.updated_at
  )
}

export class APIRuleRepository {
  constructor(private readonly request = ApiService) {}

  async list(projectId: number): Promise<Rule[]> {
    const url = `/projects/${projectId}/rules`
    const response = await this.request.get(url)
    return response.data.results.map(toRuleModel)
  }

  async create(projectId: number, rule: Omit<Rule, "id" | "score">): Promise<Rule> {
	const url = `/projects/${projectId}/rules`
	const response = await this.request.post(url, {
	  title: rule.title,
	  description: rule.description,
	  project: rule.project
	})
	return toRuleModel(response.data)
  }

  async vote(projectId: number, ruleId: number, vote: number): Promise<void> {
    const url = `/projects/${projectId}/rules/${ruleId}/vote`
    await this.request.post(url, { vote })
  }

  async status(projectId: number, ruleId: number, status_value: number): Promise<void> {
    const url = `projects/${projectId}/rules/${ruleId}/update-status`
    await this.request.patch(url, { status_value })

  }

  async addComment(projectId: number, ruleId: number, content: string): Promise<Comment> {
    const url = `/projects/${projectId}/rules/${ruleId}/comments`
    const response = await this.request.post(url, { content })
    return toCommentModel(response.data)
  }

  async bulkDelete(projectId: number, ruleIds: number[]): Promise<void> {
    await this.request.delete(`/projects/${projectId}/rules`, { data: { ids: ruleIds } })
  }

  // Add this method to APIRuleRepository class
	async getComments(projectId: number, ruleId: number): Promise<Comment[]> {
		const url = `/projects/${projectId}/rules/${ruleId}/comments?limit=1000`
		const response = await this.request.get(url)
		return response.data.results.map(toCommentModel)
	}
}
