/* ═══ Incident Analytics ═══ */

function renderAnalytics(container) {
    const days = 30;
    const dates = [], fireD = [], medD = [], secD = [], respD = [];
    for (let i = days - 1; i >= 0; i--) {
        const d = new Date(); d.setDate(d.getDate() - i);
        dates.push(d.toLocaleDateString('en-US', { month: 'short', day: 'numeric' }));
        fireD.push(Math.floor(Math.random() * 4));
        medD.push(Math.floor(Math.random() * 6));
        secD.push(Math.floor(Math.random() * 3));
        respD.push(30 + Math.floor(Math.random() * 150));
    }

    const totalInc = fireD.reduce((a, b) => a + b) + medD.reduce((a, b) => a + b) + secD.reduce((a, b) => a + b);
    const avgResp = Math.round(respD.reduce((a, b) => a + b) / days);
    const fastest = Math.min(...respD);
    const resRate = (92 + Math.random() * 7).toFixed(1);

    // Bar chart
    let barHTML = '<div style="display:flex;align-items:flex-end;gap:3px;height:200px;">';
    for (let i = 0; i < days; i++) {
        const t = fireD[i] + medD[i] + secD[i];
        const h = t > 0 ? Math.max((t / 12) * 180, 4) : 2;
        const fH = t ? fireD[i] / t * h : 0, mH = t ? medD[i] / t * h : 0, sH = t ? secD[i] / t * h : 0;
        barHTML += `<div style="flex:1;display:flex;flex-direction:column;justify-content:flex-end;cursor:pointer;" title="${dates[i]}: F${fireD[i]} M${medD[i]} S${secD[i]}">
            <div style="height:${fH}px;background:var(--red);border-radius:2px 2px 0 0;"></div>
            <div style="height:${mH}px;background:var(--blue);"></div>
            <div style="height:${sH}px;background:var(--orange);border-radius:0 0 2px 2px;"></div>
        </div>`;
    }
    barHTML += '</div>';

    // Response dots
    const maxR = Math.max(...respD);
    let dotsHTML = respD.map((v, i) => {
        const x = (i / (days - 1)) * 100, y = 100 - (v / maxR) * 100;
        return `<div style="position:absolute;left:${x}%;top:${y}%;width:5px;height:5px;background:var(--cyan);border-radius:50%;transform:translate(-50%,-50%);cursor:pointer;" title="${dates[i]}: ${v}s"></div>`;
    }).join('');
    // Connect dots with SVG line
    let svgPoints = respD.map((v, i) => `${(i / (days - 1)) * 100},${100 - (v / maxR) * 100}`).join(' ');

    // Severity
    const sevD = { CRITICAL: 5 + Math.floor(Math.random() * 10), PRIORITY: 10 + Math.floor(Math.random() * 15), MODERATE: 15 + Math.floor(Math.random() * 15), LOW: 8 + Math.floor(Math.random() * 12) };
    const sevT = Object.values(sevD).reduce((a, b) => a + b);
    const sevC = { CRITICAL: 'var(--red)', PRIORITY: 'var(--orange)', MODERATE: 'var(--yellow)', LOW: 'var(--green)' };
    let sevHTML = '';
    for (const [s, c] of Object.entries(sevD)) {
        const p = Math.round(c / sevT * 100);
        sevHTML += `<div class="sev-bar"><div class="sev-label"><span>${s}</span><span style="color:${sevC[s]}">${c} (${p}%)</span></div><div class="sev-track"><div class="sev-fill" style="width:${p}%;background:${sevC[s]}"></div></div></div>`;
    }

    // Donut
    const tF = fireD.reduce((a, b) => a + b), tM = medD.reduce((a, b) => a + b), tS = secD.reduce((a, b) => a + b), tA = tF + tM + tS;
    const pF = Math.round(tF / tA * 360), pM = Math.round(tM / tA * 360);

    container.innerHTML = `
    <div class="page-header">
        <div>
            <div class="page-title">Incident Analytics</div>
            <div class="page-meta">RESPONSE METRICS • TREND ANALYSIS • 30-DAY OVERVIEW</div>
        </div>
    </div>

    <div class="grid grid-4 mb-16">
        <div class="metric-card cyan"><div class="metric-value" style="color:var(--cyan)">${totalInc}</div><div class="metric-label">TOTAL INCIDENTS</div></div>
        <div class="metric-card orange"><div class="metric-value" style="color:var(--orange)">${avgResp}s</div><div class="metric-label">AVG RESPONSE</div></div>
        <div class="metric-card green"><div class="metric-value" style="color:var(--green)">${fastest}s</div><div class="metric-label">FASTEST</div></div>
        <div class="metric-card green"><div class="metric-value" style="color:var(--green)">${resRate}%</div><div class="metric-label">RESOLUTION RATE</div></div>
    </div>

    <div class="grid grid-2 mb-16">
        <div class="card">
            <div class="section-title">INCIDENTS BY TYPE (30 DAYS)</div>
            ${barHTML}
            <div class="flex justify-between mt-4" style="font-size:10px;color:var(--text-3);">
                <span>${dates[0]}</span><span>${dates[14]}</span><span>${dates[29]}</span>
            </div>
            <div class="flex gap-12 mt-8" style="font-size:11px;">
                <span><span style="display:inline-block;width:10px;height:10px;background:var(--red);border-radius:2px;margin-right:4px;vertical-align:middle;"></span>Fire</span>
                <span><span style="display:inline-block;width:10px;height:10px;background:var(--blue);border-radius:2px;margin-right:4px;vertical-align:middle;"></span>Medical</span>
                <span><span style="display:inline-block;width:10px;height:10px;background:var(--orange);border-radius:2px;margin-right:4px;vertical-align:middle;"></span>Security</span>
            </div>
        </div>
        <div class="card">
            <div class="section-title">RESPONSE TIME TREND</div>
            <div style="position:relative;height:200px;">
                <svg style="position:absolute;inset:0;width:100%;height:100%;" viewBox="0 0 100 100" preserveAspectRatio="none">
                    <polyline points="${svgPoints}" fill="none" stroke="#06b6d4" stroke-width="0.5" vector-effect="non-scaling-stroke"/>
                    <polyline points="0,100 ${svgPoints} 100,100" fill="rgba(6,182,212,0.08)" stroke="none"/>
                </svg>
                ${dotsHTML}
            </div>
            <div class="flex justify-between mt-4" style="font-size:10px;color:var(--text-3);">
                <span>${dates[0]}</span><span>${dates[29]}</span>
            </div>
        </div>
    </div>

    <div class="grid grid-2">
        <div class="card">
            <div class="section-title">INCIDENT DISTRIBUTION</div>
            <div class="flex items-center" style="justify-content:center;padding:24px;gap:28px;">
                <div style="width:170px;height:170px;border-radius:50%;background:conic-gradient(var(--red) 0deg ${pF}deg,var(--blue) ${pF}deg ${pF + pM}deg,var(--orange) ${pF + pM}deg 360deg);position:relative;box-shadow:0 0 30px rgba(0,0,0,0.3);">
                    <div style="position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);width:90px;height:90px;border-radius:50%;background:var(--bg-2);display:flex;align-items:center;justify-content:center;flex-direction:column;">
                        <span class="mono" style="font-size:20px;font-weight:800;">${tA}</span>
                        <span style="font-size:8px;color:var(--text-3);letter-spacing:1px;">TOTAL</span>
                    </div>
                </div>
                <div style="font-size:13px;line-height:2.4;">
                    <div>🔥 Fire: <span class="mono" style="color:var(--red);font-weight:600;">${tF}</span></div>
                    <div>🏥 Medical: <span class="mono" style="color:var(--blue);font-weight:600;">${tM}</span></div>
                    <div>🚨 Security: <span class="mono" style="color:var(--orange);font-weight:600;">${tS}</span></div>
                </div>
            </div>
        </div>
        <div class="card">
            <div class="section-title">SEVERITY BREAKDOWN</div>
            ${sevHTML}
        </div>
    </div>`;
}
