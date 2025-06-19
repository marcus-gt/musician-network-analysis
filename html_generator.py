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
            background-color: #f5f5f5;
        }
        .header {
            text-align: center;
            margin-bottom: 30px;
        }
        .title {
            color: #333;
            margin-bottom: 10px;
        }
        .subtitle {
            color: #666;
            font-size: 14px;
        }
        
        /* Tab Navigation */
        .tab-container {
            margin-bottom: 20px;
        }
        .tab-nav {
            display: flex;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        .tab-btn {
            flex: 1;
            padding: 15px 20px;
            border: none;
            background: white;
            cursor: pointer;
            transition: all 0.3s ease;
            font-size: 14px;
            font-weight: 500;
        }
        .tab-btn:hover {
            background: #f8f9fa;
        }
        .tab-btn.active {
            background: #007bff;
            color: white;
        }
        .tab-btn:not(:last-child) {
            border-right: 1px solid #e9ecef;
        }
        
        /* Tab Content */
        .tab-content {
            display: none;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            padding: 20px;
        }
        .tab-content.active {
            display: block;
        }
        
        /* Network Tab Styles */
        #container {
            width: 100%;
            height: 800px;
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
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
            color: #333;
        }
        
        select, input[type="range"] {
            padding: 8px 12px;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 14px;
        }
        
        .multi-select {
            position: relative;
            min-width: 250px;
        }
        
        .multi-select-input {
            width: 100%;
            padding: 8px 12px;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 14px;
            cursor: pointer;
            background: white;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        
        .multi-select-input:hover {
            border-color: #007bff;
        }
        
        .multi-select-arrow {
            margin-left: 8px;
            font-size: 12px;
            color: #666;
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
            background: white;
            border: 1px solid #ddd;
            border-radius: 4px;
            max-height: 400px;
            z-index: 1000;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            overflow: hidden;
        }
        
        .multi-select-dropdown.show {
            display: block;
        }
        
        .multi-select-search {
            padding: 12px;
            border-bottom: 1px solid #e9ecef;
            background: #f8f9fa;
        }
        
        .multi-select-search input {
            width: 100%;
            padding: 8px 12px;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 14px;
            outline: none;
        }
        
        .multi-select-search input:focus {
            border-color: #007bff;
            box-shadow: 0 0 0 2px rgba(0, 123, 255, 0.25);
        }
        
        .multi-select-controls {
            padding: 8px 12px;
            border-bottom: 1px solid #e9ecef;
            background: #f8f9fa;
            display: flex;
            gap: 10px;
        }
        
        .multi-select-control-btn {
            padding: 4px 8px;
            font-size: 12px;
            border: 1px solid #007bff;
            background: white;
            color: #007bff;
            border-radius: 3px;
            cursor: pointer;
            transition: all 0.2s;
        }
        
        .multi-select-control-btn:hover {
            background: #007bff;
            color: white;
        }
        
        .multi-select-options {
            max-height: 250px;
            overflow-y: auto;
        }
        
        .multi-select-option {
            padding: 10px 12px;
            cursor: pointer;
            border-bottom: 1px solid #f0f0f0;
            display: flex;
            align-items: center;
            transition: background-color 0.2s;
        }
        
        .multi-select-option:hover {
            background-color: #f8f9fa;
        }
        
        .multi-select-option.selected {
            background-color: #e3f2fd;
            color: #1976d2;
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
            background: #f8f9fa;
            border-top: 1px solid #e9ecef;
            font-size: 12px;
            color: #666;
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
        
        .stats-panel {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 6px;
            margin-bottom: 20px;
        }
        
        .stats-item {
            display: inline-block;
            margin-right: 20px;
            font-size: 14px;
            color: #666;
        }
        
        .stats-value {
            font-weight: bold;
            color: #333;
        }
        
        .info-panel {
            margin-top: 20px;
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
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
            color: #333;
            border-bottom: 2px solid #007bff;
            padding-bottom: 5px;
        }
        
        .info-content {
            line-height: 1.6;
        }
        
        .tag {
            display: inline-block;
            background: #e3f2fd;
            color: #1976d2;
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
            background: white;
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        
        .chart-container h3 {
            margin: 0 0 15px 0;
            color: #333;
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
            border-bottom: 1px solid #eee;
            cursor: pointer;
            transition: background-color 0.2s;
        }
        
        .musician-item:hover {
            background-color: #f8f9fa;
        }
        
        .musician-name {
            font-weight: 500;
            color: #333;
        }
        
        .musician-stats {
            font-size: 12px;
            color: #666;
        }
        
        .search-container {
            margin-bottom: 20px;
        }
        
        .search-input {
            width: 100%;
            padding: 12px;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 16px;
        }
        
        .debug-info {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 6px;
            margin: 10px 0;
        }
        
        .debug-section {
            margin-bottom: 15px;
        }
        
        .debug-section h4 {
            margin: 0 0 8px 0;
            color: #333;
        }
        
        .debug-list {
            list-style: none;
            padding: 0;
            margin: 0;
        }
        
        .debug-list li {
            padding: 4px 0;
            border-bottom: 1px solid #e9ecef;
        }
        
        .click-hint {
            text-align: center;
            color: #666;
            font-size: 14px;
            margin-bottom: 15px;
            padding: 10px;
            background: #fff3cd;
            border-radius: 4px;
            border: 1px solid #ffeaa7;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1 class="title">🎵 Musician Network Analysis</h1>
        <p class="subtitle">Explore connections, discover top musicians, and analyze your collection</p>
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
        <div class="controls">
            <div class="control-group">
                <label for="genreFilter">Genre Filter:</label>
                <select id="genreFilter">
                    <option value="">All Genres</option>
                </select>
            </div>
            
            <div class="control-group">
                <label for="styleFilter">Style Filter:</label>
                <select id="styleFilter">
                    <option value="">All Styles</option>
                </select>
            </div>
            
            <div class="control-group">
                <label for="connectionSlider">Min Connections: <span id="connectionValue">1</span></label>
                <input type="range" id="connectionSlider" min="1" max="31" value="1">
            </div>
            
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
                <label for="customColumnFilter">Custom Filter:</label>
                <select id="customColumnFilter" onchange="onCustomColumnChange()">
                    <option value="">Select Column...</option>
                </select>
            </div>
            
            <div class="control-group" id="customValueFilterGroup" style="display: none;">
                <label for="customValueFilter">Values:</label>
                <div class="multi-select">
                    <div class="multi-select-input" onclick="toggleCustomValueDropdown()">
                        <span id="customValueFilterDisplay">All values selected</span>
                        <span class="multi-select-arrow" id="customValueArrow">▼</span>
                    </div>
                    <div id="customValueDropdown" class="multi-select-dropdown">
                        <div class="multi-select-search">
                            <input type="text" id="customValueSearchInput" placeholder="Search values..." oninput="searchCustomValues()" onclick="event.stopPropagation()">
                        </div>
                        <div class="multi-select-controls">
                            <button class="multi-select-control-btn" onclick="selectAllCustomValues()">Select All</button>
                            <button class="multi-select-control-btn" onclick="deselectAllCustomValues()">Deselect All</button>
                        </div>
                        <div class="multi-select-options" id="customValueOptions">
                            <!-- Custom value options will be populated here -->
                        </div>
                        <div class="multi-select-count" id="customValueCount">
                            0 of 0 values selected
                        </div>
                    </div>
                </div>
            </div>
            
            <button onclick="resetFilters()" class="reset-button">Reset Filters</button>
        </div>
        
        <div class="stats-panel" id="statsPanel">
            <span class="stats-item">Musicians: <span class="stats-value" id="musicianCount">0</span></span>
            <span class="stats-item">Artists: <span class="stats-value" id="artistCount">0</span></span>
            <span class="stats-item">Connections: <span class="stats-value" id="connectionCount">0</span></span>
            <span class="stats-item">Active Filters: <span class="stats-value" id="activeFilters">None</span></span>
        </div>
        
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
                <canvas id="topMusiciansChart" width="400" height="300"></canvas>
            </div>
            
            <div class="chart-container">
                <h3>Main Artist vs Session Work</h3>
                <canvas id="sessionScatterChart" width="400" height="300"></canvas>
            </div>
        </div>
        
        <div class="chart-container">
            <h3>Top Musicians List</h3>
            <div id="topMusiciansList" class="musician-list"></div>
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
        let selectedCustomValues = new Set();
        let currentCustomColumn = '';
        
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
        document.getElementById('genreFilter').addEventListener('change', filterData);
        document.getElementById('styleFilter').addEventListener('change', filterData);
        
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
            const genreFilter = document.getElementById('genreFilter');
            const styleFilter = document.getElementById('styleFilter');
            const roleOptions = document.getElementById('roleOptions');
            const customColumnFilter = document.getElementById('customColumnFilter');
            
            // Get unique values from full data
            const genres = [...new Set(fullNetworkData.nodes.flatMap(node => node.genres || []))].sort();
            const styles = [...new Set(fullNetworkData.nodes.flatMap(node => node.styles || []))].sort();
            const roles = [...new Set(fullNetworkData.links.flatMap(link => link.roles || []))].sort();
            
            // Store all roles globally for search functionality
            window.allRoles = roles;
            
            // Populate genre filter
            genres.forEach(genre => {
                const option = document.createElement('option');
                option.value = genre;
                option.textContent = genre;
                genreFilter.appendChild(option);
            });
            
            // Populate style filter
            styles.forEach(style => {
                const option = document.createElement('option');
                option.value = style;
                option.textContent = style;
                styleFilter.appendChild(option);
            });
            
            // Populate custom column filter
            Object.keys(customFilterData).forEach(column => {
                const option = document.createElement('option');
                option.value = column;
                option.textContent = column;
                customColumnFilter.appendChild(option);
            });
            
            // Populate role filter with enhanced structure
            populateRoleOptions(roles);
            
            // Initialize all roles as selected
            selectedRoles = new Set(roles);
            updateRoleFilterDisplay();
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
                
                // Also close custom value dropdown
                const customDropdown = document.getElementById('customValueDropdown');
                const customArrow = document.getElementById('customValueArrow');
                if (customDropdown) {
                    customDropdown.classList.remove('show');
                    customArrow.classList.remove('open');
                    const customSearchInput = document.getElementById('customValueSearchInput');
                    if (customSearchInput) {
                        customSearchInput.value = '';
                        searchCustomValues();
                    }
                }
            }
        });
        
        // Custom filter functions
        function onCustomColumnChange() {
            const selectedColumn = document.getElementById('customColumnFilter').value;
            const customValueGroup = document.getElementById('customValueFilterGroup');
            
            if (selectedColumn) {
                currentCustomColumn = selectedColumn;
                customValueGroup.style.display = 'block';
                populateCustomValueOptions(customFilterData[selectedColumn]);
                // Initialize all values as selected
                selectedCustomValues = new Set(customFilterData[selectedColumn]);
                updateCustomValueFilterDisplay();
            } else {
                currentCustomColumn = '';
                customValueGroup.style.display = 'none';
                selectedCustomValues.clear();
            }
            filterData();
        }
        
        function populateCustomValueOptions(values) {
            const customValueOptions = document.getElementById('customValueOptions');
            customValueOptions.innerHTML = '';
            
            values.forEach(value => {
                const div = document.createElement('div');
                div.className = 'multi-select-option';
                div.dataset.value = value;
                
                const checkbox = document.createElement('input');
                checkbox.type = 'checkbox';
                checkbox.className = 'multi-select-checkbox';
                checkbox.checked = selectedCustomValues.has(value);
                checkbox.onchange = () => toggleCustomValue(value);
                
                const label = document.createElement('span');
                label.textContent = value;
                label.onclick = () => toggleCustomValue(value);
                
                div.appendChild(checkbox);
                div.appendChild(label);
                customValueOptions.appendChild(div);
            });
        }
        
        function toggleCustomValue(value) {
            if (selectedCustomValues.has(value)) {
                selectedCustomValues.delete(value);
            } else {
                selectedCustomValues.add(value);
            }
            updateCustomValueFilterDisplay();
            updateCustomValueCheckboxes();
            filterData();
        }
        
        function selectAllCustomValues() {
            const visibleValues = getVisibleCustomValues();
            visibleValues.forEach(value => selectedCustomValues.add(value));
            updateCustomValueFilterDisplay();
            updateCustomValueCheckboxes();
            filterData();
        }
        
        function deselectAllCustomValues() {
            const visibleValues = getVisibleCustomValues();
            visibleValues.forEach(value => selectedCustomValues.delete(value));
            updateCustomValueFilterDisplay();
            updateCustomValueCheckboxes();
            filterData();
        }
        
        function getVisibleCustomValues() {
            const visibleOptions = document.querySelectorAll('#customValueOptions .multi-select-option:not(.hidden)');
            return Array.from(visibleOptions).map(option => option.dataset.value);
        }
        
        function updateCustomValueFilterDisplay() {
            const display = document.getElementById('customValueFilterDisplay');
            const count = document.getElementById('customValueCount');
            const totalValues = currentCustomColumn ? customFilterData[currentCustomColumn].length : 0;
            
            if (selectedCustomValues.size === 0) {
                display.textContent = 'No values selected';
            } else if (selectedCustomValues.size === totalValues) {
                display.textContent = 'All values selected';
            } else if (selectedCustomValues.size === 1) {
                display.textContent = Array.from(selectedCustomValues)[0];
            } else {
                display.textContent = `${selectedCustomValues.size} values selected`;
            }
            
            count.textContent = `${selectedCustomValues.size} of ${totalValues} values selected`;
        }
        
        function updateCustomValueCheckboxes() {
            const options = document.querySelectorAll('#customValueOptions .multi-select-option');
            options.forEach(option => {
                const value = option.dataset.value;
                const checkbox = option.querySelector('.multi-select-checkbox');
                checkbox.checked = selectedCustomValues.has(value);
                
                if (selectedCustomValues.has(value)) {
                    option.classList.add('selected');
                } else {
                    option.classList.remove('selected');
                }
            });
        }
        
        function searchCustomValues() {
            const searchTerm = document.getElementById('customValueSearchInput').value.toLowerCase();
            const options = document.querySelectorAll('#customValueOptions .multi-select-option');
            
            options.forEach(option => {
                const value = option.dataset.value.toLowerCase();
                if (value.includes(searchTerm)) {
                    option.classList.remove('hidden');
                } else {
                    option.classList.add('hidden');
                }
            });
        }
        
        function toggleCustomValueDropdown() {
            const dropdown = document.getElementById('customValueDropdown');
            const arrow = document.getElementById('customValueArrow');
            const isOpen = dropdown.classList.contains('show');
            
            if (isOpen) {
                dropdown.classList.remove('show');
                arrow.classList.remove('open');
                // Clear search when closing
                document.getElementById('customValueSearchInput').value = '';
                searchCustomValues();
            } else {
                dropdown.classList.add('show');
                arrow.classList.add('open');
                // Focus search input when opening
                setTimeout(() => {
                    document.getElementById('customValueSearchInput').focus();
                }, 100);
            }
        }
        
        function filterData() {
            const genreFilter = document.getElementById('genreFilter').value;
            const styleFilter = document.getElementById('styleFilter').value;
            const connectionThreshold = parseInt(document.getElementById('connectionSlider').value);
            
            // Filter nodes
            let filteredNodes = fullNetworkData.nodes.filter(node => {
                // Genre filter
                if (genreFilter && (!node.genres || !node.genres.includes(genreFilter))) {
                    return false;
                }
                
                // Style filter
                if (styleFilter && (!node.styles || !node.styles.includes(styleFilter))) {
                    return false;
                }
                
                // Connection threshold
                if (node.value < connectionThreshold) {
                    return false;
                }
                
                return true;
            });
            
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
                
                // Custom filter
                if (currentCustomColumn && selectedCustomValues.size > 0 && link.custom_data) {
                    const linkValues = link.custom_data[currentCustomColumn];
                    if (linkValues) {
                        let hasSelectedValue = false;
                        if (Array.isArray(linkValues)) {
                            // Check if any value in the array matches selected values
                            hasSelectedValue = linkValues.some(value => {
                                if (typeof value === 'string' && value.includes(',')) {
                                    // Handle comma-separated values
                                    const parts = value.split(',').map(p => p.trim());
                                    return parts.some(part => selectedCustomValues.has(part));
                                }
                                return selectedCustomValues.has(String(value));
                            });
                        } else {
                            // Single value
                            if (typeof linkValues === 'string' && linkValues.includes(',')) {
                                // Handle comma-separated values
                                const parts = linkValues.split(',').map(p => p.trim());
                                hasSelectedValue = parts.some(part => selectedCustomValues.has(part));
                            } else {
                                hasSelectedValue = selectedCustomValues.has(String(linkValues));
                            }
                        }
                        if (!hasSelectedValue) {
                            return false;
                        }
                    }
                }
                
                return true;
            });
            
            // Update current data
            currentData = {
                nodes: filteredNodes,
                links: filteredLinks,
                categories: fullNetworkData.categories
            };
            
            updateChart();
            updateStats();
        }
        
        function updateStats() {
            const musicianNodes = currentData.nodes.filter(node => node.category === 'musician');
            const artistNodes = currentData.nodes.filter(node => node.category === 'artist');
            
            document.getElementById('musicianCount').textContent = musicianNodes.length;
            document.getElementById('artistCount').textContent = artistNodes.length;
            document.getElementById('connectionCount').textContent = currentData.links.length;
            
            // Show active filters
            const activeFilters = [];
            const genreFilter = document.getElementById('genreFilter').value;
            const styleFilter = document.getElementById('styleFilter').value;
            const connectionThreshold = parseInt(document.getElementById('connectionSlider').value);
            
            if (genreFilter) activeFilters.push(`Genre: ${genreFilter}`);
            if (styleFilter) activeFilters.push(`Style: ${styleFilter}`);
            if (connectionThreshold > 1) activeFilters.push(`Min Connections: ${connectionThreshold}`);
            if (selectedRoles.size < [...new Set(fullNetworkData.links.flatMap(link => link.roles || []))].length) {
                activeFilters.push(`Roles: ${selectedRoles.size} selected`);
            }
            if (currentCustomColumn && selectedCustomValues.size > 0) {
                const totalCustomValues = customFilterData[currentCustomColumn] ? customFilterData[currentCustomColumn].length : 0;
                if (selectedCustomValues.size < totalCustomValues) {
                    activeFilters.push(`${currentCustomColumn}: ${selectedCustomValues.size} selected`);
                }
            }
            
            document.getElementById('activeFilters').textContent = activeFilters.length > 0 ? activeFilters.join(', ') : 'None';
        }
        
        function resetFilters() {
            document.getElementById('genreFilter').value = '';
            document.getElementById('styleFilter').value = '';
            document.getElementById('connectionSlider').value = 1;
            document.getElementById('connectionValue').textContent = '1';
            
            // Reset role filter
            selectedRoles = new Set(window.allRoles);
            updateRoleFilterDisplay();
            updateRoleCheckboxes();
            
            // Clear role search
            document.getElementById('roleSearchInput').value = '';
            searchRoles();
            
            // Reset custom filter
            document.getElementById('customColumnFilter').value = '';
            document.getElementById('customValueFilterGroup').style.display = 'none';
            currentCustomColumn = '';
            selectedCustomValues.clear();
            
            currentData = JSON.parse(JSON.stringify(fullNetworkData));
            updateChart();
            updateStats();
        }
        
        // Connection slider update
        document.getElementById('connectionSlider').addEventListener('input', function() {
            document.getElementById('connectionValue').textContent = this.value;
            filterData();
        });
        
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
                        fontWeight: 'bold'
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
                    })
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
                        borderColor: '#fff',
                        borderWidth: 1,
                        shadowBlur: 10,
                        shadowColor: 'rgba(0, 0, 0, 0.3)'
                    },
                    label: {
                        show: true,
                        position: 'right',
                        formatter: '{b}',
                        fontSize: 10
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
        
        // Top Musicians Tab
        function initTopMusiciansTab() {
            if (window.topMusiciansInitialized) return;
            window.topMusiciansInitialized = true;
            
            // Create bar chart for top musicians
            const ctx1 = document.getElementById('topMusiciansChart').getContext('2d');
            const topMusicians = musicianStatsData.sort((a, b) => b.total_records - a.total_records).slice(0, 15);
            
            new Chart(ctx1, {
                type: 'bar',
                data: {
                    labels: topMusicians.map(m => m.musician),
                    datasets: [{
                        label: 'Total Records',
                        data: topMusicians.map(m => m.total_records),
                        backgroundColor: 'rgba(54, 162, 235, 0.8)',
                        borderColor: 'rgba(54, 162, 235, 1)',
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    indexAxis: 'y',
                    plugins: {
                        legend: {
                            display: false
                        }
                    },
                    scales: {
                        x: {
                            beginAtZero: true
                        }
                    }
                }
            });
            
            // Create scatter plot for main artist vs session work
            const ctx2 = document.getElementById('sessionScatterChart').getContext('2d');
            
            new Chart(ctx2, {
                type: 'scatter',
                data: {
                    datasets: [{
                        label: 'Musicians',
                        data: musicianStatsData.map(m => ({
                            x: m.as_main_artist,
                            y: m.as_session_musician,
                            musician: m.musician,
                            total: m.total_records
                        })),
                        backgroundColor: 'rgba(255, 99, 132, 0.6)',
                        borderColor: 'rgba(255, 99, 132, 1)',
                        pointRadius: function(context) {
                            return Math.max(3, context.raw.total * 0.5);
                        }
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        tooltip: {
                            callbacks: {
                                label: function(context) {
                                    return `${context.raw.musician}: ${context.raw.total} total records`;
                                }
                            }
                        }
                    },
                    scales: {
                        x: {
                            title: {
                                display: true,
                                text: 'Records as Main Artist'
                            }
                        },
                        y: {
                            title: {
                                display: true,
                                text: 'Records as Session Musician'
                            }
                        }
                    }
                }
            });
            
            // Populate musicians list
            const listContainer = document.getElementById('topMusiciansList');
            topMusicians.forEach(musician => {
                const item = document.createElement('div');
                item.className = 'musician-item';
                item.innerHTML = `
                    <div>
                        <div class="musician-name">${musician.musician}</div>
                        <div class="musician-stats">
                            Total: ${musician.total_records} | 
                            Main Artist: ${musician.as_main_artist} | 
                            Session: ${musician.as_session_musician}
                        </div>
                    </div>
                `;
                listContainer.appendChild(item);
            });
        }
        
        // Session Musicians Tab
        function initSessionMusiciansTab() {
            if (window.sessionMusiciansInitialized) return;
            window.sessionMusiciansInitialized = true;
            
            const listContainer = document.getElementById('sessionMusiciansList');
            
            sessionMusiciansData.forEach(musician => {
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
                    <h4>Albums (${musician.records.length})</h4>
                    <ul class="debug-list">
            `;
            
            musician.records.slice(0, 20).forEach(record => {
                content += `<li>${record}</li>`;
            });
            
            if (musician.records.length > 20) {
                content += `<li><em>... and ${musician.records.length - 20} more</em></li>`;
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
            
            const matchingMusicians = musicianStatsData.filter(m => 
                m.musician.toLowerCase().includes(searchTerm)
            ).slice(0, 10);
            
            if (matchingMusicians.length === 0) {
                resultsContainer.innerHTML = '<p>No musicians found matching your search.</p>';
                return;
            }
            
            let html = '<h4>Search Results:</h4>';
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
            const musician = musicianStatsData.find(m => m.musician === musicianName);
            if (!musician) return;
            
            const detailsContainer = document.getElementById('debugDetails');
            const nameElement = document.getElementById('debugMusicianName');
            const infoElement = document.getElementById('debugMusicianInfo');
            
            nameElement.textContent = `Debug: ${musicianName}`;
            
            let content = `
                <div class="debug-section">
                    <h4>Basic Statistics</h4>
                    <ul class="debug-list">
                        <li>Total Records: ${musician.total_records}</li>
                        <li>As Main Artist: ${musician.as_main_artist}</li>
                        <li>As Session Musician: ${musician.as_session_musician}</li>
                        <li>Session Ratio: ${(musician.session_ratio * 100).toFixed(1)}%</li>
                    </ul>
                </div>
                
                <div class="debug-section">
                    <h4>Network Presence</h4>
                    <ul class="debug-list">
                        <li>Appears in network: ${fullNetworkData.nodes.some(n => n.name === musicianName) ? 'Yes' : 'No'}</li>
                        <li>Node connections: ${fullNetworkData.nodes.find(n => n.name === musicianName)?.value || 0}</li>
                        <li>Currently visible: ${currentData.nodes.some(n => n.name === musicianName) ? 'Yes' : 'No'}</li>
                    </ul>
                </div>
                
                <div class="debug-section">
                    <h4>Albums (${musician.records.length})</h4>
                    <ul class="debug-list">
            `;
            
            musician.records.slice(0, 15).forEach(record => {
                content += `<li>${record}</li>`;
            });
            
            if (musician.records.length > 15) {
                content += `<li><em>... and ${musician.records.length - 15} more</em></li>`;
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
