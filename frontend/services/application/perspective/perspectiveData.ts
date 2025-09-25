// services/application/perspective/perspectiveData.ts
import { ExamplePerspectiveStats, Item, ItemValue, Value } from '~/domain/models/perspective/perspective'

// Data Transfer Objects
export class ItemDTO {
  constructor(
    public readonly id: number,
    public readonly project: number,
    public readonly name: string,
    public readonly predefined_values: ItemValueDTO[],
    public readonly created_at: string,
    public readonly updated_at: string
  ) {}

  static fromDomain(item: Item): ItemDTO {
    return new ItemDTO(
      item.id,
      item.project,
      item.name,
      item.predefined_values.map(ItemValueDTO.fromDomain),
      item.created_at,
      item.updated_at
    )
  }
}

export class ItemValueDTO {
  constructor(
    public readonly id: number,
    public readonly item: number,
    public readonly name: string,
    public readonly created_at: string
  ) {}

  static fromDomain(value: ItemValue): ItemValueDTO {
    return new ItemValueDTO(
      value.id,
      value.item,
      value.name,
      value.created_at
    )
  }
}

export class ValueDTO {
  constructor(
    public readonly id: number,
    public readonly example: number,
    public readonly user: number,
    public readonly item: number,
    public readonly item_value: number,
    public readonly created_at: string,
    public readonly item_name?: string,
    public readonly value_name?: string,
    public readonly user_name?: string
  ) {}

  static fromDomain(value: Value): ValueDTO {
    return new ValueDTO(
      value.id,
      value.example,
      value.user,
      value.item,
      value.item_value,
      value.created_at,
      value.item_name,
      value.value_name,
      value.user_name
    )
  }
}

export class ExamplePerspectiveStatsDTO {
	constructor(
	  public readonly example_id: number,
    public readonly annotators: number,
	  public readonly statistics: {
		[itemName: string]: {
		  [valueName: string]: number;
		};
	  }
	) {}
  
	static fromDomain(stats: ExamplePerspectiveStats): ExamplePerspectiveStatsDTO {
	  return new ExamplePerspectiveStatsDTO(
		stats.example_id,
    stats.annotators,
		stats.statistics
	  );
	}
  }
  

// Command Types
export type CreateItemCommand = {
  project: number
  name: string
}

export type UpdateItemCommand = {
  id: number
  project: number
  name: string
}

export type CreateValueCommand = {
  example: number
  user: number
  item: number
  item_value: number
}

export type UpdateValueCommand = {
  id: number
  example: number
  user: number
  item: number
  item_value: number
}