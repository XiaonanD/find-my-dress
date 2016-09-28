/* Main page dispatcher.
*/
requirejs(['app/index',
           'app/edit',
           'app/categorize',
           'helper/colormap',
           'helper/util'],
function(indexPage, editPage, categorizePage, colormap, util) {
  var dataURL = "/images/",  // Change this to another dataset.
      params = util.getQueryParams();

  // Create a colormap for display. The following is an example.
  function createColormap(label, labels) {
    return (label) ?
      colormap.create("single", {
        size: labels.length,
        index: labels.indexOf(label)
      }) :
      [
       [255, 255, 255],
       [0, 0, 0],
       [64, 32, 32]].concat(colormap.create("hsv", {
        size: labels.length - 3
      }));
  }

  // Load dataset before rendering a view.
  function renderPage(renderer) {
    util.requestJSON(dataURL, function(data) {
      data.colormap = createColormap(params.label, data.labels);
      renderer(data, params);
    });
  }

  switch(params.view) {
    case "index":
      renderPage(indexPage);
      break;
    case "edit":
      renderPage(editPage);
      break;
    case "categorize":
      renderPage(categorizePage);
      break;
    default:
      params.view = "index";
      window.location = util.makeQueryParams(params);
      break;
  }
});
