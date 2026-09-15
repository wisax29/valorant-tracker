/**
 * VALORANT TRACKER - FRONTEND ENGINE
 */

document.addEventListener("DOMContentLoaded", () => {
    // DOM Elements
    const searchForm = document.getElementById("search-form");
    const playerInput = document.getElementById("player-input");
    const regionSelect = document.getElementById("region-select");
    const searchSuggestions = document.getElementById("search-suggestions");

    const statusBanner = document.getElementById("status-banner");
    const bannerText = document.getElementById("banner-text");
    const bannerClose = document.getElementById("banner-close");

    const loadingSpinner = document.getElementById("loading-spinner");
    const profileContainer = document.getElementById("profile-container");

    // Profile elements
    const playerBackdrop = document.getElementById("profile-backdrop");
    const playerCardImg = document.getElementById("player-card-img");
    const playerLevel = document.getElementById("player-level");
    const playerName = document.getElementById("player-name");
    const playerTag = document.getElementById("player-tag");
    const playerRegion = document.getElementById("player-region");
    const btnShare = document.getElementById("btn-share");

    // Rank & Stats elements
    const rankIcon = document.getElementById("rank-icon");
    const rankName = document.getElementById("rank-name");
    const rankRr = document.getElementById("rank-rr");
    const rrFill = document.getElementById("rr-fill");
    const rankLastChange = document.getElementById("rank-last-change");

    const peakRankIcon = document.getElementById("peak-rank-icon");
    const peakRankName = document.getElementById("peak-rank-name");
    const peakSeason = document.getElementById("peak-season");

    const statKd = document.getElementById("stat-kd");
    const statWinrate = document.getElementById("stat-winrate");
    const statHs = document.getElementById("stat-hs");
    const statAcs = document.getElementById("stat-acs");

    // Matches elements
    const matchesList = document.getElementById("matches-list");
    const filterTabs = document.querySelectorAll(".tab-btn");

    // Match Details Modal
    const matchModal = document.getElementById("match-modal");
    const modalClose = document.getElementById("modal-close");
    const modalMapName = document.getElementById("modal-map-name");
    const modalModeBadge = document.getElementById("modal-mode-badge");
    const modalScore = document.getElementById("modal-score");
    const teamBlueScore = document.getElementById("team-blue-score");
    const teamRedScore = document.getElementById("team-red-score");
    const teamBlueBody = document.getElementById("team-blue-body");
    const teamRedBody = document.getElementById("team-red-body");

    // Quick tag buttons
    const quickTagBtns = document.querySelectorAll(".tag-btn[data-search]");

    // State
    let currentPlayerData = null;
    let currentMatches = [];
    let activeFilterMode = "all";

    // Known popular / pro suggestions
    const POPULAR_PLAYERS = [
        { name: "wisax", tag: "wisax", region: "eu" },
        { name: "TenZ", tag: "SEN", region: "na" },
        { name: "Boaster", tag: "FNC", region: "eu" },
        { name: "ScreaM", tag: "EDG", region: "eu" },
        { name: "Aspas", tag: "LEV", region: "na" },
        { name: "Derke", tag: "FNC", region: "eu" },
        { name: "cNed", tag: "FUT", region: "eu" },
        { name: "Chronos", tag: "FR1", region: "eu" }
    ];

    // ==========================================
    // Recent Searches & Suggestions Engine
    // ==========================================
    function getRecentSearches() {
        try {
            return JSON.parse(localStorage.getItem("valo_recent_searches") || "[]");
        } catch {
            return [];
        }
    }

    function saveRecentSearch(name, tag, region) {
        let recents = getRecentSearches();
        recents = recents.filter(item => !(item.name.toLowerCase() === name.toLowerCase() && item.tag.toLowerCase() === tag.toLowerCase()));
        recents.unshift({ name, tag, region });
        if (recents.length > 6) recents = recents.slice(0, 6);
        localStorage.setItem("valo_recent_searches", JSON.stringify(recents));
    }

    function removeRecentSearch(name, tag, e) {
        if (e) e.stopPropagation();
        let recents = getRecentSearches();
        recents = recents.filter(item => !(item.name.toLowerCase() === name.toLowerCase() && item.tag.toLowerCase() === tag.toLowerCase()));
        localStorage.setItem("valo_recent_searches", JSON.stringify(recents));
        renderSuggestions(playerInput.value);
    }

    function renderSuggestions(queryText = "") {
        if (!searchSuggestions) return;
        const q = (queryText || "").toLowerCase().trim();
        searchSuggestions.innerHTML = "";

        const recents = getRecentSearches();
        let matchedRecents = recents;
        let matchedPopular = POPULAR_PLAYERS;

        if (q) {
            matchedRecents = recents.filter(p => 
                `${p.name}#${p.tag}`.toLowerCase().includes(q) || p.name.toLowerCase().includes(q)
            );
            matchedPopular = POPULAR_PLAYERS.filter(p => 
                `${p.name}#${p.tag}`.toLowerCase().includes(q) || p.name.toLowerCase().includes(q)
            );
        }

        // Avoid showing duplicate in popular if already in recents
        matchedPopular = matchedPopular.filter(pop => 
            !matchedRecents.some(rec => rec.name.toLowerCase() === pop.name.toLowerCase() && rec.tag.toLowerCase() === pop.tag.toLowerCase())
        );

        if (matchedRecents.length === 0 && matchedPopular.length === 0) {
            searchSuggestions.classList.add("hidden");
            return;
        }

        // Section: Recherches récentes
        if (matchedRecents.length > 0) {
            const secRecents = document.createElement("div");
            secRecents.className = "suggestion-section";
            secRecents.innerHTML = `<div class="suggestion-section-title"><i class="fa-solid fa-clock-rotate-left"></i> RÉCENTES</div>`;

            matchedRecents.forEach(p => {
                const item = document.createElement("div");
                item.className = "suggestion-item";
                item.innerHTML = `
                    <div class="suggestion-left">
                        <i class="fa-regular fa-clock suggestion-icon"></i>
                        <span class="suggestion-name">${p.name}</span>
                        <span class="suggestion-tag">#${p.tag}</span>
                        <span class="suggestion-region-badge">${p.region.toUpperCase()}</span>
                    </div>
                    <button type="button" class="suggestion-del-btn" title="Supprimer de l'historique">&times;</button>
                `;

                item.addEventListener("click", () => {
                    selectSuggestion(p.name, p.tag, p.region);
                });

                const delBtn = item.querySelector(".suggestion-del-btn");
                delBtn.addEventListener("click", (e) => {
                    removeRecentSearch(p.name, p.tag, e);
                });

                secRecents.appendChild(item);
            });
            searchSuggestions.appendChild(secRecents);
        }

        // Section: Suggestions Populaires
        if (matchedPopular.length > 0) {
            const secPop = document.createElement("div");
            secPop.className = "suggestion-section";
            secPop.innerHTML = `<div class="suggestion-section-title"><i class="fa-solid fa-fire text-red"></i> SUGGESTIONS</div>`;

            matchedPopular.forEach(p => {
                const item = document.createElement("div");
                item.className = "suggestion-item";
                item.innerHTML = `
                    <div class="suggestion-left">
                        <i class="fa-solid fa-crosshairs suggestion-icon text-red"></i>
                        <span class="suggestion-name">${p.name}</span>
                        <span class="suggestion-tag">#${p.tag}</span>
                        <span class="suggestion-region-badge">${p.region.toUpperCase()}</span>
                    </div>
                `;

                item.addEventListener("click", () => {
                    selectSuggestion(p.name, p.tag, p.region);
                });

                secPop.appendChild(item);
            });
            searchSuggestions.appendChild(secPop);
        }

        searchSuggestions.classList.remove("hidden");
    }

    function selectSuggestion(name, tag, region) {
        playerInput.value = `${name}#${tag}`;
        if (region && regionSelect) regionSelect.value = region.toLowerCase();
        searchSuggestions.classList.add("hidden");
        triggerSearch();
    }

    // Input event listeners for suggestions
    playerInput.addEventListener("focus", () => {
        renderSuggestions(playerInput.value);
    });

    playerInput.addEventListener("input", () => {
        renderSuggestions(playerInput.value);
    });

    document.addEventListener("click", (e) => {
        if (!playerInput.contains(e.target) && !searchSuggestions?.contains(e.target)) {
            searchSuggestions?.classList.add("hidden");
        }
    });

    // Banner handler
    function showBanner(message, isError = false) {
        bannerText.textContent = message;
        statusBanner.className = isError ? "status-banner banner-error" : "status-banner";
        statusBanner.classList.remove("hidden");
    }

    bannerClose?.addEventListener("click", () => {
        statusBanner.classList.add("hidden");
    });

    // Check URL parameters on startup (?name=TenZ&tag=SEN&region=na)
    const urlParams = new URLSearchParams(window.location.search);
    const urlName = urlParams.get("name");
    const urlTag = urlParams.get("tag");
    const urlRegion = urlParams.get("region");

    if (urlName && urlTag) {
        playerInput.value = `${urlName}#${urlTag}`;
        if (urlRegion) regionSelect.value = urlRegion.toLowerCase();
        fetchPlayerData(urlName, urlTag, regionSelect.value);
    }

    // Quick search tags
    quickTagBtns.forEach(btn => {
        btn.addEventListener("click", () => {
            const searchVal = btn.getAttribute("data-search");
            const regVal = btn.getAttribute("data-region");
            playerInput.value = searchVal;
            if (regVal) regionSelect.value = regVal;
            triggerSearch();
        });
    });

    // Search form submission
    searchForm.addEventListener("submit", (e) => {
        e.preventDefault();
        triggerSearch();
    });

    function triggerSearch() {
        searchSuggestions?.classList.add("hidden");
        const rawInput = playerInput.value.trim();
        if (!rawInput) return;

        let name = "";
        let tag = "";

        if (rawInput.includes("#")) {
            const parts = rawInput.split("#");
            name = parts[0].trim();
            tag = parts[1].trim();
        } else {
            showBanner("Veuillez préciser votre Riot ID complet avec son hashtag (ex: MonPseudo#EUW, TenZ#SEN)", true);
            return;
        }

        const region = regionSelect.value;

        // Save to recent searches
        saveRecentSearch(name, tag, region);

        // Update URL query string without reloading page for direct sharing
        const newUrl = `${window.location.pathname}?name=${encodeURIComponent(name)}&tag=${encodeURIComponent(tag)}&region=${encodeURIComponent(region)}`;
        window.history.pushState({ path: newUrl }, "", newUrl);

        fetchPlayerData(name, tag, region);
    }

    // Main fetch function
    async function fetchPlayerData(name, tag, region) {
        loadingSpinner.classList.remove("hidden");
        profileContainer.classList.add("hidden");
        statusBanner.classList.add("hidden");

        try {
            // 1. Fetch player overview
            const playerRes = await fetch(`/api/player/${region}/${encodeURIComponent(name)}/${encodeURIComponent(tag)}`);
            const playerData = await playerRes.json();

            if (!playerRes.ok || playerData.status >= 400) {
                loadingSpinner.classList.add("hidden");
                showBanner(playerData.error || "Impossible de récupérer ce joueur. Vérifiez le pseudo#TAG.", true);
                return;
            }

            currentPlayerData = playerData.data;
            renderProfile(currentPlayerData);

            // 2. Fetch recent matches
            const matchesRes = await fetch(`/api/matches/${region}/${encodeURIComponent(name)}/${encodeURIComponent(tag)}`);
            const matchesData = await matchesRes.json();

            if (matchesRes.ok && matchesData.data) {
                currentMatches = matchesData.data;
                calculateAggregateStats(currentMatches, currentPlayerData);
                renderMatches(currentMatches);
            }

            loadingSpinner.classList.add("hidden");
            profileContainer.classList.remove("hidden");

        } catch (err) {
            console.error("Erreur de requête:", err);
            loadingSpinner.classList.add("hidden");
            showBanner("Une erreur réseau est survenue lors de la communication avec le serveur.", true);
        }
    }

    // Render Profile Header & Rank
    function renderProfile(data) {
        playerName.textContent = data.name || "--";
        playerTag.textContent = `#${data.tag || "--"}`;
        playerRegion.textContent = data.region || "EU";
        if (data.region && regionSelect) {
            regionSelect.value = data.region.toLowerCase();
        }
        playerLevel.textContent = data.account_level || 1;

        if (data.card) {
            playerCardImg.src = data.card;
            playerBackdrop.style.backgroundImage = `url('${data.card}')`;
        }

        // Rank info
        const curRank = data.current_rank || {};
        rankName.textContent = curRank.name || "Unranked";
        rankRr.textContent = curRank.rr !== undefined ? curRank.rr : 0;
        rrFill.style.width = `${Math.min(100, Math.max(0, curRank.rr || 0))}%`;
        
        if (curRank.icon) {
            rankIcon.src = curRank.icon;
        }

        if (curRank.last_change) {
            rankLastChange.textContent = `Dernier match : ${curRank.last_change} RR`;
        }

        // Peak Rank
        const peak = data.peak_rank || {};
        peakRankName.textContent = peak.name || "Non disponible";
        peakSeason.textContent = peak.season ? `Saison ${peak.season}` : "";
        if (curRank.icon) {
            peakRankIcon.src = curRank.icon;
        }
    }

    // Compute stats from match history
    function calculateAggregateStats(matches, profile) {
        if (!matches || matches.length === 0) {
            if (profile.stats) {
                statKd.textContent = profile.stats.kd || "--";
                statWinrate.textContent = `${profile.stats.winrate || 0}%`;
                statHs.textContent = `${profile.stats.headshot_pct || 0}%`;
                statAcs.textContent = profile.stats.avg_combat_score || "--";
            }
            return;
        }

        let totalKills = 0;
        let totalDeaths = 0;
        let totalWins = 0;
        let totalHsPct = 0;
        let totalAcs = 0;

        matches.forEach(m => {
            const st = m.stats || {};
            totalKills += (st.kills || 0);
            totalDeaths += (st.deaths || 0);
            if (m.result === "Victory") totalWins++;
            totalHsPct += (st.headshot_pct || 0);
            totalAcs += (st.acs || 0);
        });

        const kd = (totalKills / Math.max(1, totalDeaths)).toFixed(2);
        const winrate = Math.round((totalWins / matches.length) * 100);
        const avgHs = (totalHsPct / matches.length).toFixed(1);
        const avgAcs = Math.round(totalAcs / matches.length);

        statKd.textContent = kd;
        statWinrate.textContent = `${winrate}%`;
        statHs.textContent = `${avgHs}%`;
        statAcs.textContent = avgAcs;
    }

    // Render matches list
    function renderMatches(matches) {
        matchesList.innerHTML = "";

        const filtered = activeFilterMode === "all" 
            ? matches 
            : matches.filter(m => (m.mode || "").toLowerCase() === activeFilterMode);

        if (filtered.length === 0) {
            matchesList.innerHTML = `<div class="empty-state" style="text-align:center; padding:30px; color:var(--text-muted);">Aucun match trouvé pour ce mode de jeu.</div>`;
            return;
        }

        filtered.forEach(m => {
            const item = document.createElement("div");
            const resultClass = (m.result || "defeat").toLowerCase();
            item.className = `match-item ${resultClass}`;

            const timeAgo = formatTimeAgo(m.timestamp);

            item.innerHTML = `
                <div class="match-col-map">
                    <span class="map-name">${m.map?.name || "CARTE"}</span>
                    <span class="match-mode">${m.mode || "Normal"} • ${timeAgo}</span>
                </div>

                <div class="match-col-agent">
                    <img src="${m.agent?.icon || ''}" alt="${m.agent?.name}" class="agent-thumb">
                    <span class="agent-name">${m.agent?.name || "Agent"}</span>
                </div>

                <div class="match-col-score">
                    <span class="score-badge ${resultClass}">${m.score_display || `${m.rounds_won}-${m.rounds_lost}`}</span>
                    <span class="result-label ${resultClass}">${m.result === "Victory" ? "Victoire" : (m.result === "Draw" ? "Égalité" : "Défaite")}</span>
                </div>

                <div class="match-col-stats">
                    <div class="stat-mini">
                        <span class="stat-mini-label">K / D / A</span>
                        <span class="stat-mini-val">${m.stats?.kills}/${m.stats?.deaths}/${m.stats?.assists}</span>
                    </div>
                    <div class="stat-mini">
                        <span class="stat-mini-label">RATIO</span>
                        <span class="stat-mini-val text-cyan">${m.stats?.kd}</span>
                    </div>
                    <div class="stat-mini">
                        <span class="stat-mini-label">ACS</span>
                        <span class="stat-mini-val text-red">${m.stats?.acs}</span>
                    </div>
                    <div class="stat-mini">
                        <span class="stat-mini-label">HS%</span>
                        <span class="stat-mini-val text-yellow">${m.stats?.headshot_pct}%</span>
                    </div>
                </div>

                <div class="match-col-action">
                    <button class="btn btn-secondary btn-sm" style="padding: 6px 12px; font-size: 0.8rem;">
                        <i class="fa-solid fa-list-ol"></i> Détails
                    </button>
                </div>
            `;

            item.addEventListener("click", () => {
                openMatchDetails(m.match_id);
            });

            matchesList.appendChild(item);
        });
    }

    // Filter tabs
    filterTabs.forEach(tab => {
        tab.addEventListener("click", () => {
            filterTabs.forEach(t => t.classList.remove("active"));
            tab.classList.add("active");
            activeFilterMode = tab.getAttribute("data-mode");
            renderMatches(currentMatches);
        });
    });

    // Match Details Modal
    async function openMatchDetails(matchId) {
        if (!matchId) return;

        const pName = currentPlayerData?.name || "TenZ";
        const pTag = currentPlayerData?.tag || "SEN";

        try {
            const res = await fetch(`/api/match/${matchId}?name=${encodeURIComponent(pName)}&tag=${encodeURIComponent(pTag)}`);
            const json = await res.json();

            if (json.status === 200 && json.data) {
                populateMatchModal(json.data);
                matchModal.classList.remove("hidden");
            }
        } catch (err) {
            console.error("Erreur chargement détails du match:", err);
        }
    }

    function populateMatchModal(data) {
        modalMapName.textContent = (data.map?.name || "Ascent").toUpperCase();
        modalModeBadge.textContent = (data.mode || "Compétitif").toUpperCase();
        modalScore.textContent = `${data.score?.blue || 0} - ${data.score?.red || 0}`;

        teamBlueScore.textContent = `${data.score?.blue || 0} MANCHES`;
        teamRedScore.textContent = `${data.score?.red || 0} MANCHES`;

        renderTeamTable(teamBlueBody, data.team_blue || []);
        renderTeamTable(teamRedBody, data.team_red || []);
    }

    function renderTeamTable(tbody, players) {
        tbody.innerHTML = "";
        players.forEach(p => {
            const tr = document.createElement("tr");
            if (p.is_current_player) {
                tr.classList.add("current-user-row");
            }

            tr.innerHTML = `
                <td>
                    <div class="player-cell">
                        <img src="${p.agent?.icon || ''}" class="player-table-agent-icon" alt="${p.agent?.name}">
                        <span>${p.agent?.name || 'Agent'}</span>
                    </div>
                </td>
                <td><strong>${p.name}</strong><span style="color:var(--text-muted); font-size:0.8rem;">#${p.tag}</span></td>
                <td><span style="font-size:0.8rem; color:var(--text-muted);">${p.rank?.name || 'Unranked'}</span></td>
                <td><strong class="text-red">${p.acs}</strong></td>
                <td>${p.kills}</td>
                <td>${p.deaths}</td>
                <td>${p.assists}</td>
                <td><span class="text-cyan">${p.kd}</span></td>
                <td><span class="text-yellow">${p.headshot_pct}%</span></td>
            `;
            tbody.appendChild(tr);
        });
    }

    modalClose?.addEventListener("click", () => matchModal.classList.add("hidden"));
    matchModal?.addEventListener("click", (e) => {
        if (e.target === matchModal) matchModal.classList.add("hidden");
    });

    // Share Profile button (copies URL to clipboard)
    btnShare?.addEventListener("click", () => {
        const shareUrl = window.location.href;
        navigator.clipboard.writeText(shareUrl).then(() => {
            showBanner("Lien du profil copié dans le presse-papier ! Envoyez-le à vos potes.");
        }).catch(() => {
            showBanner("Impossible de copier automatiquement le lien. Copiez l'URL de votre barre d'adresse.");
        });
    });

    // Helpers
    function formatTimeAgo(timestamp) {
        if (!timestamp) return "Récemment";
        const now = Math.floor(Date.now() / 1000);
        const diff = Math.max(0, now - timestamp);

        if (diff < 3600) {
            const m = Math.floor(diff / 60);
            return `Il y a ${m} min`;
        } else if (diff < 86400) {
            const h = Math.floor(diff / 3600);
            return `Il y a ${h} j`;
        } else {
            const d = Math.floor(diff / 86400);
            return `Il y a ${d} j`;
        }
    }
});
