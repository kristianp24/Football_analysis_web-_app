import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import numpy as np
import io


class MatchReportCreator:
    def __init__(self, report):
        self.report = report
    
    def _create_pie_chart_image(self, title, values, labels, colours):
        buffer = io.BytesIO()
        plt.figure(figsize=(6, 6))
        plt.pie(values, labels=labels, colors=colours, autopct='%1.1f%%', startangle=140)
        plt.title(f'{title} Pie Chart')
        plt.tight_layout()
        plt.savefig(buffer, format='png')
        plt.close()
        buffer.seek(0)
        return ImageReader(buffer)
    
    def _create_bar_chart_image(self, title, values, labels, colours):
        buffer = io.BytesIO()
        plt.figure(figsize=(10, 6))
        plt.bar(labels, values, color=colours)
        plt.title(f'{title} Bar Chart')
        plt.xlabel('Players')
        plt.ylabel('Values')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(buffer, format='png')
        plt.close()
        buffer.seek(0)
        return ImageReader(buffer)
    
    def _normalize_rgb(self, rgb):
        return [x / 255 for x in rgb]
    
    def create_pdf(self):
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4
        
        c.setFont("Helvetica-Bold", 24)
        c.drawString(100, height - 50, f"Match Report {self.report['video_name']}")
        
        c.setFont("Helvetica", 12)
        y = height - 100
       
        team_0_name = self.report['team_0']['name']
        team_1_name = self.report['team_1']['name']

        for i, team_key in enumerate(['team_0', 'team_1']):
            team = self.report[team_key]
            c.drawString(50, y, f"{team['name']}:")
            y -= 20
            for key, value in team.items():
                if key != 'colour' and key != 'name':
                    c.drawString(70, y, f"{key.replace('_', ' ').capitalize()}: {value}")
                    y -= 20
            y -= 10
        
        
        normalized_colour_0 = self._normalize_rgb(self.report['team_0']['colour'])
        normalized_colour_1 = self._normalize_rgb(self.report['team_1']['colour'])

        passes_pie = self._create_pie_chart_image(
                        'Passes',
                        [self.report['team_0']['number_of_passes'], self.report['team_1']['number_of_passes']],
                        [team_0_name, team_1_name],
                        [normalized_colour_0, normalized_colour_1]
                    )
        
        possession_pie = self._create_pie_chart_image(
                            'Ball Possession',
                            [self.report['team_0']['percentage_possesion'], self.report['team_1']['percentage_possesion']],
                            [team_0_name, team_1_name],
                            [normalized_colour_0, normalized_colour_1]
                        )
        
        km_runned_bar = self._create_bar_chart_image(
                        'Estimated Distance (km)',
                        [self.report['team_0']['km_runned'], self.report['team_1']['km_runned']],
                        [team_0_name, team_1_name],
                        [normalized_colour_0, normalized_colour_1]
                    )
        
        c.drawImage(passes_pie, 50, y - 200, width=240, height=180)
        c.drawImage(possession_pie, 300, y - 200, width=240, height=180)
        c.showPage()

        c.setFont("Helvetica-Bold", 18)
        c.drawImage(km_runned_bar, 50, y - 400, width=500, height=300)

        c.save()
        buffer.seek(0)
        return buffer


    