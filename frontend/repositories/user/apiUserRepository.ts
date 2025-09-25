import { UserItem } from '@/domain/models/user/user'
import ApiService from '@/services/api.service'

function toModel(item: { [key: string]: any }): UserItem {
  return new UserItem(item.id, item.username, item.email, 
    item.first_name, item.last_name, item.is_superuser, item.is_staff)
}

export class APIUserRepository {
  constructor(private readonly request = ApiService) {}

  async getProfile(): Promise<UserItem> {
    const url = '/me'
    const response = await this.request.get(url)
    return toModel(response.data)
  }

  async list(query: string): Promise<UserItem[]> {
    const url = `/users?q=${query}`
    const response = await this.request.get(url)
    return response.data.map((item: { [key: string]: any }) => toModel(item))
  }

  async updateUsername(newUsername: string): Promise<void> {
    const url = '/me/update-username/'
    await this.request.put(url, { username: newUsername })
  }

  async updatePassword(oldPassword: string, newPassword: string): Promise<void> {
    const url = '/me/update-password/'
    try {
      const response = await this.request.put(url, { oldPassword, newPassword })
      return response.data
    } catch (error) {
      throw new Error('Failed to update password')
    }
  }

  async updateEmail(newEmail: string): Promise<void> {
    const url = '/me/update-email/'
    await this.request.put(url, { email: newEmail })
  }

  async updateFirstName(newFirstName: string): Promise<void> {
    const url = '/me/update-first-name/'
    await this.request.put(url, { first_name: newFirstName })
}

async updateLastName(newLastName: string): Promise<void> {
    const url = '/me/update-last-name/'
    await this.request.put(url, { last_name: newLastName })
}
}
