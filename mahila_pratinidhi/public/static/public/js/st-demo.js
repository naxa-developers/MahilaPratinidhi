;(function() {
  'use strict';


  $(activate);


  function activate() {

    $('.nav-tabs')
      .scrollingTabs()
      .on('ready.scrtabs', function() {
        $('.tab-content').show();
      });

  }
}());
