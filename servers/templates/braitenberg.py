from .base import render_template

_EXTRA_CSS = '''
.speed-display { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin-top: 8px; }
.speed-box { text-align: center; padding: 8px; background: var(--bg-sidebar); border: 1px solid var(--border-color); border-radius: 6px; }
.speed-value { font-size: 22px; font-weight: 700; font-family: monospace; color: var(--accent-blue); }
.speed-label { font-size: 11px; color: var(--text-muted); text-transform: uppercase; margin-top: 3px; }

.hsv-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 6px 16px; margin-bottom: 8px; }
.hsv-label { font-size: 11px; color: var(--text-muted); text-transform: uppercase; margin-bottom: 2px; }

.mask-toggle { display: flex; gap: 6px; margin-bottom: 10px; }
.toggle-btn {
    flex: 1; padding: 5px; font-size: 11px;
    border: 1px solid var(--border-color); border-radius: 4px;
    cursor: pointer; background: var(--bg-sidebar); color: var(--text-secondary);
    font-family: 'Inter', sans-serif; transition: all 0.15s;
}
.toggle-btn.active { border-color: var(--accent-blue); color: var(--accent-blue); background: rgba(31,111,235,0.1); }
'''

_CONTENT = '''
    <div class="container">
        <div class="video-section">
            <img src="{{ url_for('video') }}" class="stream" id="video-stream">
        </div>

        <div class="controls-section">

            <div class="card">
                <div class="card-header">Motor Speeds</div>
                <div class="speed-display">
                    <div class="speed-box">
                        <div class="speed-value" id="speed-left">0.00</div>
                        <div class="speed-label">Left wheel</div>
                    </div>
                    <div class="speed-box">
                        <div class="speed-value" id="speed-right">0.00</div>
                        <div class="speed-label">Right wheel</div>
                    </div>
                </div>
                <div class="stats-grid" style="margin-top:8px">
                    <div class="stat-box">
                        <div class="stat-value" id="det-left">0</div>
                        <div class="stat-label">Left pixels</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-value" id="det-right">0</div>
                        <div class="stat-label">Right pixels</div>
                    </div>
                </div>
            </div>

            <div class="card">
                <div class="card-header">Braitenberg Config</div>
                <div class="slider-group">
                    <div class="slider-label"><span>Base speed (const)</span><span id="const-val">0.30</span></div>
                    <div class="slider-controls">
                        <input type="range" class="slider" id="const" min="0" max="100" value="30">
                        <input type="number" class="input-box" id="const-input" min="0" max="100" value="30">
                    </div>
                </div>
                <div class="slider-group">
                    <div class="slider-label"><span>Gain</span><span id="gain-val">1.50</span></div>
                    <div class="slider-controls">
                        <input type="range" class="slider" id="gain" min="0" max="500" value="150">
                        <input type="number" class="input-box" id="gain-input" min="0" max="500" value="150">
                    </div>
                </div>
                <div class="slider-group">
                    <div class="slider-label"><span>Detection threshold (px)</span><span id="thresh-val">100</span></div>
                    <div class="slider-controls">
                        <input type="range" class="slider" id="thresh" min="0" max="5000" value="100">
                        <input type="number" class="input-box" id="thresh-input" min="0" max="5000" value="100">
                    </div>
                </div>
                <button class="button" onclick="saveConfig()">Save Config</button>
                <div class="status" id="config-status"></div>
            </div>

            <div class="card">
                <div class="card-header">HSV Duck Color</div>
                <div class="mask-toggle">
                    <button class="toggle-btn active" id="btn-normal" onclick="setView('normal')">Camera</button>
                    <button class="toggle-btn" id="btn-mask" onclick="setView('mask')">Mask</button>
                    <button class="toggle-btn" id="btn-overlay" onclick="setView('overlay')">Overlay</button>
                </div>
                <div class="hsv-grid">
                    <div>
                        <div class="hsv-label">Lower H (0–180)</div>
                        <div class="slider-controls">
                            <input type="range" class="slider" id="lower_h" min="0" max="180" value="5">
                            <input type="number" class="input-box" id="lower_h-input" min="0" max="180" value="5">
                        </div>
                    </div>
                    <div>
                        <div class="hsv-label">Upper H (0–180)</div>
                        <div class="slider-controls">
                            <input type="range" class="slider" id="upper_h" min="0" max="180" value="35">
                            <input type="number" class="input-box" id="upper_h-input" min="0" max="180" value="35">
                        </div>
                    </div>
                    <div>
                        <div class="hsv-label">Lower S (0–255)</div>
                        <div class="slider-controls">
                            <input type="range" class="slider" id="lower_s" min="0" max="255" value="50">
                            <input type="number" class="input-box" id="lower_s-input" min="0" max="255" value="50">
                        </div>
                    </div>
                    <div>
                        <div class="hsv-label">Upper S (0–255)</div>
                        <div class="slider-controls">
                            <input type="range" class="slider" id="upper_s" min="0" max="255" value="255">
                            <input type="number" class="input-box" id="upper_s-input" min="0" max="255" value="255">
                        </div>
                    </div>
                    <div>
                        <div class="hsv-label">Lower V (0–255)</div>
                        <div class="slider-controls">
                            <input type="range" class="slider" id="lower_v" min="0" max="255" value="80">
                            <input type="number" class="input-box" id="lower_v-input" min="0" max="255" value="80">
                        </div>
                    </div>
                    <div>
                        <div class="hsv-label">Upper V (0–255)</div>
                        <div class="slider-controls">
                            <input type="range" class="slider" id="upper_v" min="0" max="255" value="255">
                            <input type="number" class="input-box" id="upper_v-input" min="0" max="255" value="255">
                        </div>
                    </div>
                </div>
                <button class="button" onclick="saveHsv()">Save HSV</button>
                <div class="status" id="hsv-status"></div>
            </div>

        </div>
    </div>
'''

_JS = '''
    let currentView = 'normal';

    function setView(view) {
        currentView = view;
        ['normal', 'mask', 'overlay'].forEach(v => {
            document.getElementById('btn-' + v).classList.toggle('active', v === view);
        });
        postJSON('/set_view', {view: view}).catch(() => {});
    }

    // Config sliders
    function saveConfig() {
        const data = {
            const:  parseInt(document.getElementById('const').value)  / 100.0,
            gain:   parseInt(document.getElementById('gain').value)    / 100.0,
            detection_threshold: parseInt(document.getElementById('thresh').value),
        };
        postJSON('/update_config', data)
            .then(() => showStatus('config-status', 'Saved', 'success'))
            .catch(() => showStatus('config-status', 'Error', 'error'));
    }

    function saveHsv() {
        const ids = ['lower_h', 'lower_s', 'lower_v', 'upper_h', 'upper_s', 'upper_v'];
        const data = {};
        ids.forEach(id => { data[id] = parseInt(document.getElementById(id).value); });
        postJSON('/update_hsv', data)
            .then(() => showStatus('hsv-status', 'Saved', 'success'))
            .catch(() => showStatus('hsv-status', 'Error', 'error'));
    }

    // Wire up sliders with display labels
    syncSliderInput('const',  () => {
        document.getElementById('const-val').textContent = (parseInt(document.getElementById('const').value)/100).toFixed(2);
    });
    syncSliderInput('gain',   () => {
        document.getElementById('gain-val').textContent  = (parseInt(document.getElementById('gain').value)/100).toFixed(2);
    });
    syncSliderInput('thresh', () => {
        document.getElementById('thresh-val').textContent = document.getElementById('thresh').value;
    });

    ['lower_h','lower_s','lower_v','upper_h','upper_s','upper_v'].forEach(id => {
        syncSliderInput(id, () => {});
    });

    // Poll status
    setInterval(() => {
        fetch('/status').then(r => r.json()).then(d => {
            document.getElementById('speed-left').textContent  = d.left_speed.toFixed(2);
            document.getElementById('speed-right').textContent = d.right_speed.toFixed(2);
            document.getElementById('det-left').textContent    = d.left_det;
            document.getElementById('det-right').textContent   = d.right_det;
        }).catch(() => {});
    }, 300);

    // Load current config on page load
    fetch('/status').then(r => r.json()).then(d => {
        if (d.config) {
            setSliderValue('const',  Math.round(d.config.const * 100));
            document.getElementById('const-val').textContent = d.config.const.toFixed(2);
            setSliderValue('gain',   Math.round(d.config.gain  * 100));
            document.getElementById('gain-val').textContent  = d.config.gain.toFixed(2);
            setSliderValue('thresh', d.config.detection_threshold);
            document.getElementById('thresh-val').textContent = d.config.detection_threshold;
        }
        if (d.hsv) {
            ['lower_h','lower_s','lower_v','upper_h','upper_s','upper_v'].forEach(id => {
                setSliderValue(id, d.hsv[id]);
            });
        }
    }).catch(() => {});
'''

BRAITENBERG_TEMPLATE = render_template(
    '{{ title }}',
    '{{ subtitle }}',
    _CONTENT,
    extra_css=_EXTRA_CSS,
    extra_js=_JS,
)
