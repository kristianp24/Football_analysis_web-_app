from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import matplotlib.pyplot as plt
import io

class MatchReportCreator:
    def __init__(self, report):
        self.report = report

    def _create_pie_chart_image(self, title, values, labels, colours):
        buffer = io.BytesIO()
        plt.figure(figsize=(6, 6))
        plt.pie(values, labels=labels, colors=colours, autopct='%1.1f%%', startangle=140)
        plt.title(title)
        plt.tight_layout()
        plt.savefig(buffer, format='png')
        plt.close()
        buffer.seek(0)
        return ImageReader(buffer)

    def _create_bar_chart_image(self, title, values, labels, colours):
        buffer = io.BytesIO()
        plt.figure(figsize=(10, 6))
        plt.bar(labels, values, color=colours)
        plt.title(title)
        plt.xlabel('Teams')
        plt.ylabel('Distance (km)')
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

        c.setFont("Helvetica-Bold", 26)
        c.drawCentredString(width / 2, height - 50, f"Match Report: {self.report['video_name']}")

        team_0 = self.report['team_0']
        team_1 = self.report['team_1']
        team_0_name = team_0['name']
        team_1_name = team_1['name']

        c.setFont("Helvetica-Bold", 16)
        c.drawString(60, height - 100, team_0_name)
        c.drawString(width / 2 + 20, height - 100, team_1_name)

        y_0 = height - 130
        y_1 = height - 130
        c.setFont("Helvetica", 12)
        for key in team_0:
            if key not in ['colour', 'name']:
                c.drawString(60, y_0, f"{key.replace('_', ' ').capitalize()}: {team_0[key]}")
                y_0 -= 18
        for key in team_1:
            if key not in ['colour', 'name']:
                c.drawString(width / 2 + 20, y_1, f"{key.replace('_', ' ').capitalize()}: {team_1[key]}")
                y_1 -= 18
        
        color_0 = self._normalize_rgb(team_0['colour'])
        color_1 = self._normalize_rgb(team_1['colour'])

        passes_pie = self._create_pie_chart_image(
            'Passes',
            [team_0['number_of_passes'], team_1['number_of_passes']],
            [team_0_name, team_1_name],
            [color_0, color_1]
        )

        possession_pie = self._create_pie_chart_image(
            'Ball Possession',
            [team_0['percentage_possesion'], team_1['percentage_possesion']],
            [team_0_name, team_1_name],
            [color_0, color_1]
        )

        km_runned_bar = self._create_bar_chart_image(
            'Estimated Distance Run (km)',
            [team_0['km_runned'], team_1['km_runned']],
            [team_0_name, team_1_name],
            [color_0, color_1]
        )

        c.drawImage(passes_pie, 50, y_0 - 220, width=240, height=180)
        c.drawImage(possession_pie, 300, y_0 - 220, width=240, height=180)

        c.showPage()
        c.setFont("Helvetica-Bold", 20)
        c.drawCentredString(width / 2, height - 50, "Distance Analysis")
        c.drawImage(km_runned_bar, 50, height - 400, width=500, height=300)

        c.save()
        buffer.seek(0)
        return buffer
