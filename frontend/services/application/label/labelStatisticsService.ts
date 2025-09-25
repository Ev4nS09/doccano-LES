
// labelStatisticsService.ts
import { AnnotationRepository } from '~/domain/models/annotation/annotationRepository'
import { ExampleDTO } from '~/domain/models/example/exampleData'
import { LabelDTO } from '~/domain/models/label/labelData'

export class LabelStatisticsService {
  constructor(private readonly annotationRepository: AnnotationRepository<any>) {}

  async getLabelCounts(projectId: string, exampleId: number): Promise<Record<number, number>> {
    const annotations = await this.annotationRepository.list(projectId, exampleId)
    const counts: Record<number, number> = {}

    annotations.forEach(annotation => {
      const labelId = annotation.label // Adjust based on your annotation model
      counts[labelId] = (counts[labelId] || 0) + 1
    })

    return counts
  }

  async processExamples(
    projectId: string,
    examples: ExampleDTO[],
    labels: LabelDTO[]
  ): Promise<any[]> {
    const processed = []

    for (const example of examples) {
      const labelCounts = await this.getLabelCounts(projectId, example.id)
      const exampleStats: any = {
        ...example,
        text: example.text
      }

      // Initialize all labels with count 0
      labels.forEach(label => {
        exampleStats[`label_${label.id}`] = 0
      })

      // Update with actual counts
      Object.entries(labelCounts).forEach(([labelId, count]) => {
        exampleStats[`label_${labelId}`] = count
      })

      processed.push(exampleStats)
    }

    return processed
  }
}
