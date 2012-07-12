var g_context;
var g_canvas;

var g_images;

var g_colors;

function load_image (filename) {
	
	var img = new Image();
	img.src = filename;

	return img;
}

function load_all_images () {
	
	g_images = new Array();
	
	g_images.push( load_image("images/flower_small.gif"));
	g_images.push( load_image("images/leaves.png"));
	g_images.push( load_image("images/vaso_small.png"));
	g_images.push( load_image("images/finestra.jpg"));
}

function gfx_init(canvas_id)
{
	load_all_images();
	
	g_canvas = document.getElementById(canvas_id);
	g_context = g_canvas.getContext("2d");
	
	g_colors = new Array( "#7BD111", "#1ABA04", "#6AB000", "#96693B");
	
	return g_context;
}

function reset_canvas () {
	//tip preso da http://diveintohtml5.org/canvas.html
	g_canvas.width = g_canvas.width;
}

function draw_line (x1,y1,x2,y2) {

	g_context.moveTo(x1,y1);
	g_context.lineTo(x2,y2);
}

function draw_image_centered(index, x, y, scale)
{
	var img = g_images[index];
	var width = img.width * scale;
	var height = img.height * scale;
	
	g_context.drawImage(img, x - width / 2, y - height / 2, width, height);
}

function draw_image(index, x, y)
{
	var img = g_images[index];
	
	g_context.drawImage(img, x, y);
}

function get_color (grow_scale) {
	
	var index = parseInt((g_colors.length-1) * grow_scale);
	
	return g_colors[index];
}

function draw_tree (tree, start_x, start_y, angle, draw_scale) {
	
	var new_angle = angle + tree.angle;

	var new_x = start_x + draw_scale * (Math.cos(new_angle) * tree.length);
	var new_y = start_y - draw_scale * (Math.sin(new_angle) * tree.length);

	g_context.strokeStyle = get_color(0.5);
	draw_line(start_x, start_y, new_x, new_y);
	
	g_context.stroke();
	
	var image_scale = draw_scale * 0.5;
	
	if(tree.node_type == 'a')
	{
		draw_image_centered(0, new_x, new_y, image_scale);
	}
	else
	{
		draw_image_centered(1, new_x, new_y, image_scale);
	}
	
	for(var i=0; i < tree.children.length; i++)
	{
		var c = tree.children[i];
		
		draw_tree(c, new_x, new_y, new_angle, draw_scale);
	}
}