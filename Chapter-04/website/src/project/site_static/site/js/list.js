jQuery(function ($) {
  var $list = $('.item-list');
  var $loader = $('script[type="text/template"].loader'); 
  $list.jscroll({
    loadingHtml: $loader.html(), 
    padding: 100,
    pagingSelector: '.pagination', 
    nextSelector: 'a.next-page:last', 
    contentSelector: '.item,.pagination'
  }); 
});