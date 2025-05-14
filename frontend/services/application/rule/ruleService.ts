import { APIRuleRepository } from '@/repositories/rule/apiRuleRepository'
import { Rule } from '@/domain/models/rule/rule'
import { Comment } from '@/domain/models/rule/comment'
import { RuleDTO } from '@/services/application/rule/ruleData'

export class RuleService {
  constructor(private readonly repository: APIRuleRepository) {}

  async list(projectId: number): Promise<RuleDTO[]> {
    const rules = await this.repository.list(projectId)
    return rules.map(rule => this.toDTO(rule))
  }

  async create(projectId: number, data: { title: string; description: string }): Promise<RuleDTO> {
    const rule = await this.repository.create(projectId, {
      project: projectId,
      created_by: 0, // Will be set by backend
      title: data.title,
      description: data.description,
      upvotes: [],
      downvotes: [],
      created_at: '',
      updated_at: '',
      status: 'On going'
    })
    return this.toDTO(rule)
  }

  async bulkDelete(projectId: number, rules: RuleDTO[]): Promise<void> {
    const ids = rules.map(rule => rule.id)
    await this.repository.bulkDelete(projectId, ids)
  }

  async vote(projectId: number, ruleId: number, vote: 1 | -1 | 0): Promise<void> {
    await this.repository.vote(projectId, ruleId, vote)
  }

  async status(projectId: number, ruleId: number, status_value: 1 | -1 | 0): Promise<void> {
    await this.repository.status(projectId, ruleId, status_value)
  }

  async addComment(projectId: number, ruleId: number, content: string): Promise<Comment> {
    return await this.repository.addComment(projectId, ruleId, content)
  }

  async getWithComments(projectId: number, ruleId: number): Promise<RuleDTO> {
	const [rule, comments] = await Promise.all([
	  this.repository.list(projectId).then(rules => 
		rules.find(r => r.id === ruleId) 
	  ),
	  this.repository.getComments(projectId, ruleId)
	]);

    if (!rule) {
    throw new Error(`Rule with ID ${ruleId} not found for project ${projectId}`);
     }

    console.error(comments.at(0)?.content)
	
	const dto = this.toDTO(rule);
	dto.comments = comments.map(comment => ({
	  id: comment.id,
	  author: comment.author,
	  author_username: '', // Will be populated by API
	  content: comment.content,
	  created_at: comment.created_at,
	  updated_at: comment.updated_at
	}));

	
	return dto;
  }

  private toDTO(rule: Rule): RuleDTO {
	return {
	  id: rule.id,
	  project: rule.project,
	  created_by: rule.created_by,
	  author_username: '', // Will be populated by API
	  title: rule.title,
	  description: rule.description,
	  upvotes: rule.upvotes,
	  downvotes: rule.downvotes,
	  score: rule.score ,
	  user_vote: 0, // Will be populated by API
	  comments: (rule as any).comments || [], // Preserve existing comments if present
	  created_at: rule.created_at,
	  updated_at: rule.updated_at,
      status: rule.status
	}
  }

  private toDomain(dto: RuleDTO): Rule {
    return Rule.create(
      dto.id,
      dto.project,
      dto.created_by,
      dto.title,
      dto.description,
      dto.upvotes,
      dto.downvotes,
      dto.created_at,
      dto.updated_at,
      dto.status,
    )
  }
}
