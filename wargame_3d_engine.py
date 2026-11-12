"""
High-Tech Tactical C4ISR Battlespace Simulation Engine (Three.js WebGL)
Professional Military Vector Display & Dynamic Trajectory Engine
No Toy/Cartoon Blocks: Clean Radar Holographic Domes, Tactical Vectors, Bathymetry Grids,
Ballistic Missile Arcs, CIWS Defense Streams, and NATO-Standard Unit Symbology.
"""

import json

def get_wargame_3d_html(units_json_str: str, theater_name: str, t_info: dict, c_data_a: dict, c_data_b: dict, country_a: str, country_b: str) -> str:
    """
    Generates a professional C4ISR Tactical Maritime Battlespace Display (Three.js WebGL):
    - Dark tactical oceanic grid with bathymetry depth contours and bearing vectors
    - 3D Holographic radar range domes and SAM missile engagement envelopes
    - Accurate 3D parabolic missile trajectory splines with dynamic lock-on tracking
    - NATO-style tactical unit beacons with altitude stems and heading velocity vectors
    - Automated CIWS anti-air tracer streams and vector burst impact indicators
    - Clean professional military telemetry without crude/toy procedural blocks
    """
    
    html = f"""<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="utf-8">
<title>C4ISR Tactical Battlespace Display</title>
<style>
    * {{
        box-sizing: border-box;
        margin: 0;
        padding: 0;
    }}
    body {{
        background-color: #f8fafc;
        color: #0f172a;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        overflow: hidden;
        user-select: none;
        width: 100vw;
        height: 100vh;
    }}
    #wargame-container {{
        position: relative;
        width: 100%;
        height: 100%;
        display: flex;
        flex-direction: row;
        background: #ffffff;
        border: 1px solid #cbd5e1;
        border-radius: 10px;
        box-shadow: 0 4px 20px rgba(15, 23, 42, 0.06);
        overflow: hidden;
    }}
    #viewport-3d {{
        flex: 1;
        position: relative;
        height: 100%;
        background: #e0f2fe;
        overflow: hidden;
    }}
    #canvas3d {{
        width: 100%;
        height: 100%;
        display: block;
    }}
    /* Top Tactical HUD Bar */
    .hud-overlay-top {{
        position: absolute;
        top: 12px;
        left: 14px;
        right: 14px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        pointer-events: none;
        z-index: 10;
    }}
    .hud-title-badge {{
        background: rgba(255, 255, 255, 0.94);
        backdrop-filter: blur(8px);
        border: 1px solid #cbd5e1;
        border-left: 4px solid #1e40af;
        padding: 7px 14px;
        border-radius: 6px;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 0.5px;
        color: #0f172a;
        box-shadow: 0 2px 8px rgba(15, 23, 42, 0.05);
    }}
    .hud-title-badge span {{
        color: #0284c7;
        font-size: 10px;
        font-weight: 600;
        font-family: monospace;
    }}
    .cam-presets {{
        display: flex;
        gap: 5px;
        pointer-events: auto;
    }}
    .cam-btn {{
        background: rgba(255, 255, 255, 0.92);
        backdrop-filter: blur(6px);
        border: 1px solid #cbd5e1;
        color: #334155;
        padding: 6px 11px;
        font-size: 10.5px;
        font-weight: 600;
        border-radius: 5px;
        cursor: pointer;
        transition: all 0.15s ease-in-out;
        font-family: inherit;
        box-shadow: 0 1px 2px rgba(15, 23, 42, 0.04);
    }}
    .cam-btn:hover, .cam-btn.active {{
        background: #1e40af;
        border-color: #1e40af;
        color: #ffffff;
        box-shadow: 0 2px 6px rgba(30, 64, 175, 0.25);
    }}
    /* Bottom Info Badge */
    .hud-overlay-bottom-left {{
        position: absolute;
        bottom: 12px;
        left: 14px;
        background: rgba(255, 255, 255, 0.92);
        backdrop-filter: blur(6px);
        border: 1px solid #cbd5e1;
        border-radius: 6px;
        padding: 7px 12px;
        font-size: 10.5px;
        color: #475569;
        pointer-events: none;
        z-index: 10;
        line-height: 1.45;
        box-shadow: 0 1px 4px rgba(15, 23, 42, 0.04);
    }}
    .hud-overlay-bottom-left b {{
        color: #0f172a;
    }}
    /* Right Control & Telemetry Panel */
    #side-panel {{
        width: 320px;
        height: 100%;
        background: #f8fafc;
        border-left: 1px solid #e2e8f0;
        display: flex;
        flex-direction: column;
        padding: 14px;
        gap: 10px;
        z-index: 20;
        box-shadow: -2px 0 10px rgba(15, 23, 42, 0.03);
        overflow-y: auto;
    }}
    .side-panel-header {{
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 0.6px;
        color: #0f172a;
        border-bottom: 1px solid #e2e8f0;
        padding-bottom: 8px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        text-transform: uppercase;
    }}
    .hp-box {{
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 6px;
        padding: 9px 12px;
        box-shadow: 0 1px 3px rgba(15, 23, 42, 0.02);
    }}
    .hp-bar-bg {{
        background: #e2e8f0;
        height: 12px;
        border-radius: 3px;
        overflow: hidden;
        margin-top: 5px;
        position: relative;
    }}
    .hp-bar-a {{
        background: linear-gradient(90deg, #dc2626, #ef4444);
        height: 100%;
        width: 100%;
        transition: width 0.25s ease-out;
    }}
    .hp-bar-b {{
        background: linear-gradient(90deg, #0284c7, #38bdf8);
        height: 100%;
        width: 100%;
        transition: width 0.25s ease-out;
    }}
    .combat-grid-stats {{
        display: flex;
        justify-content: space-between;
        font-size: 10px;
        margin-top: 5px;
        color: #64748b;
    }}
    .btn-panel {{
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 6px;
    }}
    button.action-btn {{
        background: #ffffff;
        color: #334155;
        border: 1px solid #cbd5e1;
        padding: 8px 6px;
        font-family: inherit;
        font-weight: 600;
        font-size: 10.5px;
        border-radius: 5px;
        cursor: pointer;
        transition: all 0.15s ease;
        text-align: center;
        box-shadow: 0 1px 2px rgba(15, 23, 42, 0.03);
    }}
    button.action-btn:hover {{
        background: #f1f5f9;
        border-color: #94a3b8;
        color: #0f172a;
    }}
    #btn-main-combat {{
        grid-column: span 2;
        background: #0284c7;
        border: 1px solid #0284c7;
        color: #ffffff;
        padding: 10px 8px;
        font-size: 11.5px;
        font-weight: 700;
    }}
    #btn-main-combat:hover {{
        background: #0369a1;
        box-shadow: 0 2px 6px rgba(2, 132, 199, 0.25);
    }}
    #btn-reset {{
        grid-column: span 2;
        background: #f8fafc;
        border: 1px solid #cbd5e1;
        color: #64748b;
    }}
    #btn-reset:hover {{
        background: #e2e8f0;
        color: #0f172a;
    }}
    #terminal-log {{
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 6px;
        flex: 1;
        min-height: 140px;
        max-height: 180px;
        overflow-y: auto;
        padding: 8px 10px;
        font-size: 10px;
        color: #334155;
        line-height: 1.45;
        font-family: "SFMono-Regular", Consolas, monospace;
    }}
    #sound-btn {{
        background: #ffffff;
        color: #334155;
        border: 1px solid #cbd5e1;
        padding: 3px 8px;
        font-size: 10px;
        font-weight: 600;
        cursor: pointer;
        border-radius: 4px;
    }}
    #sound-btn:hover {{
        background: #f1f5f9;
    }}
    ::-webkit-scrollbar {{
        width: 4px;
    }}
    ::-webkit-scrollbar-track {{
        background: #f8fafc;
    }}
    ::-webkit-scrollbar-thumb {{
        background: #cbd5e1;
        border-radius: 2px;
    }}
</style>

<!-- Three.js + OrbitControls -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>

</head>
<body>

<div id="wargame-container">
    <!-- 3D C4ISR Battlespace Canvas -->
    <div id="viewport-3d">
        <canvas id="canvas3d"></canvas>
        
        <!-- Top HUD -->
        <div class="hud-overlay-top">
            <div class="hud-title-badge">
                C4ISR MARITIME THEATER // {theater_name.upper()}<br>
                <span>GRID: {t_info['lat']} | {t_info['lon']} // STATUS: ACTIVE TACTICAL VECTOR DISPLAY</span>
            </div>
            
            <div class="cam-presets">
                <button class="cam-btn active" onclick="setCameraView('isometric')">TACTICAL ISOMETRIC</button>
                <button class="cam-btn" onclick="setCameraView('satellite')">SATELLITE C4ISR</button>
                <button class="cam-btn" onclick="setCameraView('sideA')">FORCE {country_a[:3].upper()}</button>
                <button class="cam-btn" onclick="setCameraView('sideB')">FORCE {country_b[:3].upper()}</button>
                <button class="cam-btn" onclick="setCameraView('intercept')">ENGAGEMENT LOCK</button>
            </div>
        </div>

        <!-- Coordinates Info -->
        <div class="hud-overlay-bottom-left">
            <span><b>SISTEM KOMANDO:</b> Tampilan Vektor 3D Taktis Standar APP-6 & Trajektori Rudal Balistik</span><br>
            <span><b>FITUR:</b> Kubah Jangkauan Sensor Radar, Jaring Batimetri, Vektor Kecepatan, Intersepsi CIWS</span>
        </div>
    </div>

    <!-- Side Control Panel -->
    <div id="side-panel">
        <div class="side-panel-header">
            <span>TELEMETRI SISTEM KOMANDO</span>
            <button id="sound-btn" onclick="toggleAudio()">AUDIO: AKTIF</button>
        </div>

        <!-- Kubu A Status -->
        <div class="hp-box">
            <div style="display:flex; justify-content:space-between; font-weight:700; font-size:11px;">
                <span style="color:#dc2626;">{country_a.upper()} ({c_data_a['iso3']})</span>
                <span id="hp-a-txt" style="color:#dc2626;">100%</span>
            </div>
            <div class="hp-bar-bg"><div id="hp-a-bar" class="hp-bar-a"></div></div>
            <div class="combat-grid-stats">
                <span>Daya Serang (&alpha;): {c_data_a['attack_mod']}</span>
                <span>Daya Tahan: {c_data_a['defense_mod']}</span>
            </div>
        </div>

        <!-- Kubu B Status -->
        <div class="hp-box">
            <div style="display:flex; justify-content:space-between; font-weight:700; font-size:11px;">
                <span style="color:#0284c7;">{country_b.upper()} ({c_data_b['iso3']})</span>
                <span id="hp-b-txt" style="color:#0284c7;">100%</span>
            </div>
            <div class="hp-bar-bg"><div id="hp-b-bar" class="hp-bar-b"></div></div>
            <div class="combat-grid-stats">
                <span>Daya Serang (&beta;): {c_data_b['attack_mod']}</span>
                <span>Daya Tahan: {c_data_b['defense_mod']}</span>
            </div>
        </div>

        <!-- Action Commands -->
        <div class="btn-panel">
            <button id="btn-main-combat" class="action-btn" onclick="toggleCombat()">MULAI SIMULASI LANCHESTER 3D</button>
            <button class="action-btn" onclick="launchSalvo('A')">SALVO RUDAL {country_a[:3].upper()}</button>
            <button class="action-btn" onclick="launchSalvo('B')">SALVO RUDAL {country_b[:3].upper()}</button>
            <button class="action-btn" onclick="launchAirStrike()">PATROLI UDARA & SERGAP</button>
            <button class="action-btn" onclick="activateCIWS()">PERTAHANAN UDARA / CIWS</button>
            <button class="action-btn" onclick="activateECM()">JAMMING SIBER / ECM</button>
            <button id="btn-reset" class="action-btn" onclick="resetWargame()">RESET MEDAN TEMPUR</button>
        </div>

        <!-- Real-Time Telemetry Terminal -->
        <div style="font-size:10px; color:#64748b; font-weight:700; text-transform:uppercase;">LOG CATATAN SISTEM TAKTIS:</div>
        <div id="terminal-log">
            [T+00s] Grid C4ISR aktif: {country_a} vs {country_b}.<br>
            [T+00s] Medan Operasi: {theater_name}.<br>
            [T+00s] Pelacakan radar pasif & aktif mengunci formasi armada kedua belah pihak.
        </div>
    </div>
</div>

<script>
    const config = {units_json_str};

    let isRunning = false;
    let soundEnabled = true;
    let hpA = 100;
    let hpB = 100;
    let tickCount = 0;
    let audioCtx = null;

    // Web Audio Synthesizer (Professional High-Tech Telemetry Audio)
    function playBeep(freq, type, duration, vol = 0.08) {{
        if (!soundEnabled) return;
        try {{
            if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
            if (audioCtx.state === 'suspended') audioCtx.resume();
            const osc = audioCtx.createOscillator();
            const gain = audioCtx.createGain();
            osc.type = type || 'sine';
            osc.frequency.setValueAtTime(freq, audioCtx.currentTime);
            gain.gain.setValueAtTime(vol, audioCtx.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.0001, audioCtx.currentTime + duration);
            osc.connect(gain);
            gain.connect(audioCtx.destination);
            osc.start();
            osc.stop(audioCtx.currentTime + duration);
        }} catch(e) {{}}
    }}

    function playExplosionSound() {{
        if (!soundEnabled) return;
        playBeep(70, 'sawtooth', 0.5, 0.16);
        playBeep(38, 'triangle', 0.65, 0.22);
    }}

    function playMissileSound() {{
        if (!soundEnabled) return;
        try {{
            if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
            const osc = audioCtx.createOscillator();
            const gain = audioCtx.createGain();
            osc.type = 'sawtooth';
            osc.frequency.setValueAtTime(320, audioCtx.currentTime);
            osc.frequency.exponentialRampToValueAtTime(950, audioCtx.currentTime + 0.35);
            gain.gain.setValueAtTime(0.08, audioCtx.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.35);
            osc.connect(gain);
            gain.connect(audioCtx.destination);
            osc.start();
            osc.stop(audioCtx.currentTime + 0.35);
        }} catch(e) {{}}
    }}

    function playSonarPing() {{
        if (!soundEnabled) return;
        playBeep(980, 'sine', 0.8, 0.09);
    }}

    function toggleAudio() {{
        soundEnabled = !soundEnabled;
        document.getElementById('sound-btn').innerText = soundEnabled ? 'AUDIO: AKTIF' : 'AUDIO: SENYAP';
    }}

    function logMessage(msg) {{
        const term = document.getElementById('terminal-log');
        const timeStr = `[T+${{Math.floor(tickCount/30)}}s]`;
        term.innerHTML = `${{timeStr}} ${{msg}}<br>` + term.innerHTML;
    }}

    // =========================================================================
    // THREE.JS TACTICAL MARITIME DISPLAY
    // =========================================================================
    const container = document.getElementById('viewport-3d');
    const canvas = document.getElementById('canvas3d');

    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0xdce7f3); // Soft coastal sky daylight
    scene.fog = new THREE.FogExp2(0xdce7f3, 0.0012);

    const camera = new THREE.PerspectiveCamera(45, container.clientWidth / container.clientHeight, 1, 4500);
    camera.position.set(0, 210, 420);

    const renderer = new THREE.WebGLRenderer({{ canvas: canvas, antialias: true, alpha: true }});
    renderer.setSize(container.clientWidth, container.clientHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

    const controls = new THREE.OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.05;
    controls.maxPolarAngle = Math.PI / 2 - 0.03;
    controls.minDistance = 30;
    controls.maxDistance = 1500;
    controls.target.set(0, 20, 0);

    window.addEventListener('resize', () => {{
        if (!container.clientWidth || !container.clientHeight) return;
        camera.aspect = container.clientWidth / container.clientHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(container.clientWidth, container.clientHeight);
    }});

    // Lighting (Daylight Maritime Sunlight & Ambient Skylight)
    const ambientLight = new THREE.AmbientLight(0xffffff, 1.25);
    scene.add(ambientLight);

    const mainLight = new THREE.DirectionalLight(0xfff8eb, 1.35);
    mainLight.position.set(180, 380, 150);
    scene.add(mainLight);

    // =========================================================================
    // TACTICAL VECTOR ENVIRONMENT (BATHYMETRY GRID, BEARING RINGS, RADAR DOMES)
    // =========================================================================
    // 1. Digital Bathymetric Ocean Plane
    const oceanGeo = new THREE.PlaneGeometry(1600, 1600, 32, 32);
    const oceanMat = new THREE.MeshStandardMaterial({{
        color: 0x0f5282, // Azure marine blue
        roughness: 0.12,
        metalness: 0.8,
        transparent: true,
        opacity: 0.94
    }});
    const ocean = new THREE.Mesh(oceanGeo, oceanMat);
    ocean.rotation.x = -Math.PI / 2;
    scene.add(ocean);

    // 2. High-Precision Tactical Grid (1000m x 1000m)
    const gridHelper = new THREE.GridHelper(1000, 50, 0x0284c7, 0x94a3b8);
    gridHelper.position.y = 0.2;
    scene.add(gridHelper);

    // 3. Concentric Radar Distance Rings (100km, 200km, 300km, 400km)
    const ringsGroup = new THREE.Group();
    [80, 160, 240, 320, 400].forEach((r, idx) => {{
        const ringGeo = new THREE.RingGeometry(r - 0.4, r + 0.4, 64);
        const ringMat = new THREE.MeshBasicMaterial({{
            color: idx % 2 === 0 ? 0x0284c7 : 0x64748b,
            side: THREE.DoubleSide,
            transparent: true,
            opacity: 0.4
        }});
        const ringMesh = new THREE.Mesh(ringGeo, ringMat);
        ringMesh.rotation.x = -Math.PI / 2;
        ringMesh.position.y = 0.3;
        ringsGroup.add(ringMesh);
    }});
    scene.add(ringsGroup);

    // 4. Rotating Holographic Radar Sweep Line
    const sweepGeo = new THREE.RingGeometry(1, 400, 32, 1, 0, Math.PI / 5);
    const sweepMat = new THREE.MeshBasicMaterial({{
        color: 0x0284c7,
        side: THREE.DoubleSide,
        transparent: true,
        opacity: 0.18
    }});
    const radarSweep = new THREE.Mesh(sweepGeo, sweepMat);
    radarSweep.rotation.x = -Math.PI / 2;
    radarSweep.position.y = 0.4;
    scene.add(radarSweep);
    // 5. 3D Holographic Radar Range Domes (Air Search & SAM Coverage Envelopes)
    function createRadarCoverageDome(x, z, radius, colorHex) {{
        const domeGeo = new THREE.SphereGeometry(radius, 24, 16, 0, Math.PI * 2, 0, Math.PI / 2);
        const domeMat = new THREE.MeshBasicMaterial({{
            color: colorHex,
            wireframe: true,
            transparent: true,
            opacity: 0.12
        }});
        const dome = new THREE.Mesh(domeGeo, domeMat);
        dome.position.set(x, 0.5, z);
        scene.add(dome);
        return dome;
    }}

    createRadarCoverageDome(-180, 0, 140, 0xdc2626); // Kubu A Radar Dome
    createRadarCoverageDome(180, 0, 140, 0x0284c7);  // Kubu B Radar Dome

    // =========================================================================
    // PROFESSIONAL MILITARY TACTICAL PLATFORMS (APP-6 STANDARD SYMBOLOGY)
    // =========================================================================
    // Creates a sleek, sharp tactical warship beacon with altitude stem & velocity leader
    function createTacticalWarshipMarker(colorHex) {{
        const group = new THREE.Group();
        const mat = new THREE.MeshStandardMaterial({{ color: colorHex, roughness: 0.3, metalness: 0.7 }});
        const glow = new THREE.MeshBasicMaterial({{ color: colorHex }});

        // Angular Stealth Frigate Hull
        const hullGeo = new THREE.ConeGeometry(5.5, 24, 4);
        hullGeo.scale(1.4, 0.45, 1);
        const hull = new THREE.Mesh(hullGeo, mat);
        hull.rotation.z = Math.PI / 2;
        hull.position.y = 2;
        group.add(hull);

        // Superstructure Bridge Pyramid
        const bridge = new THREE.Mesh(new THREE.ConeGeometry(3.5, 6, 4), mat);
        bridge.position.set(-1, 5, 0);
        group.add(bridge);

        // Rotating Phased Array Antenna Beacon
        const beacon = new THREE.Mesh(new THREE.OctahedronGeometry(1.8), glow);
        beacon.position.set(-1, 9, 0);
        beacon.name = "sensorBeacon";
        group.add(beacon);

        // Heading Vector Line (Leader Line)
        const leaderGeo = new THREE.BufferGeometry().setFromPoints([
            new THREE.Vector3(0, 2, 0),
            new THREE.Vector3(18, 2, 0)
        ]);
        const leader = new THREE.Line(leaderGeo, new THREE.LineBasicMaterial({{ color: colorHex, linewidth: 2 }}));
        group.add(leader);

        return group;
    }}

    // Air Superiority Strike Jet Beacon (High Altitude)
    function createTacticalAirMarker(colorHex) {{
        const group = new THREE.Group();
        const mat = new THREE.MeshBasicMaterial({{ color: colorHex }});

        // Chevron / Delta Wing Vector Glyph
        const wingShape = new THREE.Shape();
        wingShape.moveTo(12, 0);
        wingShape.lineTo(-6, 8);
        wingShape.lineTo(-3, 0);
        wingShape.lineTo(-6, -8);
        wingShape.closePath();

        const wing = new THREE.Mesh(new THREE.ShapeGeometry(wingShape), mat);
        wing.rotation.x = -Math.PI / 2;
        group.add(wing);

        // Altitude Stem (Dashed line down to sea level)
        const stemGeo = new THREE.BufferGeometry().setFromPoints([
            new THREE.Vector3(0, 0, 0),
            new THREE.Vector3(0, -50, 0)
        ]);
        const stem = new THREE.Line(stemGeo, new THREE.LineDashedMaterial({{ color: colorHex, dashSize: 3, gapSize: 2, transparent: true, opacity: 0.5 }}));
        stem.computeLineDistances();
        group.add(stem);

        return group;
    }}

    // Sub-surface Submarine Beacon
    function createTacticalSubMarker(colorHex) {{
        const group = new THREE.Group();
        const mat = new THREE.MeshBasicMaterial({{ color: colorHex, wireframe: true }});

        const sub = new THREE.Mesh(new THREE.CylinderGeometry(2.5, 2.5, 20, 8), mat);
        sub.rotation.z = Math.PI / 2;
        sub.position.y = -4;
        group.add(sub);

        // Pulsing Acoustic Sonar Halo
        const halo = new THREE.Mesh(
            new THREE.RingGeometry(8, 9, 32),
            new THREE.MeshBasicMaterial({{ color: colorHex, side: THREE.DoubleSide, transparent: true, opacity: 0.45 }})
        );
        halo.rotation.x = -Math.PI / 2;
        halo.position.y = 0.5;
        halo.name = "sonarHalo";
        group.add(halo);

        return group;
    }}

    // Coastal Defense Missile / SAM Battery
    function createTacticalSAMMarker(colorHex) {{
        const group = new THREE.Group();
        const mat = new THREE.MeshStandardMaterial({{ color: colorHex, roughness: 0.4 }});

        const base = new THREE.Mesh(new THREE.CylinderGeometry(8, 10, 3, 6), mat);
        base.position.y = 1.5;
        group.add(base);

        const radarDish = new THREE.Mesh(new THREE.BoxGeometry(2, 6, 8), new THREE.MeshBasicMaterial({{ color: 0x38bdf8 }}));
        radarDish.position.set(0, 6, 0);
        radarDish.name = "samRadar";
        group.add(radarDish);

        return group;
    }}

    // Tactical Billboard Sprite Labels
    function createTacticalLabel(name, side, colorHex) {{
        const canvas = document.createElement('canvas');
        canvas.width = 256;
        canvas.height = 64;
        const ctx = canvas.getContext('2d');

        ctx.fillStyle = "rgba(4, 11, 24, 0.88)";
        ctx.strokeStyle = colorHex;
        ctx.lineWidth = 2;
        ctx.fillRect(4, 4, 248, 56);
        ctx.strokeRect(4, 4, 248, 56);

        ctx.fillStyle = "#ffffff";
        ctx.font = "bold 15px -apple-system, monospace";
        ctx.fillText(name.substring(0, 20), 12, 28);

        ctx.fillStyle = colorHex;
        ctx.fillRect(12, 38, 230, 8);

        const texture = new THREE.CanvasTexture(canvas);
        const sprite = new THREE.Sprite(new THREE.SpriteMaterial({{ map: texture, transparent: true }}));
        sprite.scale.set(32, 8, 1);
        sprite.position.y = 18;
        return {{ sprite: sprite, canvas: canvas, ctx: ctx, texture: texture }};
    }}

    // =========================================================================
    // DEPLOY TACTICAL TASK GROUPS
    // =========================================================================
    const units = [];

    function initTacticalUnits() {{
        units.forEach(u => {{
            scene.remove(u.mesh);
            scene.remove(u.label.sprite);
        }});
        units.length = 0;

        // Force A (Red Force: #dc2626)
        config.countryA.units.forEach((uData, idx) => {{
            let mesh;
            let startY = 2;
            const colorHex = 0xdc2626;

            if (uData.type === 'ship') {{
                mesh = createTacticalWarshipMarker(colorHex);
                startY = 2;
            }} else if (uData.type === 'sub') {{
                mesh = createTacticalSubMarker(colorHex);
                startY = -3;
            }} else if (uData.type === 'jet' || uData.type === 'heli') {{
                mesh = createTacticalAirMarker(colorHex);
                startY = 52 + idx * 8;
            }} else {{
                mesh = createTacticalSAMMarker(colorHex);
                startY = 2;
            }}

            const startX = -240 + (idx % 2) * 50;
            const startZ = -120 + idx * 55;
            mesh.position.set(startX, startY, startZ);
            scene.add(mesh);

            const label = createTacticalLabel(uData.id, 'A', '#dc2626');
            label.sprite.position.set(startX, startY + 16, startZ);
            scene.add(label.sprite);

            units.push({{
                data: uData,
                side: 'A',
                name: uData.id,
                type: uData.type,
                mesh: mesh,
                label: label,
                startY: startY,
                x: startX, y: startY, z: startZ,
                vx: 0.16 * config.countryA.speed,
                vz: (Math.random() - 0.5) * 0.1,
                hp: 100,
                color: '#dc2626',
                colorHex: colorHex,
                attack: config.countryA.attack,
                defense: config.countryA.defense,
                cooldown: Math.floor(Math.random() * 40)
            }});
        }});

        // Force B (Blue Force: #0284c7)
        config.countryB.units.forEach((uData, idx) => {{
            let mesh;
            let startY = 2;
            const colorHex = 0x0284c7;

            if (uData.type === 'ship') {{
                mesh = createTacticalWarshipMarker(colorHex);
                mesh.rotation.y = Math.PI; // Facing West
                startY = 2;
            }} else if (uData.type === 'sub') {{
                mesh = createTacticalSubMarker(colorHex);
                startY = -3;
            }} else if (uData.type === 'jet' || uData.type === 'heli') {{
                mesh = createTacticalAirMarker(colorHex);
                mesh.rotation.y = Math.PI;
                startY = 54 + idx * 8;
            }} else {{
                mesh = createTacticalSAMMarker(colorHex);
                startY = 2;
            }}

            const startX = 240 - (idx % 2) * 50;
            const startZ = -120 + idx * 55;
            mesh.position.set(startX, startY, startZ);
            scene.add(mesh);

            const label = createTacticalLabel(uData.id, 'B', '#0284c7');
            label.sprite.position.set(startX, startY + 16, startZ);
            scene.add(label.sprite);

            units.push({{
                data: uData,
                side: 'B',
                name: uData.id,
                type: uData.type,
                mesh: mesh,
                label: label,
                startY: startY,
                x: startX, y: startY, z: startZ,
                vx: -0.16 * config.countryB.speed,
                vz: (Math.random() - 0.5) * 0.1,
                hp: 100,
                color: '#0284c7',
                colorHex: colorHex,
                attack: config.countryB.attack,
                defense: config.countryB.defense,
                cooldown: Math.floor(Math.random() * 40)
            }});
        }});
    }}

    initTacticalUnits();

    // =========================================================================
    // TACTICAL BALLISTIC MISSILE TRAJECTORIES & CIWS INTERCEPT STREAMS
    // =========================================================================
    const missiles = [];
    const bursts = [];
    const tracers = [];

    // Launch Ballistic / Sea-Skimming Missile with Arc Spline
    function spawnMissile(sourceUnit, targetUnit) {{
        playMissileSound();

        // Missile Head (High-intensity luminous beacon)
        const mHead = new THREE.Mesh(
            new THREE.SphereGeometry(1.4, 8, 8),
            new THREE.MeshBasicMaterial({{ color: sourceUnit.colorHex }})
        );
        const startPos = sourceUnit.mesh.position.clone();
        mHead.position.copy(startPos);
        scene.add(mHead);

        // Flight Trajectory Arc Spline Curve
        const midPoint = new THREE.Vector3().lerpVectors(startPos, targetUnit.mesh.position, 0.5);
        midPoint.y += 65 + Math.random() * 30; // Parabolic apogee

        const curve = new THREE.QuadraticBezierCurve3(startPos, midPoint, targetUnit.mesh.position);
        const curvePoints = curve.getPoints(36);
        const trajectoryGeo = new THREE.BufferGeometry().setFromPoints(curvePoints);
        const trajectoryLine = new THREE.Line(
            trajectoryGeo,
            new THREE.LineDashedMaterial({{ color: sourceUnit.colorHex, dashSize: 4, gapSize: 3, transparent: true, opacity: 0.6 }})
        );
        trajectoryLine.computeLineDistances();
        scene.add(trajectoryLine);

        missiles.push({{
            head: mHead,
            line: trajectoryLine,
            curve: curve,
            progress: 0,
            speed: 0.016 * 1.4,
            source: sourceUnit,
            target: targetUnit,
            colorHex: sourceUnit.colorHex
        }});

        logMessage(`<span style='color:${{sourceUnit.color}}; font-weight:600;'>[LAUNCH] ${{sourceUnit.name}} meluncurkan salvo rudal taktis pandu ke arah ${{targetUnit.name}}!</span>`);
    }}

    // CIWS / Intercept Laser Stream
    function spawnCIWSTracer(fromPos, toPos, colorHex) {{
        playBeep(850, 'square', 0.06, 0.04);
        const geo = new THREE.BufferGeometry().setFromPoints([fromPos, toPos]);
        const line = new THREE.Line(geo, new THREE.LineBasicMaterial({{ color: colorHex, linewidth: 2 }}));
        scene.add(line);
        tracers.push({{ line: line, life: 6 }});
    }}

    // Vector Burst Indicator on Impact
    function spawnVectorBurst(pos, colorHex) {{
        playExplosionSound();
        const burstGeo = new THREE.RingGeometry(1, 14, 24);
        const burstMat = new THREE.MeshBasicMaterial({{ color: colorHex, side: THREE.DoubleSide, transparent: true, opacity: 0.9 }});
        const burst = new THREE.Mesh(burstGeo, burstMat);
        burst.rotation.x = -Math.PI / 2;
        burst.position.copy(pos);
        burst.position.y += 0.8;
        scene.add(burst);
        bursts.push({{ mesh: burst, scale: 1, maxLife: 28, life: 28 }});
    }}

    function damageSide(side, amount) {{
        if (side === 'A') {{
            hpA = Math.max(0, hpA - amount);
            document.getElementById('hp-a-bar').style.width = hpA + '%';
            document.getElementById('hp-a-txt').innerText = Math.round(hpA) + '%';
        }} else {{
            hpB = Math.max(0, hpB - amount);
            document.getElementById('hp-b-bar').style.width = hpB + '%';
            document.getElementById('hp-b-txt').innerText = Math.round(hpB) + '%';
        }}

        if (hpA <= 0 && hpB > 0) {{
            isRunning = false;
            logMessage(`<b style='color:#0284c7;'>[HASIL AKHIR] ${{config.countryB.name.toUpperCase()}} MENGUASAI MEDAN OPERASI!</b>`);
        }} else if (hpB <= 0 && hpA > 0) {{
            isRunning = false;
            logMessage(`<b style='color:#dc2626;'>[HASIL AKHIR] ${{config.countryA.name.toUpperCase()}} MENGUASAI MEDAN OPERASI!</b>`);
        }}
    }}

    // =========================================================================
    // USER COMMAND ACTIONS
    // =========================================================================
    function toggleCombat() {{
        isRunning = !isRunning;
        const btn = document.getElementById('btn-main-combat');
        if (isRunning) {{
            btn.innerHTML = 'JEDA SIMULASI TEMPUR';
            btn.style.background = '#dc2626';
            logMessage("<span style='color:#0284c7; font-weight:600;'>Komputasi atrisi Lanchester aktif: Pertempuran taktis berjalan 60 FPS.</span>");
        }} else {{
            btn.innerHTML = 'LANJUTKAN SIMULASI 3D';
            btn.style.background = '#0284c7';
            logMessage("Simulasi dijeda oleh komando.");
        }}
    }}

    function launchSalvo(fromSide) {{
        const attackers = units.filter(u => u.side === fromSide && u.hp > 0);
        const defenders = units.filter(u => u.side !== fromSide && u.hp > 0);
        if (attackers.length === 0 || defenders.length === 0) return;

        const count = Math.min(3, attackers.length);
        for (let i = 0; i < count; i++) {{
            const att = attackers[i % attackers.length];
            const def = defenders[Math.floor(Math.random() * defenders.length)];
            setTimeout(() => spawnMissile(att, def), i * 220);
        }}
    }}

    function launchAirStrike() {{
        logMessage("<span style='color:#0284c7; font-weight:600;'>[AIR STRIKE] Gugus tempur udara melancarkan serangan presisi anti-permukaan!</span>");
        launchSalvo('A');
        setTimeout(() => launchSalvo('B'), 350);
    }}

    function activateCIWS() {{
        logMessage("<span style='color:#059669; font-weight:600;'>[AIR DEFENSE] Sistem hanud & CIWS Phalanx aktif mencegat seluruh vektor ancaman!</span>");
        for (let i = missiles.length - 1; i >= 0; i--) {{
            const m = missiles[i];
            spawnCIWSTracer(m.target.mesh.position, m.head.position, 0x059669);
            spawnVectorBurst(m.head.position, 0x059669);
            scene.remove(m.head);
            scene.remove(m.line);
            missiles.splice(i, 1);
            logMessage(`<span style='color:#059669;'>[INTERCEPT] Rudal ancaman berhasil dinetralisasi di udara sebelum mencapai koordinat sasaran.</span>`);
        }}
    }}

    function activateECM() {{
        logMessage("<span style='color:#7c3aed; font-weight:600;'>[ELECTRONIC WARFARE] Jamming radar dan pemancar decoy aktif mereduksi akurasi lawan!</span>");
        const emp = new THREE.Mesh(
            new THREE.SphereGeometry(15, 24, 24),
            new THREE.MeshBasicMaterial({{ color: 0x7c3aed, wireframe: true, transparent: true, opacity: 0.8 }})
        );
        emp.position.set(0, 20, 0);
        scene.add(emp);

        let scale = 1;
        const interval = setInterval(() => {{
            scale += 3.5;
            emp.scale.set(scale, scale, scale);
            emp.material.opacity -= 0.05;
            if (emp.material.opacity <= 0) {{
                clearInterval(interval);
                scene.remove(emp);
            }}
        }}, 40);
        playBeep(260, 'sine', 0.6, 0.12);
    }}

    function resetWargame() {{
        isRunning = false;
        hpA = 100;
        hpB = 100;
        tickCount = 0;
        document.getElementById('hp-a-bar').style.width = '100%';
        document.getElementById('hp-b-bar').style.width = '100%';
        document.getElementById('hp-a-txt').innerText = '100%';
        document.getElementById('hp-b-txt').innerText = '100%';
        document.getElementById('btn-main-combat').innerHTML = 'MULAI SIMULASI LANCHESTER 3D';
        document.getElementById('btn-main-combat').style.background = '#0284c7';

        missiles.forEach(m => {{
            scene.remove(m.head);
            scene.remove(m.line);
        }});
        missiles.length = 0;

        bursts.forEach(b => scene.remove(b.mesh));
        bursts.length = 0;

        tracers.forEach(t => scene.remove(t.line));
        tracers.length = 0;

        initTacticalUnits();
        setCameraView('isometric');
        logMessage("[RESET] Grid taktis dan posisi seluruh armada dikembalikan ke kondisi awal.");
    }}

    // Spectator Camera Presets
    function setCameraView(preset) {{
        document.querySelectorAll('.cam-btn').forEach(b => b.classList.remove('active'));
        if (preset === 'isometric') {{
            camera.position.set(0, 210, 410);
            controls.target.set(0, 20, 0);
        }} else if (preset === 'satellite') {{
            camera.position.set(0, 490, 10);
            controls.target.set(0, 0, 0);
        }} else if (preset === 'sideA') {{
            camera.position.set(-340, 95, 120);
            controls.target.set(-140, 20, 0);
        }} else if (preset === 'sideB') {{
            camera.position.set(340, 95, 120);
            controls.target.set(140, 20, 0);
        }} else if (preset === 'intercept') {{
            camera.position.set(0, 75, 190);
            controls.target.set(0, 30, 0);
        }}
    }}

    // =========================================================================
    // 60 FPS RENDER LOOP
    // =========================================================================
    const clock = new THREE.Clock();

    function animate() {{
        requestAnimationFrame(animate);
        const delta = clock.getDelta();
        tickCount++;

        // 1. Radar Sweep Rotation
        radarSweep.rotation.z += 0.024;
        if (Math.abs(radarSweep.rotation.z % (Math.PI * 2)) < 0.028 && isRunning) {{
            playSonarPing();
        }}

        // 2. Animate Tactical Platforms
        units.forEach(u => {{
            const beacon = u.mesh.getObjectByName("sensorBeacon");
            if (beacon) beacon.rotation.y += 0.05;

            const samRadar = u.mesh.getObjectByName("samRadar");
            if (samRadar) samRadar.rotation.y += 0.04;

            const halo = u.mesh.getObjectByName("sonarHalo");
            if (halo) {{
                const s = 1 + Math.sin(tickCount * 0.08) * 0.25;
                halo.scale.set(s, s, s);
            }}

            if (isRunning) {{
                u.mesh.position.x += u.vx;
                u.mesh.position.z += u.vz;

                if (Math.abs(u.mesh.position.x) > 340) u.vx *= -1;
                if (Math.abs(u.mesh.position.z) > 160) u.vz *= -1;

                u.label.sprite.position.set(u.mesh.position.x, u.mesh.position.y + 16, u.mesh.position.z);

                u.cooldown--;
                if (u.cooldown <= 0) {{
                    u.cooldown = 110 + Math.floor(Math.random() * 80);
                    const enemies = units.filter(e => e.side !== u.side && e.hp > 0);
                    if (enemies.length > 0 && Math.random() < 0.65) {{
                        const target = enemies[Math.floor(Math.random() * enemies.length)];
                        spawnMissile(u, target);
                    }}
                }}
            }}
        }});

        // 3. Animate Guided Missile Spline Trajectories
        for (let i = missiles.length - 1; i >= 0; i--) {{
            const m = missiles[i];
            m.progress += m.speed;

            if (m.progress >= 1.0) {{
                spawnVectorBurst(m.target.mesh.position, m.colorHex);
                const dmg = 8.5 * (m.source.attack / m.target.defense);
                damageSide(m.target.side, dmg);

                if (Math.random() < 0.45) {{
                    spawnCIWSTracer(m.target.mesh.position, m.head.position, 0x0284c7);
                }}

                logMessage(`<span style='color:${{m.source.color}}; font-weight:700;'>[IMPACT] Vektor rudal ${{m.source.name}} menghantam platform ${{m.target.name}}! (-${{dmg.toFixed(1)}}% HP)</span>`);
                scene.remove(m.head);
                scene.remove(m.line);
                missiles.splice(i, 1);
            }} else {{
                const p = m.curve.getPoint(m.progress);
                m.head.position.copy(p);
            }}
        }}

        // 4. Animate Vector Bursts
        for (let i = bursts.length - 1; i >= 0; i--) {{
            const b = bursts[i];
            b.scale += 0.8;
            b.mesh.scale.set(b.scale, b.scale, b.scale);
            b.life--;
            b.mesh.material.opacity = b.life / b.maxLife;

            if (b.life <= 0) {{
                scene.remove(b.mesh);
                bursts.splice(i, 1);
            }}
        }}

        // 5. Animate CIWS Tracers
        for (let i = tracers.length - 1; i >= 0; i--) {{
            const t = tracers[i];
            t.life--;
            t.line.material.opacity = t.life / 6;
            if (t.life <= 0) {{
                scene.remove(t.line);
                tracers.splice(i, 1);
            }}
        }}

        // 6. Lanchester Stochastic Combat Ticks
        if (isRunning && tickCount % 45 === 0) {{
            const lossA = (0.28 * config.countryB.attack) / config.countryA.defense;
            const lossB = (0.28 * config.countryA.attack) / config.countryB.defense;
            damageSide('A', lossA);
            damageSide('B', lossB);
        }}

        controls.update();
        renderer.render(scene, camera);
    }}

    animate();
</script>

</body>
</html>
"""
    return html

