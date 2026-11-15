"""MkDocs hook for the local-only full Teacher Portal (`mkdocs.docente.yml`).

Exposes unpublished `publicar: false` practice solutions, `privado_evaluacion/`
exams/rubrics/solutions, `raw/procesados/` curated sources, and a dynamic
Obsidian-style Graph View without duplicating any source files or altering the
public student build (`mkdocs.yml`).
"""

from __future__ import annotations

import json
import os
import re
from pathlib import Path
from typing import Any

from mkdocs.structure.files import File

_TITLE_RE = re.compile(r"^#\s+(.+)$", re.MULTILINE)
_FM_RE = re.compile(r"^\ufeff?---\r?\n(.*?)\r?\n---(?:\r?\n|$)", re.DOTALL)
_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)#]+\.md)(?:#[^)]*)?\)")
_RA_RE = re.compile(r"(?:^|[/_-])(ra[1-7]|RA[1-7])(?:[/_.-]|$)")


def _repo_root(config: Any) -> Path:
    """Return repository root derived from `docs_dir` (`wiki/`)."""
    return Path(config.docs_dir).resolve().parent


def _extract_title(path: Path) -> str:
    """Extract the first Markdown H1 heading, falling back to filename."""
    try:
        txt = path.read_text(encoding="utf-8")
    except OSError:
        return path.stem
    m = _TITLE_RE.search(txt)
    if m:
        return m.group(1).strip()
    return path.stem


def _is_private_frontmatter(txt: str) -> bool:
    """Return True when YAML frontmatter sets `publicar: false`."""
    m = _FM_RE.match(txt)
    if not m:
        return False
    return bool(re.search(r"^publicar:\s*false\b", m.group(1), re.MULTILINE))


def _nav_label(path: Path, prefix: str = "") -> str:
    """Build a concise human-readable sidebar label for private/raw docs."""
    title = _extract_title(path)
    ra_m = _RA_RE.search(path.name)
    ra = ra_m.group(1).upper() if ra_m else ""
    short = title if len(title) <= 58 else title[:55].rstrip() + "…"
    if prefix and ra and ra not in short:
        return f"{ra} · {prefix}: {short}"
    return short


def _collect_graph_payload(repo_root: Path, site_dir: str, use_directory_urls: bool) -> dict[str, Any]:
    """Scan wiki/, raw/procesados/, and privado_evaluacion/ to build graph JSON."""
    wiki_dir = repo_root / "wiki"
    raw_dir = repo_root / "raw" / "procesados"
    priv_dir = repo_root / "privado_evaluacion"

    md_paths = sorted(
        list(wiki_dir.rglob("*.md"))
        + (list(raw_dir.glob("*.md")) if raw_dir.exists() else [])
        + (list(priv_dir.rglob("*.md")) if priv_dir.exists() else [])
    )

    nodes: list[dict[str, Any]] = []
    idx_map: dict[str, int] = {}

    for p in md_paths:
        rel_repo = p.relative_to(repo_root).as_posix()
        txt = p.read_text(encoding="utf-8")
        m_title = _TITLE_RE.search(txt)
        title = m_title.group(1).strip() if m_title else p.name
        stem = p.stem

        if rel_repo.startswith("wiki/"):
            rel_wiki = p.relative_to(wiki_dir).as_posix()
            mk_path = rel_wiki
            src_dir = str(wiki_dir)
            cat = rel_wiki.split("/")[0] if "/" in rel_wiki else "portada"
            is_priv = _is_private_frontmatter(txt)
            if rel_repo == "wiki/index.md":
                label = "Inicio"
            elif rel_repo == "wiki/log.md":
                label = "log.md"
            elif stem == "index":
                label = f"{cat}/index"
            elif cat == "ra":
                label = stem
            else:
                label = stem[:28] + ("…" if len(stem) > 28 else "")
        elif rel_repo.startswith("raw/"):
            mk_path = rel_repo
            src_dir = str(repo_root)
            cat = "raw"
            is_priv = False
            label = "raw/" + (stem[:22] + ("…" if len(stem) > 22 else ""))
        else:
            mk_path = rel_repo
            src_dir = str(repo_root)
            cat = "privado"
            is_priv = True
            label = stem[:26] + ("…" if len(stem) > 26 else "")

        fobj = File(
            path=mk_path,
            src_dir=src_dir,
            dest_dir=site_dir,
            use_directory_urls=use_directory_urls,
        )
        ra_m = _RA_RE.search(rel_repo)
        ra = ra_m.group(1).upper() if ra_m else "GLOBAL"

        idx_map[rel_repo] = len(nodes)
        nodes.append(
            {
                "id": rel_repo,
                "l": label,
                "t": title[:90],
                "c": cat,
                "r": ra,
                "p": 1 if is_priv else 0,
                "u": fobj.url,
            }
        )

    edges_set: set[tuple[int, int]] = set()
    for p in md_paths:
        rel_repo = p.relative_to(repo_root).as_posix()
        src_i = idx_map[rel_repo]
        node = nodes[src_i]
        txt = p.read_text(encoding="utf-8")
        cur_dir = p.parent

        for target in _LINK_RE.findall(txt):
            if target.startswith(("http://", "https://")):
                continue
            resolved = (cur_dir / target).resolve()
            try:
                norm_repo = resolved.relative_to(repo_root).as_posix()
            except ValueError:
                continue
            if norm_repo in idx_map and norm_repo != rel_repo:
                edges_set.add((src_i, idx_map[norm_repo]))

        if node["c"] in ("raw", "privado") or (node["c"] == "practicas" and node["p"] == 1):
            if node["r"] != "GLOBAL":
                hub = f"wiki/ra/{node['r']}.md"
                if hub in idx_map and idx_map[hub] != src_i:
                    edges_set.add((idx_map[hub], src_i))

    if "wiki/practicas/p00-plantilla-solucion.md" in idx_map and "wiki/practicas/index.md" in idx_map:
        edges_set.add(
            (idx_map["wiki/practicas/index.md"], idx_map["wiki/practicas/p00-plantilla-solucion.md"])
        )
    if "privado_evaluacion/README.md" in idx_map and "wiki/index.md" in idx_map:
        edges_set.add((idx_map["wiki/index.md"], idx_map["privado_evaluacion/README.md"]))

    return {"nodes": nodes, "edges": sorted(edges_set)}


def _build_graph_markdown(payload: dict[str, Any]) -> str:
    """Render `grafo-docente.md` with an inline, zero-blank-line interactive Graph View."""
    raw_json = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    total_nodes = len(payload["nodes"])
    pub_nodes = sum(1 for n in payload["nodes"] if n["p"] == 0 and n["c"] != "raw")

    html_block = f"""
<div id="wikisi-graph-app">
  <div class="wg-toolbar">
    <div class="wg-controls">
      <input id="wg-search" type="search" placeholder="Buscar .md..." />
      <select id="wg-ra">
        <option value="ALL">Todos los RA</option>
        <option value="GLOBAL">Global / Índices</option>
        <option value="RA1">RA1 · Hardware</option>
        <option value="RA2">RA2 · Instalación SO</option>
        <option value="RA3">RA3 · Discos/Backups</option>
        <option value="RA4">RA4 · Usuarios/ACL</option>
        <option value="RA5">RA5 · Redes TCP/IP</option>
        <option value="RA6">RA6 · Servicios/AD</option>
        <option value="RA7">RA7 · Docs/Correo</option>
      </select>
      <button id="wg-scope" type="button">Portal completo ({total_nodes})</button>
    </div>
    <div class="wg-controls">
      <span id="wg-stats" class="wg-stats"></span>
      <button id="wg-fit" type="button">Ajustar</button>
      <button id="wg-reheat" type="button">Relajar</button>
    </div>
  </div>
  <div class="wg-stage">
    <canvas id="wg-canvas"></canvas>
    <div id="wg-legend" class="wg-legend"></div>
    <div class="wg-hint">Rueda: zoom · Arrastra nodos/fondo · Doble clic: abrir página</div>
  </div>
  <div class="wg-inspector">
    <div class="wg-sel-info">
      <span id="wg-badge" class="wg-badge">grafo</span>
      <span id="wg-title" class="wg-title">Haz clic en un nodo para inspeccionarlo o doble clic para abrir la página en el Portal Docente</span>
    </div>
    <div class="wg-sel-actions">
      <span id="wg-deg" class="wg-stats"></span>
      <a id="wg-open" class="wg-open hidden" href="#">Abrir página en el Portal Docente ↗</a>
    </div>
  </div>
  <div id="wg-neighbors" class="wg-neighbors hidden"></div>
</div>
<style>
  #wikisi-graph-app {{ display: flex; flex-direction: column; gap: 10px; user-select: none; margin-top: 8px; }}
  .wg-toolbar {{ display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 8px; padding-bottom: 8px; border-bottom: 1px solid var(--md-default-fg-color--lightest); }}
  .wg-controls {{ display: flex; flex-wrap: wrap; align-items: center; gap: 6px; }}
  #wikisi-graph-app input, #wikisi-graph-app select, #wikisi-graph-app button {{ font-size: 0.78rem; padding: 5px 9px; border-radius: 6px; border: 1px solid var(--md-default-fg-color--lightest); background: var(--md-default-bg-color); color: var(--md-default-fg-color); }}
  #wikisi-graph-app button {{ cursor: pointer; font-weight: 500; }}
  #wikisi-graph-app button:hover {{ border-color: var(--md-primary-fg-color); }}
  .wg-stats {{ font-family: var(--md-code-font-family, monospace); font-size: 0.74rem; color: var(--md-default-fg-color--light); }}
  .wg-stage {{ position: relative; width: 100%; height: 540px; border-radius: 8px; border: 1px solid var(--md-default-fg-color--lightest); background: var(--md-code-bg-color); overflow: hidden; }}
  #wg-canvas {{ display: block; width: 100%; height: 100%; cursor: grab; touch-action: none; }}
  #wg-canvas:active {{ cursor: grabbing; }}
  .wg-legend {{ position: absolute; top: 10px; left: 10px; display: flex; flex-wrap: wrap; gap: 10px; padding: 5px 9px; border-radius: 6px; font-size: 0.72rem; background: var(--md-default-bg-color); border: 1px solid var(--md-default-fg-color--lightest); pointer-events: none; opacity: 0.92; }}
  .wg-leg-item {{ display: inline-flex; align-items: center; gap: 5px; color: var(--md-default-fg-color); }}
  .wg-dot {{ width: 8px; height: 8px; border-radius: 9999px; display: inline-block; }}
  .wg-hint {{ position: absolute; bottom: 8px; right: 10px; font-size: 0.70rem; padding: 3px 8px; border-radius: 4px; background: var(--md-default-bg-color); color: var(--md-default-fg-color--light); opacity: 0.88; pointer-events: none; }}
  .wg-inspector {{ display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 8px; padding: 6px 0; }}
  .wg-sel-info {{ display: flex; align-items: center; gap: 8px; min-width: 0; flex: 1; }}
  .wg-badge {{ font-family: monospace; font-size: 0.72rem; padding: 2px 7px; border-radius: 4px; border: 1px solid var(--md-default-fg-color--lightest); white-space: nowrap; }}
  .wg-title {{ font-size: 0.80rem; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }}
  .wg-sel-actions {{ display: flex; align-items: center; gap: 8px; }}
  .wg-open {{ font-size: 0.76rem; font-weight: 600; padding: 4px 10px; border-radius: 6px; background: var(--md-primary-fg-color); color: var(--md-primary-bg-color) !important; text-decoration: none !important; }}
  .wg-open:hover {{ opacity: 0.9; }}
  .wg-neighbors {{ display: flex; flex-wrap: wrap; gap: 6px; padding-top: 2px; }}
  .wg-chip {{ font-size: 0.72rem !important; padding: 3px 7px !important; }}
  .hidden {{ display: none !important; }}
</style>
<script>
(function() {{
  const RAW_DATA = {raw_json};
  const PUB_COUNT = {pub_nodes};
  const CAT_META = {{
    ra: {{ label: "RA1–RA7", dark: "#f59e0b", light: "#d97706" }},
    portada: {{ label: "Inicio/Log", dark: "#f43f5e", light: "#e11d48" }},
    conceptos: {{ label: "Conceptos", dark: "#38bdf8", light: "#0284c7" }},
    ejercicios: {{ label: "Ejercicios", dark: "#34d399", light: "#059669" }},
    practicas: {{ label: "Prácticas", dark: "#a78bfa", light: "#7c3aed" }},
    raw: {{ label: "Raw", dark: "#22d3ee", light: "#0891b2" }},
    privado: {{ label: "Privado 🔒", dark: "#f472b6", light: "#db2777" }}
  }};
  const RA_ANGLES = {{
    GLOBAL: null,
    RA1: -Math.PI / 2,
    RA2: -Math.PI / 2 + (1 * 2 * Math.PI) / 7,
    RA3: -Math.PI / 2 + (2 * 2 * Math.PI) / 7,
    RA4: -Math.PI / 2 + (3 * 2 * Math.PI) / 7,
    RA5: -Math.PI / 2 + (4 * 2 * Math.PI) / 7,
    RA6: -Math.PI / 2 + (5 * 2 * Math.PI) / 7,
    RA7: -Math.PI / 2 + (6 * 2 * Math.PI) / 7
  }};
  const canvas = document.getElementById("wg-canvas");
  const ctx = canvas.getContext("2d");
  const searchEl = document.getElementById("wg-search");
  const raEl = document.getElementById("wg-ra");
  const scopeBtn = document.getElementById("wg-scope");
  const fitBtn = document.getElementById("wg-fit");
  const reheatBtn = document.getElementById("wg-reheat");
  const statsEl = document.getElementById("wg-stats");
  const legendEl = document.getElementById("wg-legend");
  const badgeEl = document.getElementById("wg-badge");
  const titleEl = document.getElementById("wg-title");
  const degEl = document.getElementById("wg-deg");
  const openEl = document.getElementById("wg-open");
  const neighborsEl = document.getElementById("wg-neighbors");
  let showAll = true, activeRa = "ALL", query = "";
  let nodes = [], edges = [], adj = new Map(), inAdj = new Map(), outAdj = new Map();
  let cam = {{ x: 0, y: 0, k: 0.9 }};
  let hoveredIdx = -1, selectedIdx = -1, dragIdx = -1;
  let isPanning = false, panStart = {{ x: 0, y: 0, cx: 0, cy: 0 }}, moved = false;
  let alpha = 1.0, rafId = null;
  function isSlate() {{
    return document.body.getAttribute("data-md-color-scheme") === "slate" ||
      document.documentElement.getAttribute("data-md-color-scheme") === "slate";
  }}
  function catColor(c) {{
    const m = CAT_META[c] || CAT_META.conceptos;
    return isSlate() ? m.dark : m.light;
  }}
  function renderLegend() {{
    const cats = showAll
      ? ["portada", "ra", "conceptos", "ejercicios", "practicas", "raw", "privado"]
      : ["portada", "ra", "conceptos", "ejercicios", "practicas"];
    legendEl.innerHTML = cats.map(c =>
      `<span class="wg-leg-item"><span class="wg-dot" style="background:${{catColor(c)}}"></span>${{CAT_META[c].label}}</span>`
    ).join("");
  }}
  function buildSubgraph() {{
    const keep = new Set();
    RAW_DATA.nodes.forEach((n, idx) => {{
      if (!showAll && (n.p === 1 || n.c === "raw" || n.c === "privado")) return;
      if (activeRa !== "ALL") {{
        const isGlobalHub = n.r === "GLOBAL" && (n.c === "portada" || n.id.endsWith("/index.md"));
        if (activeRa === "GLOBAL") {{ if (n.r !== "GLOBAL") return; }}
        else if (n.r !== activeRa && !isGlobalHub) return;
      }}
      keep.add(idx);
    }});
    const oldToNew = new Map();
    const prevPos = new Map(nodes.map(nd => [nd.id, {{ x: nd.x, y: nd.y }}]));
    nodes = [];
    RAW_DATA.nodes.forEach((n, idx) => {{
      if (!keep.has(idx)) return;
      const ni = nodes.length;
      oldToNew.set(idx, ni);
      const angle = RA_ANGLES[n.r];
      let x, y;
      if (prevPos.has(n.id)) {{ x = prevPos.get(n.id).x; y = prevPos.get(n.id).y; }}
      else if (angle == null) {{
        const j = (ni * 2.39996) % (Math.PI * 2);
        const r0 = n.id === "wiki/index.md" ? 0 : 48 + (ni % 5) * 16;
        x = Math.cos(j) * r0; y = Math.sin(j) * r0;
      }} else {{
        const r0 = n.c === "ra" ? 150 : n.c === "raw" ? 260 : n.c === "privado" ? 280 : 215;
        const sp = ((ni % 11) - 5) * 0.085;
        x = Math.cos(angle + sp) * (r0 + ((ni % 4) - 1.5) * 24);
        y = Math.sin(angle + sp) * (r0 + ((ni % 4) - 1.5) * 24);
      }}
      nodes.push({{ ...n, ni, x, y, vx: 0, vy: 0, deg: 0, anchorAngle: angle }});
    }});
    edges = []; adj = new Map(); inAdj = new Map(); outAdj = new Map();
    for (let i = 0; i < nodes.length; i++) {{ adj.set(i, new Set()); inAdj.set(i, new Set()); outAdj.set(i, new Set()); }}
    RAW_DATA.edges.forEach(([s, t]) => {{
      const ns = oldToNew.get(s), nt = oldToNew.get(t);
      if (ns !== undefined && nt !== undefined && ns !== nt) {{
        edges.push([ns, nt]);
        adj.get(ns).add(nt); adj.get(nt).add(ns);
        outAdj.get(ns).add(nt); inAdj.get(nt).add(ns);
        nodes[ns].deg++; nodes[nt].deg++;
      }}
    }});
    hoveredIdx = -1; selectedIdx = -1;
    updateInspector();
    statsEl.textContent = `${{nodes.length}} .md · ${{edges.length}} enlaces`;
    scopeBtn.textContent = showAll ? `Portal completo (${{RAW_DATA.nodes.length}})` : `Solo alumnos (${{PUB_COUNT}})`;
    renderLegend();
    alpha = 1.0;
    startSim();
  }}
  function nodeRadius(n) {{
    if (n.id === "wiki/index.md") return 10;
    if (n.c === "ra") return 8;
    if (n.id.endsWith("/index.md")) return 7;
    return Math.min(7.2, 3.3 + Math.sqrt(n.deg) * 0.88);
  }}
  function stepPhysics() {{
    const N = nodes.length;
    if (!N) return 0;
    for (let i = 0; i < N; i++) {{
      const n = nodes[i];
      if (i === dragIdx) continue;
      if (n.anchorAngle != null) {{
        const tr = n.c === "ra" ? 155 : n.c === "raw" ? 265 : n.c === "privado" ? 285 : 220;
        n.vx += (Math.cos(n.anchorAngle) * tr - n.x) * 0.012 * alpha;
        n.vy += (Math.sin(n.anchorAngle) * tr - n.y) * 0.012 * alpha;
      }} else {{
        n.vx += -n.x * 0.018 * alpha;
        n.vy += -n.y * 0.018 * alpha;
      }}
    }}
    const rep = activeRa === "ALL" ? 640 : 980;
    for (let i = 0; i < N; i++) {{
      const a = nodes[i];
      for (let j = i + 1; j < N; j++) {{
        const b = nodes[j];
        const dx = b.x - a.x, dy = b.y - a.y;
        const d2 = dx * dx + dy * dy + 16;
        if (d2 > 32000) continue;
        const dist = Math.sqrt(d2);
        const f = (rep / d2) * alpha;
        const fx = (dx / dist) * f, fy = (dy / dist) * f;
        if (i !== dragIdx) {{ a.vx -= fx; a.vy -= fy; }}
        if (j !== dragIdx) {{ b.vx += fx; b.vy += fy; }}
      }}
    }}
    const sLen = activeRa === "ALL" ? 70 : 84;
    for (let e = 0; e < edges.length; e++) {{
      const [si, ti] = edges[e];
      const a = nodes[si], b = nodes[ti];
      const dx = b.x - a.x, dy = b.y - a.y;
      const dist = Math.hypot(dx, dy) || 0.1;
      const st = (dist - sLen) * 0.036 * alpha;
      const fx = (dx / dist) * st, fy = (dy / dist) * st;
      if (si !== dragIdx) {{ a.vx += fx; a.vy += fy; }}
      if (ti !== dragIdx) {{ b.vx -= fx; b.vy -= fy; }}
    }}
    let energy = 0;
    for (let i = 0; i < N; i++) {{
      const n = nodes[i];
      if (i === dragIdx) {{ n.vx = 0; n.vy = 0; continue; }}
      n.vx *= 0.80; n.vy *= 0.80;
      const sp = Math.hypot(n.vx, n.vy);
      if (sp > 14) {{ n.vx = (n.vx / sp) * 14; n.vy = (n.vy / sp) * 14; }}
      n.x += n.vx; n.y += n.vy;
      energy += sp;
    }}
    alpha = Math.max(0.02, alpha * 0.992);
    return energy / N;
  }}
  function resizeCanvas() {{
    const rect = canvas.getBoundingClientRect();
    const dpr = window.devicePixelRatio || 1;
    const w = Math.max(320, Math.floor(rect.width));
    const h = Math.max(320, Math.floor(rect.height));
    if (canvas.width !== w * dpr || canvas.height !== h * dpr) {{
      canvas.width = w * dpr; canvas.height = h * dpr;
    }}
    return {{ w, h, dpr }};
  }}
  function draw() {{
    const {{ w, h, dpr }} = resizeCanvas();
    const slate = isSlate();
    const fg = slate ? "#e2e8f0" : "#1e293b";
    const muted = slate ? "#94a3b8" : "#475569";
    const borderCol = slate ? "rgba(226,232,240,0.16)" : "rgba(15,23,42,0.16)";
    ctx.save();
    ctx.scale(dpr, dpr);
    ctx.clearRect(0, 0, w, h);
    ctx.translate(w / 2 + cam.x * cam.k, h / 2 + cam.y * cam.k);
    ctx.scale(cam.k, cam.k);
    const focusIdx = hoveredIdx !== -1 ? hoveredIdx : selectedIdx;
    const focusNbr = focusIdx !== -1 ? adj.get(focusIdx) : null;
    const q = query.trim().toLowerCase();
    const matched = q ? new Set(nodes.filter(n => n.id.toLowerCase().includes(q) || n.t.toLowerCase().includes(q)).map(n => n.ni)) : null;
    for (let e = 0; e < edges.length; e++) {{
      const [si, ti] = edges[e];
      const a = nodes[si], b = nodes[ti];
      const touchesFocus = focusIdx !== -1 && (si === focusIdx || ti === focusIdx);
      const touchesMatch = matched && matched.has(si) && matched.has(ti);
      if (focusIdx !== -1) {{
        ctx.strokeStyle = touchesFocus ? catColor(nodes[focusIdx].c) : borderCol;
        ctx.globalAlpha = touchesFocus ? 0.85 : 0.08;
        ctx.lineWidth = (touchesFocus ? 1.6 : 0.7) / Math.max(0.55, cam.k);
      }} else if (matched) {{
        ctx.strokeStyle = borderCol;
        ctx.globalAlpha = touchesMatch ? 0.6 : 0.08;
        ctx.lineWidth = 0.9 / Math.max(0.55, cam.k);
      }} else {{
        ctx.strokeStyle = borderCol;
        ctx.globalAlpha = 1;
        ctx.lineWidth = 0.9 / Math.max(0.55, cam.k);
      }}
      ctx.beginPath(); ctx.moveTo(a.x, a.y); ctx.lineTo(b.x, b.y); ctx.stroke();
    }}
    for (let i = 0; i < nodes.length; i++) {{
      const n = nodes[i], r = nodeRadius(n), col = catColor(n.c);
      const isF = i === focusIdx, isN = focusNbr && focusNbr.has(i), isM = !matched || matched.has(i);
      let aN = 0.95;
      if (focusIdx !== -1 && !isF && !isN) aN = 0.16;
      else if (matched && !isM) aN = 0.14;
      ctx.globalAlpha = aN;
      ctx.beginPath(); ctx.arc(n.x, n.y, r, 0, Math.PI * 2); ctx.fillStyle = col; ctx.fill();
      if (n.p === 1) {{
        ctx.strokeStyle = fg; ctx.lineWidth = 1.1 / Math.max(0.6, cam.k);
        ctx.setLineDash([2, 2]); ctx.stroke(); ctx.setLineDash([]);
      }}
      if (isF || (matched && isM)) {{
        ctx.beginPath(); ctx.arc(n.x, n.y, r + 2.6, 0, Math.PI * 2);
        ctx.strokeStyle = fg; ctx.lineWidth = 1.6 / Math.max(0.6, cam.k); ctx.stroke();
      }}
    }}
    ctx.textAlign = "center"; ctx.textBaseline = "top";
    const fSz = Math.max(8, Math.min(12.5, 11 / Math.sqrt(cam.k)));
    ctx.font = `500 ${{fSz}}px system-ui, -apple-system, sans-serif`;
    for (let i = 0; i < nodes.length; i++) {{
      const n = nodes[i], isF = i === focusIdx, isN = focusNbr && focusNbr.has(i), isM = matched && matched.has(i);
      const isHub = n.c === "ra" || n.id === "wiki/index.md" || n.id.endsWith("/index.md");
      if (!(isF || isN || isM || (focusIdx === -1 && isHub) || (focusIdx === -1 && cam.k > 1.2 && n.deg >= 3) || (focusIdx === -1 && cam.k > 1.75))) continue;
      const r = nodeRadius(n);
      ctx.globalAlpha = isF || isM ? 1 : isN ? 0.92 : 0.85;
      ctx.fillStyle = isF ? fg : muted;
      ctx.fillText(n.l, n.x, n.y + r + 3);
    }}
    ctx.restore();
  }}
  function startSim() {{
    if (rafId) cancelAnimationFrame(rafId);
    function loop() {{
      const e = stepPhysics();
      draw();
      if (dragIdx !== -1 || e > 0.03 || alpha > 0.04) rafId = requestAnimationFrame(loop);
      else rafId = null;
    }}
    rafId = requestAnimationFrame(loop);
  }}
  function screenToWorld(sx, sy) {{
    const rect = canvas.getBoundingClientRect();
    return {{ x: (sx - rect.width / 2) / cam.k - cam.x, y: (sy - rect.height / 2) / cam.k - cam.y }};
  }}
  function pickNode(sx, sy) {{
    const wp = screenToWorld(sx, sy);
    let best = -1, bestD = Infinity;
    for (let i = nodes.length - 1; i >= 0; i--) {{
      const n = nodes[i], hitR = nodeRadius(n) + 7 / cam.k, d = Math.hypot(wp.x - n.x, wp.y - n.y);
      if (d <= hitR && d < bestD) {{ best = i; bestD = d; }}
    }}
    return best;
  }}
  function fitView() {{
    if (!nodes.length) return;
    let minX = Infinity, maxX = -Infinity, minY = Infinity, maxY = -Infinity;
    for (const n of nodes) {{
      if (n.x < minX) minX = n.x; if (n.x > maxX) maxX = n.x;
      if (n.y < minY) minY = n.y; if (n.y > maxY) maxY = n.y;
    }}
    const rect = canvas.getBoundingClientRect();
    const sX = Math.max(140, maxX - minX + 80), sY = Math.max(140, maxY - minY + 80);
    cam.k = Math.max(0.35, Math.min(1.9, Math.min(rect.width / sX, rect.height / sY)));
    cam.x = -(minX + maxX) / 2; cam.y = -(minY + maxY) / 2;
    draw();
  }}
  function updateInspector() {{
    const idx = hoveredIdx !== -1 ? hoveredIdx : selectedIdx;
    if (idx === -1 || !nodes[idx]) {{
      badgeEl.textContent = "grafo";
      titleEl.textContent = "Haz clic en un nodo para inspeccionarlo o doble clic para abrir la página en el Portal Docente";
      degEl.textContent = "";
      openEl.classList.add("hidden");
      neighborsEl.classList.add("hidden");
      neighborsEl.innerHTML = "";
      return;
    }}
    const n = nodes[idx];
    const inc = [...(inAdj.get(idx) || [])], out = [...(outAdj.get(idx) || [])];
    badgeEl.textContent = `${{n.r}} · ${{n.c}}${{n.p ? " 🔒" : ""}}`;
    titleEl.textContent = `${{n.id}} — ${{n.t}}`;
    degEl.textContent = `${{inc.length}} ent · ${{out.length}} sal`;
    openEl.href = "../" + n.u;
    openEl.classList.remove("hidden");
    const combined = [...out.map(ni => ({{ ni, dir: "→" }})), ...inc.filter(ni => !out.includes(ni)).map(ni => ({{ ni, dir: "←" }}))].slice(0, 14);
    if (combined.length) {{
      neighborsEl.classList.remove("hidden");
      neighborsEl.innerHTML = combined.map(({{ ni, dir }}) =>
        `<button type="button" data-ni="${{ni}}" class="wg-chip">${{dir}} ${{nodes[ni].l}}</button>`
      ).join("");
    }} else neighborsEl.classList.add("hidden");
  }}
  neighborsEl.addEventListener("click", (e) => {{
    const btn = e.target.closest("button[data-ni]");
    if (!btn) return;
    const ni = Number(btn.dataset.ni);
    if (Number.isInteger(ni) && nodes[ni]) {{ selectedIdx = ni; hoveredIdx = -1; updateInspector(); draw(); }}
  }});
  canvas.addEventListener("pointerdown", (e) => {{
    const r = canvas.getBoundingClientRect(), sx = e.clientX - r.left, sy = e.clientY - r.top;
    moved = false;
    const hit = pickNode(sx, sy);
    canvas.setPointerCapture(e.pointerId);
    if (hit !== -1) {{ dragIdx = hit; alpha = Math.max(alpha, 0.35); startSim(); }}
    else {{ isPanning = true; panStart = {{ x: sx, y: sy, cx: cam.x, cy: cam.y }}; }}
  }});
  canvas.addEventListener("pointermove", (e) => {{
    const r = canvas.getBoundingClientRect(), sx = e.clientX - r.left, sy = e.clientY - r.top;
    if (dragIdx !== -1) {{
      moved = true;
      const wp = screenToWorld(sx, sy);
      nodes[dragIdx].x = wp.x; nodes[dragIdx].y = wp.y; nodes[dragIdx].vx = 0; nodes[dragIdx].vy = 0;
      if (!rafId) draw();
    }} else if (isPanning) {{
      if (Math.hypot(sx - panStart.x, sy - panStart.y) > 3) moved = true;
      cam.x = panStart.cx + (sx - panStart.x) / cam.k; cam.y = panStart.cy + (sy - panStart.y) / cam.k;
      draw();
    }} else {{
      const hit = pickNode(sx, sy);
      if (hit !== hoveredIdx) {{ hoveredIdx = hit; canvas.style.cursor = hit !== -1 ? "pointer" : "grab"; updateInspector(); draw(); }}
    }}
  }});
  canvas.addEventListener("pointerup", (e) => {{
    const r = canvas.getBoundingClientRect(), sx = e.clientX - r.left, sy = e.clientY - r.top;
    if (!moved) {{ const hit = pickNode(sx, sy); selectedIdx = hit === selectedIdx ? -1 : hit; updateInspector(); draw(); }}
    dragIdx = -1; isPanning = false;
    try {{ canvas.releasePointerCapture(e.pointerId); }} catch {{}}
  }});
  canvas.addEventListener("dblclick", (e) => {{
    const r = canvas.getBoundingClientRect();
    const hit = pickNode(e.clientX - r.left, e.clientY - r.top);
    if (hit !== -1 && nodes[hit]) window.location.href = "../" + nodes[hit].u;
    else fitView();
  }});
  canvas.addEventListener("wheel", (e) => {{
    e.preventDefault();
    const r = canvas.getBoundingClientRect(), sx = e.clientX - r.left, sy = e.clientY - r.top;
    const before = screenToWorld(sx, sy);
    cam.k = Math.max(0.25, Math.min(3.5, cam.k * (e.deltaY < 0 ? 1.12 : 0.89)));
    const after = screenToWorld(sx, sy);
    cam.x += after.x - before.x; cam.y += after.y - before.y;
    draw();
  }}, {{ passive: false }});
  searchEl.addEventListener("input", () => {{ query = searchEl.value; draw(); }});
  raEl.addEventListener("change", () => {{ activeRa = raEl.value; buildSubgraph(); setTimeout(fitView, 120); }});
  scopeBtn.addEventListener("click", () => {{ showAll = !showAll; buildSubgraph(); setTimeout(fitView, 120); }});
  fitBtn.addEventListener("click", fitView);
  reheatBtn.addEventListener("click", () => {{ alpha = 1.0; startSim(); }});
  new MutationObserver(() => {{ renderLegend(); draw(); }}).observe(document.body, {{ attributes: true, attributeFilter: ["data-md-color-scheme"] }});
  window.addEventListener("resize", draw);
  buildSubgraph();
  setTimeout(fitView, 180);
}})();
</script>
"""
    # Strip empty lines inside the HTML block so Python-Markdown never splits it into <p> tags.
    compact_html = "\n".join(line for line in html_block.splitlines() if line.strip())

    return (
        "---\n"
        'title: "Graph View · Mapa de Relaciones (Portal Docente)"\n'
        "hide:\n"
        "  - navigation\n"
        "  - toc\n"
        "---\n\n"
        "# Graph View · Mapa de Relaciones `wikiSI` (Portal Docente)\n\n"
        "Grafo autogenerado al vuelo con **todos** los documentos `.md` públicos, las fuentes curadas (`raw/procesados/`), las soluciones de prácticas (`publicar: false`) y el banco privado de evaluación (`privado_evaluacion/`). Haz **doble clic** sobre cualquier nodo (o usa **Abrir página ↗**) para navegar directamente al documento.\n\n"
        f"{compact_html}\n"
    )


def _augment_practicas_nav(nav: list[Any], wiki_dir: Path) -> list[Any]:
    """Insert each pXX solution (`publicar: false`) right below its enunciado and append p00."""
    sol_by_prefix: dict[str, str] = {}
    for p in sorted((wiki_dir / "practicas").glob("p*-solucion.md")):
        prefix = p.name.split("-", 1)[0]
        sol_by_prefix[prefix] = f"practicas/{p.name}"

    out: list[Any] = []
    seen_sols: set[str] = set()
    for item in nav:
        out.append(item)
        if isinstance(item, dict):
            val = next(iter(item.values()))
            if isinstance(val, str) and val.startswith("practicas/") and val.endswith("-enunciado.md"):
                prefix = Path(val).name.split("-", 1)[0]
                if prefix in sol_by_prefix:
                    sol_rel = sol_by_prefix[prefix]
                    out.append({f"{prefix} · Solución Docente 🔒": sol_rel})
                    seen_sols.add(sol_rel)

    for prefix, sol_rel in sorted(sol_by_prefix.items()):
        if sol_rel not in seen_sols:
            label = (
                "p00 · Plantilla de Solución 🔒"
                if prefix == "p00"
                else f"{prefix} · Solución Docente 🔒"
            )
            out.append({label: sol_rel})
    return out


def on_config(config: Any) -> Any:
    """Generate the dynamic Obsidian Graph View page and extend navigation for the Teacher Portal."""
    repo_root = _repo_root(config)
    cache_grafo_dir = repo_root / ".cache_docente" / "grafo"
    cache_grafo_dir.mkdir(parents=True, exist_ok=True)
    grafo_md = cache_grafo_dir / "grafo-docente.md"

    payload = _collect_graph_payload(repo_root, config.site_dir, config.use_directory_urls)
    new_md = _build_graph_markdown(payload)
    if not grafo_md.exists() or grafo_md.read_text(encoding="utf-8") != new_md:
        grafo_md.write_text(new_md, encoding="utf-8")

    nav = list(config.nav or [])
    if any(isinstance(entry, dict) and "🕸️ Graph View" in entry for entry in nav):
        return config

    for entry in nav:
        if isinstance(entry, dict) and "Prácticas" in entry and isinstance(entry["Prácticas"], list):
            entry["Prácticas"] = _augment_practicas_nav(entry["Prácticas"], repo_root / "wiki")

    priv_dir = repo_root / "privado_evaluacion"
    eval_nav: list[Any] = []
    if (priv_dir / "README.md").exists():
        eval_nav.append({"Índice de Evaluación": "privado_evaluacion/README.md"})
    for sub_dir, sub_label, prefix in [
        ("examenes", "Exámenes (con GIFT)", "Examen"),
        ("soluciones", "Solucionarios", "Solución"),
        ("rubricas", "Rúbricas", "Rúbrica"),
    ]:
        items = [
            {_nav_label(p, prefix): p.relative_to(repo_root).as_posix()}
            for p in sorted((priv_dir / sub_dir).glob("*.md"))
        ]
        if items:
            eval_nav.append({sub_label: items})

    if eval_nav:
        nav.append({"🔒 Evaluación Docente": eval_nav})

    raw_dir = repo_root / "raw" / "procesados"
    raw_items = [
        {_nav_label(p): p.relative_to(repo_root).as_posix()}
        for p in sorted(raw_dir.glob("*.md"))
    ]
    if raw_items:
        nav.append({"📚 Fuentes Curadas (Raw)": raw_items})

    nav.append({"🕸️ Graph View": "grafo-docente.md"})
    config["nav"] = nav
    return config


def on_files(files: Any, config: Any) -> Any:
    """Attach `privado_evaluacion/`, `raw/procesados/`, and `grafo-docente.md` without copying files."""
    repo_root = _repo_root(config)
    existing = {f.src_path for f in files}

    for folder in [repo_root / "privado_evaluacion", repo_root / "raw" / "procesados"]:
        if not folder.exists():
            continue
        for md_path in sorted(folder.rglob("*.md")):
            rel_path = md_path.relative_to(repo_root).as_posix()
            if rel_path in existing:
                continue
            files.append(
                File(
                    path=rel_path,
                    src_dir=str(repo_root),
                    dest_dir=config.site_dir,
                    use_directory_urls=config.use_directory_urls,
                )
            )
            existing.add(rel_path)

    cache_grafo_dir = repo_root / ".cache_docente" / "grafo"
    if "grafo-docente.md" not in existing and (cache_grafo_dir / "grafo-docente.md").exists():
        files.append(
            File(
                path="grafo-docente.md",
                src_dir=str(cache_grafo_dir),
                dest_dir=config.site_dir,
                use_directory_urls=config.use_directory_urls,
            )
        )

    return files
