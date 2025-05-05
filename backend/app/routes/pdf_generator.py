import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from prediction.pdf_match_report import MatchReportCreator
from flask import Blueprint, request, send_file

pdf_generator_bp = Blueprint('pdf_generator_bp', __name__)

@pdf_generator_bp.route('/createPDF', methods=['POST'])
def create_pdf():
    data = request.json
    if not data:
        return "No data provided", 400
    report = data['report']
    video_name = report['video_name']
    
    pdf_creator = MatchReportCreator(report)
    pdf_buf = pdf_creator.create_pdf()

    pdf_buf.seek(0)

    return send_file(
        pdf_buf,
        mimetype='application/pdf',
        as_attachment=True,
        download_name=f"{video_name}_match_report.pdf"
    )