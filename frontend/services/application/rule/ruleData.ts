export interface CommentDTO {
  id: number
  author: number
  author_username: string
  content: string
  created_at: string
  updated_at: string
}

export interface RuleDTO {
  id: number
  project: number
  created_by: number
  author_username: string
  title: string
  description: string
  upvotes: number[]
  downvotes: number[]
  score: number
  user_vote: number
  comments: CommentDTO[]
  created_at: string
  updated_at: string
  status: string
}
