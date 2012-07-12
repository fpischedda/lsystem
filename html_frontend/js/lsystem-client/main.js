var __host = 'localhost:8000';

function login (username, password, callback) {
	
	$.get('http://'+__host+'/login/' + username + '/' + password, function(data) {
		
		var obj = eval("(" + data + ")");
		
		if(obj.result=="OK")
		{
			callback(obj.session_id);
		}
	});
}

function get_usernames (sid, callback) {
	
	$.get('http://'+__host+'/user.get_all_names/'+sid, function(data) {
		
		var obj = eval("(" + data + ")");

		if(obj.result=="OK")
		{
			callback(obj.users);
		}
	});
}

function get_environments (sid, callback) {
	
	$.get('http://'+__host+'/user.environments/'+sid, function(data) {
		
		var obj = eval("(" + data + ")");
		
		if(obj.result=="OK")
		{
			callback(obj.environments);
		}
	});
}

function load_plant (sid, plant_name, callback) {
	
	$.get('http://'+__host+'/user.plant/'+sid+'/' + plant_name, function(data) {
		
		var obj = eval("(" + data + ")");
		
		if(obj.result=="OK")
		{
			callback(obj.plant);
		}
	});
}

function load_user (sid, callback) {

	$.get('http://'+__host+'/user.details/'+sid, function(data) {
		
		var obj = eval("(" + data + ")");
		
		if(obj.result=="OK")
		{
			callback(obj);
		}
	});
}

function add_water (sid, plant_name, callback) {

	$.get('http://'+__host+'/add_water/'+sid+'/'+plant_name+'/1', function(data) {
		
		var obj = eval("(" + data + ")");
		
		if(obj.result=="OK")
		{
			callback(obj.available_water);
		}
	});
}

function grow (sid, plant_name, callback) {

	$.get('http://'+__host+'/grow/'+sid+'/'+plant_name, function(data) {
		
		var obj = eval("(" + data + ")");
		
		if(obj.result=="OK")
		{
			callback(obj.plant);
		}
	});
}

function eat (sid, plant_name, callback) {

	$.get('http://'+__host+'/eat/'+sid+'/'+plant_name, function(data) {

		var obj = eval("(" + data + ")");
		
		if(obj.result=="OK")
		{
			callback(obj.plant);
		}
	});
}

function timeline_last_messages (last_id, callback) {

	$.get('http://'+__host+'/timeline.last_messages/'+last_id, function(data) {

		var obj = eval("(" + data + ")");
		
		if(obj.result=="OK")
		{
			callback(obj.timeline);
		}
	});
}