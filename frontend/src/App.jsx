import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [inputText, setInputText] = useState('');
  const [corrections, setCorrections] = useState([]);

  const checkSpelling = async () => {
    try {
      const res = await axios.post('http://localhost:8000/spellcheck', {
        message: inputText,
      });
      const json = JSON.parse(res.data);
      setCorrections(json.corrections);
    } catch (err) {
      alert("서버에서 오류가 발생했습니다.");
      console.error(err);
    }
  };

  const renderCorrectedText = () => {
    let result = [];
    let lastIndex = 0;

    corrections.forEach((corr, idx) => {
      result.push(<span key={`plain-${idx}`}>{inputText.slice(lastIndex, corr.start)}</span>);
      result.push(
        <span
          key={`error-${idx}`}
          className="underline"
          title={`수정 제안: ${corr.suggestion}`}
        >
          {inputText.slice(corr.start, corr.end)}
        </span>
      );
      lastIndex = corr.end;
    });

    result.push(<span key="last">{inputText.slice(lastIndex)}</span>);
    return result;
  };

  return (
    <div className="App">
      <h1>✏️ 맞춤법 검사기</h1>
      <textarea
        rows={4}
        cols={60}
        value={inputText}
        onChange={(e) => setInputText(e.target.value)}
        placeholder="문장을 입력하세요"
      />
      <br />
      <button onClick={checkSpelling}>검사하기</button>

      <div className="result">{renderCorrectedText()}</div>
    </div>
  );
}

export default App;
