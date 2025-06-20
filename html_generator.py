"""
HTML generation module for musician network visualization.
Creates the complete interactive HTML file with all tabs and functionality.
"""

import json


def get_html_template():
    """Return the complete HTML template with placeholders for data."""
    return '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Musician Network - Complete Analysis</title>
    <script src="https://cdn.jsdelivr.net/npm/echarts@5.4.3/dist/echarts.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body {
            margin: 0;
            padding: 20px;
            font-family: Arial, sans-serif;
            background-color: #1a1a1a;
            color: #e0e0e0;
        }
        .header {
            text-align: center;
            margin-bottom: 30px;
        }
        .title {
            color: #ffffff;
            margin-bottom: 10px;
        }
        .subtitle {
            color: #b0b0b0;
            font-size: 14px;
        }
        
        /* Tab Navigation */
        .tab-container {
            margin-bottom: 20px;
        }
        .tab-nav {
            display: flex;
            background: #2d2d2d;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.3);
            overflow: hidden;
        }
        .tab-btn {
            flex: 1;
            padding: 15px 20px;
            border: none;
            background: #2d2d2d;
            color: #e0e0e0;
            cursor: pointer;
            transition: all 0.3s ease;
            font-size: 14px;
            font-weight: 500;
        }
        .tab-btn:hover {
            background: #3a3a3a;
        }
        .tab-btn.active {
            background: #0066cc;
            color: white;
        }
        .tab-btn:not(:last-child) {
            border-right: 1px solid #404040;
        }
        
        /* Tab Content */
        .tab-content {
            display: none;
            background: #2d2d2d;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.3);
            padding: 20px;
        }
        .tab-content.active {
            display: block;
        }
        
        /* Network Tab Styles */
        #container {
            width: 100%;
            height: 800px;
            background-color: #1e1e1e;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.3);
        }
        
        .controls {
            display: flex;
            gap: 20px;
            margin-bottom: 20px;
            flex-wrap: wrap;
            align-items: flex-end;
        }
        
        .control-group {
            display: flex;
            flex-direction: column;
            gap: 5px;
        }
        
        .control-group label {
            font-size: 12px;
            font-weight: bold;
            color: #e0e0e0;
        }
        
        select, input[type="range"] {
            padding: 8px 12px;
            border: 1px solid #555;
            border-radius: 4px;
            font-size: 14px;
            background: #3a3a3a;
            color: #e0e0e0;
        }
        
        .multi-select {
            position: relative;
            min-width: 250px;
        }
        
        .multi-select-input {
            width: 100%;
            padding: 8px 12px;
            border: 1px solid #555;
            border-radius: 4px;
            font-size: 14px;
            cursor: pointer;
            background: #3a3a3a;
            color: #e0e0e0;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        
        .multi-select-input:hover {
            border-color: #0066cc;
        }
        
        .multi-select-arrow {
            margin-left: 8px;
            font-size: 12px;
            color: #b0b0b0;
            transition: transform 0.2s;
        }
        
        .multi-select-arrow.open {
            transform: rotate(180deg);
        }
        
        .multi-select-dropdown {
            display: none;
            position: absolute;
            top: 100%;
            left: 0;
            right: 0;
            background: #3a3a3a;
            border: 1px solid #555;
            border-radius: 4px;
            max-height: 400px;
            z-index: 1000;
            box-shadow: 0 4px 12px rgba(0,0,0,0.4);
            overflow: hidden;
        }
        
        .multi-select-dropdown.show {
            display: block;
        }
        
        .multi-select-search {
            padding: 12px;
            border-bottom: 1px solid #555;
            background: #2d2d2d;
        }
        
        .multi-select-search input {
            width: 100%;
            padding: 8px 12px;
            border: 1px solid #555;
            border-radius: 4px;
            font-size: 14px;
            outline: none;
            background: #4a4a4a;
            color: #e0e0e0;
        }
        
        .multi-select-search input:focus {
            border-color: #0066cc;
            box-shadow: 0 0 0 2px rgba(0, 102, 204, 0.25);
        }
        
        .multi-select-controls {
            padding: 8px 12px;
            border-bottom: 1px solid #555;
            background: #2d2d2d;
            display: flex;
            gap: 10px;
        }
        
        .multi-select-control-btn {
            padding: 4px 8px;
            font-size: 12px;
            border: 1px solid #0066cc;
            background: #3a3a3a;
            color: #0066cc;
            border-radius: 3px;
            cursor: pointer;
            transition: all 0.2s;
        }
        
        .multi-select-control-btn:hover {
            background: #0066cc;
            color: white;
        }
        
        .multi-select-options {
            max-height: 250px;
            overflow-y: auto;
        }
        
        .multi-select-option {
            padding: 10px 12px;
            cursor: pointer;
            border-bottom: 1px solid #555;
            display: flex;
            align-items: center;
            transition: background-color 0.2s;
            color: #e0e0e0;
        }
        
        .multi-select-option:hover {
            background-color: #4a4a4a;
        }
        
        .multi-select-option.selected {
            background-color: #1a4d7a;
            color: #66b3ff;
        }
        
        .multi-select-option.hidden {
            display: none;
        }
        
        .multi-select-checkbox {
            margin-right: 8px;
            width: 16px;
            height: 16px;
            cursor: pointer;
        }
        
        .multi-select-count {
            padding: 8px 12px;
            background: #3a3a3a;
            border-top: 1px solid #555;
            font-size: 12px;
            color: #b0b0b0;
            text-align: center;
        }
        
        .reset-button {
            padding: 8px 16px;
            background: #dc3545;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 14px;
            height: fit-content;
            align-self: flex-end;
            margin-left: auto;
            transition: background-color 0.2s;
        }
        
        .reset-button:hover {
            background: #c82333;
        }
        
        .custom-filters-container {
            display: flex;
            flex-direction: column;
            gap: 10px;
            margin-bottom: 10px;
        }
        
        .custom-filter-item {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 12px;
            background: #3a3a3a;
            border-radius: 6px;
            border: 1px solid #555;
        }
        
        .custom-filter-column {
            min-width: 150px;
            flex-shrink: 0;
        }
        
        .custom-filter-column select {
            width: 100%;
            padding: 8px 12px;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 14px;
            height: 38px;
            box-sizing: border-box;
        }
        
        .custom-filter-values {
            flex: 1;
            min-width: 200px;
            margin-right: 8px;
        }
        
        .custom-filter-values .multi-select-input {
            height: 38px;
            box-sizing: border-box;
            padding: 8px 12px;
            font-size: 14px;
        }
        
        .custom-filter-remove {
            padding: 8px 12px;
            background: #dc3545;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 14px;
            height: 38px;
            min-width: 38px;
            flex-shrink: 0;
            box-sizing: border-box;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .custom-filter-remove:hover {
            background: #c82333;
        }
        
        .add-filter-btn {
            padding: 8px 12px;
            background: #28a745;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 13px;
            transition: background-color 0.2s;
        }
        
        .add-filter-btn:hover {
            background: #218838;
        }
        
        .custom-filter-label {
            font-size: 12px;
            font-weight: bold;
            color: #b0b0b0;
            margin-bottom: 4px;
        }
        
        .stats-panel {
            background: #3a3a3a;
            padding: 15px;
            border-radius: 6px;
            margin-bottom: 20px;
        }
        
        .stats-item {
            display: inline-block;
            margin-right: 20px;
            font-size: 14px;
            color: #b0b0b0;
        }
        
        .stats-value {
            font-weight: bold;
            color: #ffffff;
        }
        
        .info-panel {
            margin-top: 20px;
            background-color: #2d2d2d;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.3);
            padding: 20px;
            display: none;
        }
        
        .info-panel.active {
            display: block;
        }
        
        .info-section {
            margin-bottom: 20px;
        }
        
        .info-section h4 {
            margin: 0 0 10px 0;
            color: #ffffff;
            border-bottom: 2px solid #0066cc;
            padding-bottom: 5px;
        }
        
        .info-content {
            line-height: 1.6;
        }
        
        .tag {
            display: inline-block;
            background: #1a4d7a;
            color: #66b3ff;
            padding: 4px 8px;
            margin: 2px;
            border-radius: 12px;
            font-size: 12px;
        }
        
        /* Analysis Tab Styles */
        .analysis-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 20px;
        }
        
        .chart-container {
            background: #2d2d2d;
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.3);
        }
        
        .chart-container h3 {
            margin: 0 0 15px 0;
            color: #ffffff;
        }
        
        .musician-list {
            max-height: 400px;
            overflow-y: auto;
        }
        
        .musician-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px;
            border-bottom: 1px solid #555;
            cursor: pointer;
            transition: background-color 0.2s;
        }
        
        .musician-item:hover {
            background-color: #3a3a3a;
        }
        
        .musician-name {
            font-weight: 500;
            color: #ffffff;
        }
        
        .musician-stats {
            font-size: 12px;
            color: #b0b0b0;
        }
        
        .search-container {
            margin-bottom: 20px;
        }
        
        .search-input {
            width: 100%;
            padding: 12px;
            border: 1px solid #555;
            border-radius: 4px;
            font-size: 16px;
            background: #3a3a3a;
            color: #e0e0e0;
        }
        
        .debug-info {
            background: #3a3a3a;
            padding: 15px;
            border-radius: 6px;
            margin: 10px 0;
        }
        
        .debug-section {
            margin-bottom: 15px;
        }
        
        .debug-section h4 {
            margin: 0 0 8px 0;
            color: #ffffff;
        }
        
        .debug-list {
            list-style: none;
            padding: 0;
            margin: 0;
        }
        
        .debug-list li {
            padding: 4px 0;
            border-bottom: 1px solid #555;
        }
        
        .click-hint {
            text-align: center;
            color: #e0e0e0;
            font-size: 14px;
            margin-bottom: 15px;
            padding: 10px;
            background: #1a4d7a;
            border-radius: 4px;
            border: 1px solid #0066cc;
        }
        
        .filters-section {
            background: #2d2d2d;
            border: 1px solid #555;
            border-radius: 8px;
            margin: 20px;
            padding: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.3);
        }
        
        /* Additional dark mode styles */
        button {
            background: #0066cc;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            cursor: pointer;
            transition: background-color 0.2s;
        }
        
        button:hover {
            background: #0052a3;
        }
        
        .add-filter-btn {
            background: #28a745;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            cursor: pointer;
            transition: background-color 0.2s;
        }
        
        .add-filter-btn:hover {
            background: #218838;
        }
        
        .reset-button {
            background: #dc3545;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            cursor: pointer;
            transition: background-color 0.2s;
        }
        
        .reset-button:hover {
            background: #c82333;
        }
        
        .stats-panel {
            background: #3a3a3a;
            border-radius: 6px;
            padding: 15px;
            margin-top: 15px;
            display: flex;
            gap: 20px;
            flex-wrap: wrap;
            border: 1px solid #555;
        }
        
        .stats-item {
            color: #b0b0b0;
            font-size: 14px;
        }
        
        .stats-value {
            color: #ffffff;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1 class="title">🎵 Musician Network Analysis</h1>
        <p class="subtitle">Explore connections, discover top musicians, and analyze your collection</p>
    </div>
    
    <!-- Global Filters Section -->
    <div class="filters-section">
        <div class="controls">
            <div class="control-group">
                <label for="roleFilter">Roles:</label>
                <div class="multi-select">
                    <div class="multi-select-input" onclick="toggleRoleDropdown()">
                        <span id="roleFilterDisplay">All roles selected</span>
                        <span class="multi-select-arrow" id="roleArrow">▼</span>
            </div>
                    <div id="roleDropdown" class="multi-select-dropdown">
                        <div class="multi-select-search">
                            <input type="text" id="roleSearchInput" placeholder="Search roles..." oninput="searchRoles()" onclick="event.stopPropagation()">
            </div>
                        <div class="multi-select-controls">
                            <button class="multi-select-control-btn" onclick="selectAllRoles()">Select All</button>
                            <button class="multi-select-control-btn" onclick="deselectAllRoles()">Deselect All</button>
                            <button class="multi-select-control-btn" onclick="selectCommonRoles()">Common Only</button>
                        </div>
                        <div class="multi-select-options" id="roleOptions">
                            <!-- Role options will be populated here -->
                        </div>
                        <div class="multi-select-count" id="roleCount">
                            0 of 0 roles selected
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="control-group">
                <label>Custom Filters:</label>
                <div class="custom-filters-container" id="customFiltersContainer">
                    <!-- Custom filters will be added here dynamically -->
                    </div>
                <button class="add-filter-btn" onclick="addCustomFilter()">+ Add Custom Filter</button>
            </div>
            
            <button onclick="resetFilters()" class="reset-button">Reset Filters</button>
        </div>
        
        <div class="stats-panel" id="statsPanel">
            <span class="stats-item">Musicians: <span class="stats-value" id="musicianCount">0</span></span>
            <span class="stats-item">Artists: <span class="stats-value" id="artistCount">0</span></span>
            <span class="stats-item">Connections: <span class="stats-value" id="connectionCount">0</span></span>
            <span class="stats-item">Active Filters: <span class="stats-value" id="activeFilters">None</span></span>
        </div>
        </div>
        
    <!-- Tab Navigation -->
    <div class="tab-container">
        <div class="tab-nav">
            <button class="tab-btn active" onclick="showTab('network')">🌐 Network</button>
            <button class="tab-btn" onclick="showTab('top-musicians')">🏆 Top Musicians</button>
            <button class="tab-btn" onclick="showTab('session-musicians')">🎭 Session Musicians</button>
            <button class="tab-btn" onclick="showTab('debug')">🔍 Debug Musician</button>
        </div>
    </div>
    
    <!-- Network Tab -->
    <div id="network-tab" class="tab-content active">
        <div class="click-hint">💡 Click on any node to see detailed information</div>
        
        <div id="container"></div>
        
        <div class="info-panel" id="infoPanel">
            <h3 id="nodeTitle">Node Details</h3>
            <div id="nodeInfo"></div>
        </div>
    </div>
    
    <!-- Top Musicians Tab -->
    <div id="top-musicians-tab" class="tab-content">
        <h2>🏆 Top Musicians by Record Count</h2>
        <p>Musicians ranked by total record appearances, showing main artist vs session work.</p>
        
        <div class="analysis-grid">
            <div class="chart-container">
                <h3>Most Active Musicians</h3>
                <div style="margin-bottom: 15px; padding: 10px; background: #3a3a3a; border-radius: 5px; font-size: 14px; color: #e0e0e0;">
                    <div style="display: flex; flex-wrap: wrap; gap: 20px; align-items: center;">
                        <div><strong>Bar Colors:</strong> Gradient by Ranking</div>
                        <div><strong>Interaction:</strong> 
                            Hover for details | Click for full info
                        </div>
                    </div>
                </div>
                <div id="topMusiciansChart" style="width: 100%; height: 500px;"></div>
            </div>
            
            <div class="chart-container">
                <h3>Main Artist vs Session Work</h3>
                <div style="margin-bottom: 15px; padding: 10px; background: #3a3a3a; border-radius: 5px; font-size: 14px; color: #e0e0e0;">
                    <div style="display: flex; flex-wrap: wrap; gap: 20px; align-items: center;">
                        <div><strong>Bubble Size:</strong> Total Records</div>
                        <div><strong>Categories:</strong> 
                            <span style="color: #e74c3c;">●</span> Session Only | 
                            <span style="color: #f39c12;">●</span> Balanced | 
                            <span style="color: #27ae60;">●</span> Main Artist Only
                        </div>
                    </div>
                </div>
                <div id="sessionScatterChart" style="width: 100%; height: 500px;"></div>
            </div>
        </div>
        

    </div>
    
    <!-- Session Musicians Tab -->
    <div id="session-musicians-tab" class="tab-content">
        <h2>🎭 Hidden Gems: Top Session Musicians</h2>
        <p>Musicians who appear on many records but are rarely the main artist - the unsung heroes!</p>
        
        <div class="chart-container">
            <h3>Session Musicians (70%+ session work, 2+ records)</h3>
            <div id="sessionMusiciansList" class="musician-list"></div>
        </div>
        
        <div id="sessionMusicianDetails" class="debug-info" style="display: none;">
            <h3 id="selectedSessionMusician">Musician Details</h3>
            <div id="sessionMusicianInfo"></div>
        </div>
    </div>
    
    <!-- Debug Tab -->
    <div id="debug-tab" class="tab-content">
        <h2>🔍 Debug Musician Connections</h2>
        <p>Search for a specific musician to see their exact connections and verify data.</p>
        
        <div class="search-container">
            <input type="text" id="debugSearchInput" class="search-input" placeholder="Enter musician name to debug..." oninput="searchMusicians()">
        </div>
        
        <div id="debugResults"></div>
        
        <div id="debugDetails" class="debug-info" style="display: none;">
            <h3 id="debugMusicianName">Musician Debug Info</h3>
            <div id="debugMusicianInfo"></div>
        </div>
    </div>

    <script>
        // Global data variables
        let fullNetworkData = {network_data_placeholder};
        let currentData = JSON.parse(JSON.stringify(fullNetworkData));
        let myChart;
        let selectedRoles = new Set();
        let customFilters = []; // Array of custom filter objects
        let nextCustomFilterId = 1;
        
        // Analysis data
        let musicianStatsData = {musician_stats_placeholder};
        let sessionMusiciansData = {session_musicians_placeholder};
        
        // Custom filter data
        let customFilterData = {custom_filter_data_placeholder};
        
        // Initialize ECharts
        myChart = echarts.init(document.getElementById('container'));
        
        // [JAVASCRIPT FUNCTIONS WILL BE ADDED HERE]
        {javascript_functions}
        
        // Initialize everything
        populateFilters();
        updateChart();
        updateStats();
        
        // Event listeners
        
        myChart.on('click', function(params) {
            if (params.dataType === 'node') {
                showNodeDetails(params.data);
            }
        });
        
        window.addEventListener('resize', function() {
            myChart.resize();
        });
        
        document.addEventListener('click', function(event) {
            if (!event.target.closest('#infoPanel') && !event.target.closest('#container')) {
                hideInfoPanel();
            }
        });
    </script>
</body>
</html>
'''


def get_javascript_functions():
    """Return all JavaScript functions for the HTML file."""
    return '''
        // Tab switching
        function showTab(tabName) {
            // Hide all tabs
            document.querySelectorAll('.tab-content').forEach(tab => tab.classList.remove('active'));
            document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
            
            // Show selected tab
            document.getElementById(tabName + '-tab').classList.add('active');
            event.target.classList.add('active');
            
            // Initialize tab-specific content
            if (tabName === 'top-musicians') {
                initTopMusiciansTab();
            } else if (tabName === 'session-musicians') {
                initSessionMusiciansTab();
            } else if (tabName === 'debug') {
                initDebugTab();
            }
        }
        
        // Network tab functions
        function populateFilters() {
            const roleOptions = document.getElementById('roleOptions');
            
            // Get unique values from full data
            const roles = [...new Set(fullNetworkData.links.flatMap(link => link.roles || []))].sort();
            
            // Store all roles globally for search functionality
            window.allRoles = roles;
            
            // Initialize all roles as selected BEFORE populating options
            selectedRoles = new Set(roles);
            
            // Populate role filter with enhanced structure
            populateRoleOptions(roles);
            updateRoleFilterDisplay();
            updateRoleCheckboxes();
        }
        
        function populateRoleOptions(roles) {
            const roleOptions = document.getElementById('roleOptions');
            roleOptions.innerHTML = '';
            
            roles.forEach(role => {
                const div = document.createElement('div');
                div.className = 'multi-select-option';
                div.dataset.role = role;
                
                const checkbox = document.createElement('input');
                checkbox.type = 'checkbox';
                checkbox.className = 'multi-select-checkbox';
                checkbox.checked = selectedRoles.has(role);
                checkbox.onchange = () => toggleRole(role);
                
                const label = document.createElement('span');
                label.textContent = role;
                label.onclick = () => toggleRole(role);
                
                div.appendChild(checkbox);
                div.appendChild(label);
                roleOptions.appendChild(div);
            });
        }
        
        function toggleRole(role) {
            if (selectedRoles.has(role)) {
                selectedRoles.delete(role);
            } else {
                selectedRoles.add(role);
            }
            updateRoleFilterDisplay();
            updateRoleCheckboxes();
            filterData();
        }
        
        function selectAllRoles() {
            const visibleRoles = getVisibleRoles();
            visibleRoles.forEach(role => selectedRoles.add(role));
            updateRoleFilterDisplay();
            updateRoleCheckboxes();
            filterData();
        }
        
        function deselectAllRoles() {
            const visibleRoles = getVisibleRoles();
            visibleRoles.forEach(role => selectedRoles.delete(role));
            updateRoleFilterDisplay();
            updateRoleCheckboxes();
            filterData();
        }
        
        function selectCommonRoles() {
            // Define common instrument roles
            const commonRoles = ['Piano', 'Guitar', 'Bass', 'Drums', 'Vocals', 'Saxophone', 'Trumpet', 'Violin'];
            selectedRoles.clear();
            commonRoles.forEach(role => {
                if (window.allRoles.includes(role)) {
                    selectedRoles.add(role);
                }
            });
            updateRoleFilterDisplay();
            updateRoleCheckboxes();
            filterData();
        }
        
        function getVisibleRoles() {
            const visibleOptions = document.querySelectorAll('#roleOptions .multi-select-option:not(.hidden)');
            return Array.from(visibleOptions).map(option => option.dataset.role);
        }
        
        function updateRoleFilterDisplay() {
            const display = document.getElementById('roleFilterDisplay');
            const count = document.getElementById('roleCount');
            const totalRoles = window.allRoles.length;
            
            if (selectedRoles.size === 0) {
                display.textContent = 'No roles selected';
            } else if (selectedRoles.size === totalRoles) {
                display.textContent = 'All roles selected';
            } else if (selectedRoles.size === 1) {
                display.textContent = Array.from(selectedRoles)[0];
            } else {
                display.textContent = `${selectedRoles.size} roles selected`;
            }
            
            count.textContent = `${selectedRoles.size} of ${totalRoles} roles selected`;
        }
        
        function updateRoleCheckboxes() {
            const options = document.querySelectorAll('#roleOptions .multi-select-option');
            options.forEach(option => {
                const role = option.dataset.role;
                const checkbox = option.querySelector('.multi-select-checkbox');
                checkbox.checked = selectedRoles.has(role);
                
                if (selectedRoles.has(role)) {
                        option.classList.add('selected');
                    } else {
                        option.classList.remove('selected');
                    }
            });
        }
        
        function searchRoles() {
            const searchTerm = document.getElementById('roleSearchInput').value.toLowerCase();
            const options = document.querySelectorAll('#roleOptions .multi-select-option');
            
            options.forEach(option => {
                const role = option.dataset.role.toLowerCase();
                if (role.includes(searchTerm)) {
                    option.classList.remove('hidden');
                } else {
                    option.classList.add('hidden');
                }
            });
        }
        
        function toggleRoleDropdown() {
            const dropdown = document.getElementById('roleDropdown');
            const arrow = document.getElementById('roleArrow');
            const isOpen = dropdown.classList.contains('show');
            
            if (isOpen) {
                dropdown.classList.remove('show');
                arrow.classList.remove('open');
                // Clear search when closing
                document.getElementById('roleSearchInput').value = '';
                searchRoles();
            } else {
                dropdown.classList.add('show');
                arrow.classList.add('open');
                // Focus search input when opening
                setTimeout(() => {
                    document.getElementById('roleSearchInput').focus();
                }, 100);
            }
        }
        
        // Close dropdown when clicking outside
        document.addEventListener('click', function(event) {
            if (!event.target.closest('.multi-select')) {
                const dropdown = document.getElementById('roleDropdown');
                const arrow = document.getElementById('roleArrow');
                dropdown.classList.remove('show');
                arrow.classList.remove('open');
                // Clear search when closing
                document.getElementById('roleSearchInput').value = '';
                searchRoles();
                
                // Also close any open custom filter dropdowns
                customFilters.forEach(filter => {
                    const customDropdown = document.getElementById(`customValueDropdown_${filter.id}`);
                    const customArrow = document.getElementById(`customValueArrow_${filter.id}`);
                    if (customDropdown) {
                        customDropdown.classList.remove('show');
                        customArrow.classList.remove('open');
                        const customSearchInput = document.getElementById(`customValueSearchInput_${filter.id}`);
                        if (customSearchInput) {
                            customSearchInput.value = '';
                            searchCustomValues(filter.id);
                        }
                    }
                });
            }
        });
        
        // Multiple Custom Filter Functions
        function addCustomFilter() {
            const filterId = nextCustomFilterId++;
            const filter = {
                id: filterId,
                column: '',
                selectedValues: new Set()
            };
            
            customFilters.push(filter);
            createCustomFilterUI(filter);
        }
        
        function createCustomFilterUI(filter) {
            const container = document.getElementById('customFiltersContainer');
            
            const filterItem = document.createElement('div');
            filterItem.className = 'custom-filter-item';
            filterItem.id = `customFilter_${filter.id}`;
            
            // Column selector
            const columnDiv = document.createElement('div');
            columnDiv.className = 'custom-filter-column';
            
            const columnLabel = document.createElement('div');
            columnLabel.className = 'custom-filter-label';
            columnLabel.textContent = 'Column:';
            
            const columnSelect = document.createElement('select');
            columnSelect.id = `customColumnSelect_${filter.id}`;
            columnSelect.onchange = () => onCustomColumnChange(filter.id);
            
            const defaultOption = document.createElement('option');
            defaultOption.value = '';
            defaultOption.textContent = 'Select Column...';
            columnSelect.appendChild(defaultOption);
            
            Object.keys(customFilterData).forEach(column => {
                const option = document.createElement('option');
                option.value = column;
                option.textContent = column;
                columnSelect.appendChild(option);
            });
            
            columnDiv.appendChild(columnLabel);
            columnDiv.appendChild(columnSelect);
            
            // Values selector
            const valuesDiv = document.createElement('div');
            valuesDiv.className = 'custom-filter-values';
            valuesDiv.id = `customValuesDiv_${filter.id}`;
            valuesDiv.style.display = 'none';
            
            const valuesLabel = document.createElement('div');
            valuesLabel.className = 'custom-filter-label';
            valuesLabel.textContent = 'Values:';
            
            const multiSelect = document.createElement('div');
            multiSelect.className = 'multi-select';
            
            const multiSelectInput = document.createElement('div');
            multiSelectInput.className = 'multi-select-input';
            multiSelectInput.onclick = () => toggleCustomValueDropdown(filter.id);
            
            const displaySpan = document.createElement('span');
            displaySpan.id = `customValueFilterDisplay_${filter.id}`;
            displaySpan.textContent = 'All values selected';
            
            const arrowSpan = document.createElement('span');
            arrowSpan.className = 'multi-select-arrow';
            arrowSpan.id = `customValueArrow_${filter.id}`;
            arrowSpan.textContent = '▼';
            
            multiSelectInput.appendChild(displaySpan);
            multiSelectInput.appendChild(arrowSpan);
            
            const dropdown = document.createElement('div');
            dropdown.className = 'multi-select-dropdown';
            dropdown.id = `customValueDropdown_${filter.id}`;
            
            // Search section
            const searchDiv = document.createElement('div');
            searchDiv.className = 'multi-select-search';
            
            const searchInput = document.createElement('input');
            searchInput.type = 'text';
            searchInput.id = `customValueSearchInput_${filter.id}`;
            searchInput.placeholder = 'Search values...';
            searchInput.oninput = () => searchCustomValues(filter.id);
            searchInput.onclick = (e) => e.stopPropagation();
            
            searchDiv.appendChild(searchInput);
            
            // Controls section
            const controlsDiv = document.createElement('div');
            controlsDiv.className = 'multi-select-controls';
            
            const selectAllBtn = document.createElement('button');
            selectAllBtn.className = 'multi-select-control-btn';
            selectAllBtn.textContent = 'Select All';
            selectAllBtn.onclick = () => selectAllCustomValues(filter.id);
            
            const deselectAllBtn = document.createElement('button');
            deselectAllBtn.className = 'multi-select-control-btn';
            deselectAllBtn.textContent = 'Deselect All';
            deselectAllBtn.onclick = () => deselectAllCustomValues(filter.id);
            
            controlsDiv.appendChild(selectAllBtn);
            controlsDiv.appendChild(deselectAllBtn);
            
            // Options section
            const optionsDiv = document.createElement('div');
            optionsDiv.className = 'multi-select-options';
            optionsDiv.id = `customValueOptions_${filter.id}`;
            
            // Count section
            const countDiv = document.createElement('div');
            countDiv.className = 'multi-select-count';
            countDiv.id = `customValueCount_${filter.id}`;
            countDiv.textContent = '0 of 0 values selected';
            
            dropdown.appendChild(searchDiv);
            dropdown.appendChild(controlsDiv);
            dropdown.appendChild(optionsDiv);
            dropdown.appendChild(countDiv);
            
            multiSelect.appendChild(multiSelectInput);
            multiSelect.appendChild(dropdown);
            
            valuesDiv.appendChild(valuesLabel);
            valuesDiv.appendChild(multiSelect);
            
            // Remove button
            const removeBtn = document.createElement('button');
            removeBtn.className = 'custom-filter-remove';
            removeBtn.textContent = '✕';
            removeBtn.onclick = () => removeCustomFilter(filter.id);
            
            filterItem.appendChild(columnDiv);
            filterItem.appendChild(valuesDiv);
            filterItem.appendChild(removeBtn);
            
            container.appendChild(filterItem);
        }
        
        function onCustomColumnChange(filterId) {
            const filter = customFilters.find(f => f.id === filterId);
            if (!filter) return;
            
            const selectedColumn = document.getElementById(`customColumnSelect_${filterId}`).value;
            const valuesDiv = document.getElementById(`customValuesDiv_${filterId}`);
            
            if (selectedColumn) {
                filter.column = selectedColumn;
                valuesDiv.style.display = 'block';
                // Initialize all values as selected BEFORE populating options
                filter.selectedValues = new Set(customFilterData[selectedColumn]);
                populateCustomValueOptions(filterId, customFilterData[selectedColumn]);
                updateCustomValueFilterDisplay(filterId);
                updateCustomValueCheckboxes(filterId);
            } else {
                filter.column = '';
                valuesDiv.style.display = 'none';
                filter.selectedValues.clear();
            }
            filterData();
        }
        
        function populateCustomValueOptions(filterId, values) {
            const customValueOptions = document.getElementById(`customValueOptions_${filterId}`);
            const filter = customFilters.find(f => f.id === filterId);
            if (!filter) return;
            
            customValueOptions.innerHTML = '';
            
            values.forEach(value => {
                const div = document.createElement('div');
                div.className = 'multi-select-option';
                div.dataset.value = value;
                
                const checkbox = document.createElement('input');
                checkbox.type = 'checkbox';
                checkbox.className = 'multi-select-checkbox';
                checkbox.checked = filter.selectedValues.has(value);
                checkbox.onchange = () => toggleCustomValue(filterId, value);
                
                const label = document.createElement('span');
                label.textContent = value;
                label.onclick = () => toggleCustomValue(filterId, value);
                
                div.appendChild(checkbox);
                div.appendChild(label);
                customValueOptions.appendChild(div);
            });
        }
        
        function toggleCustomValue(filterId, value) {
            const filter = customFilters.find(f => f.id === filterId);
            if (!filter) return;
            
            if (filter.selectedValues.has(value)) {
                filter.selectedValues.delete(value);
            } else {
                filter.selectedValues.add(value);
            }
            updateCustomValueFilterDisplay(filterId);
            updateCustomValueCheckboxes(filterId);
            filterData();
        }
        
        function selectAllCustomValues(filterId) {
            const filter = customFilters.find(f => f.id === filterId);
            if (!filter) return;
            
            const visibleValues = getVisibleCustomValues(filterId);
            visibleValues.forEach(value => filter.selectedValues.add(value));
            updateCustomValueFilterDisplay(filterId);
            updateCustomValueCheckboxes(filterId);
            filterData();
        }
        
        function deselectAllCustomValues(filterId) {
            const filter = customFilters.find(f => f.id === filterId);
            if (!filter) return;
            
            const visibleValues = getVisibleCustomValues(filterId);
            visibleValues.forEach(value => filter.selectedValues.delete(value));
            updateCustomValueFilterDisplay(filterId);
            updateCustomValueCheckboxes(filterId);
            filterData();
        }
        
        function getVisibleCustomValues(filterId) {
            const visibleOptions = document.querySelectorAll(`#customValueOptions_${filterId} .multi-select-option:not(.hidden)`);
            return Array.from(visibleOptions).map(option => option.dataset.value);
        }
        
        function updateCustomValueFilterDisplay(filterId) {
            const filter = customFilters.find(f => f.id === filterId);
            if (!filter) return;
            
            const display = document.getElementById(`customValueFilterDisplay_${filterId}`);
            const count = document.getElementById(`customValueCount_${filterId}`);
            const totalValues = filter.column ? customFilterData[filter.column].length : 0;
            
            if (filter.selectedValues.size === 0) {
                display.textContent = 'No values selected';
            } else if (filter.selectedValues.size === totalValues) {
                display.textContent = 'All values selected';
            } else if (filter.selectedValues.size === 1) {
                display.textContent = Array.from(filter.selectedValues)[0];
            } else {
                display.textContent = `${filter.selectedValues.size} values selected`;
            }
            
            count.textContent = `${filter.selectedValues.size} of ${totalValues} values selected`;
        }
        
        function updateCustomValueCheckboxes(filterId) {
            const filter = customFilters.find(f => f.id === filterId);
            if (!filter) return;
            
            const options = document.querySelectorAll(`#customValueOptions_${filterId} .multi-select-option`);
            options.forEach(option => {
                const value = option.dataset.value;
                const checkbox = option.querySelector('.multi-select-checkbox');
                checkbox.checked = filter.selectedValues.has(value);
                
                if (filter.selectedValues.has(value)) {
                    option.classList.add('selected');
                } else {
                    option.classList.remove('selected');
                }
            });
        }
        
        function searchCustomValues(filterId) {
            const searchTerm = document.getElementById(`customValueSearchInput_${filterId}`).value.toLowerCase();
            const options = document.querySelectorAll(`#customValueOptions_${filterId} .multi-select-option`);
            
            options.forEach(option => {
                const value = option.dataset.value.toLowerCase();
                if (value.includes(searchTerm)) {
                    option.classList.remove('hidden');
                } else {
                    option.classList.add('hidden');
                }
            });
        }
        
        function toggleCustomValueDropdown(filterId) {
            const dropdown = document.getElementById(`customValueDropdown_${filterId}`);
            const arrow = document.getElementById(`customValueArrow_${filterId}`);
            const isOpen = dropdown.classList.contains('show');
            
            if (isOpen) {
                dropdown.classList.remove('show');
                arrow.classList.remove('open');
                // Clear search when closing
                document.getElementById(`customValueSearchInput_${filterId}`).value = '';
                searchCustomValues(filterId);
            } else {
                dropdown.classList.add('show');
                arrow.classList.add('open');
                // Focus search input when opening
                setTimeout(() => {
                    document.getElementById(`customValueSearchInput_${filterId}`).focus();
                }, 100);
            }
        }
        
        function removeCustomFilter(filterId) {
            // Remove from array
            customFilters = customFilters.filter(f => f.id !== filterId);
            
            // Remove from DOM
            const filterElement = document.getElementById(`customFilter_${filterId}`);
            if (filterElement) {
                filterElement.remove();
            }
            
            // Reapply filters
            filterData();
        }
        
        function filterData() {
            // Start with all nodes (no node-level filtering needed)
            let filteredNodes = fullNetworkData.nodes;
            
            // Get node names for link filtering
            const nodeNames = new Set(filteredNodes.map(node => node.name));
            
            // Filter links
            let filteredLinks = fullNetworkData.links.filter(link => {
                // Only include links between filtered nodes
                if (!nodeNames.has(link.source) || !nodeNames.has(link.target)) {
                    return false;
                }
                
                // Role filter
                if (selectedRoles.size > 0 && link.roles) {
                    const hasSelectedRole = link.roles.some(role => selectedRoles.has(role));
                    if (!hasSelectedRole) {
                        return false;
                    }
                }
                
                // Custom filters - only apply if there are actually configured filters
                if (customFilters.length > 0) {
                    const activeCustomFilters = customFilters.filter(filter => 
                        filter.column && 
                        filter.selectedValues.size > 0 && 
                        filter.selectedValues.size < (customFilterData[filter.column] ? customFilterData[filter.column].length : 0)
                    );
                    
                    for (const filter of activeCustomFilters) {
                        if (link.custom_data) {
                            const linkValues = link.custom_data[filter.column];
                            if (linkValues) {
                                let hasSelectedValue = false;
                                if (Array.isArray(linkValues)) {
                                    // Check if any value in the array matches selected values
                                    hasSelectedValue = linkValues.some(value => {
                                        if (typeof value === 'string' && value.includes(',')) {
                                            // Handle comma-separated values
                                            const parts = value.split(',').map(p => p.trim());
                                            return parts.some(part => filter.selectedValues.has(part));
                                        }
                                        return filter.selectedValues.has(String(value));
                                    });
                                } else {
                                    // Single value
                                    if (typeof linkValues === 'string' && linkValues.includes(',')) {
                                        // Handle comma-separated values
                                        const parts = linkValues.split(',').map(p => p.trim());
                                        hasSelectedValue = parts.some(part => filter.selectedValues.has(part));
                                    } else {
                                        hasSelectedValue = filter.selectedValues.has(String(linkValues));
                                    }
                                }
                                if (!hasSelectedValue) {
                                    return false; // This link doesn't match this custom filter
                                }
                            }
                        }
                    }
                }
                
                return true;
            });
            
            // After filtering links, remove nodes that have no connections
            const connectedNodeNames = new Set();
            filteredLinks.forEach(link => {
                connectedNodeNames.add(link.source);
                connectedNodeNames.add(link.target);
            });
            
            // Only keep nodes that have at least one connection
            const finalFilteredNodes = filteredNodes.filter(node => connectedNodeNames.has(node.name));
            
            // Update current data
            currentData = {
                nodes: finalFilteredNodes,
                links: filteredLinks,
                categories: fullNetworkData.categories
            };
            
            updateChart();
            updateStats();
            
            // Update all tabs with filtered data
            if (window.topMusiciansInitialized) {
                updateTopMusiciansTab();
            }
            if (window.sessionMusiciansInitialized) {
                updateSessionMusiciansTab();
            }
        }
        
        function updateStats() {
            const musicianNodes = currentData.nodes.filter(node => node.category === 'musician');
            const artistNodes = currentData.nodes.filter(node => node.category === 'artist');
            
            document.getElementById('musicianCount').textContent = musicianNodes.length;
            document.getElementById('artistCount').textContent = artistNodes.length;
            document.getElementById('connectionCount').textContent = currentData.links.length;
            
            // Show active filters
            const activeFilters = [];
            
            if (selectedRoles.size < [...new Set(fullNetworkData.links.flatMap(link => link.roles || []))].length) {
                activeFilters.push(`Roles: ${selectedRoles.size} selected`);
            }
            // Add active custom filters (only those that are actually filtering)
            customFilters.forEach(filter => {
                if (filter.column && filter.selectedValues.size > 0) {
                    const totalCustomValues = customFilterData[filter.column] ? customFilterData[filter.column].length : 0;
                    if (filter.selectedValues.size < totalCustomValues) {
                        activeFilters.push(`${filter.column}: ${filter.selectedValues.size} selected`);
                    }
                }
            });
            
            document.getElementById('activeFilters').textContent = activeFilters.length > 0 ? activeFilters.join(', ') : 'None';
        }
        
        function resetFilters() {
            // Reset role filter
            selectedRoles = new Set(window.allRoles);
            updateRoleFilterDisplay();
            updateRoleCheckboxes();
            
            // Clear role search
            document.getElementById('roleSearchInput').value = '';
            searchRoles();
            
            // Reset custom filters
            customFilters.forEach(filter => {
                const filterElement = document.getElementById(`customFilter_${filter.id}`);
                if (filterElement) {
                    filterElement.remove();
                }
            });
            customFilters = [];
            nextCustomFilterId = 1;
            
            currentData = JSON.parse(JSON.stringify(fullNetworkData));
            updateChart();
            updateStats();
            
            // Update all tabs with reset data
            if (window.topMusiciansInitialized) {
                updateTopMusiciansTab();
            }
            if (window.sessionMusiciansInitialized) {
                updateSessionMusiciansTab();
            }
        }
        

        
        function showNodeDetails(nodeData) {
            const infoPanel = document.getElementById('infoPanel');
            const nodeTitle = document.getElementById('nodeTitle');
            const nodeInfo = document.getElementById('nodeInfo');
            
            nodeTitle.textContent = nodeData.name;
            
            let content = '<div class="info-section">';
            content += '<h4>Basic Information</h4>';
            content += '<div class="info-content">';
            content += `<p><strong>Type:</strong> ${nodeData.category === 'musician' ? 'Musician' : 'Artist'}</p>`;
            content += `<p><strong>Connections:</strong> ${nodeData.value}</p>`;
            content += '</div></div>';
            
            if (nodeData.genres && nodeData.genres.length > 0) {
                content += '<div class="info-section">';
                content += '<h4>Genres</h4>';
                content += '<div class="info-content">';
                nodeData.genres.forEach(genre => {
                    content += `<span class="tag">${genre}</span>`;
                });
                content += '</div></div>';
            }
            
            if (nodeData.styles && nodeData.styles.length > 0) {
                content += '<div class="info-section">';
                content += '<h4>Styles</h4>';
                content += '<div class="info-content">';
                nodeData.styles.forEach(style => {
                    content += `<span class="tag">${style}</span>`;
                });
                content += '</div></div>';
            }
            
            if (nodeData.roles && nodeData.roles.length > 0) {
                content += '<div class="info-section">';
                content += '<h4>Roles</h4>';
                content += '<div class="info-content">';
                nodeData.roles.forEach(role => {
                    content += `<span class="tag">${role}</span>`;
                });
                content += '</div></div>';
            }
            
            if (nodeData.albums && nodeData.albums.length > 0) {
                content += '<div class="info-section">';
                content += '<h4>Albums</h4>';
                content += '<div class="info-content">';
                content += '<ul>';
                nodeData.albums.slice(0, 10).forEach(album => {
                    content += `<li>${album}</li>`;
                });
                if (nodeData.albums.length > 10) {
                    content += `<li><em>... and ${nodeData.albums.length - 10} more</em></li>`;
                }
                content += '</ul></div></div>';
            }
            
            if (nodeData.collaborations && nodeData.collaborations.length > 0) {
                content += '<div class="info-section">';
                content += '<h4>Collaborations</h4>';
                content += '<div class="info-content">';
                content += '<ul>';
                nodeData.collaborations.slice(0, 10).forEach(collab => {
                    content += `<li>${collab}</li>`;
                });
                if (nodeData.collaborations.length > 10) {
                    content += `<li><em>... and ${nodeData.collaborations.length - 10} more</em></li>`;
                }
                content += '</ul></div></div>';
            }
            
            nodeInfo.innerHTML = content;
            infoPanel.classList.add('active');
        }
        
        function hideInfoPanel() {
            document.getElementById('infoPanel').classList.remove('active');
        }
        
        function updateChart() {
            const option = {
                title: {
                    text: 'Musician-Artist Network',
                    subtext: 'Click nodes for details | Use filters above',
                    top: '2%',
                    left: 'center',
                    textStyle: {
                        fontSize: 18,
                        fontWeight: 'bold',
                        color: '#ffffff'
                    },
                    subtextStyle: {
                        color: '#b0b0b0'
                    }
                },
                tooltip: {
                    trigger: 'item',
                    formatter: function(params) {
                        if (params.dataType === 'node') {
                            const node = params.data;
                            let tooltip = `<strong>${node.name}</strong><br/>`;
                            if (node.category === 'musician') {
                                tooltip += `Works with ${node.value} artists<br/>`;
                            } else {
                                tooltip += `${node.value} musicians<br/>`;
                            }
                            if (node.genres && node.genres.length > 0) {
                                tooltip += `Genres: ${node.genres.slice(0, 3).join(', ')}${node.genres.length > 3 ? '...' : ''}<br/>`;
                            }
                            if (node.styles && node.styles.length > 0) {
                                tooltip += `Styles: ${node.styles.slice(0, 3).join(', ')}${node.styles.length > 3 ? '...' : ''}`;
                            }
                            return tooltip;
                        } else if (params.dataType === 'edge') {
                            const link = params.data;
                            let tooltip = `${link.source} → ${link.target}<br/>`;
                            if (link.roles && link.roles.length > 0) {
                                tooltip += `Roles: ${link.roles.slice(0, 3).join(', ')}${link.roles.length > 3 ? '...' : ''}<br/>`;
                            }
                            if (link.albums && link.albums.length > 0) {
                                tooltip += `Albums: ${link.albums.slice(0, 2).join(', ')}${link.albums.length > 2 ? '...' : ''}`;
                            }
                            return tooltip;
                        }
                    }
                },
                legend: {
                    x: "center",
                    top: '10%',
                    data: currentData.categories.map(function(a) {
                        return a.name;
                    }),
                    textStyle: {
                        color: '#e0e0e0'
                    }
                },
                animationDuration: 1000,
                animationEasingUpdate: 'quinticInOut',
                series: [{
                    name: 'Musician Network',
                    type: 'graph',
                    layout: 'force',
                    data: currentData.nodes,
                    links: currentData.links,
                    categories: currentData.categories,
                    roam: true,
                    focusNodeAdjacency: true,
                    itemStyle: {
                        borderWidth: 0,
                        shadowBlur: 10,
                        shadowColor: 'rgba(0, 0, 0, 0.5)'
                    },
                    label: {
                        show: true,
                        position: 'right',
                        formatter: '{b}',
                        fontSize: 10,
                        color: '#ffffff'
                    },
                    lineStyle: {
                        color: 'source',
                        curveness: 0.1,
                        opacity: 0.6
                    },
                    emphasis: {
                        focus: 'adjacency',
                        lineStyle: {
                            width: 3,
                            opacity: 0.9
                        }
                    },
                    force: {
                        repulsion: 200,
                        edgeLength: [50, 100],
                        gravity: 0.1
                    }
                }]
            };
            
            myChart.setOption(option, true);
        }
        
        // Calculate filtered musician statistics from current network data
        function calculateFilteredMusicianStats() {
            // Get the list of all visible nodes (both musicians and artists)
            // because musicians who are also main artists appear as artist nodes
            const visibleNodeNames = new Set(
                currentData.nodes.map(node => node.name)
            );
            
            // Filter the original musician stats data to only include visible musicians
            return musicianStatsData.filter(musician => 
                visibleNodeNames.has(musician.musician)
            );
        }
        
        // Top Musicians Tab
        function initTopMusiciansTab() {
            if (window.topMusiciansInitialized) return;
            window.topMusiciansInitialized = true;
            
            // Store chart instances globally so we can update them
            window.topMusiciansChart = null;
            window.sessionScatterChart = null;
            
            updateTopMusiciansTab();
        }
        
        function updateTopMusiciansTab() {
            console.log(`updateTopMusiciansTab called. musicianStatsData has ${musicianStatsData.length} musicians`);
            const filteredStats = calculateFilteredMusicianStats();
            const topMusicians = filteredStats.sort((a, b) => b.total_records - a.total_records).slice(0, 15);
            
            // Update or create bar chart
            const barChartContainer = document.getElementById('topMusiciansChart');
            if (window.topMusiciansChart) {
                window.topMusiciansChart.dispose();
            }
            
            window.topMusiciansChart = echarts.init(barChartContainer);
            
            const barOption = {
                backgroundColor: '#1e1e1e',
                tooltip: {
                    trigger: 'axis',
                    axisPointer: {
                        type: 'shadow'
                    },
                    formatter: function(params) {
                        const data = params[0];
                        const musician = topMusicians[data.dataIndex];
                        return `
                            <div style="font-weight: bold; margin-bottom: 8px;">${data.name}</div>
                            <div>Total Records: <span style="color: #3498db; font-weight: bold;">${data.value}</span></div>
                            <div>Main Artist: <span style="color: #27ae60; font-weight: bold;">${musician.as_main_artist}</span></div>
                            <div>Session Work: <span style="color: #e74c3c; font-weight: bold;">${musician.as_session_musician}</span></div>
                            <div>Session Ratio: <span style="color: #f39c12; font-weight: bold;">${(musician.session_ratio * 100).toFixed(1)}%</span></div>
                            <div style="margin-top: 8px; font-size: 12px; color: #666;">Click for detailed view</div>
                        `;
                    },
                    backgroundColor: 'rgba(45, 45, 45, 0.95)',
                    borderColor: '#555',
                    borderWidth: 1,
                    textStyle: {
                        color: '#e0e0e0'
                    }
                },
                grid: {
                    left: '15%',
                    right: '10%',
                    bottom: '10%',
                    top: '5%'
                },
                xAxis: {
                    type: 'value',
                    name: 'Total Records',
                    nameLocation: 'middle',
                    nameGap: 30,
                    nameTextStyle: {
                        fontSize: 12,
                        fontWeight: 'bold',
                        color: '#e0e0e0'
                    },
                    splitLine: {
                        lineStyle: {
                            color: '#404040'
                        }
                    },
                    axisLabel: {
                        color: '#e0e0e0'
                    },
                    axisLine: {
                        lineStyle: {
                            color: '#555'
                        }
                    }
                },
                yAxis: {
                    type: 'category',
                    data: topMusicians.map(m => m.musician),
                    axisLabel: {
                        fontSize: 11,
                        interval: 0,
                        color: '#e0e0e0',  // Add light color for dark mode
                        formatter: function(value) {
                            // Truncate long names
                            return value.length > 20 ? value.substring(0, 20) + '...' : value;
                        }
                    },
                    axisTick: {
                        alignWithLabel: true
                    },
                    axisLine: {
                        lineStyle: {
                            color: '#555'  // Add dark mode line color
                        }
                    }
                },
                series: [{
                    name: 'Total Records',
                    type: 'bar',
                    data: topMusicians.map((m, index) => {
                        // Create a gradient from blue to purple based on position
                        const ratio = index / Math.max(topMusicians.length - 1, 1);
                        const r = Math.floor(52 + ratio * 100);   // 52 to 152
                        const g = Math.floor(152 - ratio * 50);   // 152 to 102
                        const b = Math.floor(219 - ratio * 20);   // 219 to 199
                        const color = `rgba(${r}, ${g}, ${b}, 0.8)`;
                        
                        return {
                            value: m.total_records,
                            itemStyle: {
                                color: color
                            }
                        };
                    }),
                    barWidth: '60%',
                    emphasis: {
                        itemStyle: {
                            shadowBlur: 10,
                            shadowColor: 'rgba(0, 0, 0, 0.3)'
                        }
                    },
                    animationDelay: function(idx) {
                        return idx * 50; // Staggered animation
                    }
                }],
                animation: true,
                animationDuration: 1000,
                animationEasing: 'cubicOut'
            };
            
            window.topMusiciansChart.setOption(barOption);
            
            // Add click handler for detailed view
            window.topMusiciansChart.on('click', function(params) {
                if (params.componentType === 'series') {
                    const musician = topMusicians[params.dataIndex];
                    const musicianData = {
                        musician: musician.musician,
                        total: musician.total_records,
                        x: musician.as_main_artist,
                        y: musician.as_session_musician,
                        sessionRatio: musician.session_ratio
                    };
                    showMusicianScatterDetails(musicianData);
                }
            });
            
            // Update or create scatter plot
            const chartContainer = document.getElementById('sessionScatterChart');
            if (window.sessionScatterChart) {
                window.sessionScatterChart.dispose();
            }
            
            // Apply filters directly to ALL musician data (bypass network node limitations)
            let allFilteredStats = [...musicianStatsData];
            console.log(`Starting with ${allFilteredStats.length} total musicians from musicianStatsData`);
            
            // Apply role filtering
            if (selectedRoles.size < window.allRoles.length && selectedRoles.size > 0) {
                const musiciansWithSelectedRoles = new Set();
                fullNetworkData.links.forEach(link => {
                    if (link.roles && link.roles.some(role => selectedRoles.has(role))) {
                        musiciansWithSelectedRoles.add(link.source);
                        musiciansWithSelectedRoles.add(link.target);
                    }
                });
                allFilteredStats = allFilteredStats.filter(m => musiciansWithSelectedRoles.has(m.musician));
            }
            
            // Apply custom filters
            if (customFilters.length > 0) {
                const activeCustomFilters = customFilters.filter(filter => 
                    filter.column && 
                    filter.selectedValues.size > 0 && 
                    filter.selectedValues.size < (customFilterData[filter.column] ? customFilterData[filter.column].length : 0)
                );
                
                if (activeCustomFilters.length > 0) {
                    allFilteredStats = allFilteredStats.filter(musician => {
                        return activeCustomFilters.every(filter => {
                            // Check if musician appears in any record that matches the filter
                            if (!musician.records) return false;
                            
                            return musician.records.some(record => {
                                // Get all the data for this record from all columns
                                let recordMatches = false;
                                
                                // Search through the custom filter data to find this record
                                Object.keys(customFilterData).forEach(dataKey => {
                                    if (recordMatches) return; // Already found a match
                                    
                                    const columnData = customFilterData[dataKey];
                                    if (Array.isArray(columnData)) {
                                        columnData.forEach((rowData, index) => {
                                            if (recordMatches) return; // Already found a match
                                            
                                            // Check if this row contains our record (album)
                                            if (rowData && typeof rowData === 'object') {
                                                const albumField = rowData['Artist'] + ' - ' + rowData['Album'];
                                                if (albumField === record || rowData['Album'] === record.split(' - ')[1]) {
                                                    // This is our record, check if it matches the filter
                                                    const filterColumnData = rowData[filter.column];
                                                    if (filterColumnData) {
                                                        if (typeof filterColumnData === 'string' && filterColumnData.includes(',')) {
                                                            // Handle comma-separated values
                                                            const parts = filterColumnData.split(',').map(p => p.trim());
                                                            recordMatches = parts.some(part => filter.selectedValues.has(part));
                                                        } else {
                                                            recordMatches = filter.selectedValues.has(String(filterColumnData));
                                                        }
                                                    }
                                                }
                                            }
                                        });
                                    }
                                });
                                
                                return recordMatches;
                            });
                        });
                    });
                }
            }
            
            console.log(`Total musicians in scatter plot: ${allFilteredStats.length} (direct filtering applied)`);
            
            const pureSessionMusicians = allFilteredStats.filter(m => m.as_main_artist === 0 && m.as_session_musician > 0);
            const balancedMusicians = allFilteredStats.filter(m => m.as_main_artist > 0 && m.as_session_musician > 0);
            const pureMainArtists = allFilteredStats.filter(m => m.as_main_artist > 0 && m.as_session_musician === 0);
            
            console.log(`Categories breakdown: Pure Session: ${pureSessionMusicians.length}, Balanced: ${balancedMusicians.length}, Pure Main: ${pureMainArtists.length}`);
            
            // Debug: Check the X,Y distribution
            console.log('Sample Pure Session Musicians X,Y values:');
            pureSessionMusicians.slice(0, 5).forEach(m => {
                console.log(`  ${m.musician}: (${m.as_main_artist}, ${m.as_session_musician})`);
            });
            
            console.log('Sample Balanced Musicians X,Y values:');
            balancedMusicians.slice(0, 5).forEach(m => {
                console.log(`  ${m.musician}: (${m.as_main_artist}, ${m.as_session_musician})`);
            });
            
            // Helper function to get size based on total records
            function getSizeByTotal(total, maxTotal) {
                const minSize = 8;
                const maxSize = 40;
                const normalizedTotal = total / Math.max(maxTotal, 1);
                return minSize + (maxSize - minSize) * Math.sqrt(normalizedTotal);
            }
            
            // Helper function to get color intensity based on total records
            function getColorIntensity(total, maxTotal) {
                return Math.sqrt(total / Math.max(maxTotal, 1)); // Use square root for better distribution
            }
            
            const maxTotal = Math.max(...allFilteredStats.map(m => m.total_records));
            
            window.sessionScatterChart = echarts.init(chartContainer);
            
            const option = {
                backgroundColor: '#1e1e1e',
                        tooltip: {
                    trigger: 'item',
                    formatter: function(params) {
                        const data = params.data;
                        return `
                            <div style="font-weight: bold; margin-bottom: 8px;">${data[3]}</div>
                            <div>Category: <span style="color: #666; font-weight: bold;">${params.seriesName}</span></div>
                            <div>Total Records: <span style="color: #e74c3c; font-weight: bold;">${data[4]}</span></div>
                            <div>Main Artist: <span style="color: #27ae60; font-weight: bold;">${data[0]}</span></div>
                            <div>Session Work: <span style="color: #3498db; font-weight: bold;">${data[1]}</span></div>
                            <div>Session Ratio: <span style="color: #f39c12; font-weight: bold;">${(data[5] * 100).toFixed(1)}%</span></div>
                            <div style="margin-top: 8px; font-size: 12px; color: #666;">Click for detailed view</div>
                        `;
                    },
                    backgroundColor: 'rgba(45, 45, 45, 0.95)',
                    borderColor: '#555',
                    borderWidth: 1,
                    textStyle: {
                        color: '#e0e0e0'
                    }
                },
                legend: {
                    data: [
                        {
                            name: 'Pure Session Musicians',
                            itemStyle: {
                                color: 'rgba(231, 76, 60, 0.8)'  // Red to match the series
                            }
                        },
                        {
                            name: 'Balanced Artists', 
                            itemStyle: {
                                color: 'rgba(243, 156, 18, 0.8)'  // Orange to match the series
                            }
                        },
                        {
                            name: 'Pure Main Artists',
                            itemStyle: {
                                color: 'rgba(39, 174, 96, 0.8)'  // Green to match the series
                            }
                        }
                    ],
                    top: '5%',
                    textStyle: {
                        color: '#e0e0e0'
                    }
                },
                grid: {
                    left: '10%',
                    right: '10%',
                    bottom: '15%',
                    top: '8%'
                },
                xAxis: {
                    type: 'value',
                    name: 'Main Artist Records',
                    nameLocation: 'middle',
                    nameGap: 30,
                    nameTextStyle: {
                        fontSize: 12,
                        fontWeight: 'bold',
                        color: '#e0e0e0'
                    },
                    splitLine: {
                        lineStyle: {
                            color: '#404040'
                        }
                    },
                    axisLabel: {
                        color: '#e0e0e0'
                    },
                    axisLine: {
                        lineStyle: {
                            color: '#555'
                        }
                    }
                },
                yAxis: {
                    type: 'value',
                    name: 'Session Work Records',
                    nameLocation: 'middle',
                    nameGap: 50,
                    nameTextStyle: {
                        fontSize: 12,
                        fontWeight: 'bold',
                        color: '#e0e0e0'
                    },
                    splitLine: {
                        lineStyle: {
                            color: '#404040'
                        }
                    },
                    axisLabel: {
                        color: '#e0e0e0'
                    },
                    axisLine: {
                        lineStyle: {
                            color: '#555'
                        }
                    }
                },
                series: [
                    {
                        name: 'Pure Session Musicians',
                        type: 'scatter',
                        data: pureSessionMusicians.map((m, index) => [
                            Math.max(0, m.as_main_artist + (Math.random() - 0.5) * 0.3), // Add jitter but keep >= 0
                            Math.max(0, m.as_session_musician + (Math.random() - 0.5) * 0.3),
                            getSizeByTotal(m.total_records, maxTotal),
                            m.musician,
                            m.total_records,
                            m.session_ratio
                        ]),
                        symbolSize: function(data) {
                            return data[2]; // Size from our calculation
                        },
                        itemStyle: {
                            color: function(params) {
                                const intensity = getColorIntensity(params.data[4], maxTotal);
                                // Red gradient for session musicians
                                const baseR = 231, baseG = 76, baseB = 60;
                                const alpha = 0.6 + intensity * 0.4; // 0.6 to 1.0
                                return `rgba(${baseR}, ${baseG}, ${baseB}, ${alpha})`;
                            },
                            borderWidth: 1,
                            borderColor: '#8b0000'  // Dark red for Pure Session Musicians
                        },
                        emphasis: {
                            itemStyle: {
                                borderColor: '#8b0000',  // Dark red border
                                borderWidth: 1
                            }
                        }
                    },
                    {
                        name: 'Balanced Artists',
                        type: 'scatter',
                        data: balancedMusicians.map(m => [
                            Math.max(0, m.as_main_artist + (Math.random() - 0.5) * 0.3), // Add jitter but keep >= 0
                            Math.max(0, m.as_session_musician + (Math.random() - 0.5) * 0.3),
                            getSizeByTotal(m.total_records, maxTotal),
                            m.musician,
                            m.total_records,
                            m.session_ratio
                        ]),
                        symbolSize: function(data) {
                            return data[2]; // Size from our calculation
                        },
                        itemStyle: {
                            color: function(params) {
                                const intensity = getColorIntensity(params.data[4], maxTotal);
                                // Orange gradient for balanced artists
                                const baseR = 243, baseG = 156, baseB = 18;
                                const alpha = 0.6 + intensity * 0.4; // 0.6 to 1.0
                                return `rgba(${baseR}, ${baseG}, ${baseB}, ${alpha})`;
                            },
                            borderWidth: 1,
                            borderColor: '#b8860b'  // Dark orange for Balanced Artists  
                        },
                        emphasis: {
                            itemStyle: {
                                borderColor: '#b8860b',  // Dark orange border
                                borderWidth: 1
                            }
                        }
                    },
                    {
                        name: 'Pure Main Artists',
                        type: 'scatter',
                        data: pureMainArtists.map(m => [
                            Math.max(0, m.as_main_artist + (Math.random() - 0.5) * 0.3), // Add jitter but keep >= 0
                            Math.max(0, m.as_session_musician + (Math.random() - 0.5) * 0.3),
                            getSizeByTotal(m.total_records, maxTotal),
                            m.musician,
                            m.total_records,
                            m.session_ratio
                        ]),
                        symbolSize: function(data) {
                            return data[2]; // Size from our calculation
                        },
                        itemStyle: {
                            color: function(params) {
                                const intensity = getColorIntensity(params.data[4], maxTotal);
                                // Green gradient for main artists
                                const baseR = 39, baseG = 174, baseB = 96;
                                const alpha = 0.6 + intensity * 0.4; // 0.6 to 1.0
                                return `rgba(${baseR}, ${baseG}, ${baseB}, ${alpha})`;
                            },
                            borderWidth: 1,
                            borderColor: '#006400'  // Dark green for Pure Main Artists
                        },
                        emphasis: {
                            itemStyle: {
                                borderColor: '#006400',  // Dark green border  
                                borderWidth: 1
                            }
                        }
                    }
                ],
                animation: true,
                animationDuration: 1000,
                animationEasing: 'cubicOut'
            };
            
            window.sessionScatterChart.setOption(option);
            
            // Add click handler for detailed view
            window.sessionScatterChart.on('click', function(params) {
                if (params.componentType === 'series') {
                    const data = params.data;
                    const musicianData = {
                        musician: data[3],
                        total: data[4],
                        x: data[0],
                        y: data[1],
                        sessionRatio: data[5]
                    };
                    showMusicianScatterDetails(musicianData);
                }
            });
            

        }
        
        function showMusicianScatterDetails(musicianData) {
            // Create a modal-like overlay to show detailed information
            const overlay = document.createElement('div');
            overlay.style.cssText = `
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0, 0, 0, 0.7);
                display: flex;
                justify-content: center;
                align-items: center;
                z-index: 1000;
            `;
            
            const modal = document.createElement('div');
            modal.style.cssText = `
                background: #2d2d2d;
                color: #e0e0e0;
                padding: 30px;
                border-radius: 10px;
                max-width: 500px;
                width: 90%;
                max-height: 80vh;
                overflow-y: auto;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
            `;
            
            // Find the full musician data
            const fullMusicianData = musicianStatsData.find(m => m.musician === musicianData.musician);
            
            modal.innerHTML = `
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                    <h2 style="margin: 0; color: #ffffff;">${musicianData.musician}</h2>
                    <button id="closeModal" style="background: none; border: none; font-size: 24px; cursor: pointer; color: #b0b0b0;">&times;</button>
                </div>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-bottom: 20px;">
                    <div style="text-align: center; padding: 15px; background: #3a3a3a; border-radius: 5px;">
                        <div style="font-size: 24px; font-weight: bold; color: #ff6b6b;">${musicianData.total}</div>
                        <div style="color: #b0b0b0;">Total Records</div>
                    </div>
                    <div style="text-align: center; padding: 15px; background: #3a3a3a; border-radius: 5px;">
                        <div style="font-size: 24px; font-weight: bold; color: #ffa726;">${(musicianData.sessionRatio * 100).toFixed(1)}%</div>
                        <div style="color: #b0b0b0;">Session Work</div>
                    </div>
                    <div style="text-align: center; padding: 15px; background: #3a3a3a; border-radius: 5px;">
                        <div style="font-size: 24px; font-weight: bold; color: #66bb6a;">${musicianData.x}</div>
                        <div style="color: #b0b0b0;">Main Artist</div>
                    </div>
                    <div style="text-align: center; padding: 15px; background: #3a3a3a; border-radius: 5px;">
                        <div style="font-size: 24px; font-weight: bold; color: #42a5f5;">${musicianData.y}</div>
                        <div style="color: #b0b0b0;">Session Work</div>
                    </div>
                </div>
                ${fullMusicianData && fullMusicianData.records ? `
                    <div>
                        <h3 style="margin-bottom: 10px;">Albums (${fullMusicianData.records.length})</h3>
                        <div style="max-height: 200px; overflow-y: auto; background: #3a3a3a; padding: 10px; border-radius: 5px;">
                            ${fullMusicianData.records.slice(0, 20).map(record => `<div style="margin-bottom: 5px; color: #e0e0e0;">• ${record}</div>`).join('')}
                            ${fullMusicianData.records.length > 20 ? `<div style="margin-top: 10px; font-style: italic; color: #b0b0b0;">... and ${fullMusicianData.records.length - 20} more albums</div>` : ''}
                        </div>
                    </div>
                ` : ''}
            `;
            
            overlay.appendChild(modal);
            document.body.appendChild(overlay);
            
            // Close modal handlers
            document.getElementById('closeModal').onclick = () => document.body.removeChild(overlay);
            overlay.onclick = (e) => {
                if (e.target === overlay) document.body.removeChild(overlay);
            };
        }
        
        // Session Musicians Tab
        function initSessionMusiciansTab() {
            if (window.sessionMusiciansInitialized) return;
            window.sessionMusiciansInitialized = true;
            
            updateSessionMusiciansTab();
        }
        
        function updateSessionMusiciansTab() {
            const filteredStats = calculateFilteredMusicianStats();
            // Filter for session musicians (70%+ session work, 2+ records)
            const sessionMusicians = filteredStats.filter(m => 
                m.total_records >= 2 && m.session_ratio >= 0.7
            ).sort((a, b) => b.session_ratio - a.session_ratio);
            
            const listContainer = document.getElementById('sessionMusiciansList');
            listContainer.innerHTML = ''; // Clear existing content
            
            sessionMusicians.forEach(musician => {
                const item = document.createElement('div');
                item.className = 'musician-item';
                item.innerHTML = `
                    <div>
                        <div class="musician-name">${musician.musician}</div>
                        <div class="musician-stats">
                            Total Records: ${musician.total_records} | 
                            Session Work: ${musician.as_session_musician} | 
                            Session Ratio: ${(musician.session_ratio * 100).toFixed(1)}%
                        </div>
                    </div>
                `;
                
                item.onclick = () => showSessionMusicianDetails(musician);
                listContainer.appendChild(item);
            });
        }
        
        function showSessionMusicianDetails(musician) {
            const detailsContainer = document.getElementById('sessionMusicianDetails');
            const nameElement = document.getElementById('selectedSessionMusician');
            const infoElement = document.getElementById('sessionMusicianInfo');
            
            nameElement.textContent = `${musician.musician} - Session Musician Details`;
            
            let content = `
                <div class="debug-section">
                    <h4>Statistics</h4>
                    <ul class="debug-list">
                        <li>Total Records: ${musician.total_records}</li>
                        <li>As Main Artist: ${musician.as_main_artist}</li>
                        <li>As Session Musician: ${musician.as_session_musician}</li>
                        <li>Session Ratio: ${(musician.session_ratio * 100).toFixed(1)}%</li>
                    </ul>
                </div>
                <div class="debug-section">
                    <h4>Albums (${musician.records ? musician.records.length : 0})</h4>
                    <ul class="debug-list">
            `;
            
            if (musician.records) {
            musician.records.slice(0, 20).forEach(record => {
                content += `<li>${record}</li>`;
            });
            
            if (musician.records.length > 20) {
                content += `<li><em>... and ${musician.records.length - 20} more</em></li>`;
                }
            } else {
                content += `<li>No album data available</li>`;
            }
            
            content += '</ul></div>';
            
            infoElement.innerHTML = content;
            detailsContainer.style.display = 'block';
        }
        
        // Debug Tab
        function initDebugTab() {
            // Already initialized through HTML
        }
        
        function searchMusicians() {
            const searchTerm = document.getElementById('debugSearchInput').value.toLowerCase();
            const resultsContainer = document.getElementById('debugResults');
            
            if (searchTerm.length < 2) {
                resultsContainer.innerHTML = '';
                return;
            }
            
            // Use filtered data for search
            const filteredStats = calculateFilteredMusicianStats();
            const matchingMusicians = filteredStats.filter(m => 
                m.musician.toLowerCase().includes(searchTerm)
            ).slice(0, 10);
            
            if (matchingMusicians.length === 0) {
                resultsContainer.innerHTML = '<p>No musicians found matching your search in current filtered data.</p>';
                return;
            }
            
            let html = '<h4>Search Results (Filtered Data):</h4>';
            matchingMusicians.forEach(musician => {
                html += `
                    <div class="musician-item" onclick="showDebugDetails('${musician.musician}')">
                        <div>
                            <div class="musician-name">${musician.musician}</div>
                            <div class="musician-stats">
                                ${musician.total_records} records | 
                                ${musician.as_main_artist} as main artist | 
                                ${musician.as_session_musician} session work
                            </div>
                        </div>
                    </div>
                `;
            });
            
            resultsContainer.innerHTML = html;
        }
        
        function showDebugDetails(musicianName) {
            const originalMusician = musicianStatsData.find(m => m.musician === musicianName);
            const filteredStats = calculateFilteredMusicianStats();
            const filteredMusician = filteredStats.find(m => m.musician === musicianName);
            
            const detailsContainer = document.getElementById('debugDetails');
            const nameElement = document.getElementById('debugMusicianName');
            const infoElement = document.getElementById('debugMusicianInfo');
            
            nameElement.textContent = `Debug: ${musicianName}`;
            
            let content = `
                <div class="debug-section">
                    <h4>Original Statistics (All Data)</h4>
                    <ul class="debug-list">
                        <li>Total Records: ${originalMusician ? originalMusician.total_records : 'N/A'}</li>
                        <li>As Main Artist: ${originalMusician ? originalMusician.as_main_artist : 'N/A'}</li>
                        <li>As Session Musician: ${originalMusician ? originalMusician.as_session_musician : 'N/A'}</li>
                        <li>Session Ratio: ${originalMusician ? (originalMusician.session_ratio * 100).toFixed(1) + '%' : 'N/A'}</li>
                    </ul>
                </div>
                
                <div class="debug-section">
                    <h4>Filtered Statistics (Current View)</h4>
                    <ul class="debug-list">
                        <li>Total Records: ${filteredMusician ? filteredMusician.total_records : 'Not visible in current filter'}</li>
                        <li>As Main Artist: ${filteredMusician ? filteredMusician.as_main_artist : 'N/A'}</li>
                        <li>As Session Musician: ${filteredMusician ? filteredMusician.as_session_musician : 'N/A'}</li>
                        <li>Session Ratio: ${filteredMusician ? (filteredMusician.session_ratio * 100).toFixed(1) + '%' : 'N/A'}</li>
                    </ul>
                </div>
                
                <div class="debug-section">
                    <h4>Network Presence</h4>
                    <ul class="debug-list">
                        <li>Appears in full network: ${fullNetworkData.nodes.some(n => n.name === musicianName) ? 'Yes' : 'No'}</li>
                        <li>Full network connections: ${fullNetworkData.nodes.find(n => n.name === musicianName)?.value || 0}</li>
                        <li>Currently visible: ${currentData.nodes.some(n => n.name === musicianName) ? 'Yes' : 'No'}</li>
                        <li>Filtered connections: ${currentData.nodes.find(n => n.name === musicianName)?.value || 0}</li>
                    </ul>
                </div>
                
                <div class="debug-section">
                    <h4>Albums (${originalMusician && originalMusician.records ? originalMusician.records.length : 0})</h4>
                    <ul class="debug-list">
            `;
            
            if (originalMusician && originalMusician.records) {
                originalMusician.records.slice(0, 15).forEach(record => {
                content += `<li>${record}</li>`;
            });
            
                if (originalMusician.records.length > 15) {
                    content += `<li><em>... and ${originalMusician.records.length - 15} more</em></li>`;
                }
            } else {
                content += `<li>No album data available</li>`;
            }
            
            content += '</ul></div>';
            
            // Show collaborations if available
            const networkNode = fullNetworkData.nodes.find(n => n.name === musicianName);
            if (networkNode && networkNode.collaborations) {
                content += `
                    <div class="debug-section">
                        <h4>Network Collaborations (${networkNode.collaborations.length})</h4>
                        <ul class="debug-list">
                `;
                
                networkNode.collaborations.slice(0, 15).forEach(collab => {
                    content += `<li>${collab}</li>`;
                });
                
                if (networkNode.collaborations.length > 15) {
                    content += `<li><em>... and ${networkNode.collaborations.length - 15} more</em></li>`;
                }
                
                content += '</ul></div>';
            }
            
            infoElement.innerHTML = content;
            detailsContainer.style.display = 'block';
        }
'''


def generate_html_file(network_data, musician_stats_data, session_musicians_data, custom_filter_data, output_path):
    """
    Generate the complete HTML file with all data embedded.
    
    Args:
        network_data: Dictionary with network visualization data
        musician_stats_data: List of dictionaries with musician statistics
        session_musicians_data: List of dictionaries with session musician data
        output_path: Path where to save the HTML file
    """
    # Get the base template
    html_template = get_html_template()
    
    # Get JavaScript functions
    js_functions = get_javascript_functions()
    
    # Replace placeholders with actual data
    html_content = html_template.replace(
        '{network_data_placeholder}', 
        json.dumps(network_data, indent=2)
    ).replace(
        '{musician_stats_placeholder}', 
        json.dumps(musician_stats_data, indent=2)
    ).replace(
        '{session_musicians_placeholder}', 
        json.dumps(session_musicians_data, indent=2)
    ).replace(
        '{custom_filter_data_placeholder}', 
        json.dumps(custom_filter_data, indent=2)
    ).replace(
        '{javascript_functions}',
        js_functions
    )
    
    # Write to file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    return output_path 
