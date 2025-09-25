import { TagItem } from '~/domain/models/tag/tag'

export const DocumentClassification = 'DocumentClassification'
export const SequenceLabeling = 'SequenceLabeling'
export const Seq2seq = 'Seq2seq'
export const IntentDetectionAndSlotFilling = 'IntentDetectionAndSlotFilling'
export const ImageClassification = 'ImageClassification'
export const ImageCaptioning = 'ImageCaptioning'
export const BoundingBox = 'BoundingBox'
export const Segmentation = 'Segmentation'
export const Speech2text = 'Speech2text'

export const allProjectTypes = <const>[
  DocumentClassification,
  SequenceLabeling,
  Seq2seq,
  IntentDetectionAndSlotFilling,
  ImageClassification,
  ImageCaptioning,
  BoundingBox,
  Segmentation,
  Speech2text
]
export type ProjectType = (typeof allProjectTypes)[number]
const MIN_LENGTH = 1
const MAX_PROJECT_NAME_LENGTH = 100

export const validateMinLength = (text: string): boolean => {
  return text.trim().length >= MIN_LENGTH
}

export const validateNameMaxLength = (name: string): boolean => {
  return name.trim().length <= MAX_PROJECT_NAME_LENGTH
}

export const canDefineCategory = (projectType: ProjectType): boolean => {
  return [
    DocumentClassification,
    IntentDetectionAndSlotFilling,
    ImageClassification,
    BoundingBox,
    Segmentation
  ].includes(projectType)
}

export const canDefineSpan = (projectType: ProjectType): boolean => {
  return [SequenceLabeling, IntentDetectionAndSlotFilling].includes(projectType)
}

export const canDefineLabel = (projectType: ProjectType): boolean => {
  return canDefineCategory(projectType) || canDefineSpan(projectType)
}

export const validateAgreementPercentage = (value: number): boolean => {
  return value >= 0.0 && value <= 100.0
}

export class Project {
  name: string
  description: string
  projectType: ProjectType
  constructor(
    readonly id: number,
    readonly _name: string,
    readonly _description: string,
    readonly guideline: string,
    readonly _projectType: string,
    readonly enableRandomOrder: boolean,
    readonly enableSharingMode: boolean,
    readonly exclusiveCategories: boolean,
    readonly allowOverlappingSpans: boolean,
    readonly enableGraphemeMode: boolean,
    readonly useRelation: boolean,
    readonly tags: TagItem[],
    readonly perspective: number,
    readonly allowMemberToCreateLabelType: boolean = false,
    readonly users: number[] = [],
    readonly createdAt: string = '',
    readonly updatedAt: string = '',
    readonly author: string = '',
    readonly isTextProject: boolean = false,
    readonly agreementPercentage: number = 50.0
  ) {
    if (!validateMinLength(_name)) {
      throw new Error('Project name is required')
    }
    if (!validateNameMaxLength(_name)) {
      throw new Error('Project name must be less than 100 characters')
    }
    if (!validateMinLength(_description)) {
      throw new Error('Project description is required')
    }
    if (!allProjectTypes.includes(_projectType as ProjectType)) {
      throw new Error(`Invalid project type: ${_projectType}`)
    }
    if (!validateAgreementPercentage(agreementPercentage)) {
      throw new Error('Agreement percentage must be between 0.0 and 100.0')
    }
    this.name = _name.trim()
    this.description = _description.trim()
    this.projectType = _projectType as ProjectType
  }

  static create(
    id: number,
    name: string,
    description: string,
    guideline: string,
    projectType: string,
    enableRandomOrder: boolean,
    enableSharingMode: boolean,
    exclusiveCategories: boolean,
    allowOverlappingSpans: boolean,
    enableGraphemeMode: boolean,
    useRelation: boolean,
    tags: TagItem[],
    perspective: number,
    allowMemberToCreateLabelType: boolean,
    agreementPercentage: number = 50.0,
    users: number[] = [],
    createdAt: string = '',
    updatedAt: string = '',
    author: string = '',
    isTextProject: boolean = false
  ) {
    return new Project(
      id,
      name,
      description,
      guideline,
      projectType,
      enableRandomOrder,
      enableSharingMode,
      exclusiveCategories,
      allowOverlappingSpans,
      enableGraphemeMode,
      useRelation,
      tags,
      perspective,
      allowMemberToCreateLabelType,
      users,
      createdAt,
      updatedAt,
      author,
      isTextProject,
      agreementPercentage
    )
  }

  get canDefineLabel(): boolean {
    return canDefineLabel(this.projectType)
  }

  get canDefineCategory(): boolean {
    return canDefineCategory(this.projectType)
  }

  get canDefineSpan(): boolean {
    return canDefineSpan(this.projectType)
  }

  get canDefineRelation(): boolean {
    return this.useRelation
  }

  get taskNames(): string[] {
    if (this.projectType === IntentDetectionAndSlotFilling) {
      return [DocumentClassification, SequenceLabeling]
    }
    return [this.projectType]
  }

  get resourceType(): string {
    if (this.projectType === DocumentClassification) {
      return 'TextClassificationProject'
    }
    return `${this.projectType}Project`
  }

  get isImageProject(): boolean {
    return [ImageClassification, ImageCaptioning, BoundingBox, Segmentation].includes(
      this.projectType
    )
  }

  get isAudioProject(): boolean {
    return [Speech2text].includes(this.projectType)
  }
}
