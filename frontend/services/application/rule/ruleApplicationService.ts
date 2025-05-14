import { RuleDTO } from './ruleData'
import { RuleService } from './ruleService'

export class RuleApplicationService {
  constructor(private readonly service: RuleService) {}

  async list(projectId: number): Promise<RuleDTO[]> {
    try {
      return await this.service.list(projectId)
    } catch (e) {
      throw new Error('Failed to fetch rules')
    }
  }

  async create(projectId: number, title: string, description: string): Promise<RuleDTO> {
    if (!title.trim() || !description.trim()) {
      throw new Error('Title and description are required')
    }
    return await this.service.create(projectId, { title, description })
  }

  async vote(projectId: number, ruleId: number, vote: 1 | -1 | 0): Promise<void> {
    if (![-1, 0, 1].includes(vote)) {
      throw new Error('Invalid vote value')
    }
    await this.service.vote(projectId, ruleId, vote)
  }

  async status(projectId: number, ruleId: number, status_value: 1 | -1 | 0): Promise<void> {
    await this.service.status(projectId, ruleId, status_value)
  }

  async comment(projectId: number, ruleId: number, content: string): Promise<void> {
    if (!content.trim()) {
      throw new Error('Comment cannot be empty')
    }
    await this.service.addComment(projectId, ruleId, content)
  }

  async deleteRules(projectId: number, rules: RuleDTO[]): Promise<void> {
    if (!rules.length) {
      throw new Error('No rules selected')
    }
    await this.service.bulkDelete(projectId, rules)
  }

  async getWithComments(projectId: number, ruleId: number): Promise<RuleDTO> {
	try {
	  return await this.service.getWithComments(projectId, ruleId)
	} catch (e) {
	  throw new Error('Failed to fetch rule with comments')
	}
  }
}
