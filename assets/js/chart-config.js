Chart.defaults.font.family = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif";

var json = null;

var primaryColor = '#42107b';
var color1 = '#1355bf'; // West Plains
var color2 = '#138bbf'; // Willow Springs
var color3 = '#13afbf'; // Mountain View
var color4 = '#13bf80'; // Other
var color5 = '#808080'; // Unknown
var categoryColors = [color1, color2, color3, color4, color5];

var ctx = document.getElementById('chart').getContext('2d');

let categories = ["West Plains", "Willow Springs", "Mountain View", "Other"]
let keys = ["west_plains", "willow_springs", "mountain_view", "other"]