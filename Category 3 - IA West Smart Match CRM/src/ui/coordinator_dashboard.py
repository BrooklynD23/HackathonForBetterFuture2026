"""Coordinator Dashboard page for IA SmartMatch.

Renders the Institutional Dashboard HTML view via st.components.v1.html(),
populated with real data from data_helpers.py.
"""

from __future__ import annotations

import streamlit as st

from src.ui.expansion_map import render_coordinator_density_map
from src.ui.data_helpers import (
    get_initials,
    get_recent_poc_activity,
    get_top_specialists_for_event,
    load_pipeline_data,
    load_poc_contacts,
    load_specialists,
)
from src.ui.html_base import render_html_page
from src.ui.page_router import navigate_to, set_user_role


def render_coordinator_dashboard(speakers_df=None) -> None:
    """Render the full Coordinator Institutional Dashboard page.

    Loads real data from data helpers, computes metrics, builds match cards
    and Live Discovery Feed items, then renders the full HTML layout using
    render_html_page(). Navigation buttons appear below the iframe.
    """
    # ── Load Data ────────────────────────────────────────────────────────────
    specialists = load_specialists()
    pocs = load_poc_contacts()
    pipeline = load_pipeline_data()
    activity = get_recent_poc_activity(5)

    # ── Compute Metrics ──────────────────────────────────────────────────────
    unique_events = list({row["event_name"] for row in pipeline if row.get("event_name")})
    scraped_events_count = len(unique_events)
    poc_count = len(pocs)
    volunteer_pct = 88  # Demo value matching mockup

    # ── Build Match Cards ────────────────────────────────────────────────────
    # Pick top 2 events by highest single match_score for the feature cards
    event_top_scores: dict[str, float] = {}
    for row in pipeline:
        event = row.get("event_name", "")
        try:
            score = float(row.get("match_score", 0))
        except (ValueError, TypeError):
            score = 0.0
        if event not in event_top_scores or score > event_top_scores[event]:
            event_top_scores[event] = score

    top_events = sorted(event_top_scores.items(), key=lambda x: -x[1])[:2]

    match_cards_html = ""
    icon_cycle = ["biotech", "architecture", "hub", "science", "school"]
    for idx, (event_name, top_score) in enumerate(top_events):
        alignment_pct = round(top_score * 100)
        top_specs = get_top_specialists_for_event(event_name, 3)
        # Build avatar row
        avatar_html = ""
        for spec in top_specs[:2]:
            initials = spec.get("initials") or get_initials(spec.get("name", "?"))
            avatar_html += (
                f'<div class="w-8 h-8 rounded-full bg-primary-container border-2 '
                f'border-white flex items-center justify-center text-white text-[10px] font-bold">'
                f"{initials}</div>"
            )
        if len(top_specs) > 2:
            extra = len(top_specs) - 2
            avatar_html += (
                f'<div class="w-8 h-8 rounded-full bg-slate-100 border-2 border-white '
                f'flex items-center justify-center text-[10px] font-bold text-slate-400">+{extra}</div>'
            )

        score_color = "text-green-600" if alignment_pct >= 90 else "text-primary"
        icon = icon_cycle[idx % len(icon_cycle)]

        # Derive institution from event name (use event name itself as fallback)
        institution = _derive_institution(event_name)

        match_cards_html += f"""
        <!-- Match Card {idx + 1} -->
        <div class="bg-surface-container-lowest p-5 rounded-2xl flex flex-col md:flex-row items-start md:items-center justify-between gap-4 transition-transform hover:scale-[1.01] cursor-pointer">
          <div class="flex items-center gap-4">
            <div class="w-12 h-12 rounded-xl bg-slate-100 flex items-center justify-center text-slate-400">
              <span class="material-symbols-outlined">{icon}</span>
            </div>
            <div>
              <h4 class="font-bold text-base">{event_name}</h4>
              <p class="text-xs text-slate-500">{institution}</p>
            </div>
          </div>
          <div class="flex items-center gap-6">
            <div class="text-right">
              <p class="text-[10px] font-bold text-slate-400 uppercase">Alignment</p>
              <p class="text-sm font-bold {score_color}">{alignment_pct}% Fit</p>
            </div>
            <div class="flex -space-x-2">
              {avatar_html}
            </div>
            <button class="px-4 py-2 bg-blue-50 text-blue-700 rounded-lg text-xs font-bold hover:bg-blue-100 transition-colors"
                    onclick="window.iaSmartMatch.navigate('matches', {{role: 'coordinator', demo: true}}); return false;">Assign</button>
          </div>
        </div>
        """

    # ── Build Live Discovery Feed ─────────────────────────────────────────────
    feed_items_html = ""

    # First item from activity data
    if activity:
        item = activity[0]
        poc_name = item.get("poc_name", "Unknown")
        org = item.get("org", "")
        comm_type = item.get("type", "email").title()
        feed_items_html += f"""
        <div class="relative pl-6 border-l-2 border-blue-100 pb-2">
          <div class="absolute -left-[9px] top-0 w-4 h-4 rounded-full bg-white border-2 border-blue-500"></div>
          <p class="text-[10px] font-bold text-primary uppercase mb-1">Just Now</p>
          <h5 class="text-sm font-bold text-on-surface">POC Activity: {poc_name}</h5>
          <p class="text-xs text-slate-500 mt-1">{org} &bull; {comm_type} logged</p>
          <div class="mt-3">
            <button class="text-xs font-bold text-primary underline underline-offset-4"
                    onclick="window.iaSmartMatch.navigate('discovery', {{role: 'coordinator', demo: true}}); return false;">Connect now</button>
          </div>
        </div>
        """

    # Second item from activity if available
    if len(activity) > 1:
        item2 = activity[1]
        poc_name2 = item2.get("poc_name", "Unknown")
        org2 = item2.get("org", "")
        summary2 = item2.get("summary", "")[:80]
        feed_items_html += f"""
        <div class="relative pl-6 border-l-2 border-blue-100 pb-2">
          <div class="absolute -left-[9px] top-0 w-4 h-4 rounded-full bg-white border-2 border-blue-200"></div>
          <p class="text-[10px] font-bold text-slate-400 uppercase mb-1">14 Minutes Ago</p>
          <h5 class="text-sm font-bold text-on-surface">POC Identified: {poc_name2}</h5>
          <p class="text-xs text-slate-500 mt-1">{org2}</p>
        </div>
        """

    # Hardcoded feed items matching mockup style
    feed_items_html += """
        <div class="relative pl-6 border-l-2 border-blue-100 pb-2">
          <div class="absolute -left-[9px] top-0 w-4 h-4 rounded-full bg-white border-2 border-blue-200"></div>
          <p class="text-[10px] font-bold text-slate-400 uppercase mb-1">2 Hours Ago</p>
          <h5 class="text-sm font-bold text-on-surface">New Event Scraped: AI Research Forum</h5>
          <p class="text-xs text-slate-500 mt-1">Caltech, Pasadena &bull; Detected via RSS/Academic Calendar</p>
          <div class="mt-3 flex gap-2">
            <span class="px-2 py-0.5 bg-slate-100 text-[10px] font-semibold rounded text-slate-600">Computer Science</span>
            <span class="px-2 py-0.5 bg-slate-100 text-[10px] font-semibold rounded text-slate-600">High Impact</span>
          </div>
        </div>
        <div class="relative pl-6 border-l-2 border-blue-100 pb-2">
          <div class="absolute -left-[9px] top-0 w-4 h-4 rounded-full bg-white border-2 border-blue-200"></div>
          <p class="text-[10px] font-bold text-slate-400 uppercase mb-1">3 Hours Ago</p>
          <h5 class="text-sm font-bold text-on-surface">Data Refresh Complete</h5>
          <p class="text-xs text-slate-500 mt-1">Oregon State University calendar sync successful. 18 new entries.</p>
        </div>
        <div class="relative pl-6 border-l-2 border-blue-100 pb-2">
          <div class="absolute -left-[9px] top-0 w-4 h-4 rounded-full bg-white border-2 border-blue-200"></div>
          <p class="text-[10px] font-bold text-slate-400 uppercase mb-1">4 Hours Ago</p>
          <h5 class="text-sm font-bold text-on-surface">Volunteer Alert: Availability Shift</h5>
          <p class="text-xs text-slate-500 mt-1">Mark Thompson (Regional Lead) updated status to 'Active'.</p>
        </div>
        <div class="relative pl-6 border-l-2 border-blue-100 pb-2">
          <div class="absolute -left-[9px] top-0 w-4 h-4 rounded-full bg-white border-2 border-blue-200"></div>
          <p class="text-[10px] font-bold text-slate-400 uppercase mb-1">Yesterday</p>
          <h5 class="text-sm font-bold text-on-surface">Monthly Summary Generated</h5>
          <p class="text-xs text-slate-500 mt-1">Academic engagement is up 22% in the Southern California region.</p>
        </div>
    """

    # ── Profile Initials Avatar ───────────────────────────────────────────────
    # Use first specialist or generic "AC" for Academic Coordinator
    profile_initials = specialists[0]["initials"] if specialists else "AC"

    # ── Build Full HTML Body ─────────────────────────────────────────────────
    body_html = f"""
<!-- TopNavBar -->
<nav class="fixed top-0 w-full z-50 bg-white/80 backdrop-blur-xl shadow-sm">
  <div class="flex items-center justify-between px-8 h-16 w-full max-w-screen-2xl mx-auto">
    <div class="flex items-center gap-8">
      <span class="text-xl font-semibold tracking-tighter text-blue-900 headline-font">IA SmartMatch</span>
      <div class="hidden md:flex gap-6 items-center font-medium text-sm tracking-tight">
        <a class="text-blue-700 border-b-2 border-blue-700 pb-1" href="#" onclick="window.iaSmartMatch.navigate('dashboard', {{role: 'coordinator', demo: true}}); return false;">Dashboard</a>
        <a class="text-slate-500 hover:text-blue-600 transition-colors" href="#" onclick="window.iaSmartMatch.navigate('matches', {{role: 'coordinator', demo: true}}); return false;">Matches</a>
        <a class="text-slate-500 hover:text-blue-600 transition-colors" href="#" onclick="window.iaSmartMatch.navigate('pipeline', {{role: 'coordinator', demo: true}}); return false;">Pipeline</a>
        <a class="text-slate-500 hover:text-blue-600 transition-colors" href="#" onclick="window.iaSmartMatch.navigate('discovery', {{role: 'coordinator', demo: true}}); return false;">Discovery</a>
        <a class="text-slate-500 hover:text-blue-600 transition-colors" href="#" onclick="window.iaSmartMatch.navigate('analytics', {{role: 'coordinator', demo: true}}); return false;">Analytics</a>
      </div>
    </div>
    <div class="flex items-center gap-4">
      <div class="relative hidden sm:block">
        <span class="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 text-sm">search</span>
        <input class="pl-10 pr-4 py-1.5 bg-surface-container-low border-none rounded-full text-sm w-64 focus:ring-2 focus:ring-primary/20" placeholder="Search institutional data..." type="text"/>
      </div>
      <button class="p-2 text-slate-500 hover:bg-blue-50/50 rounded-full transition-colors">
        <span class="material-symbols-outlined">notifications</span>
      </button>
      <button class="p-2 text-slate-500 hover:bg-blue-50/50 rounded-full transition-colors">
        <span class="material-symbols-outlined">settings</span>
      </button>
      <div class="w-8 h-8 rounded-full bg-primary-container flex items-center justify-center text-white text-xs font-bold">{profile_initials}</div>
    </div>
  </div>
</nav>

<div class="flex min-h-screen pt-16 bg-surface">
  <!-- Left SideNavBar -->
  <aside class="hidden lg:flex flex-col py-6 px-4 gap-2 h-[calc(100vh-64px)] w-64 bg-slate-50 border-r-0 sticky top-16">
    <div class="px-4 mb-6">
      <div class="flex items-center gap-3">
        <div class="w-10 h-10 rounded-xl bg-primary flex items-center justify-center text-white">
          <span class="material-symbols-outlined">school</span>
        </div>
        <div>
          <p class="text-sm font-bold text-blue-900 headline-font">Academic Curator</p>
          <p class="text-[10px] text-slate-500 uppercase tracking-widest">Institutional Unit</p>
        </div>
      </div>
    </div>
    <nav class="flex-1 space-y-1">
      <a class="flex items-center gap-3 px-4 py-2.5 bg-white text-blue-700 rounded-lg shadow-sm font-semibold text-sm" href="#" onclick="window.iaSmartMatch.navigate('dashboard', {{role: 'coordinator', demo: true}}); return false;">
        <span class="material-symbols-outlined" style="font-variation-settings: 'FILL' 1;">dashboard</span>
        Dashboard
      </a>
      <a class="flex items-center gap-3 px-4 py-2.5 text-slate-600 hover:bg-slate-200/50 rounded-lg transition-transform duration-150 active:scale-95 text-sm font-semibold" href="#" onclick="window.iaSmartMatch.navigate('matches', {{role: 'coordinator', demo: true}}); return false;">
        <span class="material-symbols-outlined">handshake</span>
        Matches
      </a>
      <a class="flex items-center gap-3 px-4 py-2.5 text-slate-600 hover:bg-slate-200/50 rounded-lg transition-transform duration-150 active:scale-95 text-sm font-semibold" href="#" onclick="window.iaSmartMatch.navigate('pipeline', {{role: 'coordinator', demo: true}}); return false;">
        <span class="material-symbols-outlined">account_tree</span>
        Pipeline
      </a>
      <a class="flex items-center gap-3 px-4 py-2.5 text-slate-600 hover:bg-slate-200/50 rounded-lg transition-transform duration-150 active:scale-95 text-sm font-semibold" href="#" onclick="window.iaSmartMatch.navigate('discovery', {{role: 'coordinator', demo: true}}); return false;">
        <span class="material-symbols-outlined">travel_explore</span>
        Discovery
      </a>
      <a class="flex items-center gap-3 px-4 py-2.5 text-slate-600 hover:bg-slate-200/50 rounded-lg transition-transform duration-150 active:scale-95 text-sm font-semibold" href="#" onclick="window.iaSmartMatch.navigate('analytics', {{role: 'coordinator', demo: true}}); return false;">
        <span class="material-symbols-outlined">analytics</span>
        Analytics
      </a>
    </nav>
    <button class="mt-4 mx-2 py-3 bg-gradient-to-br from-primary to-primary-container text-white rounded-xl shadow-md flex items-center justify-center gap-2 font-semibold text-sm hover:opacity-90 transition-opacity"
            onclick="window.iaSmartMatch.navigate('matches', {{role: 'coordinator', demo: true}}); return false;">
      <span class="material-symbols-outlined text-sm">add</span>
      New Match
    </button>
    <div class="mt-auto pt-6 border-t border-slate-200/50 space-y-1">
      <a class="flex items-center gap-3 px-4 py-2 text-slate-500 hover:bg-slate-200/50 rounded-lg text-xs font-semibold" href="#" onclick="window.iaSmartMatch.navigate('analytics', {{role: 'coordinator', demo: true}}); return false;">
        <span class="material-symbols-outlined text-sm">help</span>
        Help Center
      </a>
      <a class="flex items-center gap-3 px-4 py-2 text-slate-500 hover:bg-slate-200/50 rounded-lg text-xs font-semibold" href="#" onclick="window.iaSmartMatch.navigate('analytics', {{role: 'coordinator', demo: true}}); return false;">
        <span class="material-symbols-outlined text-sm">contact_support</span>
        Support
      </a>
    </div>
  </aside>

  <!-- Main Content -->
  <main class="flex-1 p-8 overflow-x-hidden">

    <!-- Header Section -->
    <header class="flex flex-col md:flex-row md:items-end justify-between gap-4 mb-10">
      <div>
        <h1 class="text-4xl font-bold tracking-tight text-on-surface headline-font">Institutional Dashboard</h1>
        <p class="text-slate-500 mt-2 font-medium">Monitoring West Coast Campus Event Density &amp; Volunteer Alignment.</p>
      </div>
      <div class="flex items-center gap-3 bg-white p-1.5 rounded-2xl shadow-sm border border-outline-variant/10">
        <button class="px-4 py-2 rounded-xl text-sm font-semibold bg-primary text-white shadow-sm">Real-time</button>
        <button class="px-4 py-2 rounded-xl text-sm font-semibold text-slate-500 hover:bg-slate-50">Historical</button>
      </div>
    </header>

    <!-- Metrics Bento Grid -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
      <!-- Scraped Events -->
      <div class="bg-surface-container-lowest p-6 rounded-2xl shadow-sm border border-outline-variant/5 flex items-center justify-between">
        <div>
          <p class="text-xs font-bold text-slate-400 uppercase tracking-widest mb-1">Scraped Events Today</p>
          <h3 class="text-3xl font-bold headline-font text-primary">{scraped_events_count}</h3>
          <p class="text-xs text-green-600 mt-2 flex items-center gap-1">
            <span class="material-symbols-outlined text-sm">trending_up</span> +12% from yesterday
          </p>
        </div>
        <div class="w-12 h-12 rounded-full bg-blue-50 flex items-center justify-center text-blue-600">
          <span class="material-symbols-outlined">data_object</span>
        </div>
      </div>
      <!-- New POC Found -->
      <div class="bg-surface-container-lowest p-6 rounded-2xl shadow-sm border border-outline-variant/5 flex items-center justify-between">
        <div>
          <p class="text-xs font-bold text-slate-400 uppercase tracking-widest mb-1">New POC Found</p>
          <h3 class="text-3xl font-bold headline-font text-primary">{poc_count}</h3>
          <p class="text-xs text-blue-600 mt-2 flex items-center gap-1">
            <span class="material-symbols-outlined text-sm">verified_user</span> Priority institutions tracked
          </p>
        </div>
        <div class="w-12 h-12 rounded-full bg-blue-50 flex items-center justify-center text-blue-600">
          <span class="material-symbols-outlined">person_add</span>
        </div>
      </div>
      <!-- Volunteer Availability -->
      <div class="bg-surface-container-lowest p-6 rounded-2xl shadow-sm border border-outline-variant/5 flex items-center justify-between">
        <div>
          <p class="text-xs font-bold text-slate-400 uppercase tracking-widest mb-1">Volunteer Availability</p>
          <h3 class="text-3xl font-bold headline-font text-primary">{volunteer_pct}%</h3>
          <div class="w-32 h-1.5 bg-slate-100 rounded-full mt-3 overflow-hidden">
            <div class="h-full bg-primary" style="width:{volunteer_pct}%"></div>
          </div>
        </div>
        <div class="w-12 h-12 rounded-full bg-blue-50 flex items-center justify-center text-blue-600">
          <span class="material-symbols-outlined">group</span>
        </div>
      </div>
    </div>

    <!-- Main 12-column grid -->
    <div class="grid grid-cols-1 lg:grid-cols-12 gap-8">

      <!-- Left: Map + Matches -->
      <div class="lg:col-span-8 flex flex-col gap-6">

        <!-- Campus Event Density Map -->
        <section class="bg-surface-container-lowest rounded-2xl shadow-sm border border-outline-variant/5 overflow-hidden flex flex-col h-[220px]">
          <div class="p-6 border-b border-outline-variant/5 flex items-center justify-between bg-white">
            <div>
              <h2 class="text-lg font-bold headline-font">Campus Coverage Map</h2>
              <p class="text-xs text-slate-500">The live Plotly coverage map is rendered directly below this dashboard shell.</p>
            </div>
            <div class="flex gap-2">
              <span class="flex items-center gap-1.5 px-3 py-1 bg-blue-50 text-blue-700 rounded-full text-[10px] font-bold">
                <span class="w-2 h-2 rounded-full bg-blue-600"></span> LIVE COVERAGE
              </span>
            </div>
          </div>
          <div class="flex-1 bg-gradient-to-br from-slate-100 via-slate-50 to-blue-50 px-6 py-8 flex flex-col justify-center">
            <p class="text-sm text-slate-600 leading-relaxed">
              The routed V2 workspace now uses a live geo chart for campus density, speaker
              coverage, and hoverable reachability details instead of a decorative mock heatmap.
            </p>
            <div class="mt-4 flex flex-wrap gap-2">
              <span class="px-3 py-1 bg-white text-xs font-semibold rounded-full text-slate-600 shadow-sm">Campus density</span>
              <span class="px-3 py-1 bg-white text-xs font-semibold rounded-full text-slate-600 shadow-sm">Speaker coverage</span>
              <span class="px-3 py-1 bg-white text-xs font-semibold rounded-full text-slate-600 shadow-sm">Hover details</span>
            </div>
          </div>
        </section>

        <!-- Active High-Priority Matches -->
        <section class="bg-surface-container-low p-8 rounded-2xl">
          <div class="flex items-center justify-between mb-8">
            <h2 class="text-2xl font-bold headline-font">Active High-Priority Matches</h2>
            <button class="text-sm font-semibold text-primary flex items-center gap-1"
                    onclick="window.iaSmartMatch.navigate('pipeline', {{role: 'coordinator', demo: true}}); return false;">
              View Pipeline <span class="material-symbols-outlined text-sm">arrow_forward</span>
            </button>
          </div>
          <div class="space-y-4">
            {match_cards_html}
          </div>
        </section>

      </div><!-- end left col -->

      <!-- Right: Live Discovery Feed -->
      <div class="lg:col-span-4 space-y-6">
        <section class="bg-surface-container-lowest rounded-2xl shadow-sm border border-outline-variant/5 h-full flex flex-col overflow-hidden">
          <div class="p-6 border-b border-outline-variant/5 flex items-center justify-between sticky top-0 bg-white z-10">
            <h2 class="text-lg font-bold headline-font">Live Discovery Feed</h2>
            <span class="flex h-2 w-2 rounded-full bg-red-500 animate-pulse"></span>
          </div>
          <div class="flex-1 p-6 overflow-y-auto max-h-[1000px]">
            <div class="space-y-6">
              {feed_items_html}
            </div>
          </div>
          <div class="p-4 bg-slate-50 border-t border-outline-variant/5 text-center">
            <button class="text-xs font-bold text-slate-500 hover:text-primary transition-colors uppercase tracking-widest">Load More Activities</button>
          </div>
        </section>
      </div>

    </div><!-- end 12-col grid -->
  </main>
</div>

<!-- Floating Action Button -->
<button class="fixed bottom-8 right-8 w-14 h-14 bg-gradient-to-br from-primary to-primary-container text-white rounded-full shadow-2xl flex items-center justify-center hover:scale-105 transition-transform">
  <span class="material-symbols-outlined">add</span>
</button>
"""

    render_html_page(
        body_html,
        title="IA SmartMatch | Coordinator Dashboard",
        height=4700,
        hide_chrome=False,
    )

    if speakers_df is not None:
        st.markdown("### Campus Coverage Map")
        st.caption(
            "Plotly coverage uses campus hubs and synthetic density shading for reachability context; "
            "it is not a street-map basemap."
        )
        figure, unmapped_metros = render_coordinator_density_map(speakers_df)
        st.plotly_chart(
            figure,
            use_container_width=True,
            config={"displayModeBar": False},
            key="coordinator_density_map",
        )
        if unmapped_metros:
            st.warning(
                "Some speaker metros are not mapped yet and were excluded from the coverage map: "
                + ", ".join(sorted(unmapped_metros))
            )

    # ── Streamlit Navigation Buttons ─────────────────────────────────────────
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("View Match Engine", type="primary", use_container_width=True):
            navigate_to("match_engine")
    with col2:
        if st.button("Sign Out", use_container_width=True):
            set_user_role(None)
            navigate_to("landing", role=None, demo=False)


# ── Helper ────────────────────────────────────────────────────────────────────

def _derive_institution(event_name: str) -> str:
    """Derive a short institution label from an event name string."""
    lower = event_name.lower()
    if "cpp" in lower or "cal poly" in lower or "bronco" in lower:
        return "Cal Poly Pomona"
    if "ucla" in lower:
        return "UCLA"
    if "stanford" in lower:
        return "Stanford University"
    if "ucsd" in lower or "san diego" in lower:
        return "UC San Diego"
    if "swift" in lower:
        return "SWIFT Consortium"
    if "our" in lower or "rsca" in lower or "cars" in lower:
        return "Cal Poly Pomona OUR"
    return "West Coast Campus"
