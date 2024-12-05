#views.py
from flask import Blueprint, request, session, render_template, redirect, url_for, jsonify
from utils import process_chart

chart = Blueprint('chart', __name__)

@chart.route('/api/chart/<int:pol_id>',methods=['GET'])
def chart_view(pol_id):
    try:
        chart_path, error = process_chart(pol_id)
        # 생성된 차트 이미지 경로를 반환
        return jsonify({"chart_image_path": chart_path})
    
    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({"error": error}), 400    
