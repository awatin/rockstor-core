/*
 *
 * @licstart  The following is the entire license notice for the
 * JavaScript code in this page.
 *
 * Copyright (c) 2012-2013 RockStor, Inc. <http://rockstor.com>
 * This file is part of RockStor.
 *
 * RockStor is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published
 * by the Free Software Foundation; either version 2 of the License,
 * or (at your option) any later version.
 *
 * RockStor is distributed in the hope that it will be useful, but
 * WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program. If not, see <http://www.gnu.org/licenses/>.
 *
 * @licend  The above is the entire license notice
 * for the JavaScript code in this page.
 *
 */

DiskDetailsLayoutView = RockstorLayoutView.extend({

    initialize: function() {
	// call initialize of base
	this.constructor.__super__.initialize.apply(this, arguments);
	this.diskName = this.options.diskName;
	this.template = window.JST.disk_disk_details_layout;
	this.disk = new Disk({diskName: this.diskName});
	this.smartinfo = new SmartInfo({diskName: this.diskName});
	this.dependencies.push(this.disk);
	this.dependencies.push(this.smartinfo);
	this.active_tab = 0;
    },

    events: {
	'click #smartinfo': 'refreshInfo',
	'click #test-start': 'startTest'
    },

    render: function() {
	this.fetch(this.renderSubViews, this);
	return this;
    },

    renderSubViews: function() {
	console.log('smartinfo', this.smartinfo);
	var capabilities = this.smartinfo.get('capabilities');
	var test_capabilities = {};
	capabilities.forEach(function(c) {
	    if ((c.name == 'Short self-test routine recommended polling time') ||
		(c.name == 'Extended self-test routine recommended polling time') ||
		(c.name == 'Conveyance self-test routine recommended polling time')) {
		var p = c.name.indexOf("routine");
		var short_name = c.name.substring(0, p);
		test_capabilities[short_name] = c.capabilities;
	    }
	});
	console.log('test capabilities', test_capabilities);
	$(this.el).html(this.template({disk: this.disk, smartinfo: this.smartinfo, tests: test_capabilities}));
	this.$("ul.css-tabs").tabs("div.css-panes > div");
	this.$("ul.css-tabs").data("tabs").click(this.active_tab);
	this.active_tab = 0;
    },

    refreshInfo: function(event) {
	var _this = this;
	var button = $(event.currentTarget);
	if (buttonDisabled(button)) return false;
	disableButton(button);
	console.log('refreshing');
	$.ajax({
	    url: '/api/disks/smart/info/' + _this.diskName,
	    type: 'POST',
	    success: function(data, status, xhr) {
		_this.render();
	    },
	    error: function(xhr, status, error) {
		enableButton(button);
	    }
	});
    },

    startTest: function(event) {
	var _this = this;
	var button = $(event.currentTarget);
	if (buttonDisabled(button)) return false;
	disableButton(button);
	console.log('test started');
	$.ajax({
	    url: '/api/disks/smart/info/' + _this.diskName,
	    type: 'POST',
	    success: function(data, status, xhr) {
		_this.render();
		_this.active_tab = 4;
	    },
	    error: function(xhr, status, error) {
		enableButton(button);
	    }
	});
    }
});
