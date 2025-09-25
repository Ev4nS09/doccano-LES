import abc

import pandas as pd

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import HorizontalBarChart


class Writer(abc.ABC):
    extension = ""

    @staticmethod
    @abc.abstractmethod
    def write(file, dataset: pd.DataFrame):
        raise NotImplementedError("Please implement this method in the subclass.")


class CsvWriter(Writer):
    extension = "csv"

    @staticmethod
    def write(file, dataset: pd.DataFrame):
        dataset.to_csv(file, index=False, encoding="utf-8")


class JsonWriter(Writer):
    extension = "json"

    @staticmethod
    def write(file, dataset: pd.DataFrame):
        dataset.to_json(file, orient="records", force_ascii=False)


class JsonlWriter(Writer):
    extension = "jsonl"

    @staticmethod
    def write(file, dataset: pd.DataFrame):
        dataset.to_json(file, orient="records", force_ascii=False, lines=True)


class FastTextWriter(Writer):
    extension = "txt"

    @staticmethod
    def write(file, dataset: pd.DataFrame):
        dataset.to_csv(file, index=False, encoding="utf-8", header=False)

class PdfWriter(Writer):
    extension = "pdf"

    @staticmethod
    def write(file_obj, data):
        try:
            # Define our alternating colors
            COLOR_A = colors.HexColor('#3498db')
            COLOR_B = colors.HexColor('#2ecc71')
            COLOR_C = colors.HexColor('#e74c3c')  # New color for perspective filters
            
            # Create document with margins
            doc = SimpleDocTemplate(file_obj, pagesize=letter,
                                 leftMargin=0.5*inch,
                                 rightMargin=0.5*inch,
                                 topMargin=0.5*inch,
                                 bottomMargin=0.5*inch)
            styles = getSampleStyleSheet()
            story = []
            
            # Title and project info
            story.append(Paragraph("Project Statistics Report", styles['Title']))
            story.append(Spacer(1, 12))
            
            if 'projectId' in data:
                story.append(Paragraph(f"Project ID: {data['projectId']}", styles['Normal']))
                story.append(Spacer(1, 12))
            
            # Basic counts section
            if 'generalStats' in data:
                gs = data['generalStats']
                
                # Basic counts table
                count_data = [
                    ["Total Examples", str(gs.get('totalExamples', 0))],
                    ["Annotated Examples", str(gs.get('annotatedExamples', 0))]
                ]
                
                count_table = Table(count_data, colWidths=[2*inch, 1*inch])
                count_table.setStyle(TableStyle([
                    ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8f9fa')),
                    ('GRID', (0,0), (-1,-1), 1, colors.HexColor('#dee2e6')),
                    ('FONTNAME', (0,0), (-1,-1), 'Helvetica-Bold'),
                    ('FONTSIZE', (0,0), (-1,-1), 10),
                    ('ALIGN', (0,0), (-1,-1), 'LEFT')
                ]))
                story.append(count_table)
                story.append(Spacer(1, 24))
                
                # Participation rates chart
                if 'participationRate' in gs and 'fullParticipationRate' in gs:
                    story.append(Paragraph("Participation Rates", styles['Heading2']))
                    story.append(Spacer(1, 12))
                    
                    # Create participation chart
                    drawing = Drawing(400, 200)
                    bc = HorizontalBarChart()
                    bc.x = 100
                    bc.y = 50
                    bc.height = 120
                    bc.width = 300
                    bc.data = [
                        [gs.get('participationRate', 0), 
                         gs.get('fullParticipationRate', 0)]
                    ]
                    bc.valueAxis.valueMin = 0
                    bc.valueAxis.valueMax = 100
                    bc.valueAxis.valueStep = 20
                    bc.categoryAxis.categoryNames = [
                        f"Participation Rate ({gs.get('participationRate', 0)}%)",
                        f"Full Participation ({gs.get('fullParticipationRate', 0)}%)"
                    ]
                    
                    # Style the bars
                    bc.bars[0].fillColor = COLOR_A  # First bar uses Color A
                    bc.bars[1].fillColor = COLOR_B  # Second bar uses Color B
                    
                    # Add chart to drawing
                    drawing.add(bc)
                    story.append(drawing)
                    story.append(Spacer(1, 24))
            
            # Perspective Filters section (NEW SECTION)
            if 'perspectiveStats' in data and data['perspectiveStats']:
                ps = data['perspectiveStats']
                
                if 'perspectiveFilters' in ps and ps['perspectiveFilters']:
                    story.append(Paragraph("Perspective Filters", styles['Heading2']))
                    story.append(Spacer(1, 12))
                    
                    # Create table for perspective filters
                    filter_data = [["Perspective", "Type", "Value"]]
                    
                    for filter_item in ps['perspectiveFilters']:
                        value = ""
                        if isinstance(filter_item['value'], dict):
                            # Handle numeric ranges
                            min_val = filter_item['value'].get('min', '')
                            max_val = filter_item['value'].get('max', '')
                            if min_val is not None and max_val is not None:
                                value = f"{min_val} - {max_val}"
                            elif min_val is not None:
                                value = f"≥ {min_val}"
                            elif max_val is not None:
                                value = f"≤ {max_val}"
                        else:
                            # Handle other types (string, boolean, list)
                            value = str(filter_item['value'])
                        
                        filter_data.append([
                            filter_item['perspective'],
                            filter_item['type'],
                            value
                        ])
                    
                    filter_table = Table(filter_data, colWidths=[2*inch, 1.5*inch, 2*inch])
                    filter_table.setStyle(TableStyle([
                        ('BACKGROUND', (0,0), (-1,0), COLOR_C),
                        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
                        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
                        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                        ('FONTSIZE', (0,0), (-1,0), 10),
                        ('BOTTOMPADDING', (0,0), (-1,0), 12),
                        ('BACKGROUND', (0,1), (-1,-1), colors.HexColor('#f8f9fa')),
                        ('GRID', (0,0), (-1,-1), 1, colors.HexColor('#dee2e6')),
                        ('FONTSIZE', (0,1), (-1,-1), 9),
                    ]))
                    story.append(filter_table)
                    story.append(Spacer(1, 24))
            
            if 'perspectiveStats' in data and data['perspectiveStats']:
                ps = data['perspectiveStats']
                
                if 'labelDistribution' in ps and ps['labelDistribution']:
                    story.append(Paragraph("Label Statistics", styles['Heading2']))
                    story.append(Spacer(1, 12))
                    
                    # Track example index for color alternation
                    example_index = 0
                    
                    for example_name, label_stats in ps['labelDistribution'].items():
                        # Example header
                        story.append(Paragraph(example_name, styles['Heading3']))
                        story.append(Spacer(1, 6))
                        
                        # Create bar chart for visualization
                        if len(label_stats) > 0:
                            # Sort labels to maintain consistent order
                            sorted_labels = sorted(label_stats.items(), key=lambda x: x[0])

                            chart_data = []
                            category_names = []
                            
                            for label_name, percentage in sorted_labels:
                                chart_data.append(percentage)
                                category_names.append(label_name)
                            
                            num_bars = len(chart_data)
                            bar_padding = 4
                            bar_height = 15
                            chart_height = max(50, (bar_height + bar_padding) * num_bars)

                            drawing = Drawing(450, chart_height + 100)
                            bc = HorizontalBarChart()
                            bc.x = 100
                            bc.y = 20
                            bc.width = 300
                            bc.height = chart_height
                            bc.barWidth = bar_height

                            bc.data = [chart_data]
                            bc.categoryAxis.categoryNames = category_names
                            bc.valueAxis.valueMin = 0
                            bc.valueAxis.valueMax = 100
                            bc.valueAxis.valueStep = 20

                            # Determine color for this example (alternating)
                            example_color = COLOR_A if example_index % 2 == 0 else COLOR_B
                            
                            # Apply same color to all bars in this example
                            for i in range(len(chart_data)):
                                bc.bars[i].fillColor = example_color

                            drawing.add(bc)
                            story.append(drawing)
                            story.append(Spacer(1, 24))
                            
                            # Increment example index for next iteration
                            example_index += 1

            doc.build(story)
            file_obj.flush()
            return True
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            return False
