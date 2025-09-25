export class UserItem {
  constructor(
    readonly id: number,
    readonly username: string,
    readonly email: string,
    readonly firstName: string,
    readonly lastName: string,
    readonly isSuperuser: boolean,
    readonly isStaff: boolean
  ) {}
}
