import streamlit as st
import streamlit.components.v1 as components

# 페이지 설정: 와이드 모드로 설정하여 프레젠테이션 느낌을 극대화합니다.
st.set_page_config(layout="wide", page_title="천문 데이터 시각화 시뮬레이터")

# 전체 HTML/JS 코드를 파이썬 문자열 변수에 담습니다.
# triple quotes (""")를 사용하여 SyntaxError를 방지합니다.
html_content = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Professional Astronomy Simulation</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Urbanist:wght@400;500;700&family=Noto+Sans+KR:wght@300;400;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    <script src="https://cdn.jsdelivr.net/npm/fitsjs@0.0.5/dist/fits.js"></script>
    <style>
        /* [1] CORE DESIGN SYSTEM */
        :root {
            --bg-color: #020617;
            --accent-cyan: #22d3ee;
            --accent-emerald: #10b981;
            --text-main: #f8fafc;
            --text-dim: #94a3b8;
            --slide-width: 1280px;
            --slide-height: 720px;
        }

        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { 
            background-color: #0f172a; 
            font-family: 'Urbanist', 'Noto Sans KR', sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 40px;
            padding: 40px 0;
        }

        /* [2] SLIDE CONTAINER */
        .slide-container {
            width: var(--slide-width);
            height: var(--slide-height);
            background-color: var(--bg-color);
            background-image: linear-gradient(rgba(2, 6, 23, 0.8), rgba(2, 6, 23, 0.8)), 
                              url('http://googleusercontent.com/image_collection/image_retrieval/7395207678265039631');
            background-size: cover;
            border-radius: 20px;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
            padding: 60px;
            position: relative;
            overflow: hidden;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }

        /* [3] TYPOGRAPHY */
        h1 { font-size: 80px; color: var(--text-main); font-weight: 700; line-height: 1.1; margin-bottom: 20px; }
        h1 span { color: var(--accent-cyan); }
        h2.slide-title { font-size: 32px; font-weight: 500; color: var(--accent-cyan); margin-bottom: 40px; text-transform: uppercase; letter-spacing: 2px; }
        p.subtitle { font-size: 20px; color: var(--text-dim); max-width: 800px; margin-bottom: 40px; }

        /* [4] LAYOUTS */
        .content-area { display: flex; gap: 40px; width: 100%; height: calc(100% - 100px); }
        .two-column { display: grid; grid-template-columns: 1fr 1fr; gap: 40px; width: 100%; }
        
        /* Simulation Visuals */
        .visual-card {
            background: rgba(15, 23, 42, 0.6);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 16px;
            padding: 24px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }

        canvas { max-width: 100%; border-radius: 8px; }

        /* [5] INPUTS & UI */
        .control-panel {
            display: flex;
            flex-direction: column;
            gap: 20px;
            color: var(--text-main);
        }
        input[type="range"] { width: 100%; accent-color: var(--accent-cyan); }
        .btn-upload {
            padding: 12px 24px;
            background: var(--accent-cyan);
            color: #000;
            border: none;
            border-radius: 8px;
            font-weight: 700;
            cursor: pointer;
            transition: transform 0.2s;
        }
        .btn-upload:hover { transform: scale(1.05); }

        /* Table Styling */
        table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        th { text-align: left; padding: 12px; color: var(--accent-emerald); border-bottom: 1px solid #334155; }
        td { padding: 12px; color: var(--text-main); border-bottom: 1px solid #1e293b; font-family: monospace; }
    </style>
</head>
<body>

<div class="slide-container" id="slide1">
    <div style="margin-top: 80px;">
        <h2 class="slide-title">Interactive Astronomy Lab</h2>
        <h1>내행성의 <span>공전 운동</span> 및<br>FITS 데이터 분석 플랫폼</h1>
        <p class="subtitle">지구과학 II 교과 과정의 행성 겉보기 운동 시뮬레이션과 실제 천문 이미지 분석을 통합한 전문 시각화 솔루션입니다.</p>
    </div>
</div>

<div class="slide-container" id="slide2">
    <h2 class="slide-title">I. 내행성 위치 및 위상 변화</h2>
    <div class="content-area">
        <div class="visual-card" style="flex: 2;">
            <canvas id="orbitCanvas" width="500" height="400"></canvas>
            <div style="margin-top: 20px; width: 80%;" class="control-panel">
                <input type="range" id="angleSlider" min="0" max="360" value="45">
                <div style="display: flex; justify-content: space-between; font-size: 14px;">
                    <span>내행성 공전 각도</span>
                    <span id="angleText" style="color: var(--accent-cyan)">45°</span>
                </div>
            </div>
        </div>
        <div class="visual-card" style="flex: 1;">
            <h3 style="color: var(--text-main); margin-bottom: 15px;">망원경 관측 위상</h3>
            <canvas id="phaseCanvas" width="200" height="200"></canvas>
            <div id="statusLabel" style="margin-top: 20px; font-weight: 700; color: var(--accent-emerald);">동방이각 부근</div>
            <p id="distInfo" style="font-size: 14px; color: var(--text-dim); margin-top: 5px;">시직경: 상대적 크기 1.2x</p>
        </div>
    </div>
</div>

<div class="slide-container" id="slide3">
    <h2 class="slide-title">II. FITS 데이터 정밀 시각화</h2>
    <div class="content-area">
        <div class="control-panel" style="flex: 1;">
            <div style="border: 2px dashed rgba(34, 211, 238, 0.3); padding: 40px; border-radius: 16px; text-align: center;">
                <i class="fa-solid fa-cloud-arrow-up" style="font-size: 40px; color: var(--accent-cyan); margin-bottom: 15px;"></i>
                <p style="color: var(--text-main); margin-bottom: 15px;">FITS 파일을 업로드하세요</p>
                <input type="file" id="fitsInput" accept=".fits,.fit" class="btn-upload">
            </div>
            <table>
                <tr><th>항목</th><th>분석 결과</th></tr>
                <tr><td>이미지 크기</td><td id="metaSize">-</td></tr>
                <tr><td>노출 시간</td><td id="metaExp">-</td></tr>
                <tr><td>평균 밝기</td><td id="metaBright">-</td></tr>
            </table>
            <button onclick="generateSample()" style="margin-top: 20px; background: transparent; border: 1px solid var(--accent-cyan); color: var(--accent-cyan); padding: 10px; border-radius: 8px; cursor: pointer;">샘플 데이터 생성</button>
        </div>
        <div class="visual-card" style="flex: 1.5; background: #000;">
            <canvas id="fitsCanvas" style="max-height: 450px;"></canvas>
            <p style="color: var(--text-dim); font-size: 12px; margin-top: 10px;">CCD RAW 시각화 엔진 v2.0</p>
        </div>
    </div>
</div>

<div class="slide-container" id="slide4">
    <h2 class="slide-title">Appendix. 물리량 산출 공식</h2>
    <div class="content-area">
        <div class="two-column">
            <div class="visual-card">
                <h3 style="color: var(--accent-cyan); margin-bottom: 20px;">회합 주기 공식</h3>
                <div id="formula-container" style="font-size: 24px; color: #fff;">
                    <math xmlns="http://www.w3.org/1998/Math/MathML" display="block">
                      <mfrac>
                        <mn>1</mn>
                        <mi>S</mi>
                      </mfrac>
                      <mo>=</mo>
                      <mfrac>
                        <mn>1</mn>
                        <mi>P</mi>
                      </mfrac>
                      <mo>&#x2212;</mo>
                      <mfrac>
                        <mn>1</mn>
                        <mi>E</mi>
                      </mfrac>
                    </math>
                </div>
                <p style="color: var(--text-dim); font-size: 14px; margin-top: 20px;">
                    S: 회합 주기, P: 행성의 공전 주기, E: 지구의 공전 주기
                </p>
            </div>
            <div class="visual-card">
                <h3 style="color: var(--accent-cyan); margin-bottom: 20px;">시직경 및 밝기 분석</h3>
                <div id="formula-container" style="font-size: 24px; color: #fff;">
                    <math xmlns="http://www.w3.org/1998/Math/MathML" display="block">
                      <mi>&#x03B4;</mi>
                      <mo>=</mo>
                      <mn>2</mn>
                      <mi>arctan</mi>
                      <mfenced>
                        <mfrac>
                          <mi>d</mi>
                          <mrow>
                            <mn>2</mn>
                            <mi>D</mi>
                          </mrow>
                        </mfrac>
                      </mfenced>
                    </math>
                </div>
                <p style="color: var(--text-dim); font-size: 14px; margin-top: 20px;">
                    D: 행성까지의 거리, d: 행성의 실제 지름
                </p>
            </div>
        </div>
    </div>
</div>

<script>
    /* [1] PLANETARY SIMULATION LOGIC */
    const orbitCanvas = document.getElementById('orbitCanvas');
    const oCtx = orbitCanvas.getContext('2d');
    const phaseCanvas = document.getElementById('phaseCanvas');
    const pCtx = phaseCanvas.getContext('2d');
    const slider = document.getElementById('angleSlider');

    function drawSim() {
        const angle = slider.value;
        document.getElementById('angleText').innerText = angle + "°";
        
        // Orbit Canvas
        oCtx.clearRect(0,0,500,400);
        const cx = 250, cy = 200;
        
        // Orbits
        oCtx.strokeStyle = 'rgba(148, 163, 184, 0.3)';
        oCtx.beginPath(); oCtx.arc(cx, cy, 80, 0, Math.PI*2); oCtx.stroke();
        oCtx.beginPath(); oCtx.arc(cx, cy, 140, 0, Math.PI*2); oCtx.stroke();
        
        // Sun
        oCtx.fillStyle = '#f59e0b';
        oCtx.shadowBlur = 20; oCtx.shadowColor = '#f59e0b';
        oCtx.beginPath(); oCtx.arc(cx, cy, 15, 0, Math.PI*2); oCtx.fill();
        oCtx.shadowBlur = 0;
        
        // Earth (Fixed at 6 o'clock for simplicity)
        const ex = cx, ey = cy + 140;
        oCtx.fillStyle = '#3b82f6';
        oCtx.beginPath(); oCtx.arc(ex, ey, 8, 0, Math.PI*2); oCtx.fill();
        
        // Planet
        const rad = (angle - 90) * Math.PI / 180;
        const px = cx + 80 * Math.cos(rad);
        const py = cy + 80 * Math.sin(rad);
        oCtx.fillStyle = '#e2e8f0';
        oCtx.beginPath(); oCtx.arc(px, py, 6, 0, Math.PI*2); oCtx.fill();

        // Guide line
        oCtx.setLineDash([5, 5]);
        oCtx.strokeStyle = 'rgba(34, 211, 238, 0.5)';
        oCtx.beginPath(); oCtx.moveTo(ex, ey); oCtx.lineTo(px, py); oCtx.stroke();
        oCtx.setLineDash([]);

        // Phase Calc
        const normAngle = angle % 360;
        updatePhase(normAngle, Math.sqrt((ex-px)**2 + (ey-py)**2));
    }

    function updatePhase(angle, dist) {
        const cx = 100, cy = 100;
        const baseR = 25;
        const scale = 220 / dist; // Simple scale
        const r = baseR * scale;
        
        pCtx.clearRect(0,0,200,200);
        pCtx.fillStyle = '#1e293b';
        pCtx.beginPath(); pCtx.arc(cx, cy, r, 0, Math.PI*2); pCtx.fill();
        
        // Light part
        pCtx.fillStyle = '#f8fafc';
        pCtx.save();
        pCtx.beginPath();
        if(angle < 180) { // Eastern
            pCtx.arc(cx, cy, r, -Math.PI/2, Math.PI/2);
            document.getElementById('statusLabel').innerText = "동방이각 부근 (상현/그믐)";
        } else { // Western
            pCtx.arc(cx, cy, r, Math.PI/2, -Math.PI/2);
            document.getElementById('statusLabel').innerText = "서방이각 부근 (하현/초승)";
        }
        const midW = r * Math.cos(angle * Math.PI / 180);
        pCtx.ellipse(cx, cy, Math.abs(midW), r, 0, Math.PI/2, -Math.PI/2, (angle > 90 && angle < 270));
        pCtx.fill();
        pCtx.restore();
        
        document.getElementById('distInfo').innerText = "시직경 상대 배율: " + scale.toFixed(2) + "x";
    }

    slider.oninput = drawSim;
    drawSim();

    /* [2] FITS ANALYZER LOGIC */
    const fitsInput = document.getElementById('fitsInput');
    const fCanvas = document.getElementById('fitsCanvas');
    const fCtx = fCanvas.getContext('2d');

    fitsInput.onchange = function(e) {
        const file = e.target.files[0];
        const reader = new FileReader();
        reader.onload = function() {
            const fits = new astro.FITS(this.result);
            const header = fits.getHDU().header;
            const dataUnit = fits.getHDU().data;
            
            document.getElementById('metaSize').innerText = header.get('NAXIS1') + " x " + header.get('NAXIS2');
            document.getElementById('metaExp').innerText = (header.get('EXPTIME') || 0) + " s";
            
            dataUnit.getFrame(0, (pixels) => {
                renderFits(pixels, header.get('NAXIS1'), header.get('NAXIS2'));
            });
        };
        reader.readAsArrayBuffer(file);
    };

    function renderFits(pixels, w, h) {
        fCanvas.width = w; fCanvas.height = h;
        const imgData = fCtx.createImageData(w, h);
        let max = 0, sum = 0;
        for(let p of pixels) { if(p > max) max = p; sum += p; }
        document.getElementById('metaBright').innerText = Math.round(sum/pixels.length) + " ADU";

        for(let i=0; i<pixels.length; i++) {
            const v = (pixels[i] / max) * 255;
            imgData.data[i*4] = imgData.data[i*4+1] = imgData.data[i*4+2] = v;
            imgData.data[i*4+3] = 255;
        }
        fCtx.putImageData(imgData, 0, 0);
    }

    function generateSample() {
        const w=300, h=300;
        const pix = new Float32Array(w*h);
        for(let i=0; i<w*h; i++) {
            const dx = (i%w) - 150, dy = Math.floor(i/w) - 150;
            pix[i] = Math.exp(-(dx*dx + dy*dy)/1000) * 1000 + Math.random()*100;
        }
        document.getElementById('metaSize').innerText = "300 x 300";
        document.getElementById('metaExp').innerText = "30.0 s";
        renderFits(pix, w, h);
    }
</script>

</body>
</html>
"""

# Streamlit 화면에 HTML 컴포넌트를 렌더링합니다.
# width를 100%로 하고, height는 슬라이드 높이에 맞춰 조절합니다.
components.html(html_content, height=800, scrolling=True)


