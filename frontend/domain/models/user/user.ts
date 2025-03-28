export class UserItem {
  constructor(
    readonly id: number,
    readonly username: string,
    readonly first_name: string,
    readonly last_name: string,
    readonly isSuperuser: boolean,
    readonly isStaff: boolean,
    readonly email: string = '',
  ) {}
}
