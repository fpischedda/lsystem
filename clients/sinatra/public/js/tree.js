function new_node (type, min_angle, max_angle, min_trunk_length, max_trunk_length) {
	
	var n = new Object();
	
	n.node_type = type;
	var range = max_angle - min_angle;
	n.angle = Math.random() * range + min_angle;
	
	range = min_trunk_length - 2.0;
	var length = Math.random() * range + 2.0;
	
	n.start_length = length;
	n.current_length = length;
	n.max_length = max_trunk_length;
	n.children = new Array();
	
	return n;
}

function gen_tree (level, min_trunk_length, max_trunk_length) {
	//elementi : tipo, figli, variazione dell'angolo rispetto al padre, lunghezza di partenza,
	// lunghezza attuale, lunghezza massima
	var base_tree = new_node('b', 0, 0, min_trunk_length, max_trunk_length);
	
	base_tree.children = base_tree.children.concat( next_node(base_tree.node_type, level, min_trunk_length, max_trunk_length) );
	
	return base_tree;
}

function next_node (parent_node_type, level, min_trunk_length, max_trunk_length) {
	
	var new_nodes = new Array();
	
	if( level <= 0)
	{
		return new_nodes;
	}
	
	if(parent_node_type == 'a')
	{
		new_nodes.push( new_node('b', -0.6, 0.6, min_trunk_length, max_trunk_length) );
	}
	else
	{
		new_nodes.push( new_node('b', -0.6, 0.6, min_trunk_length, max_trunk_length),
						new_node('a', -0.6, 0.6, min_trunk_length, max_trunk_length) );
	}

	//se il livello non è maggiore di 1 il codice sotto è semplicemente inutile
	if( level > 1)
	{
		for(var i=0; i < new_nodes.length; i++)
		{
			n = new_nodes[i];
			
			n.children = n.children.concat( next_node(n.node_type, level - 1, min_trunk_length, max_trunk_length) );
		}
	}
	
	return new_nodes;
}

function grow_tree (tree, time_lapsed) {
	
	for(var i=0; i<tree.children.length; i++)
	{
		grow_tree(tree.children[i], time_lapsed);
	}

	if ( tree.current_length < tree.max_length)
	{
		tree.current_length += time_lapsed * 2;
		
		//genero nuovi rami se il ramo attuale è arrivato a tre quarti della sua
		//lunghezza massima
		if( tree.children.length <= 0 && tree.current_length > tree.max_length * 3 / 4)
		{
			tree.children = tree.children.concat( next_node(tree.node_type, 1, tree.start_length, tree.max_length));
		}
		
		if( tree.current_length > tree.max_length )
		{
			tree.current_length > tree.max_length;
		}
	}
}