# ==============================================================================
# PROJECT: W8 OTP SENDER
# CREDIT : CREDIT BY NOYON (@NOYON_OFFICIAL_99 & @CODEX_NOYON)
# ARCHITECTURE: SINGLE FILE PYTHON FLASK + RGB CYBER-TECH UI
# ==============================================================================

import os
import re
import requests
from datetime import datetime
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# ==================== REAL UPSTREAM API LOGIC ====================
UPSTREAM_API = "https://allo-gang.vercel.app/api/send-code"
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')

def dispatch_otp_request(email: str) -> dict:
    """
    Real API call extracted directly from single_unsubscribe.py & bot.py.
    Sends the request to the upstream Garena SSO gateway.
    """
    api_url = f"{UPSTREAM_API}?email={requests.utils.quote(email)}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
        "Accept": "application/json",
    }
    try:
        response = requests.get(api_url, headers=headers, timeout=25)
        
        if response.status_code == 200:
            try:
                data = response.json()
                garena_resp = data.get("response", {}) or data.get("garena_response", {})
                result_code = garena_resp.get("result")
                status_str = data.get("status", "")

                if result_code == 0 or status_str == "success":
                    return {
                        "success": True,
                        "status_code": 200,
                        "message": "Single Unsubscribe OTP Sent Successfully to your email!",
                        "email": email,
                        "timestamp": datetime.now().strftime("%H:%M:%S")
                    }
                else:
                    error_detail = garena_resp.get("error") or data.get("message") or "Gateway rejected dispatch"
                    return {
                        "success": False,
                        "status_code": 200,
                        "message": f"OTP Send Failed: {error_detail}",
                        "email": email,
                        "timestamp": datetime.now().strftime("%H:%M:%S")
                    }
            except ValueError:
                return {
                    "success": False,
                    "status_code": 502,
                    "message": "Invalid response format received from upstream server.",
                    "email": email,
                    "timestamp": datetime.now().strftime("%H:%M:%S")
                }
        else:
            return {
                "success": False,
                "status_code": response.status_code,
                "message": f"Server returned HTTP error {response.status_code}.",
                "email": email,
                "timestamp": datetime.now().strftime("%H:%M:%S")
            }
            
    except requests.exceptions.Timeout:
        return {
            "success": False,
            "status_code": 504,
            "message": "Gateway Timeout: Server took too long to respond.",
            "email": email,
            "timestamp": datetime.now().strftime("%H:%M:%S")
        }
    except requests.exceptions.ConnectionError:
        return {
            "success": False,
            "status_code": 503,
            "message": "Connection Error: Check internet connection or API status.",
            "email": email,
            "timestamp": datetime.now().strftime("%H:%M:%S")
        }
    except Exception as e:
        return {
            "success": False,
            "status_code": 500,
            "message": f"Transmission error: {str(e)[:45]}",
            "email": email,
            "timestamp": datetime.now().strftime("%H:%M:%S")
        }

# ==================== BACKEND API ROUTES ====================
@app.route("/api/send-otp", methods=["POST"])
def api_send_otp():
    payload = request.get_json(silent=True) or {}
    email = payload.get("email", "").strip().lower()

    if not email:
        return jsonify({"success": False, "message": "Email address cannot be empty."}), 400

    if not EMAIL_REGEX.match(email):
        return jsonify({"success": False, "message": "Invalid email address format."}), 400

    result = dispatch_otp_request(email)
    http_status = 200 if result["success"] else (400 if result["status_code"] == 200 else result["status_code"])
    return jsonify(result), http_status

@app.route("/api/status", methods=["GET"])
def api_status():
    return jsonify({
        "status": "online",
        "project": "W8 OTP SENDER",
        "credit": "CREDIT BY NOYON",
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }), 200

# ==================== EMBEDDED FRONTEND UI ====================
HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>W8 OTP SENDER | CREDIT BY NOYON</title>
    <!-- Fonts & Icons -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500;600&family=Rajdhani:wght@600;700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.2/css/all.min.css">

    <style>
        :root {
            --bg-base: #05070e;
            --card-bg: rgba(11, 16, 30, 0.78);
            --card-border: rgba(0, 240, 255, 0.18);
            --cyan-neon: #00f0ff;
            --cyan-glow: rgba(0, 240, 255, 0.45);
            --purple-neon: #bf40ff;
            --purple-glow: rgba(191, 64, 255, 0.4);
            --green-status: #00ff88;
            --red-error: #ff3366;
            --text-primary: #ffffff;
            --text-secondary: #94a3b8;
            --text-muted: #64748b;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Inter', sans-serif;
            -webkit-tap-highlight-color: transparent;
        }

        body {
            background-color: var(--bg-base);
            background-image: 
                radial-gradient(circle at 15% 15%, rgba(0, 240, 255, 0.09) 0%, transparent 42%),
                radial-gradient(circle at 85% 85%, rgba(191, 64, 255, 0.1) 0%, transparent 45%),
                linear-gradient(rgba(255, 255, 255, 0.02) 1px, transparent 1px),
                linear-gradient(90deg, rgba(255, 255, 255, 0.02) 1px, transparent 1px);
            background-size: 100% 100%, 100% 100%, 28px 28px, 28px 28px;
            color: var(--text-primary);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            padding: 20px 14px 90px;
            overflow-x: hidden;
        }

        .app-container {
            width: 100%;
            max-width: 440px;
            display: flex;
            flex-direction: column;
            position: relative;
        }

        /* RGB LIGHTING EFFECT BASE */
        @keyframes rgbSpin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        @keyframes rgbPulse {
            0%, 100% { box-shadow: 0 0 15px rgba(0, 240, 255, 0.5), 0 0 25px rgba(255, 0, 85, 0.35); }
            50% { box-shadow: 0 0 25px rgba(0, 255, 136, 0.6), 0 0 35px rgba(191, 64, 255, 0.5); }
        }

        .rgb-border {
            position: relative;
            z-index: 1;
            overflow: hidden;
        }

        .rgb-border::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: conic-gradient(#ff0055, #ffbe0b, #00ff66, #00f0ff, #bf40ff, #ff0055);
            animation: rgbSpin 3s linear infinite;
            z-index: -2;
        }

        .rgb-border::after {
            content: '';
            position: absolute;
            inset: 2px;
            background: #0a0e1c;
            border-radius: inherit;
            z-index: -1;
        }

        /* HEADER */
        .app-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding-bottom: 16px;
            margin-bottom: 16px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.07);
        }

        .header-brand {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        /* CUSTOM LOGO WITH RGB LIGHTING */
        .logo-avatar-wrap {
            width: 50px;
            height: 50px;
            border-radius: 50%;
            padding: 2.5px;
            animation: rgbPulse 3s infinite ease-in-out;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .logo-avatar-img {
            width: 100%;
            height: 100%;
            border-radius: 50%;
            object-fit: cover;
            display: block;
        }

        .header-titles h1 {
            font-family: 'Rajdhani', sans-serif;
            font-size: 1.35rem;
            font-weight: 700;
            letter-spacing: 1.2px;
            color: #fff;
            line-height: 1.1;
        }

        .header-titles span {
            font-size: 0.72rem;
            color: var(--cyan-neon);
            font-weight: 600;
            letter-spacing: 0.8px;
            display: flex;
            align-items: center;
            gap: 5px;
            margin-top: 3px;
        }

        .status-badge {
            display: flex;
            align-items: center;
            gap: 6px;
            padding: 6px 12px;
            border-radius: 20px;
            background: rgba(0, 255, 136, 0.08);
            border: 1px solid rgba(0, 255, 136, 0.3);
            font-size: 0.7rem;
            font-weight: 700;
            color: var(--green-status);
        }

        .pulse-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: var(--green-status);
            box-shadow: 0 0 8px var(--green-status);
            animation: blink 1.6s infinite;
        }

        @keyframes blink {
            0%, 100% { opacity: 1; transform: scale(1); }
            50% { opacity: 0.4; transform: scale(0.85); }
        }

        /* METRICS STRIP */
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 8px;
            margin-bottom: 16px;
        }

        .stat-box {
            background: var(--card-bg);
            border: 1px solid rgba(255, 255, 255, 0.06);
            border-radius: 12px;
            padding: 10px 6px;
            text-align: center;
            display: flex;
            flex-direction: column;
            gap: 2px;
        }

        .stat-lbl {
            font-size: 0.62rem;
            color: var(--text-muted);
            font-weight: 600;
            letter-spacing: 0.5px;
        }

        .stat-val {
            font-family: 'Rajdhani', sans-serif;
            font-size: 1.05rem;
            font-weight: 700;
            color: #fff;
        }

        .text-cyan { color: var(--cyan-neon); }
        .text-green { color: var(--green-status); }

        /* GLASSMORPHISM CARD */
        .glass-card {
            background: var(--card-bg);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid var(--card-border);
            border-radius: 20px;
            padding: 20px;
            margin-bottom: 16px;
            box-shadow: 0 10px 35px rgba(0, 0, 0, 0.45);
            position: relative;
        }

        .card-head {
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 16px;
        }

        .head-icon {
            width: 38px;
            height: 38px;
            border-radius: 10px;
            background: rgba(0, 240, 255, 0.1);
            color: var(--cyan-neon);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1rem;
            border: 1px solid rgba(0, 240, 255, 0.25);
        }

        .head-text h2 {
            font-family: 'Rajdhani', sans-serif;
            font-size: 1.15rem;
            font-weight: 700;
            letter-spacing: 0.8px;
        }

        .head-text p {
            font-size: 0.74rem;
            color: var(--text-secondary);
        }

        /* FORM */
        .form-group {
            margin-bottom: 16px;
        }

        .form-label {
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 0.72rem;
            font-weight: 600;
            color: var(--text-secondary);
            letter-spacing: 0.8px;
            margin-bottom: 8px;
        }

        .badge-req {
            font-size: 0.62rem;
            background: rgba(191, 64, 255, 0.15);
            color: var(--purple-neon);
            padding: 2px 6px;
            border-radius: 4px;
            border: 1px solid rgba(191, 64, 255, 0.3);
        }

        .input-wrap {
            position: relative;
            display: flex;
            align-items: center;
        }

        .input-wrap i.prefix {
            position: absolute;
            left: 14px;
            color: var(--text-muted);
            font-size: 0.95rem;
            pointer-events: none;
        }

        .cyber-input {
            width: 100%;
            height: 50px;
            background: rgba(8, 12, 22, 0.9);
            border: 1px solid rgba(255, 255, 255, 0.12);
            border-radius: 12px;
            padding: 0 42px 0 40px;
            color: #fff;
            font-size: 0.9rem;
            outline: none;
            transition: all 0.25s ease;
        }

        .cyber-input:focus {
            border-color: var(--cyan-neon);
            box-shadow: 0 0 14px var(--cyan-glow);
        }

        .clear-btn {
            position: absolute;
            right: 12px;
            background: none;
            border: none;
            color: var(--text-muted);
            cursor: pointer;
            font-size: 0.95rem;
            display: none;
        }

        .clear-btn:hover { color: #fff; }

        /* SEND BUTTON WITH RGB LIGHTING */
        .send-btn {
            width: 100%;
            height: 52px;
            border-radius: 14px;
            color: #ffffff;
            font-family: 'Rajdhani', sans-serif;
            font-size: 1.15rem;
            font-weight: 700;
            letter-spacing: 1.2px;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
            border: none;
            transition: all 0.25s ease;
        }

        .send-btn:hover:not(:disabled) {
            transform: translateY(-2px);
            box-shadow: 0 0 30px var(--cyan-glow), 0 0 45px var(--purple-glow);
        }

        .send-btn:active {
            transform: scale(0.98);
        }

        .send-btn:disabled {
            opacity: 0.65;
            cursor: not-allowed;
        }

        .spinner {
            display: none;
            width: 20px;
            height: 20px;
            border: 2.5px solid rgba(255, 255, 255, 0.3);
            border-radius: 50%;
            border-top-color: #fff;
            animation: spin 0.7s linear infinite;
        }

        @keyframes spin { to { transform: rotate(360deg); } }

        /* CONTACT BUTTONS WITH RGB LIGHTING */
        .contact-section {
            margin-bottom: 16px;
        }

        .section-label {
            font-family: 'Rajdhani', sans-serif;
            font-size: 0.92rem;
            font-weight: 700;
            letter-spacing: 0.8px;
            margin-bottom: 10px;
            color: #e2e8f0;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .contact-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
        }

        .contact-btn {
            height: 52px;
            border-radius: 14px;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
            text-decoration: none;
            color: #ffffff;
            transition: all 0.25s ease;
        }

        .contact-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 0 20px rgba(0, 240, 255, 0.4), 0 0 30px rgba(191, 64, 255, 0.3);
        }

        .contact-btn:active {
            transform: scale(0.97);
        }

        .contact-btn i {
            font-size: 1.4rem;
        }

        .contact-btn.tg i { color: #229ed9; text-shadow: 0 0 10px rgba(34, 158, 217, 0.6); }
        .contact-btn.wa i { color: #25d366; text-shadow: 0 0 10px rgba(37, 211, 102, 0.6); }

        .btn-text-block {
            display: flex;
            flex-direction: column;
            text-align: left;
        }

        .btn-main-title {
            font-family: 'Rajdhani', sans-serif;
            font-size: 0.88rem;
            font-weight: 700;
            line-height: 1;
        }

        .btn-sub-value {
            font-size: 0.72rem;
            color: var(--text-secondary);
        }

        /* TERMINAL LOG CARD */
        .terminal-card {
            background: #04070d;
            border: 1px solid rgba(0, 240, 255, 0.22);
            padding: 0;
            overflow: hidden;
        }

        .term-head {
            background: rgba(14, 20, 36, 0.9);
            border-bottom: 1px solid rgba(255, 255, 255, 0.08);
            padding: 10px 14px;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }

        .term-dots {
            display: flex;
            align-items: center;
            gap: 6px;
        }

        .dot { width: 9px; height: 9px; border-radius: 50%; }
        .dot.r { background: #ff5f56; }
        .dot.y { background: #ffbd2e; }
        .dot.g { background: #27c93f; }

        .term-title {
            font-family: 'Fira Code', monospace;
            font-size: 0.75rem;
            color: var(--cyan-neon);
            font-weight: 500;
            margin-left: 8px;
        }

        .term-clear {
            background: transparent;
            border: none;
            color: var(--text-muted);
            font-size: 0.7rem;
            font-weight: 600;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 4px;
        }

        .term-clear:hover { color: #fff; }

        .term-body {
            height: 160px;
            overflow-y: auto;
            padding: 12px;
            font-family: 'Fira Code', monospace;
            font-size: 0.76rem;
            display: flex;
            flex-direction: column;
            gap: 6px;
        }

        .log-row { word-break: break-word; line-height: 1.4; }
        .ts { color: var(--text-muted); }
        .info { color: #38bdf8; }
        .success { color: var(--green-status); }
        .error { color: var(--red-error); }
        .warn { color: var(--yellow-warn); }

        /* TABS VIEWS */
        .tab-content {
            display: none;
            animation: fadeIn 0.25s ease;
        }

        .tab-content.active { display: block; }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(6px); }
            to { opacity: 1; transform: translateY(0); }
        }

        /* BOTTOM NAV */
        .bottom-nav {
            position: fixed;
            bottom: 0;
            left: 50%;
            transform: translateX(-50%);
            width: 100%;
            max-width: 440px;
            height: 64px;
            background: rgba(10, 14, 24, 0.94);
            backdrop-filter: blur(14px);
            -webkit-backdrop-filter: blur(14px);
            border-top: 1px solid rgba(255, 255, 255, 0.08);
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            z-index: 100;
        }

        .nav-btn {
            background: transparent;
            border: none;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            gap: 4px;
            color: var(--text-muted);
            cursor: pointer;
            font-size: 0.7rem;
            font-weight: 600;
            transition: all 0.2s;
        }

        .nav-btn i { font-size: 1.15rem; }
        .nav-btn.active { color: var(--cyan-neon); }

        /* SETTINGS ROWS */
        .setting-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 12px 0;
            border-bottom: 1px solid rgba(255, 255, 255, 0.06);
        }

        .setting-row:last-child { border-bottom: none; }

        .setting-info span {
            font-size: 0.85rem;
            font-weight: 600;
            display: block;
        }

        .setting-info small {
            font-size: 0.72rem;
            color: var(--text-muted);
        }

        .badge {
            padding: 4px 8px;
            border-radius: 6px;
            font-size: 0.7rem;
            font-weight: 700;
        }

        .badge-online {
            background: rgba(0, 255, 136, 0.12);
            color: var(--green-status);
            border: 1px solid rgba(0, 255, 136, 0.25);
        }

        .about-box {
            background: rgba(8, 12, 22, 0.6);
            border: 1px dashed rgba(191, 64, 255, 0.35);
            border-radius: 12px;
            padding: 14px;
            font-size: 0.78rem;
            line-height: 1.6;
            margin-top: 14px;
        }

        .about-box b { color: var(--cyan-neon); }

        /* TOAST */
        .toast-box {
            position: fixed;
            top: 20px;
            left: 50%;
            transform: translateX(-50%);
            z-index: 1000;
            display: flex;
            flex-direction: column;
            gap: 8px;
            width: 90%;
            max-width: 400px;
            pointer-events: none;
        }

        .toast-item {
            background: rgba(13, 19, 33, 0.96);
            border: 1px solid rgba(255, 255, 255, 0.12);
            color: #fff;
            padding: 12px 16px;
            border-radius: 10px;
            font-size: 0.82rem;
            display: flex;
            align-items: center;
            gap: 10px;
            box-shadow: 0 8px 30px rgba(0, 0, 0, 0.6);
            animation: slideDown 0.3s ease;
        }

        .toast-item.succ { border-color: var(--green-status); }
        .toast-item.err { border-color: var(--red-error); }
        .toast-item.inf { border-color: var(--cyan-neon); }

        @keyframes slideDown {
            from { opacity: 0; transform: translateY(-12px); }
            to { opacity: 1; transform: translateY(0); }
        }
    </style>
</head>
<body>

<div class="app-container">
    <!-- APP HEADER (WITH CUSTOM LOGO) -->
    <header class="app-header">
        <div class="header-brand">
            <div class="logo-avatar-wrap rgb-border">
                <img src="https://i.ibb.co/bgF7Hr4d/188def88e834.png" alt="Noyon Logo" class="logo-avatar-img">
            </div>
            <div class="header-titles">
                <h1>W8 OTP SENDER</h1>
                <span><i class="fa-solid fa-shield-halved"></i> CREDIT BY NOYON</span>
            </div>
        </div>
        <div class="status-badge">
            <div class="pulse-dot"></div>
            <span>ONLINE</span>
        </div>
    </header>

    <!-- MAIN VIEW WRAPPER -->
    <main>
        <!-- ================= TAB 1: HOME ================= -->
        <section class="tab-content active" id="tabHome">
            <!-- STATS STRIP -->
            <div class="stats-grid">
                <div class="stat-box">
                    <span class="stat-lbl">TOTAL SENT</span>
                    <span class="stat-val" id="statSent">0</span>
                </div>
                <div class="stat-box">
                    <span class="stat-lbl">SUCCESS RATE</span>
                    <span class="stat-val text-cyan" id="statRate">100%</span>
                </div>
                <div class="stat-box">
                    <span class="stat-lbl">GATEWAY</span>
                    <span class="stat-val text-green">ACTIVE</span>
                </div>
            </div>

            <!-- OTP FORM CARD -->
            <div class="glass-card">
                <div class="card-head">
                    <div class="head-icon"><i class="fa-solid fa-paper-plane"></i></div>
                    <div class="head-text">
                        <h2>DISPATCH OTP CODE</h2>
                        <p>Official Garena SSO Unsubscribe Endpoint</p>
                    </div>
                </div>

                <div class="form-group">
                    <div class="form-label">
                        <span>EMAIL ADDRESS</span>
                        <span class="badge-req">REQUIRED</span>
                    </div>
                    <div class="input-wrap">
                        <i class="fa-regular fa-envelope prefix"></i>
                        <input type="email" id="emailInput" class="cyber-input" placeholder="Enter target email address" autocomplete="email" spellcheck="false">
                        <button type="button" class="clear-btn" id="clearBtn"><i class="fa-solid fa-xmark"></i></button>
                    </div>
                </div>

                <!-- SEND OTP BUTTON WITH RGB LIGHTING -->
                <button type="button" class="send-btn rgb-border" id="sendBtn">
                    <div class="spinner" id="btnSpinner"></div>
                    <span id="btnText"><i class="fa-solid fa-bolt"></i> SEND OTP</span>
                </button>
            </div>

            <!-- DIRECT CONTACT BUTTONS (WITH RGB LIGHTING) -->
            <div class="contact-section">
                <div class="section-label">
                    <i class="fa-solid fa-headset text-cyan"></i>
                    <span>DEVELOPER CONTACT & SUPPORT</span>
                </div>
                <div class="contact-grid">
                    <a href="https://t.me/w8noyon" target="_blank" rel="noopener noreferrer" class="contact-btn rgb-border tg">
                        <i class="fa-brands fa-telegram"></i>
                        <div class="btn-text-block">
                            <span class="btn-main-title">TELEGRAM</span>
                            <span class="btn-sub-value">@w8noyon</span>
                        </div>
                    </a>
                    <a href="https://wa.me/8801717897877" target="_blank" rel="noopener noreferrer" class="contact-btn rgb-border wa">
                        <i class="fa-brands fa-whatsapp"></i>
                        <div class="btn-text-block">
                            <span class="btn-main-title">WHATSAPP</span>
                            <span class="btn-sub-value">01717897877</span>
                        </div>
                    </a>
                </div>
            </div>

            <!-- TERMINAL LIVE LOG -->
            <div class="glass-card terminal-card">
                <div class="term-head">
                    <div class="term-dots">
                        <div class="dot r"></div>
                        <div class="dot y"></div>
                        <div class="dot g"></div>
                        <span class="term-title"><i class="fa-solid fa-terminal"></i> LIVE ACTIVITY</span>
                    </div>
                    <button type="button" class="term-clear" id="clearTerminalBtn">
                        <i class="fa-solid fa-trash-can"></i> CLEAR
                    </button>
                </div>
                <div class="term-body" id="terminalBody"></div>
            </div>
        </section>

        <!-- ================= TAB 2: LOGS ================= -->
        <section class="tab-content" id="tabLogs">
            <div class="glass-card">
                <div class="card-head">
                    <div class="head-icon"><i class="fa-solid fa-clock-rotate-left"></i></div>
                    <div class="head-text">
                        <h2>REQUEST LOGS</h2>
                        <p>Session history of all dispatched requests</p>
                    </div>
                </div>
                <div id="historyContainer" style="display: flex; flex-direction: column; gap: 8px;">
                    <div id="emptyHistory" style="text-align: center; color: var(--text-muted); padding: 30px 10px; font-size: 0.85rem;">
                        <i class="fa-regular fa-folder-open" style="font-size: 1.8rem; margin-bottom: 8px; display: block;"></i>
                        No requests logged in this session yet.
                    </div>
                </div>
            </div>
        </section>

        <!-- ================= TAB 3: SETTINGS ================= -->
        <section class="tab-content" id="tabSettings">
            <div class="glass-card">
                <div class="card-head">
                    <div class="head-icon"><i class="fa-solid fa-sliders"></i></div>
                    <div class="head-text">
                        <h2>SYSTEM STATUS</h2>
                        <p>Gateway & Developer Diagnostic Information</p>
                    </div>
                </div>

                <div class="setting-row">
                    <div class="setting-info">
                        <span>Upstream SSO Endpoint</span>
                        <small>allo-gang.vercel.app/api/send-code</small>
                    </div>
                    <span class="badge badge-online">CONNECTED</span>
                </div>

                <div class="setting-row">
                    <div class="setting-info">
                        <span>Backend Server</span>
                        <small>Python Flask Gateway</small>
                    </div>
                    <span class="badge badge-online">OPERATIONAL</span>
                </div>

                <div class="about-box">
                    <div><b>Project:</b> W8 OTP SENDER</div>
                    <div><b>Developer:</b> @NOYON_OFFICIAL_99</div>
                    <div><b>Associate:</b> @CODEX_NOYON</div>
                    <div><b>Telegram Contact:</b> @w8noyon</div>
                    <div><b>WhatsApp Contact:</b> 01717897877</div>
                    <div><b>Version:</b> 2.5.0 RGB Cyber Edition</div>
                </div>
            </div>
        </section>
    </main>

    <!-- MOBILE BOTTOM NAVIGATION -->
    <nav class="bottom-nav">
        <button type="button" class="nav-btn active" data-target="tabHome">
            <i class="fa-solid fa-house"></i>
            <span>HOME</span>
        </button>
        <button type="button" class="nav-btn" data-target="tabLogs">
            <i class="fa-solid fa-list-check"></i>
            <span>LOGS</span>
        </button>
        <button type="button" class="nav-btn" data-target="tabSettings">
            <i class="fa-solid fa-gear"></i>
            <span>SETTINGS</span>
        </button>
    </nav>
</div>

<!-- TOAST ALERT CONTAINER -->
<div class="toast-box" id="toastBox"></div>

<script>
    document.addEventListener('DOMContentLoaded', () => {
        const emailInput = document.getElementById('emailInput');
        const clearBtn = document.getElementById('clearBtn');
        const sendBtn = document.getElementById('sendBtn');
        const btnSpinner = document.getElementById('btnSpinner');
        const btnText = document.getElementById('btnText');
        const terminalBody = document.getElementById('terminalBody');
        const clearTerminalBtn = document.getElementById('clearTerminalBtn');

        const statSent = document.getElementById('statSent');
        const statRate = document.getElementById('statRate');
        const historyContainer = document.getElementById('historyContainer');
        const emptyHistory = document.getElementById('emptyHistory');

        let totalRequests = 0;
        let successRequests = 0;

        // Terminal Log Appender
        function appendLog(text, type = 'info') {
            const now = new Date();
            const timeStr = now.toTimeString().split(' ')[0];
            const div = document.createElement('div');
            div.className = 'log-row';
            
            let prefix = '>>';
            if (type === 'success') prefix = '[✓]';
            if (type === 'error') prefix = '[✗]';
            if (type === 'warn') prefix = '[!]';

            div.innerHTML = `<span class="ts">[${timeStr}]</span> <span class="${type}">${prefix} ${text}</span>`;
            terminalBody.appendChild(div);
            terminalBody.scrollTop = terminalBody.scrollHeight;
        }

        // Toast System
        function showToast(msg, type = 'inf') {
            const toastBox = document.getElementById('toastBox');
            const toast = document.createElement('div');
            toast.className = `toast-item ${type}`;

            let icon = '<i class="fa-solid fa-circle-info text-cyan"></i>';
            if (type === 'succ') icon = '<i class="fa-solid fa-circle-check text-green"></i>';
            if (type === 'err') icon = '<i class="fa-solid fa-circle-xmark text-pink"></i>';

            toast.innerHTML = `${icon}<span>${msg}</span>`;
            toastBox.appendChild(toast);

            setTimeout(() => {
                toast.style.opacity = '0';
                setTimeout(() => toast.remove(), 300);
            }, 3000);
        }

        // Initialize Terminal
        appendLog('System initialized. W8 Gateway ready.', 'info');
        appendLog('SSO Endpoint: https://allo-gang.vercel.app/api/send-code', 'info');

        // Input clear handler
        emailInput.addEventListener('input', () => {
            clearBtn.style.display = emailInput.value.trim().length > 0 ? 'block' : 'none';
        });

        clearBtn.addEventListener('click', () => {
            emailInput.value = '';
            clearBtn.style.display = 'none';
            emailInput.focus();
        });

        clearTerminalBtn.addEventListener('click', () => {
            terminalBody.innerHTML = '';
            appendLog('Terminal logs cleared.', 'warn');
        });

        // Bottom Navigation Switcher
        document.querySelectorAll('.nav-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));
                document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));

                btn.classList.add('active');
                document.getElementById(btn.dataset.target).classList.add('active');
            });
        });

        // Send OTP Action
        sendBtn.addEventListener('click', async () => {
            const email = emailInput.value.trim().toLowerCase();

            if (!email) {
                showToast('Please enter an email address.', 'err');
                appendLog('Validation failed: Empty email input.', 'error');
                return;
            }

            const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
            if (!emailRegex.test(email)) {
                showToast('Invalid email address format.', 'err');
                appendLog(`Validation failed: [${email}] is invalid.`, 'error');
                return;
            }

            // Lock button & show loading state
            sendBtn.disabled = true;
            btnSpinner.style.display = 'block';
            btnText.innerHTML = 'DISPATCHING...';

            appendLog(`Target Email: ${email}`, 'info');
            appendLog('Connecting to Garena SSO Gateway...', 'info');

            try {
                const res = await fetch('/api/send-otp', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ email: email })
                });

                const data = await res.json();
                totalRequests++;

                if (res.ok && data.success) {
                    successRequests++;
                    showToast(data.message, 'succ');
                    appendLog(`Success: ${data.message}`, 'success');
                    appendLog('OTP sent to email. Check inbox / spam.', 'success');
                    addHistoryItem(email, 'SUCCESS', 'green');
                } else {
                    const err = data.message || 'OTP Send Failed';
                    showToast(err, 'err');
                    appendLog(`Failed: ${err}`, 'error');
                    addHistoryItem(email, 'FAILED', 'red');
                }
            } catch (err) {
                totalRequests++;
                showToast('Network error while reaching server.', 'err');
                appendLog(`Network Exception: ${err.message}`, 'error');
                addHistoryItem(email, 'ERROR', 'red');
            } finally {
                // Update metrics
                statSent.textContent = totalRequests;
                const rate = Math.round((successRequests / totalRequests) * 100);
                statRate.textContent = `${rate}%`;

                // Re-enable button
                sendBtn.disabled = false;
                btnSpinner.style.display = 'none';
                btnText.innerHTML = '<i class="fa-solid fa-bolt"></i> SEND OTP';
            }
        });

        // Add to history tab
        function addHistoryItem(email, status, color) {
            if (emptyHistory) emptyHistory.style.display = 'none';
            const now = new Date();
            const timeStr = now.toTimeString().split(' ')[0];

            const item = document.createElement('div');
            item.style.cssText = 'padding: 10px 14px; background: rgba(8, 12, 22, 0.7); border: 1px solid rgba(255, 255, 255, 0.05); border-radius: 10px; display: flex; justify-content: space-between; align-items: center;';
            item.innerHTML = `
                <div>
                    <span style="font-size: 0.85rem; font-weight: 600; color: #fff;">${email}</span><br>
                    <small style="font-size: 0.7rem; color: var(--text-muted);">${timeStr}</small>
                </div>
                <span style="font-size: 0.72rem; font-weight: 700; color: var(--${color == 'green' ? 'green-status' : 'red-error'});">${status}</span>
            `;
            historyContainer.prepend(item);
        }
    });
</script>

</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML_PAGE)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"🚀 W8 OTP SENDER (Credit: Noyon) Running on http://127.0.0.1:{port}")
    app.run(host="0.0.0.0", port=port, debug=False)
