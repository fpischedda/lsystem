var g_resources;

function init_resources (asset_base_url) {
	
	g_resources = Array();
	
	load_media([{type:'audio',name:'mouseover'}, {type:'image','background'}, {type:'image','leaves'}, {type:'image','pot'}], asset_base_url)
}

function load_media (files, asset_base_url) {
	
	var elem;
	
	var extensions = {audio:'.ogg', image:'.png'};
	
	for (var i = files.length - 1; i >= 0; i--){
		elem = files[i];
		
		elem.url = asset_base_url + elem.type + '/' + name + extensions[elem.type];
		
		add_resource(elem);
	};
}

function add_resource (resource, force_reload) {

	var res = g_resources[type];
	
	if(!res)
	{
		g_resources[type] = Array();
	}
	
	if(!g_resource[type][resource.name] || force_reload)
	{
		g_resource[type][resource.name] = create_resource(resource);
	}
	
	return g_resource[type][resource.name];
}

function create_resource (resource) {
	
	var res;
	
	switch(resource.type)
	{
		case 'image':
			res = new Image();
			img.src = filename;
			
			break;
		case 'audio':
			res = document.createElement('audio');
			res.setAttribute('id', 'res:' + resource.type + elem.name);
			res.setAttribute('src', resource.url);
	}
	
	resource.resource = res;
}

function get_resource (type, name) {
	
	return g_resource[type][name];
}