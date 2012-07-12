//var __host = 'localhost:8000';
//var __protocol = 'http:://';

var __host = '';
var __protocol = '';

function login (username, password, callback) {
	
	$.get(__protocol+__host+'/login/' + username + '/' + password, function(data) {
		
		var obj = eval("(" + data + ")");
		
		if(obj.result=="OK")
		{
			callback(true);
		}
		else
		{
			callback(false);
		}
	});
}

function get_usernames (callback) {
	
	$.get(__protocol+__host+'/user.get_all_names', function(data) {
		
		var obj = eval("(" + data + ")");

		if(obj.result=="OK")
		{
			callback(obj.users);
		}
	});
}

function get_environments (callback) {
	
	$.get(__protocol+__host+'/user.environments/auth', function(data) {
		
		var obj = eval("(" + data + ")");
		
		if(obj.result=="OK")
		{
			callback(obj.environments);
		}
	});
}

function load_plant (plant_name, callback) {
	
	$.get(__protocol+__host+'/user.plant_details/auth/' + plant_name, function(data) {
		
		var obj = eval("(" + data + ")");
		
		if(obj.result=="OK")
		{
			callback(obj.plant);
		}
	});
}

function load_user (callback) {

	$.get(__protocol+__host+'/user.details/auth/', function(data) {
		
		var obj = eval("(" + data + ")");
		
		if(obj.result=="OK")
		{
			callback(obj);
		}
	});
}

function add_water (plant_name, callback) {

	$.get(__protocol+__host+'/add_water/auth/'+plant_name+'/5', function(data) {
		
		var obj = eval("(" + data + ")");
		
		if(obj.result=="OK")
		{
			callback(obj.available_water, obj.water_reserve);
		}
	});
}

function grow (plant_name, callback) {

	$.get(__protocol+__host+'/grow/auth/'+plant_name, function(data) {
		
		var obj = eval("(" + data + ")");
		
		if(obj.result=="OK")
		{
			callback(obj.plant);
		}
	});
}

function eat (plant_name, callback) {

	$.get(__protocol+__host+'/eat/auth/'+plant_name, function(data) {

		var obj = eval("(" + data + ")");
		
		if(obj.result=="OK")
		{
			callback(obj.plant);
		}
	});
}

function timeline_last_messages (last_id, callback) {

	$.get(__protocol+__host+'/timeline.last_messages/'+last_id, function(data) {

		var obj = eval("(" + data + ")");
		
		if(obj.result=="OK")
		{
			callback(obj.timeline);
		}
	});
}

function user_items (callback) {
	
	$.get(__protocol+__host+'/user.items/auth', function(data) {

		var obj = eval("(" + data + ")");
		
		if(obj.result=="OK")
		{
			callback(obj);
		}
	});
}

function use_item (item_name, plant_name, callback) {
	
	
	$.get(__protocol+__host+'/user.use_item/auth/'+item_name + '/' + plant_name, function(data) {

		var obj = eval("(" + data + ")");
		
		if(obj.result=="OK")
		{
			callback(obj.item, obj.plant, true);
		}
		else
		{
			console.log(obj);
			callback(item_name, null, false);
		}
	});
}

function use_magic_bottle (name, callback) {
	
	$.get(__protocol+__host+'/user.use_magic_bottle/auth/'+name, function(data) {

		var obj = eval("(" + data + ")");
		
		if(obj.result=="OK")
		{
			callback(obj.plant);
		}
		else
		{
			console.log('unable to use the magic bottle, reason:' + obj.reason);
		}
	});
}

var g_item_descriptions = {
		'water-tank':'This is the water tank',
		'water-reserve':'This is the amount of water that you can use',
		'magic-bottle':'Use the magic bottle to recover <br>a deadly plant or to grow it faster'};
		
function get_item_description (name) {
	
	return g_item_descriptions[name];
}