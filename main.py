import streamlit as st
import streamlit.components.v1 as components

# 페이지 설정: 와이드 모드
st.set_page_config(layout="wide", page_title="천문 데이터 시각화 시뮬레이터")

# 전체 HTML/JS 코드를 파이썬 문자열 변수에 담습니다.
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
        /* CORE DESIGN SYSTEM */
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

        /* SLIDE CONTAINER */
        .slide-container {
            width: var(--slide-width);
            height: var(--slide-height);
            background-color: var(--bg-color);
            background-image: linear-gradient(rgba(2, 6, 23, 0.85), rgba(2, 6, 23, 0.85)), 
                              url('http://googleusercontent.com/image_collection/image_retrieval/7395207678265039631');
            background-size: cover;
            border-radius: 20px;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
            padding: 60px;
            position: relative;
            overflow: hidden;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }

        /* TYPOGRAPHY */
        h1 { font-size: 80px; color: var(--text-main); font-weight: 700; line-height: 1.1; margin-bottom: 20px; }
        h1 span { color: var(--accent-cyan); }
        h2.slide-title { font-size: 32px; font-weight: 500; color: var(--accent-cyan); margin-bottom: 40px; text-transform: uppercase; letter-spacing: 2px; }
        p.subtitle { font-size: 20px; color: var(--text-dim); max-width: 800px; margin-bottom: 40px; }

        /* LAYOUTS */
        .content-area { display: flex; gap: 40px; width: 100%; height: calc(100% - 100px); }
        
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

        /* INPUTS & UI */
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
        
        .status-msg { color: var(--text-dim); font-size: 14px; margin-top: 10px; }
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
        <div class="visual-card" style="flex: 1.8;">
            <canvas id="orbitCanvas" width="500" height="400"></canvas>
            <div style="margin-top: 20px; width: 80%;" class="control-panel">
                <input type="range" id="angleSlider" min="0" max="360" value="45">
                <div style="display: flex; justify-content: space-between; font-size: 14px;">
                    <span>내행성 공전 각도 (태양-지구 선 기준)</span>
                    <span id="angleText" style="color: var(--accent-cyan)">45°</span>
                </div>
            </div>
        </div>
        <div class="visual-card" style="flex: 1.2;">
            <h3 style="color: var(--text-main); margin-bottom: 15px;">망원경 관측 위상 (실제 배율 확대)</h3>
            <div style="background: #020617; border: 1px solid #1e293b; padding: 20px; border-radius: 12px; display: flex; justify-content: center; align-items: center; width: 100%;">
                <canvas id="phaseCanvas" width="260" height="260"></canvas>
            </div>
            <div id="statusLabel" style="margin-top: 20px; font-size: 18px; font-weight: 700; color: var(--accent-cyan);">동방이각 부근</div>
            <p id="distInfo" style="font-size: 14px; color: var(--text-dim); margin-top: 5px;">시직경 배율: 1.20x</p>
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
                <div id="uploadStatus" class="status-msg">대기 중...</div>
            </div>
            <table>
                <tr><th>항목</th><th>분석 결과</th></tr>
                <tr><td>이미지 크기</td><td id="metaSize">-</td></tr>
                <tr><td>노출 시간</td><td id="metaExp">-</td></tr>
                <tr><td>평균 밝기</td><td id="metaBright">-</td></tr>
            </table>
            <button onclick="generateSample()" style="margin-top: 20px; background: transparent; border: 1px solid var(--accent-cyan); color: var(--accent-cyan); padding: 10px; border-radius: 8px; cursor: pointer;">테스트용 샘플 데이터 생성</button>
        </div>
        <div class="visual-card" style="flex: 1.5; background: #000; position: relative;">
            <canvas id="fitsCanvas" style="max-width: 100%; max-height: 440px; display: none;"></canvas>
            <div id="canvasPlaceholder" style="color: var(--text-dim); font-size: 14px;">파일이 업로드되면 천체 이미지가 렌더링됩니다.</div>
            <p style="color: var(--text-dim); font-size: 12px; margin-top: 10px; position: absolute; bottom: 10px;">CCD RAW Log-Stretch 시각화 엔진 v3.0</p>
        </div>
    </div>
</div>

<script>
    /* PLANETARY SIMULATION LOGIC */
    const orbitCanvas = document.getElementById('orbitCanvas');
    const oCtx = orbitCanvas.getContext('2d');
    const phaseCanvas = document.getElementById('phaseCanvas');
    const pCtx = phaseCanvas.getContext('2d');
    const slider = document.getElementById('angleSlider');

    function drawSim() {
        const angle = parseInt(slider.value);
        document.getElementById('angleText').innerText = angle + "°";
        
        oCtx.clearRect(0,0,500,400);
        const cx = 250, cy = 200;
        
        oCtx.strokeStyle = 'rgba(148, 163, 184, 0.2)';
        oCtx.beginPath(); oCtx.arc(cx, cy, 90, 0, Math.PI*2); oCtx.stroke();
        oCtx.beginPath(); oCtx.arc(cx, cy, 150, 0, Math.PI*2); oCtx.stroke();
        
        oCtx.fillStyle = '#f59e0b';
        oCtx.shadowBlur = 25; oCtx.shadowColor = '#f59e0b';
        oCtx.beginPath(); oCtx.arc(cx, cy, 18, 0, Math.PI*2); oCtx.fill();
        oCtx.shadowBlur = 0;
        
        const ex = cx, ey = cy + 150;
        oCtx.fillStyle = '#3b82f6';
        oCtx.beginPath(); oCtx.arc(ex, ey, 9, 0, Math.PI*2); oCtx.fill();
        
        const rad = (angle + 90) * Math.PI / 180;
        const px = cx + 90 * Math.cos(rad);
        const py = cy + 90 * Math.sin(rad);
        
        oCtx.fillStyle = '#e2e8f0';
        oCtx.beginPath(); oCtx.arc(px, py, 7, 0, Math.PI*2); oCtx.fill();

        oCtx.setLineDash([4, 4]);
        oCtx.strokeStyle = 'rgba(34, 211, 238, 0.4)';
        oCtx.beginPath(); oCtx.moveTo(ex, ey); oCtx.lineTo(px, py); oCtx.stroke();
        oCtx.setLineDash([]);

        oCtx.fillStyle = '#94a3b8';
        oCtx.font = '12px sans-serif';
        oCtx.fillText('태양', cx - 11, cy - 25);
        oCtx.fillText('지구', ex - 11, ey + 25);

        const normAngle = angle % 360;
        const dist = Math.sqrt((ex-px)**2 + (ey-py)**2);
        
        const maxDist = 150 + 90;
        const scale = (maxDist / dist) * 0.9;

        updatePhaseView(normAngle, scale);
    }

    function updatePhaseView(angle, scale) {
        const cx = 130, cy = 130;
        const baseRadius = 45; 
        const r = baseRadius * scale;
        
        pCtx.clearRect(0,0,260,260);
        pCtx.fillStyle = '#020617';
        pCtx.fillRect(0,0,260,260);
        
        pCtx.fillStyle = '#1e293b';
        pCtx.beginPath(); pCtx.arc(cx, cy, r, 0, Math.PI*2); pCtx.fill();
        
        pCtx.fillStyle = '#f8fafc';
        pCtx.save();
        pCtx.beginPath();
        
        if(angle > 0 && angle < 180) {
            pCtx.arc(cx, cy, r, -Math.PI/2, Math.PI/2, false);
        } else if (angle > 180 && angle < 360) {
            pCtx.arc(cx, cy, r, Math.PI/2, -Math.PI/2, false);
        } else if (angle === 180 || angle === 0) {
            if (angle === 180) pCtx.arc(cx, cy, r, 0, Math.PI*2);
        }
        
        const midWidth = r * Math.cos(angle * Math.PI / 180);
        pCtx.ellipse(cx, cy, Math.abs(midWidth), r, 0, Math.PI/2, -Math.PI/2, (angle > 90 && angle < 270));
        pCtx.fill();
        pCtx.restore();
        
        let statusText = "";
        if (angle === 0 || angle === 360) statusText = "내합 (삭, 관측 불가)";
        else if (angle > 0 && angle < 90) statusText = "동방이각 초입 (그믐달 모양, 저녁)";
        else if (angle === 90) statusText = "동방최대이각 (상현달 모양, 저녁)";
        else if (angle > 90 && angle < 180) statusText = "동방이각 말기 (볼록한 달, 저녁)";
        else if (angle === 180) statusText = "외합 (망/보름달, 관측 불가)";
        else if (angle > 180 && angle < 270) statusText = "서방이각 초입 (볼록한 달, 새벽)";
        else if (angle === 270) statusText = "서방최대이각 (하현달 모양, 새벽)";
        else if (angle > 270 && angle < 360) statusText = "서방이각 말기 (초승달 모양, 새벽)";

        document.getElementById('statusLabel').innerText = statusText;
        document.getElementById('distInfo').innerText = "시직경 상대 배율: " + scale.toFixed(2) + "x";
    }

    slider.oninput = drawSim;
    drawSim();


    /* FITS ANALYZER LOGIC (개선된 파일 처리 시스템) */
    const fitsInput = document.getElementById('fitsInput');
    const fCanvas = document.getElementById('fitsCanvas');
    const fCtx = fCanvas.getContext('2d');
    const uploadStatus = document.getElementById('uploadStatus');
    const placeholder = document.getElementById('canvasPlaceholder');

    fitsInput.onchange = function(e) {
        const file = e.target.files[0];
        if (!file) return;

        uploadStatus.innerText = "파일 로드 중...";
        const reader = new FileReader();
        
        reader.onload = function() {
            try {
                uploadStatus.innerText = "FITS 데이터 파싱 중...";
                const fits = new astro.FITS(this.result);
                const hdu = fits.getHDU();
                
                if(!hdu) {
                    throw new Error("유효한 HDU 구조를 찾을 수 없습니다.");
                }

                const header = hdu.header;
                const dataUnit = hdu.data;
                
                const w = header.get('NAXIS1');
                const h = header.get('NAXIS2');
                const exptime = header.get('EXPTIME') || 0;
                
                if(!w || !h) {
                    throw new Error("이미지 차원(NAXIS) 정보가 누락되었습니다.");
                }

                document.getElementById('metaSize').innerText = w + " x " + h;
                document.getElementById('metaExp').innerText = exptime.toFixed(1) + " s";
                
                uploadStatus.innerText = "이미지 픽셀 렌더링 중...";
                
                dataUnit.getFrame(0, (pixels) => {
                    if (!pixels) {
                        uploadStatus.innerText = "픽셀 데이터를 읽지 못했습니다.";
                        return;
                    }
                    renderFitsLogarithmic(pixels, w, h);
                    uploadStatus.innerText = "분석 완료";
                    placeholder.style.display = "none";
                    fCanvas.style.display = "block";
                });

            } catch (err) {
                uploadStatus.innerText = "오류 발생";
                alert("FITS 해석 실패: " + err.message + "\\n압축되지 않은 표준 FITS 파일인지 확인하세요.");
                console.error(err);
            }
        };
        
        reader.onerror = function() {
            uploadStatus.innerText = "파일 읽기 실패";
        };
        
        reader.readAsArrayBuffer(file);
    };

    // 로그 가속(Logarithmic Stretch) 연산을 사용한 정밀 천체 렌더링 엔진
    function renderFitsLogarithmic(pixels, w, h) {
        fCanvas.width = w; 
        fCanvas.height = h;
        const imgData = fCtx.createImageData(w, h);
        
        let min = Infinity;
        let max = -Infinity;
        let sum = 0;
        
        for(let i=0; i<pixels.length; i++) {
            const p = pixels[i];
            if (p < min) min = p;
            if (p > max) max = p;
            sum += p;
        }
        
        document.getElementById('metaBright').innerText = Math.round(sum/pixels.length) + " ADU";

        // 데이터 편차가 큰 천문 이미지를 선명하게 보여주는 Log 변환
        // 공식: Pixel_Out = ln(Pixel_In - min + 1) / ln(max - min + 1) * 255
        const logMax = Math.log(max - min + 1);

        for(let i=0; i<pixels.length; i++) {
            const rawValue = pixels[i];
            let intensity = 0;
            
            if (max - min > 0) {
                intensity = Math.log(rawValue - min + 1) / logMax * 255;
            }
            
            // 0 ~ 255 사이 제한 방어코드
            intensity = Math.min(Math.max(intensity, 0), 255);

            const idx = i * 4;
            imgData.data[idx]     = intensity; // R
            imgData.data[idx + 1] = intensity; // G
            imgData.data[idx + 2] = intensity; // B
            imgData.data[idx + 3] = 255;       // Alpha
        }
        
        fCtx.putImageData(imgData, 0, 0);
    }

    // 샘플 데이터 생성 기능에도 동일 로그 스케일 검증 적용
    function generateSample() {
        const w = 300, h = 300;
        const pix = new Float32Array(w*h);
        for(let i=0; i<w*h; i++) {
            const dx = (i%w) - 150, dy = Math.floor(i/w) - 150;
            // 일부러 가치를 높인 하이 다이내믹 레인지 데이터 시뮬레이션 (최대 5000 ADU)
            pix[i] = Math.exp(-(dx*dx + dy*dy)/600) * 5000 + Math.random()*200;
        }
        document.getElementById('metaSize').innerText = "300 x 300";
        document.getElementById('metaExp').innerText = "30.0 s";
        
        renderFitsLogarithmic(pix, w, h);
        uploadStatus.innerText = "가상 샘플 로드 완료";
        placeholder.style.display = "none";
        fCanvas.style.display = "block";
    }
</script>

</body>
</html>
"""

# Streamlit 화면에 HTML 컴포넌트를 렌더링합니다.
components.html(html_content, height=800, scrolling=True)
