#!/usr/bin/env python3
import os
import re
import time
from pathlib import Path
from urllib import error, request
import json

from dotenv import load_dotenv
from flask import Flask, abort, jsonify, request as flask_request, send_file, send_from_directory

ROOT = Path(__file__).parent
load_dotenv(ROOT / ".env")

from generate_legal_pdf import OUT as LEGAL_PDF, build as build_pdf

app = Flask(__name__, static_folder=None)
WEBHOOK = os.environ.get("DISCORD_WEBHOOK_URL", "").strip()
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
NAME_RE = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9_-]{1,31}$")
_last_hit = {}


def price_of(cpu: int, ram_mb: int, disk_gb: int) -> int:
    return round(cpu * 40 + ram_mb * 0.6 + disk_gb * 90)


def rate_ok(ip: str) -> bool:
    now = time.time()
    prev = _last_hit.get(ip, 0)
    if now - prev < 8:
        return False
    _last_hit[ip] = now
    return True


@app.get("/")
def index():
    return send_from_directory(ROOT, "index.html")


@app.get("/static/<path:name>")
def static_files(name):
    return send_from_directory(ROOT / "static", name)


@app.get("/adatkezeles/")
@app.get("/adatkezeles/index.html")
def legal_page():
    return send_from_directory(ROOT / "adatkezeles", "index.html")


@app.get("/adatkezeles/adatkezeles.pdf")
def legal_pdf_file():
    if not LEGAL_PDF.exists():
        build_pdf()
    public = ROOT / "adatkezeles" / "adatkezeles.pdf"
    path = public if public.exists() else LEGAL_PDF
    return send_file(path, mimetype="application/pdf")


@app.get("/adatkezeles")
@app.get("/adatkezeles.pdf")
@app.get("/aszf")
@app.get("/aszf.html")
def legal():
    if not LEGAL_PDF.exists():
        build_pdf()
    return send_file(LEGAL_PDF, mimetype="application/pdf", download_name="dewyhosting-adatkezeles.pdf")


@app.post("/api/order")
def order():
    if not WEBHOOK:
        return jsonify(ok=False, error="A rendelési csatorna nincs beállítva."), 500
    ip = flask_request.headers.get("X-Forwarded-For", flask_request.remote_addr or "0").split(",")[0].strip()
    if not rate_ok(ip):
        return jsonify(ok=False, error="Túl gyorsan küldted. Várj néhány másodpercet."), 429

    data = flask_request.get_json(silent=True) or {}
    server = str(data.get("serverName", "")).strip()
    email = str(data.get("email", "")).strip()
    kind = str(data.get("kind", "")).strip()
    coupon = str(data.get("coupon", "")).strip().upper()
    accepted = bool(data.get("acceptedLegal"))

    if not NAME_RE.match(server):
        return jsonify(ok=False, error="A szerver neve 2–32 karakter, betű/szám/_/-."), 400
    if not EMAIL_RE.match(email):
        return jsonify(ok=False, error="Adj meg egy érvényes e-mail címet."), 400
    if not accepted:
        return jsonify(ok=False, error="Az adatkezelési tájékoztató elfogadása kötelező."), 400

    if kind == "discord":
        cpu, ram, disk = 3, 300, 1
        label = "Discord csomag"
    elif kind == "custom":
        try:
            cpu = int(data.get("cpu"))
            ram = int(data.get("ram"))
            disk = int(data.get("disk"))
        except (TypeError, ValueError):
            return jsonify(ok=False, error="Az egyedi csomag értékei hibásak."), 400
        if not (1 <= cpu <= 50 and 128 <= ram <= 4096 and 1 <= disk <= 50):
            return jsonify(ok=False, error="Az egyedi csomag tartományon kívül esik."), 400
        label = "Egyedi csomag"
    else:
        return jsonify(ok=False, error="Válassz csomagot."), 400

    base = price_of(cpu, ram, disk)
    discount = 0.2 if coupon == "HELLO20" else 0.0
    final = round(base * (1 - discount))

    embed = {
        "title": "Új DewyHosting rendelés",
        "color": 16744192,
        "fields": [
            {"name": "Szerver neve", "value": server, "inline": True},
            {"name": "E-mail", "value": email, "inline": True},
            {"name": "Csomag", "value": label, "inline": True},
            {"name": "CPU", "value": f"{cpu}%", "inline": True},
            {"name": "RAM", "value": f"{ram} MB", "inline": True},
            {"name": "Tárhely", "value": f"{disk} GB", "inline": True},
            {"name": "Hálózat", "value": "1 Gbps", "inline": True},
            {"name": "Lokáció", "value": "Frankfurt, node1", "inline": True},
            {"name": "Kupon", "value": coupon or "—", "inline": True},
            {"name": "Listaár", "value": f"{base} Ft/hó", "inline": True},
            {"name": "Fizetendő", "value": f"{final} Ft/hó", "inline": True},
        ],
        "footer": {"text": "DewyHosting · hobbi projekt · Németország, Frankfurt"},
    }
    payload = json.dumps({"username": "DewyHosting", "embeds": [embed]}).encode("utf-8")
    req = request.Request(
        WEBHOOK,
        data=payload,
        headers={"Content-Type": "application/json", "User-Agent": "DewyHosting/1.0"},
        method="POST",
    )
    try:
        with request.urlopen(req, timeout=12) as resp:
            if resp.status not in (200, 204):
                raise RuntimeError(resp.status)
    except error.HTTPError as exc:
        return jsonify(ok=False, error="A Discord értesítés nem ment ki."), 502 if exc.code >= 500 else 400
    except Exception:
        return jsonify(ok=False, error="A Discord értesítés nem ment ki."), 502

    return jsonify(ok=True, price=final, base=base, discount=discount)


def main():
    if not LEGAL_PDF.exists():
        build_pdf()
    port = int(os.environ.get("PORT", "5050"))
    app.run(host="0.0.0.0", port=port, debug=False)


if __name__ == "__main__":
    main()
