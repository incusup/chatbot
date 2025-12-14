from flask import Flask, request, jsonify
from openai import OpenAI
import os


app = Flask(__name__)


# OpenAI 클라이언트 생성 (환경변수 OPENAI_API_KEY 필요)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


@app.route("/ask", methods=["POST"])
def ask_gpt():
  data = request.get_json()
  question = data.get("question")


  if not question:
    return jsonify({"error": "question is required"}), 400


  response = client.chat.completions.create(
  model="gpt-4.1-mini",
  messages=[
  {"role": "system", "content": "You are a helpful assistant."},
  {"role": "user", "content": question}
  ]
  )


  answer = response.choices[0].message.content


  return jsonify({"answer": answer})


@app.route("/")
def index():
  return '''
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<title>GPT 질문 페이지</title>
<style>
body { font-family: Arial, sans-serif; margin: 40px; }
textarea { width: 100%; height: 120px; }
button { padding: 10px 20px; margin-top: 10px; }
#answer { margin-top: 20px; white-space: pre-wrap; }
</style>
</head>
<body>
<h2>GPT에게 질문하기</h2>
<textarea id="question" placeholder="질문을 입력하세요"></textarea><br>
<button onclick="askGPT()">질문하기</button>


<div id="answer"></div>


<script>
async function askGPT() {
const question = document.getElementById('question').value;
document.getElementById('answer').innerText = '답변 생성 중...';


const response = await fetch('/ask', {
method: 'POST',
headers: { 'Content-Type': 'application/json' },
body: JSON.stringify({ question })
});


const data = await response.json();
document.getElementById('answer').innerText = data.answer || data.error;
}
</script>
</body>
</html>
'''


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000, debug=True)