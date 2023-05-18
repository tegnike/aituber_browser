from dotenv import load_dotenv
load_dotenv()
from flask import Flask, render_template, jsonify
import boto3
from boto3.dynamodb.conditions import Key
import os

app = Flask(__name__)

# AWSの認証情報を設定します。通常は環境変数を使用します。
boto3.setup_default_session(region_name=os.getenv('AWS_REGION_NAME'),
                            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('test20')

@app.route('/')
def home():
    return render_template('index.html')

from datetime import datetime

@app.route('/get_data')
def get_data():
    # nikechanの最新のデータを取得します
    response_nikechan = table.query(
        KeyConditionExpression=Key('username').eq('nikechan'),
        Limit=1,
        ScanIndexForward=False
    )
    data_nikechan = response_nikechan['Items'][0] if response_nikechan['Items'] else None
    timestamp_nikechan = datetime.strptime(data_nikechan['timestamp'], "%Y%m%d%H%M%S") if data_nikechan else None

    # testの最新のデータを取得します
    response_test = table.query(
        KeyConditionExpression=Key('username').eq('test'),
        Limit=1,
        ScanIndexForward=False
    )
    data_test = response_test['Items'][0] if response_test['Items'] else None
    timestamp_test = datetime.strptime(data_test['timestamp'], "%Y%m%d%H%M%S") if data_test else None

    # 両者のtimestampを比較し、最新のデータを返す
    if timestamp_nikechan and timestamp_test:
        if timestamp_nikechan > timestamp_test:
            return jsonify(data_nikechan)
        else:
            return jsonify(data_test)
    elif timestamp_nikechan:
        return jsonify(data_nikechan)
    elif timestamp_test:
        return jsonify(data_test)
    else:
        return jsonify({})

if __name__ == '__main__':
    app.run(debug=True)
