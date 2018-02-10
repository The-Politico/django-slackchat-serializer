window.onload = function() {
  var simplemdeJQuery = null;

  if (typeof jQuery !== 'undefined') {
    simplemdeJQuery = jQuery;
  } else if (typeof django !== 'undefined') {
    simplemdeJQuery = django.jQuery
  } else {
    console.error('Cant find jQuery, please make sure your have jQuery imported for markdown editor.');
  }

  function initSimpleMDE() {
    simplemdeJQuery.each(simplemdeJQuery('.markdown-editor'), function(i, elem) {
      if (typeof elem.SimpleMDE !== 'undefined') return;
      var id = simplemdeJQuery(elem).attr('id');
      if (id.indexOf('__prefix__') >= 0) return; // Exclude prefixed forms
      var simplemde = new SimpleMDE({
        element: elem,
        placeholder: "Write in Markdown syntax using the toolbar.",
        status: false,
        forceSync: true,
        toolbar: ["bold", "italic", "|", "link", "|", "preview"],
      });
      elem.SimpleMDE = simplemde;
    });
  }

  if (!!simplemdeJQuery) simplemdeJQuery(initSimpleMDE);

  simplemdeJQuery(document).on('formset:added', initSimpleMDE);
}
