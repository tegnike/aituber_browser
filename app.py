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
table = dynamodb.Table('test2')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_data')
def get_data():
    # DynamoDBから最新のデータを取得します
    response = table.query(
        KeyConditionExpression=Key('username').eq('nikechan'),
        Limit=1,
        ScanIndexForward=False
)

    # データがある場合は最初の項目を返す、それ以外の場合はNoneを返す
    data = response['Items'][0] if response['Items'] else None
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
