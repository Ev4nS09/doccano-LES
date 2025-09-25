import { Rule } from '@/domain/models/rule/rule'
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
    item.start_at,
    item.end_at,
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
	 project: rule.project,
    status: rule.status,
	 start_at: rule.start_at,
	 end_at: rule.end_at
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

  async bulkDelete(projectId: number, ruleIds: number[]): Promise<void> {
    await Promise.all(
      ruleIds.map(ruleId =>
        this.request.delete(`/projects/${projectId}/rules/${ruleId}`)
      )
    )
  }
}